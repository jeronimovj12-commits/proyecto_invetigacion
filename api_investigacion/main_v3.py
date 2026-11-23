# Ejecuta la instruccion indicada dentro del flujo actual.
"""Ensamblaje v3; main:app conserva v2."""
# Importa JSONResponse desde fastapi.responses para usar esas definiciones.
from fastapi.responses import JSONResponse
# Importa app desde main para usar esas definiciones.
from main import app
# Importa router desde controllers.autenticacion_controller para usar esas definiciones.
from controllers.autenticacion_controller import router
# Importa router as seguridad desde controllers.seguridad_controller para usar esas definiciones.
from controllers.seguridad_controller import router as seguridad
# Importa crear_servicio_autenticacion desde servicios.ensamblador_autenticacion para usar esas definiciones.
from servicios.ensamblador_autenticacion import crear_servicio_autenticacion
# Importa AutenticacionFallida, PermisoInsuficiente desde seguridad.errores para usar esas definiciones.
from seguridad.errores import AutenticacionFallida, PermisoInsuficiente

# Asigna a autenticacion el valor calculado a la derecha.
autenticacion = crear_servicio_autenticacion()
# Asigna a app.title el valor calculado a la derecha.
app.title = 'API Investigación — v3'
# Asigna a app.version el valor calculado a la derecha.
app.version = 'v3'
# Asigna a app.description el valor calculado a la derecha.
app.description = 'Investigación y seguridad con autenticación y permisos.'
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
app.include_router(router)
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
app.include_router(seguridad)

# Aplica @app.middleware a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.middleware('http')
# Define la funcion proteger con los parametros declarados; su bloque realiza esta operacion.
async def proteger(solicitud, siguiente):
    # Asigna a ruta el valor calculado a la derecha.
    ruta = solicitud.url.path
    # Ejecuta el bloque siguiente solo cuando se cumple: ruta.startswith('/api/') and ruta not in ('/api/login', '/api/logout', '/api/sesion').
    if ruta.startswith('/api/') and ruta not in ('/api/login', '/api/logout', '/api/sesion'):
        # Inicia un bloque cuya excepcion se manejara en los except siguientes.
        try:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            esquema, _, token = solicitud.headers.get('Authorization', '').partition(' ')
            # Ejecuta el bloque siguiente solo cuando se cumple: esquema.lower() != 'bearer' or not token.
            if esquema.lower() != 'bearer' or not token:
                # Lanza la excepcion indicada y detiene el flujo normal.
                raise AutenticacionFallida()
            # Asigna a usuario el valor calculado a la derecha.
            usuario = await autenticacion.sesion(token)
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            autenticacion.comprobar_permiso(usuario,
                # Asigna a escritura el valor calculado a la derecha.
                escritura=solicitud.method not in ('GET', 'HEAD', 'OPTIONS'),
                # Asigna a seguridad el valor calculado a la derecha.
                seguridad=ruta.split('/')[2] in ('usuario', 'rol', 'rol_usuario'))
        # Captura la excepcion indicada para manejarla sin dejarla propagarse.
        except (AutenticacionFallida, PermisoInsuficiente) as error:
            # Asigna a estado el valor calculado a la derecha.
            estado = 401 if isinstance(error, AutenticacionFallida) else 403
            # Devuelve al llamador el resultado de la expresion indicada.
            return JSONResponse({'estado': estado, 'mensaje': 'Autenticación requerida.' if estado == 401 else 'Acceso denegado.',
                # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                'detalle': 'La sesión o los permisos no permiten esta operación.'}, status_code=estado,
                # Asigna a headers el valor calculado a la derecha.
                headers={'Cache-Control': 'no-store', **({'WWW-Authenticate': 'Bearer'} if estado == 401 else {})})
        # Captura la excepcion indicada para manejarla sin dejarla propagarse.
        except Exception:
            # Devuelve al llamador el resultado de la expresion indicada.
            return JSONResponse({'estado': 500, 'mensaje': 'Servicio de seguridad no disponible.', 'detalle': 'Intenta nuevamente.'}, status_code=500)
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = await siguiente(solicitud)
    # Ejecuta el bloque siguiente solo cuando se cumple: ruta.startswith('/api/').
    if ruta.startswith('/api/'):
        # Ejecuta el bloque siguiente solo cuando se cumple: respuesta.status_code >= 500.
        if respuesta.status_code >= 500:
            # Asigna a respuesta el valor calculado a la derecha.
            respuesta = JSONResponse({'estado': 500, 'mensaje': 'No se pudo completar la operación.', 'detalle': 'Error interno del servicio.'}, status_code=500)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        respuesta.headers['Cache-Control'] = 'no-store'
    # Devuelve al llamador el resultado de la expresion indicada.
    return respuesta

# El middleware controla permisos; OpenAPI también debe informar al cliente Swagger
# que envíe la credencial al usar «Authorize» en investigación y administración.
# Asigna a _openapi_original el valor calculado a la derecha.
_openapi_original = app.openapi

# Define la funcion contratos_v3 con los parametros declarados; su bloque realiza esta operacion.
def contratos_v3():
    # Asigna a esquema el valor calculado a la derecha.
    esquema = _openapi_original()
    # Recorre los elementos de la coleccion indicada y ejecuta el bloque para cada uno.
    for ruta, operaciones in esquema['paths'].items():
        # Ejecuta el bloque siguiente solo cuando se cumple: ruta.startswith('/api/') and ruta != '/api/login'.
        if ruta.startswith('/api/') and ruta != '/api/login':
            # Recorre los elementos de la coleccion indicada y ejecuta el bloque para cada uno.
            for metodo, operacion in operaciones.items():
                # Ejecuta el bloque siguiente solo cuando se cumple: metodo in ('get', 'post', 'put', 'patch', 'delete', 'head', 'options').
                if metodo in ('get', 'post', 'put', 'patch', 'delete', 'head', 'options'):
                    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                    operacion['security'] = [{'HTTPBearer': []}]
    # Devuelve al llamador el resultado de la expresion indicada.
    return esquema

# Asigna a app.openapi el valor calculado a la derecha.
app.openapi = contratos_v3
