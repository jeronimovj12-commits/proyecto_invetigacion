# Ejecuta la instruccion indicada dentro del flujo actual.
"""Arranque de presentación v3, separado del front v2."""
# Carga el modulo o los modulos os.
import os
# Carga el modulo o los modulos secrets.
import secrets
# Importa abort, g, redirect, render_template, request, session, url_for, flash desde flask para usar esas definiciones.
from flask import abort, g, redirect, render_template, request, session, url_for, flash
# Carga el modulo o los modulos cliente_api.
import cliente_api
# Importa app desde app para usar esas definiciones.
from app import app
# Importa SesionesServidor desde sesiones_servidor para usar esas definiciones.
from sesiones_servidor import SesionesServidor

# La clave de Flask viene del entorno; una clave debil invalida la proteccion de la cookie.
# Asigna a clave el valor calculado a la derecha.
clave = os.environ.get('CLAVE_SESION', '')
# Ejecuta el bloque siguiente solo cuando se cumple: len(clave.encode()) < 32 or clave.startswith('REEMPLAZAR').
if len(clave.encode()) < 32 or clave.startswith('REEMPLAZAR'):
    # Lanza la excepcion indicada y detiene el flujo normal.
    raise RuntimeError('CLAVE_SESION externa de al menos 32 bytes es obligatoria.')
# Asigna a app.secret_key el valor calculado a la derecha.
app.secret_key = clave
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
app.config.update(SESSION_COOKIE_NAME='investigacion_v3', SESSION_COOKIE_HTTPONLY=True,
    # Asigna a SESSION_COOKIE_SAMESITE el valor calculado a la derecha.
    SESSION_COOKIE_SAMESITE='Lax', SESSION_COOKIE_SECURE=os.environ.get('COOKIE_SECURE', '0') == '1',
    # Asigna a MAX_CONTENT_LENGTH el valor calculado a la derecha.
    MAX_CONTENT_LENGTH=1024 * 1024)
# Asigna a sesiones el valor calculado a la derecha.
sesiones = SesionesServidor(os.environ.get('SESIONES_ARCHIVO', '/tmp/investigacion-v3/sesiones.sqlite3'))

# Importa SesionTerminada, AccesoDenegado desde errores_seguridad para usar esas definiciones.
from errores_seguridad import SesionTerminada, AccesoDenegado

# Define la funcion limpiar con los parametros declarados; su bloque realiza esta operacion.
def limpiar():
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    sesiones.retirar(session.get('sid'))
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    session.clear()

# Define la funcion csrf con los parametros declarados; su bloque realiza esta operacion.
def csrf():
    # Ejecuta el bloque siguiente solo cuando se cumple: 'csrf' not in session.
    if 'csrf' not in session:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        session['csrf'] = secrets.token_urlsafe(32)
    # Devuelve al llamador el resultado de la expresion indicada.
    return session['csrf']

# Aplica @app.context_processor a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.context_processor
# Define la funcion contexto_seguridad con los parametros declarados; su bloque realiza esta operacion.
def contexto_seguridad():
    # Devuelve al llamador el resultado de la expresion indicada.
    return {'csrf_token': csrf, 'usuario_sesion': getattr(g, 'usuario', None),
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            'puede_escribir': bool(getattr(g, 'usuario', None) and 'administrador' in g.usuario['roles']),
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            'seguridad_v3': True}

# Aplica @app.before_request a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.before_request
# Define la funcion proteger_front con los parametros declarados; su bloque realiza esta operacion.
def proteger_front():
    # Una sola guarda valida formularios, sesion remota y permisos antes de cada vista.
    # Ejecuta el bloque siguiente solo cuando se cumple: request.endpoint == 'static'.
    if request.endpoint == 'static':
        # Termina la funcion sin devolver un valor.
        return
    # Ejecuta el bloque siguiente solo cuando se cumple: request.method not in ('GET', 'HEAD', 'OPTIONS').
    if request.method not in ('GET', 'HEAD', 'OPTIONS'):
        # Asigna a recibido el valor calculado a la derecha.
        recibido = request.form.get('csrf_token', '')
        # La comparacion constante evita filtrar diferencias del token por tiempo de respuesta.
        # Ejecuta el bloque siguiente solo cuando se cumple: not recibido or not secrets.compare_digest(recibido.encode(), session.get('csrf', '').encode()).
        if not recibido or not secrets.compare_digest(recibido.encode(), session.get('csrf', '').encode()):
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            abort(400, description='El formulario venció. Recarga la página e intenta de nuevo.')
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    csrf()
    # El login es la unica pantalla que no exige una sesion ya autenticada.
    # Ejecuta el bloque siguiente solo cuando se cumple: request.endpoint == 'login_v3'.
    if request.endpoint == 'login_v3':
        # Termina la funcion sin devolver un valor.
        return
    # El navegador conserva solo un identificador; el token vive en el almacen del servidor.
    # Asigna a token el valor calculado a la derecha.
    token = sesiones.obtener(session.get('sid'))
    # Ejecuta el bloque siguiente solo cuando se cumple: token is None.
    if token is None:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        limpiar()
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        flash('Inicia sesión para continuar. Si tenías una sesión, ha vencido.', 'error')
        # Devuelve al llamador el resultado de la expresion indicada.
        return redirect(url_for('login_v3'))
    # Asigna a g.token_api el valor calculado a la derecha.
    g.token_api = token
    # Ejecuta el bloque siguiente solo cuando se cumple: request.endpoint == 'logout_v3'.
    if request.endpoint == 'logout_v3':
        # Termina la funcion sin devolver un valor.
        return
    # Consulta a la API en cada peticion para detectar sesiones o roles revocados.
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = cliente_api._llamar('GET', '/api/sesion')
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None or respuesta.status_code != 200.
    if respuesta is None or respuesta.status_code != 200:
        # Devuelve al llamador el resultado de la expresion indicada.
        return render_template('estado_v3.html', mensaje='El servicio no está disponible. Intenta nuevamente.'), 503
    # Inicia un bloque cuya excepcion se manejara en los except siguientes.
    try:
        # Asigna a usuario el valor calculado a la derecha.
        usuario = respuesta.json()
        # Ejecuta el bloque siguiente solo cuando se cumple: not isinstance(usuario, dict) or not isinstance(usuario.get('roles'), list).
        if not isinstance(usuario, dict) or not isinstance(usuario.get('roles'), list):
            # Lanza la excepcion indicada y detiene el flujo normal.
            raise ValueError()
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except ValueError:
        # Devuelve al llamador el resultado de la expresion indicada.
        return render_template('estado_v3.html', mensaje='El servicio no está disponible. Intenta nuevamente.'), 503
    # Asigna a g.usuario el valor calculado a la derecha.
    g.usuario = usuario
    # Asigna a escritura el valor calculado a la derecha.
    escritura = request.method not in ('GET', 'HEAD', 'OPTIONS') or (request.endpoint or '').startswith(('crear_', 'editar_', 'eliminar_'))
    # El front refuerza el permiso para la interfaz; la API tambien lo valida.
    # Ejecuta el bloque siguiente solo cuando se cumple: (escritura or (request.endpoint or '').startswith('seguridad_')) and 'administrador' not in g.usuario['roles'].
    if (escritura or (request.endpoint or '').startswith('seguridad_')) and 'administrador' not in g.usuario['roles']:
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise AccesoDenegado()

# Aplica @app.errorhandler a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.errorhandler(SesionTerminada)
# Define la funcion sesion_terminada con los parametros declarados; su bloque realiza esta operacion.
def sesion_terminada(_error):
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    limpiar()
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    flash('Tu sesión ha vencido o fue invalidada. Inicia sesión de nuevo.', 'error')
    # Devuelve al llamador el resultado de la expresion indicada.
    return redirect(url_for('login_v3'))

# Aplica @app.errorhandler a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.errorhandler(AccesoDenegado)
# Define la funcion sin_permiso con los parametros declarados; su bloque realiza esta operacion.
def sin_permiso(_error):
    # Devuelve al llamador el resultado de la expresion indicada.
    return render_template('estado_v3.html', mensaje='No tienes permisos para esta operación.'), 403

# Aplica @app.after_request a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.after_request
# Define la funcion cabeceras con los parametros declarados; su bloque realiza esta operacion.
def cabeceras(respuesta):
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    respuesta.headers['Cache-Control'] = 'no-store'
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    respuesta.headers['X-Content-Type-Options'] = 'nosniff'
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    respuesta.headers['X-Frame-Options'] = 'DENY'
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    respuesta.headers['Content-Security-Policy'] = "default-src 'self'; form-action 'self'; frame-ancestors 'none'; base-uri 'self'"
    # Devuelve al llamador el resultado de la expresion indicada.
    return respuesta

# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route('/login', methods=['GET', 'POST'])
# Define la funcion login_v3 con los parametros declarados; su bloque realiza esta operacion.
def login_v3():
    # Ejecuta el bloque siguiente solo cuando se cumple: request.method == 'POST'.
    if request.method == 'POST':
        # Asigna a respuesta el valor calculado a la derecha.
        respuesta = cliente_api._llamar('POST', '/api/login', json={
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            'username': request.form.get('username', ''), 'password': request.form.get('password', '')})
        # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is not None and respuesta.status_code == 200.
        if respuesta is not None and respuesta.status_code == 200:
            # Asigna a datos el valor calculado a la derecha.
            datos = respuesta.json()
            # Se elimina cualquier sesion anterior antes de crear el nuevo identificador.
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            limpiar()
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            session['sid'] = sesiones.crear(datos['access_token'], datos['expires_in'])
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            csrf()
            # Devuelve al llamador el resultado de la expresion indicada.
            return redirect(url_for('inicio'))
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        flash('No se pudo iniciar sesión. Revisa tus credenciales y permisos.' if respuesta is not None else 'El servicio no está disponible.', 'error')
    # Devuelve al llamador el resultado de la expresion indicada.
    return render_template('login_v3.html')

# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route('/logout', methods=['POST'])
# Define la funcion logout_v3 con los parametros declarados; su bloque realiza esta operacion.
def logout_v3():
    # Primero se revoca el token en la API; luego se elimina la sesion local.
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = cliente_api._llamar('POST', '/api/logout')
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None or respuesta.status_code != 200.
    if respuesta is None or respuesta.status_code != 200:
        # Devuelve al llamador el resultado de la expresion indicada.
        return render_template('estado_v3.html', mensaje='No se pudo cerrar la sesión en el servicio. Intenta nuevamente.'), 503
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    limpiar()
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    flash('Sesión cerrada en todos los dispositivos.', 'exito')
    # Devuelve al llamador el resultado de la expresion indicada.
    return redirect(url_for('login_v3'))

# Define la funcion guardar_seguridad con los parametros declarados; su bloque realiza esta operacion.
def guardar_seguridad(recurso, campos, claves=None):
    # Asigna a datos el valor calculado a la derecha.
    datos = {c: request.form.get(c, '') for c in campos}
    # Una clave vacia al editar significa conservar el hash existente.
    # Ejecuta el bloque siguiente solo cuando se cumple: recurso == 'usuario' and claves and not datos.get('password').
    if recurso == 'usuario' and claves and not datos.get('password'):
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        datos.pop('password', None)
    # Ejecuta el bloque siguiente solo cuando se cumple: recurso == 'rol_usuario'.
    if recurso == 'rol_usuario':
        # La API recibe identificadores numericos, aunque HTML los envie como texto.
        # Recorre los elementos de la coleccion indicada y ejecuta el bloque para cada uno.
        for c in datos:
            # Inicia un bloque cuya excepcion se manejara en los except siguientes.
            try:
                # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                datos[c] = int(datos[c])
            # Captura la excepcion indicada para manejarla sin dejarla propagarse.
            except ValueError:
                # Deja el bloque intencionalmente vacio sin ejecutar una operacion.
                pass
    # Asigna a ruta el valor calculado a la derecha.
    ruta = '/api/' + recurso + ('/' + claves if claves else '')
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = cliente_api._llamar('PATCH' if claves else 'POST', ruta, json=datos)
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        flash('El servicio no está disponible.', 'error')
    # Prueba esta condicion alternativa si las anteriores fueron falsas.
    elif respuesta.status_code in (200, 201):
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        flash('Cambios guardados.', 'exito')
    # Define el caso alternativo cuando las condiciones anteriores no se cumplen.
    else:
        # Recorre los elementos de la coleccion indicada y ejecuta el bloque para cada uno.
        for mensaje in cliente_api._mensajes(respuesta):
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            flash(mensaje, 'error')

# Define la funcion pagina_seguridad con los parametros declarados; su bloque realiza esta operacion.
def pagina_seguridad(recurso, campos):
    # Ejecuta el bloque siguiente solo cuando se cumple: request.method == 'POST'.
    if request.method == 'POST':
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        guardar_seguridad(recurso, campos, request.form.get('id') or None)
        # Devuelve al llamador el resultado de la expresion indicada.
        return redirect(request.path)
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = cliente_api._llamar('GET', '/api/' + recurso, params={'limite': 1000})
    # Asigna a filas el valor calculado a la derecha.
    filas = []
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None or respuesta.status_code != 200.
    if respuesta is None or respuesta.status_code != 200:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        flash('No se pudo cargar la información.', 'error')
    # Define el caso alternativo cuando las condiciones anteriores no se cumplen.
    else:
        # Asigna a filas el valor calculado a la derecha.
        filas = respuesta.json()['datos']
    # Devuelve al llamador el resultado de la expresion indicada.
    return render_template('seguridad_v3.html', recurso=recurso, campos=campos, filas=filas)

# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route('/seguridad/usuarios', methods=['GET', 'POST'])
# Define la funcion seguridad_usuarios con los parametros declarados; su bloque realiza esta operacion.
def seguridad_usuarios():
    # Devuelve al llamador el resultado de la expresion indicada.
    return pagina_seguridad('usuario', ('username', 'email', 'nombre_completo', 'password'))

# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route('/seguridad/roles', methods=['GET', 'POST'])
# Define la funcion seguridad_roles con los parametros declarados; su bloque realiza esta operacion.
def seguridad_roles():
    # Devuelve al llamador el resultado de la expresion indicada.
    return pagina_seguridad('rol', ('nombre', 'descripcion'))

# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route('/seguridad/asignaciones', methods=['GET', 'POST'])
# Define la funcion seguridad_asignaciones con los parametros declarados; su bloque realiza esta operacion.
def seguridad_asignaciones():
    # Devuelve al llamador el resultado de la expresion indicada.
    return pagina_seguridad('rol_usuario', ('usuario_id', 'rol_id'))

# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route('/seguridad/<recurso>/<claves>/retirar', methods=['POST'])
# Define la funcion seguridad_retirar con los parametros declarados; su bloque realiza esta operacion.
def seguridad_retirar(recurso, claves):
    # Solo se aceptan los recursos administrables definidos por estas rutas.
    # Asigna a destinos el valor calculado a la derecha.
    destinos = {'usuario': 'seguridad_usuarios', 'rol': 'seguridad_roles', 'rol_usuario': 'seguridad_asignaciones'}
    # Ejecuta el bloque siguiente solo cuando se cumple: recurso not in destinos.
    if recurso not in destinos:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        abort(404)
    # Ejecuta el bloque siguiente solo cuando se cumple: recurso == 'rol_usuario'.
    if recurso == 'rol_usuario':
        # Inicia un bloque cuya excepcion se manejara en los except siguientes.
        try:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            usuario, rol = (int(c) for c in claves.split('-'))
        # Captura la excepcion indicada para manejarla sin dejarla propagarse.
        except ValueError:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            abort(404)
        # Asigna a claves el valor calculado a la derecha.
        claves = f'{usuario}/{rol}'
    # Prueba esta condicion alternativa si las anteriores fueron falsas.
    elif not claves.isdigit():
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        abort(404)
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = cliente_api._llamar('DELETE', '/api/' + recurso + '/' + claves)
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        flash('El servicio no está disponible.', 'error')
    # Prueba esta condicion alternativa si las anteriores fueron falsas.
    elif respuesta.status_code == 200:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        flash('Registro retirado.', 'exito')
    # Define el caso alternativo cuando las condiciones anteriores no se cumplen.
    else:
        # Recorre los elementos de la coleccion indicada y ejecuta el bloque para cada uno.
        for mensaje in cliente_api._mensajes(respuesta):
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            flash(mensaje, 'error')
    # Devuelve al llamador el resultado de la expresion indicada.
    return redirect(url_for(destinos[recurso]))

# Ejecuta el bloque siguiente solo cuando se cumple: __name__ == '__main__'.
if __name__ == '__main__':
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    app.run(host='0.0.0.0', port=int(os.environ.get('PUERTO', '8078')), debug=False)
