"""La asignación no se borra lógicamente porque el esquema no tiene columna activo."""

from fastapi import APIRouter, Depends, HTTPException, Path, Response
from sqlalchemy.exc import IntegrityError

from models.rol_usuario import RolUsuarioCrear
from seguridad.dependencias import requerir_roles
from servicios.abstracciones.i_servicio_rol_usuario import IServicioRolUsuario
from servicios.ensamblador import crear_servicio_rol_usuario


router = APIRouter(prefix="/api", tags=["rol_usuario"])
_SOLO_ADMIN = [Depends(requerir_roles("ADMIN"))]


def _servicio() -> IServicioRolUsuario:
    return crear_servicio_rol_usuario()


def _error(estado: int, mensaje: str, detalle: str) -> HTTPException:
    return HTTPException(
        status_code=estado,
        detail={"estado": estado, "mensaje": mensaje, "detalle": detalle},
    )


@router.get("/rol_usuario", dependencies=_SOLO_ADMIN)
async def listar_rol_usuario(limite: int = 1000):
    try:
        filas = await _servicio().listar(limite)
        if not filas:
            return Response(status_code=204)
        return {
            "tabla": "rol_usuario",
            "limite": limite,
            "total": len(filas),
            "datos": [
                {"usuarioId": fila["usuario_id"], "rolId": fila["rol_id"]}
                for fila in filas
            ],
        }
    except ValueError as excepcion:
        raise _error(400, "Parámetros inválidos.", str(excepcion)) from excepcion
    except Exception as excepcion:
        raise _error(500, "Error al consultar las asignaciones.", str(excepcion)) from excepcion


@router.get(
    "/rol_usuario/{usuario_id}/{rol_id}",
    dependencies=_SOLO_ADMIN,
)
async def obtener_rol_usuario(
    usuario_id: int = Path(),
    rol_id: int = Path(),
):
    try:
        fila = await _servicio().obtener(usuario_id, rol_id)
        return {"usuarioId": fila["usuario_id"], "rolId": fila["rol_id"]}
    except LookupError as excepcion:
        raise _error(404, "Asignación no encontrada.", str(excepcion)) from excepcion
    except Exception as excepcion:
        raise _error(500, "Error al consultar la asignación.", str(excepcion)) from excepcion


@router.post("/rol_usuario", dependencies=_SOLO_ADMIN)
async def crear_rol_usuario(datos: RolUsuarioCrear):
    try:
        await _servicio().crear(datos.model_dump())
        return {"estado": 200, "mensaje": "Asignación de rol creada exitosamente."}
    except IntegrityError as excepcion:
        raise _error(400, "La asignación ya existe o viola una llave foránea.", str(excepcion)) from excepcion
    except LookupError as excepcion:
        raise _error(404, "Usuario o rol no encontrado.", str(excepcion)) from excepcion
    except Exception as excepcion:
        raise _error(500, "No se pudo crear la asignación.", str(excepcion)) from excepcion


@router.delete(
    "/rol_usuario/{usuario_id}/{rol_id}",
    dependencies=_SOLO_ADMIN,
)
async def eliminar_rol_usuario(
    usuario_id: int = Path(),
    rol_id: int = Path(),
):
    try:
        filas = await _servicio().eliminar(usuario_id, rol_id)
        return {
            "estado": 200,
            "mensaje": "Asignación de rol eliminada.",
            "filasAfectadas": filas,
        }
    except LookupError as excepcion:
        raise _error(404, "Asignación no encontrada.", str(excepcion)) from excepcion
    except Exception as excepcion:
        raise _error(500, "No se pudo eliminar la asignación.", str(excepcion)) from excepcion
