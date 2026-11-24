"""Las dependencias centralizan 401/403 y mantienen el RBAC fuera de cada vista."""

from collections.abc import Callable

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from seguridad.jwt_handler import decodificar_token
from servicios.ensamblador import crear_servicio_usuario


esquema_bearer = HTTPBearer(auto_error=False)


def _no_autorizado(detalle: str = "Se requiere un token Bearer válido.") -> HTTPException:
    return HTTPException(
        status_code=401,
        detail={"estado": 401, "mensaje": "Autenticación requerida.", "detalle": detalle},
        headers={"WWW-Authenticate": "Bearer"},
    )


async def obtener_usuario_actual(
    credenciales: HTTPAuthorizationCredentials | None = Depends(esquema_bearer),
) -> dict:
    if credenciales is None or credenciales.scheme.lower() != "bearer":
        raise _no_autorizado()
    try:
        carga = decodificar_token(credenciales.credentials)
        identificador = int(carga["sub"])
    except (KeyError, TypeError, ValueError, RuntimeError) as excepcion:
        raise _no_autorizado("El token no es válido o expiró.") from excepcion

    usuario = await crear_servicio_usuario().obtener_identidad_activa(identificador)
    if usuario is None:
        raise _no_autorizado("La cuenta no existe o está inactiva.")
    return usuario


def requerir_roles(*roles_permitidos: str) -> Callable:
    async def verificar_roles(
        usuario: dict = Depends(obtener_usuario_actual),
    ) -> dict:
        roles_actuales = set(usuario.get("roles", []))
        if not roles_actuales.intersection(roles_permitidos):
            raise HTTPException(
                status_code=403,
                detail={
                    "estado": 403,
                    "mensaje": "Acceso denegado.",
                    "detalle": "El usuario no tiene un rol autorizado para esta operación.",
                },
            )
        return usuario

    return verificar_roles
