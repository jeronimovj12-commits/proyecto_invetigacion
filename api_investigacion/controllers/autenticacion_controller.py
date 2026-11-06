import logging
from collections.abc import Awaitable
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from models.autenticacion import Login, UsuarioSesion, TokenSesion, SesionCerrada
from seguridad.errores import AutenticacionFallida, PermisoInsuficiente
from servicios.abstracciones.i_servicio_autenticacion import IServicioAutenticacion
from servicios.ensamblador_autenticacion import crear_servicio_autenticacion

router = APIRouter(prefix='/api', tags=['autenticación v3 parcial'])
bearer = HTTPBearer(auto_error=False)
Servicio = Annotated[IServicioAutenticacion, Depends(crear_servicio_autenticacion)]
Credenciales = Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)]


def _token(credenciales: HTTPAuthorizationCredentials | None) -> str:
    if credenciales is None or credenciales.scheme.lower() != 'bearer':
        raise HTTPException(401, detail={'estado': 401, 'mensaje': 'Autenticación requerida.',
                                        'detalle': 'Presenta credenciales vigentes.'},
                            headers={'WWW-Authenticate': 'Bearer'})
    return credenciales.credentials


async def _ejecutar(operacion: Awaitable):
    try:
        return await operacion
    except AutenticacionFallida:
        raise HTTPException(401, detail={'estado': 401, 'mensaje': 'Credenciales inválidas.',
                                        'detalle': 'La identidad o sesión no está vigente.'},
                            headers={'WWW-Authenticate': 'Bearer'}) from None
    except PermisoInsuficiente:
        raise HTTPException(403, detail={'estado': 403, 'mensaje': 'Acceso denegado.',
                                        'detalle': 'No tienes permisos para esta operación.'}) from None
    except Exception:
        # Ni exc_info ni str(excepcion): SQLAlchemy puede contener parámetros sensibles.
        logging.getLogger(__name__).error('Fallo interno de autenticación; detalles sensibles omitidos.')
        raise HTTPException(500, detail={'estado': 500, 'mensaje': 'No se pudo completar la operación.',
                                        'detalle': 'Error interno del servicio de seguridad.'}) from None


def _sin_cache(respuesta: Response):
    respuesta.headers['Cache-Control'] = 'no-store'
    respuesta.headers['Pragma'] = 'no-cache'


@router.post('/login', response_model=TokenSesion)
async def login(datos: Login, respuesta: Response, servicio: Servicio):
    _sin_cache(respuesta)
    return await _ejecutar(servicio.login(datos.username, datos.password.get_secret_value()))


@router.get('/sesion', response_model=UsuarioSesion)
async def sesion(respuesta: Response, servicio: Servicio, credenciales: Credenciales):
    _sin_cache(respuesta)
    return await _ejecutar(servicio.sesion(_token(credenciales)))


@router.post('/logout', response_model=SesionCerrada)
async def logout(respuesta: Response, servicio: Servicio, credenciales: Credenciales):
    _sin_cache(respuesta)
    await _ejecutar(servicio.logout(_token(credenciales)))
    return SesionCerrada()
