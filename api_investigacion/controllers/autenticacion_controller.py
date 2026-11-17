# Ejecuta la instruccion indicada dentro del flujo actual.
"""Controlador HTTP: registra rutas, llama a servicios y convierte sus resultados o errores en respuestas HTTP."""
# Carga el modulo o los modulos logging.
import logging
# Importa Awaitable desde collections.abc para usar esas definiciones.
from collections.abc import Awaitable
# Importa Annotated desde typing para usar esas definiciones.
from typing import Annotated

# Importa APIRouter, Depends, HTTPException, Response desde fastapi para usar esas definiciones.
from fastapi import APIRouter, Depends, HTTPException, Response
# Importa HTTPAuthorizationCredentials, HTTPBearer desde fastapi.security para usar esas definiciones.
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

# Importa Login, UsuarioSesion, TokenSesion, SesionCerrada desde models.autenticacion para usar esas definiciones.
from models.autenticacion import Login, UsuarioSesion, TokenSesion, SesionCerrada
# Importa AutenticacionFallida, PermisoInsuficiente desde seguridad.errores para usar esas definiciones.
from seguridad.errores import AutenticacionFallida, PermisoInsuficiente
# Importa IServicioAutenticacion desde servicios.abstracciones.i_servicio_autenticacion para usar esas definiciones.
from servicios.abstracciones.i_servicio_autenticacion import IServicioAutenticacion
# Importa crear_servicio_autenticacion desde servicios.ensamblador_autenticacion para usar esas definiciones.
from servicios.ensamblador_autenticacion import crear_servicio_autenticacion

# Crea el router FastAPI que agrupa las rutas de este modulo.
router = APIRouter(prefix='/api', tags=['autenticación v3 parcial'])
# Asigna a bearer el valor calculado a la derecha.
bearer = HTTPBearer(auto_error=False)
# Asigna a Servicio el valor calculado a la derecha.
Servicio = Annotated[IServicioAutenticacion, Depends(crear_servicio_autenticacion)]
# Asigna a Credenciales el valor calculado a la derecha.
Credenciales = Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)]


# Define la funcion _token con los parametros declarados; su bloque realiza esta operacion.
def _token(credenciales: HTTPAuthorizationCredentials | None) -> str:
    # Ejecuta el bloque siguiente solo cuando se cumple: credenciales is None or credenciales.scheme.lower() != 'bearer'.
    if credenciales is None or credenciales.scheme.lower() != 'bearer':
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise HTTPException(401, detail={'estado': 401, 'mensaje': 'Autenticación requerida.',
                                        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                                        'detalle': 'Presenta credenciales vigentes.'},
                            # Asigna a headers el valor calculado a la derecha.
                            headers={'WWW-Authenticate': 'Bearer'})
    # Devuelve al llamador el resultado de la expresion indicada.
    return credenciales.credentials


# Define la funcion _ejecutar con los parametros declarados; su bloque realiza esta operacion.
async def _ejecutar(operacion: Awaitable):
    # Inicia un bloque cuya excepcion se manejara en los except siguientes.
    try:
        # Devuelve al llamador el resultado de la expresion indicada.
        return await operacion
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except AutenticacionFallida:
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise HTTPException(401, detail={'estado': 401, 'mensaje': 'Credenciales inválidas.',
                                        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                                        'detalle': 'La identidad o sesión no está vigente.'},
                            # Asigna a headers el valor calculado a la derecha.
                            headers={'WWW-Authenticate': 'Bearer'}) from None
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except PermisoInsuficiente:
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise HTTPException(403, detail={'estado': 403, 'mensaje': 'Acceso denegado.',
                                        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                                        'detalle': 'No tienes permisos para esta operación.'}) from None
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except Exception:
        # Ni exc_info ni str(excepcion): SQLAlchemy puede contener parámetros sensibles.
        # Registra el evento indicado para seguimiento o diagnostico.
        logging.getLogger(__name__).error('Fallo interno de autenticación; detalles sensibles omitidos.')
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise HTTPException(500, detail={'estado': 500, 'mensaje': 'No se pudo completar la operación.',
                                        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                                        'detalle': 'Error interno del servicio de seguridad.'}) from None


# Define la funcion _sin_cache con los parametros declarados; su bloque realiza esta operacion.
def _sin_cache(respuesta: Response):
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    respuesta.headers['Cache-Control'] = 'no-store'
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    respuesta.headers['Pragma'] = 'no-cache'


# Aplica @router.post a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@router.post('/login', response_model=TokenSesion)
# Define la funcion login con los parametros declarados; su bloque realiza esta operacion.
async def login(datos: Login, respuesta: Response, servicio: Servicio):
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    _sin_cache(respuesta)
    # Devuelve al llamador el resultado de la expresion indicada.
    return await _ejecutar(servicio.login(datos.username, datos.password.get_secret_value()))


# Aplica @router.get a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@router.get('/sesion', response_model=UsuarioSesion)
# Define la funcion sesion con los parametros declarados; su bloque realiza esta operacion.
async def sesion(respuesta: Response, servicio: Servicio, credenciales: Credenciales):
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    _sin_cache(respuesta)
    # Devuelve al llamador el resultado de la expresion indicada.
    return await _ejecutar(servicio.sesion(_token(credenciales)))


# Aplica @router.post a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@router.post('/logout', response_model=SesionCerrada)
# Define la funcion logout con los parametros declarados; su bloque realiza esta operacion.
async def logout(respuesta: Response, servicio: Servicio, credenciales: Credenciales):
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    _sin_cache(respuesta)
    # Espera que termine la operacion asincronica antes de continuar.
    await _ejecutar(servicio.logout(_token(credenciales)))
    # Devuelve al llamador el resultado de la expresion indicada.
    return SesionCerrada()
