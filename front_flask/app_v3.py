"""Arranque de presentación v3, separado del front v2."""
import os
import secrets
from flask import abort, g, redirect, render_template, request, session, url_for, flash
import cliente_api
from app import app
from sesiones_servidor import SesionesServidor

clave = os.environ.get('CLAVE_SESION', '')
if len(clave.encode()) < 32 or clave.startswith('REEMPLAZAR'):
    raise RuntimeError('CLAVE_SESION externa de al menos 32 bytes es obligatoria.')
app.secret_key = clave
app.config.update(SESSION_COOKIE_NAME='investigacion_v3', SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax', SESSION_COOKIE_SECURE=os.environ.get('COOKIE_SECURE', '0') == '1',
    MAX_CONTENT_LENGTH=1024 * 1024)
sesiones = SesionesServidor(os.environ.get('SESIONES_ARCHIVO', '/tmp/investigacion-v3/sesiones.sqlite3'))

from errores_seguridad import SesionTerminada, AccesoDenegado

def limpiar():
    sesiones.retirar(session.get('sid'))
    session.clear()

def csrf():
    if 'csrf' not in session:
        session['csrf'] = secrets.token_urlsafe(32)
    return session['csrf']

@app.context_processor
def contexto_seguridad():
    return {'csrf_token': csrf, 'usuario_sesion': getattr(g, 'usuario', None),
            'puede_escribir': bool(getattr(g, 'usuario', None) and 'administrador' in g.usuario['roles']),
            'seguridad_v3': True}

@app.before_request
def proteger_front():
    if request.endpoint == 'static':
        return
    if request.method not in ('GET', 'HEAD', 'OPTIONS'):
        recibido = request.form.get('csrf_token', '')
        if not recibido or not secrets.compare_digest(recibido.encode(), session.get('csrf', '').encode()):
            abort(400, description='El formulario venció. Recarga la página e intenta de nuevo.')
    csrf()
    if request.endpoint == 'login_v3':
        return
    token = sesiones.obtener(session.get('sid'))
    if token is None:
        limpiar()
        flash('Inicia sesión para continuar. Si tenías una sesión, ha vencido.', 'error')
        return redirect(url_for('login_v3'))
    g.token_api = token
    if request.endpoint == 'logout_v3':
        return
    respuesta = cliente_api._llamar('GET', '/api/sesion')
    if respuesta is None or respuesta.status_code != 200:
        return render_template('estado_v3.html', mensaje='El servicio no está disponible. Intenta nuevamente.'), 503
    try:
        usuario = respuesta.json()
        if not isinstance(usuario, dict) or not isinstance(usuario.get('roles'), list):
            raise ValueError()
    except ValueError:
        return render_template('estado_v3.html', mensaje='El servicio no está disponible. Intenta nuevamente.'), 503
    g.usuario = usuario
    escritura = request.method not in ('GET', 'HEAD', 'OPTIONS') or (request.endpoint or '').startswith(('crear_', 'editar_', 'eliminar_'))
    if (escritura or (request.endpoint or '').startswith('seguridad_')) and 'administrador' not in g.usuario['roles']:
        raise AccesoDenegado()

@app.errorhandler(SesionTerminada)
def sesion_terminada(_error):
    limpiar()
    flash('Tu sesión ha vencido o fue invalidada. Inicia sesión de nuevo.', 'error')
    return redirect(url_for('login_v3'))

@app.errorhandler(AccesoDenegado)
def sin_permiso(_error):
    return render_template('estado_v3.html', mensaje='No tienes permisos para esta operación.'), 403

@app.after_request
def cabeceras(respuesta):
    respuesta.headers['Cache-Control'] = 'no-store'
    respuesta.headers['X-Content-Type-Options'] = 'nosniff'
    respuesta.headers['X-Frame-Options'] = 'DENY'
    respuesta.headers['Content-Security-Policy'] = "default-src 'self'; form-action 'self'; frame-ancestors 'none'; base-uri 'self'"
    return respuesta

@app.route('/login', methods=['GET', 'POST'])
def login_v3():
    if request.method == 'POST':
        respuesta = cliente_api._llamar('POST', '/api/login', json={
            'username': request.form.get('username', ''), 'password': request.form.get('password', '')})
        if respuesta is not None and respuesta.status_code == 200:
            datos = respuesta.json()
            limpiar()
            session['sid'] = sesiones.crear(datos['access_token'], datos['expires_in'])
            csrf()
            return redirect(url_for('inicio'))
        flash('No se pudo iniciar sesión. Revisa tus credenciales y permisos.' if respuesta is not None else 'El servicio no está disponible.', 'error')
    return render_template('login_v3.html')

@app.route('/logout', methods=['POST'])
def logout_v3():
    respuesta = cliente_api._llamar('POST', '/api/logout')
    if respuesta is None or respuesta.status_code != 200:
        return render_template('estado_v3.html', mensaje='No se pudo cerrar la sesión en el servicio. Intenta nuevamente.'), 503
    limpiar()
    flash('Sesión cerrada en todos los dispositivos.', 'exito')
    return redirect(url_for('login_v3'))

def guardar_seguridad(recurso, campos, claves=None):
    datos = {c: request.form.get(c, '') for c in campos}
    if recurso == 'usuario' and claves and not datos.get('password'):
        datos.pop('password', None)
    if recurso == 'rol_usuario':
        for c in datos:
            try:
                datos[c] = int(datos[c])
            except ValueError:
                pass
    ruta = '/api/' + recurso + ('/' + claves if claves else '')
    respuesta = cliente_api._llamar('PATCH' if claves else 'POST', ruta, json=datos)
    if respuesta is None:
        flash('El servicio no está disponible.', 'error')
    elif respuesta.status_code in (200, 201):
        flash('Cambios guardados.', 'exito')
    else:
        for mensaje in cliente_api._mensajes(respuesta):
            flash(mensaje, 'error')

def pagina_seguridad(recurso, campos):
    if request.method == 'POST':
        guardar_seguridad(recurso, campos, request.form.get('id') or None)
        return redirect(request.path)
    respuesta = cliente_api._llamar('GET', '/api/' + recurso, params={'limite': 1000})
    filas = []
    if respuesta is None or respuesta.status_code != 200:
        flash('No se pudo cargar la información.', 'error')
    else:
        filas = respuesta.json()['datos']
    return render_template('seguridad_v3.html', recurso=recurso, campos=campos, filas=filas)

@app.route('/seguridad/usuarios', methods=['GET', 'POST'])
def seguridad_usuarios():
    return pagina_seguridad('usuario', ('username', 'email', 'nombre_completo', 'password'))

@app.route('/seguridad/roles', methods=['GET', 'POST'])
def seguridad_roles():
    return pagina_seguridad('rol', ('nombre', 'descripcion'))

@app.route('/seguridad/asignaciones', methods=['GET', 'POST'])
def seguridad_asignaciones():
    return pagina_seguridad('rol_usuario', ('usuario_id', 'rol_id'))

@app.route('/seguridad/<recurso>/<claves>/retirar', methods=['POST'])
def seguridad_retirar(recurso, claves):
    destinos = {'usuario': 'seguridad_usuarios', 'rol': 'seguridad_roles', 'rol_usuario': 'seguridad_asignaciones'}
    if recurso not in destinos:
        abort(404)
    if recurso == 'rol_usuario':
        try:
            usuario, rol = (int(c) for c in claves.split('-'))
        except ValueError:
            abort(404)
        claves = f'{usuario}/{rol}'
    elif not claves.isdigit():
        abort(404)
    respuesta = cliente_api._llamar('DELETE', '/api/' + recurso + '/' + claves)
    if respuesta is None:
        flash('El servicio no está disponible.', 'error')
    elif respuesta.status_code == 200:
        flash('Registro retirado.', 'exito')
    else:
        for mensaje in cliente_api._mensajes(respuesta):
            flash(mensaje, 'error')
    return redirect(url_for(destinos[recurso]))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PUERTO', '8078')), debug=False)
