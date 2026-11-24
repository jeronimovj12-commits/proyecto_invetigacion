"""Adaptador HTTP de claves compuestas; las rutas se concretan en cada controlador de recurso."""

from collections.abc import Callable

from fastapi import APIRouter, Depends, HTTPException, Path, Response
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from seguridad.dependencias import requerir_roles


def _error(estado: int, mensaje: str, detalle: str) -> HTTPException:
    return HTTPException(
        status_code=estado,
        detail={"estado": estado, "mensaje": mensaje, "detalle": detalle},
    )


def crear_controlador_compuesto(
    tabla: str,
    etiqueta: str,
    clave_primera: str,
    clave_segunda: str,
    campos_publicos: dict[str, str],
    modelo_crear: type[BaseModel],
    modelo_reemplazo: type[BaseModel],
    modelo_actualizar: type[BaseModel],
    ensamblar: Callable[[], object],
) -> APIRouter:
    # La fábrica evita duplicar traducción HTTP, pero los valores fijos generan rutas distintas y explícitas.
    router = APIRouter(prefix="/api", tags=[tabla])
    dependencias_lectura = [Depends(requerir_roles("ADMIN", "INVESTIGADOR", "CONSULTOR"))]
    dependencias_escritura = [Depends(requerir_roles("ADMIN", "INVESTIGADOR"))]

    def serializar(fila: dict) -> dict:
        return {publico: fila[columna] for columna, publico in campos_publicos.items()}

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
            raise _error(500, "Error al consultar los registros.", str(excepcion)) from excepcion

    router.add_api_route(
        f"/{tabla}", listar, methods=["GET"], name=f"listar_{tabla}",
        dependencies=dependencias_lectura,
    )

    async def obtener(
        primera: int = Path(alias=clave_primera),
        segunda: int = Path(alias=clave_segunda),
    ):
        try:
            return serializar(await ensamblar().obtener(primera, segunda))
        except LookupError as excepcion:
            raise _error(404, f"{etiqueta} no encontrada.", str(excepcion)) from excepcion
        except Exception as excepcion:
            raise _error(500, "Error al consultar el registro.", str(excepcion)) from excepcion

    async def reemplazar(
        datos: modelo_reemplazo,
        primera: int = Path(alias=clave_primera),
        segunda: int = Path(alias=clave_segunda),
    ):
        try:
            filas = await ensamblar().actualizar(primera, segunda, datos.model_dump())
            return {"estado": 200, "mensaje": f"{etiqueta} reemplazada.",
                    "filasAfectadas": filas}
        except ValueError as excepcion:
            raise _error(400, "Datos inválidos.", str(excepcion)) from excepcion
        except LookupError as excepcion:
            raise _error(404, f"{etiqueta} no encontrada.", str(excepcion)) from excepcion
        except Exception as excepcion:
            raise _error(500, f"No se pudo reemplazar {etiqueta}.", str(excepcion)) from excepcion

    async def actualizar(
        datos: modelo_actualizar,
        primera: int = Path(alias=clave_primera),
        segunda: int = Path(alias=clave_segunda),
    ):
        try:
            cambios = datos.model_dump(exclude_unset=True)
            filas = await ensamblar().actualizar(primera, segunda, cambios)
            return {"estado": 200, "mensaje": f"{etiqueta} actualizada.",
                    "filasAfectadas": filas}
        except ValueError as excepcion:
            raise _error(400, "Datos inválidos.", str(excepcion)) from excepcion
        except LookupError as excepcion:
            raise _error(404, f"{etiqueta} no encontrada.", str(excepcion)) from excepcion
        except Exception as excepcion:
            raise _error(500, f"No se pudo actualizar {etiqueta}.", str(excepcion)) from excepcion

    async def crear(datos: modelo_crear):
        try:
            await ensamblar().crear(datos.model_dump())
            return {"estado": 200, "mensaje": f"{etiqueta} creada exitosamente."}
        except IntegrityError as excepcion:
            raise _error(400, "No se pudo guardar por integridad referencial.", str(excepcion)) from excepcion
        except Exception as excepcion:
            raise _error(500, f"No se pudo crear {etiqueta}.", str(excepcion)) from excepcion

    async def eliminar(
        primera: int = Path(alias=clave_primera),
        segunda: int = Path(alias=clave_segunda),
    ):
        try:
            filas = await ensamblar().eliminar(primera, segunda)
            return {"estado": 200, "mensaje": f"{etiqueta} eliminada.",
                    "filasAfectadas": filas}
        except LookupError as excepcion:
            raise _error(404, f"{etiqueta} no encontrada.", str(excepcion)) from excepcion
        except Exception as excepcion:
            raise _error(500, f"No se pudo eliminar {etiqueta}.", str(excepcion)) from excepcion

    sufijo = f"/{{{clave_primera}}}/{{{clave_segunda}}}"
    router.add_api_route(
        f"/{tabla}{sufijo}", obtener, methods=["GET"], name=f"obtener_{tabla}",
        dependencies=dependencias_lectura,
    )
    router.add_api_route(
        f"/{tabla}", crear, methods=["POST"], name=f"crear_{tabla}",
        dependencies=dependencias_escritura,
    )
    router.add_api_route(
        f"/{tabla}{sufijo}", reemplazar, methods=["PUT"], name=f"reemplazar_{tabla}",
        dependencies=dependencias_escritura,
    )
    router.add_api_route(
        f"/{tabla}{sufijo}", actualizar, methods=["PATCH"], name=f"actualizar_{tabla}",
        dependencies=dependencias_escritura,
    )
    router.add_api_route(
        f"/{tabla}{sufijo}", eliminar, methods=["DELETE"], name=f"eliminar_{tabla}",
        dependencies=dependencias_escritura,
    )
    return router
