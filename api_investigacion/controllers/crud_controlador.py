"""Adaptador HTTP común; cada módulo declara su propia ruta y contratos específicos."""

from collections.abc import Callable

from fastapi import APIRouter, Depends, HTTPException, Path, Response
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError

from models.respuestas import RespuestaActualizacion, RespuestaCreacion
from servicios.abstracciones.i_servicio_base import IServicioBase
from seguridad.dependencias import requerir_roles


def _error(estado: int, mensaje: str, detalle: str) -> HTTPException:
    return HTTPException(
        status_code=estado,
        detail={"estado": estado, "mensaje": mensaje, "detalle": detalle},
    )


def crear_controlador(
    tabla: str,
    etiqueta: str,
    campos_publicos: dict[str, str],
    clave_tipo: type,
    modelo_crear: type[BaseModel],
    modelo_reemplazo: type[BaseModel],
    modelo_actualizar: type[BaseModel],
    ensamblar: Callable[[], IServicioBase],
    nombre_parametro: str | None = None,
    roles_lectura: tuple[str, ...] = ("ADMIN", "INVESTIGADOR", "CONSULTOR"),
    roles_escritura: tuple[str, ...] = ("ADMIN", "INVESTIGADOR"),
    ocultar_detalle_error: bool = False,
) -> APIRouter:
    # Los nombres de tabla y ruta son constantes pasadas por cada controlador, nunca segmentos capturados.
    router = APIRouter(prefix="/api", tags=[tabla])
    dependencias_lectura = [Depends(requerir_roles(*roles_lectura))]
    dependencias_escritura = [Depends(requerir_roles(*roles_escritura))]
    nombre_parametro = nombre_parametro or (
        "termino" if tabla == "termino_clave" else "id"
    )

    def serializar(fila: dict) -> dict:
        return {publico: fila[columna] for columna, publico in campos_publicos.items()}

    def detalle(excepcion: Exception) -> str:
        if ocultar_detalle_error:
            return "La operación no pudo completarse por un error de persistencia."
        return str(excepcion)

    @router.get(f"/{tabla}", dependencies=dependencias_lectura)
    async def listar(limite: int = 1000):
        try:
            filas = await ensamblar().listar(limite)
            if not filas:
                return Response(status_code=204)
            return {"tabla": tabla, "limite": limite, "total": len(filas),
                    "datos": [serializar(fila) for fila in filas]}
        except ValueError as excepcion:
            raise _error(400, "Parámetros inválidos.", str(excepcion)) from excepcion
        except Exception as excepcion:
            raise _error(500, "Error al consultar los registros.", detalle(excepcion)) from excepcion

    @router.get(f"/{tabla}/{{{nombre_parametro}}}", dependencies=dependencias_lectura)
    async def obtener(identificador: clave_tipo = Path(alias=nombre_parametro)):
        try:
            fila = await ensamblar().obtener(identificador)
            return serializar(fila)
        except ValueError as excepcion:
            raise _error(400, "Parámetros inválidos.", str(excepcion)) from excepcion
        except LookupError as excepcion:
            raise _error(404, f"{etiqueta} no encontrada.", str(excepcion)) from excepcion
        except HTTPException:
            raise
        except Exception as excepcion:
            raise _error(500, "Error al consultar el registro.", detalle(excepcion)) from excepcion

    @router.post(f"/{tabla}", dependencies=dependencias_escritura)
    async def crear(datos: modelo_crear):
        try:
            creado = await ensamblar().crear(datos.model_dump())
            respuesta = RespuestaCreacion(
                estado=200, mensaje=f"{etiqueta} creada exitosamente."
            ).model_dump(by_alias=True)
            if tabla == "linea_investigacion":
                respuesta["id"] = creado
            return respuesta
        except ValueError as excepcion:
            raise _error(400, "Datos inválidos.", str(excepcion)) from excepcion
        except IntegrityError as excepcion:
            raise _error(400, "No se pudo guardar por integridad referencial.", detalle(excepcion)) from excepcion
        except Exception as excepcion:
            raise _error(500, f"No se pudo crear {etiqueta}.", detalle(excepcion)) from excepcion

    @router.put(f"/{tabla}/{{{nombre_parametro}}}", dependencies=dependencias_escritura)
    async def reemplazar(identificador: clave_tipo = Path(alias=nombre_parametro), datos: modelo_reemplazo = ...):
        try:
            filas = await ensamblar().actualizar(identificador, datos.model_dump())
            return RespuestaActualizacion(
                estado=200, mensaje=f"{etiqueta} reemplazada.", filas_afectadas=filas
            ).model_dump(by_alias=True)
        except ValueError as excepcion:
            raise _error(400, "Parámetros inválidos.", str(excepcion)) from excepcion
        except LookupError as excepcion:
            raise _error(404, f"{etiqueta} no encontrada.", str(excepcion)) from excepcion
        except HTTPException:
            raise
        except Exception as excepcion:
            raise _error(500, f"No se pudo reemplazar {etiqueta}.", detalle(excepcion)) from excepcion

    @router.patch(f"/{tabla}/{{{nombre_parametro}}}", dependencies=dependencias_escritura)
    async def actualizar(identificador: clave_tipo = Path(alias=nombre_parametro), datos: modelo_actualizar = ...):
        try:
            cambios = datos.model_dump(exclude_unset=True)
            filas = await ensamblar().actualizar(identificador, cambios)
            return RespuestaActualizacion(
                estado=200, mensaje=f"{etiqueta} actualizada.", filas_afectadas=filas
            ).model_dump(by_alias=True)
        except ValueError as excepcion:
            raise _error(400, "Parámetros inválidos.", str(excepcion)) from excepcion
        except LookupError as excepcion:
            raise _error(404, f"{etiqueta} no encontrada.", str(excepcion)) from excepcion
        except HTTPException:
            raise
        except Exception as excepcion:
            raise _error(500, f"No se pudo actualizar {etiqueta}.", detalle(excepcion)) from excepcion

    @router.delete(f"/{tabla}/{{{nombre_parametro}}}", dependencies=dependencias_escritura)
    async def eliminar(identificador: clave_tipo = Path(alias=nombre_parametro)):
        try:
            filas = await ensamblar().eliminar(identificador)
            return RespuestaActualizacion(
                estado=200, mensaje=f"{etiqueta} eliminada.", filas_afectadas=filas
            ).model_dump(by_alias=True)
        except ValueError as excepcion:
            raise _error(400, "Parámetros inválidos.", str(excepcion)) from excepcion
        except LookupError as excepcion:
            raise _error(404, f"{etiqueta} no encontrada.", str(excepcion)) from excepcion
        except HTTPException:
            raise
        except Exception as excepcion:
            raise _error(500, f"No se pudo eliminar {etiqueta}.", detalle(excepcion)) from excepcion

    return router
