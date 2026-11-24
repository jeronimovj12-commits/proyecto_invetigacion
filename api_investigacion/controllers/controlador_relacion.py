"""Este adaptador publica solo las operaciones requeridas para las cinco tablas puente."""

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


def crear_controlador_relacion(
    tabla: str,
    etiqueta: str,
    clave_primera: str,
    clave_segunda: str,
    tipo_primera: type,
    tipo_segunda: type,
    campos_publicos: dict[str, str],
    modelo_crear: type[BaseModel],
    ensamblar: Callable[[], object],
) -> APIRouter:
    # Cada fábrica recibe nombres y tipos constantes para mantener rutas explícitas y claves fieles al esquema.
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
            return {
                "tabla": tabla,
                "limite": limite,
                "total": len(filas),
                "datos": [serializar(fila) for fila in filas],
            }
        except ValueError as excepcion:
            raise _error(400, "Parámetros inválidos.", str(excepcion)) from excepcion
        except Exception as excepcion:
            raise _error(500, "Error al consultar los registros.", str(excepcion)) from excepcion

    async def obtener(
        primera: tipo_primera = Path(alias=clave_primera),
        segunda: tipo_segunda = Path(alias=clave_segunda),
    ):
        try:
            return serializar(await ensamblar().obtener(primera, segunda))
        except LookupError as excepcion:
            raise _error(404, f"{etiqueta} no encontrada.", str(excepcion)) from excepcion
        except Exception as excepcion:
            raise _error(500, "Error al consultar el vínculo.", str(excepcion)) from excepcion

    async def crear(datos: modelo_crear):
        try:
            await ensamblar().crear(datos.model_dump())
            return {"estado": 200, "mensaje": f"{etiqueta} creada exitosamente."}
        except IntegrityError as excepcion:
            raise _error(400, "No se pudo guardar por integridad referencial.", str(excepcion)) from excepcion
        except Exception as excepcion:
            raise _error(500, f"No se pudo crear {etiqueta}.", str(excepcion)) from excepcion

    async def eliminar(
        primera: tipo_primera = Path(alias=clave_primera),
        segunda: tipo_segunda = Path(alias=clave_segunda),
    ):
        try:
            filas = await ensamblar().eliminar(primera, segunda)
            return {
                "estado": 200,
                "mensaje": f"{etiqueta} retirada exitosamente.",
                "filasAfectadas": filas,
            }
        except LookupError as excepcion:
            raise _error(404, f"{etiqueta} no encontrada.", str(excepcion)) from excepcion
        except Exception as excepcion:
            raise _error(500, f"No se pudo retirar {etiqueta}.", str(excepcion)) from excepcion

    sufijo = f"/{{{clave_primera}}}/{{{clave_segunda}}}"
    router.add_api_route(
        f"/{tabla}", listar, methods=["GET"], name=f"listar_{tabla}",
        dependencies=dependencias_lectura,
    )
    router.add_api_route(
        f"/{tabla}{sufijo}", obtener, methods=["GET"], name=f"obtener_{tabla}",
        dependencies=dependencias_lectura,
    )
    router.add_api_route(
        f"/{tabla}", crear, methods=["POST"], name=f"crear_{tabla}",
        dependencies=dependencias_escritura,
    )
    router.add_api_route(
        f"/{tabla}{sufijo}", eliminar, methods=["DELETE"], name=f"eliminar_{tabla}",
        dependencies=dependencias_escritura,
    )
    return router
