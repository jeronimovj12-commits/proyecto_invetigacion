"""Ensamblaje v3; main:app conserva v2."""
from fastapi.responses import JSONResponse
from main import app
from controllers.autenticacion_controller import router
from controllers.seguridad_controller import router as seguridad
from servicios.ensamblador_autenticacion import crear_servicio_autenticacion
from seguridad.errores import AutenticacionFallida, PermisoInsuficiente

autenticacion = crear_servicio_autenticacion()
app.title = 'API Investigación — v3'
app.version = 'v3'
app.description = 'Investigación y seguridad con autenticación y permisos.'
app.include_router(router)
app.include_router(seguridad)

@app.middleware('http')
async def proteger(solicitud, siguiente):
    ruta = solicitud.url.path
    if ruta.startswith('/api/') and ruta not in ('/api/login', '/api/logout', '/api/sesion'):
        try:
            esquema, _, token = solicitud.headers.get('Authorization', '').partition(' ')
            if esquema.lower() != 'bearer' or not token:
                raise AutenticacionFallida()
            usuario = await autenticacion.sesion(token)
            autenticacion.comprobar_permiso(usuario,
                escritura=solicitud.method not in ('GET', 'HEAD', 'OPTIONS'),
                seguridad=ruta.split('/')[2] in ('usuario', 'rol', 'rol_usuario'))
        except (AutenticacionFallida, PermisoInsuficiente) as error:
            estado = 401 if isinstance(error, AutenticacionFallida) else 403
            return JSONResponse({'estado': estado, 'mensaje': 'Autenticación requerida.' if estado == 401 else 'Acceso denegado.',
                'detalle': 'La sesión o los permisos no permiten esta operación.'}, status_code=estado,
                headers={'Cache-Control': 'no-store', **({'WWW-Authenticate': 'Bearer'} if estado == 401 else {})})
        except Exception:
            return JSONResponse({'estado': 500, 'mensaje': 'Servicio de seguridad no disponible.', 'detalle': 'Intenta nuevamente.'}, status_code=500)
    respuesta = await siguiente(solicitud)
    if ruta.startswith('/api/'):
        if respuesta.status_code >= 500:
            respuesta = JSONResponse({'estado': 500, 'mensaje': 'No se pudo completar la operación.', 'detalle': 'Error interno del servicio.'}, status_code=500)
        respuesta.headers['Cache-Control'] = 'no-store'
    return respuesta

# El middleware controla permisos; OpenAPI también debe informar al cliente Swagger
# que envíe la credencial al usar «Authorize» en investigación y administración.
_openapi_original = app.openapi

def contratos_v3():
    esquema = _openapi_original()
    for ruta, operaciones in esquema['paths'].items():
        if ruta.startswith('/api/') and ruta != '/api/login':
            for metodo, operacion in operaciones.items():
                if metodo in ('get', 'post', 'put', 'patch', 'delete', 'head', 'options'):
                    operacion['security'] = [{'HTTPBearer': []}]
    return esquema

app.openapi = contratos_v3
