# Ejecuta la instruccion indicada dentro del flujo actual.
"""Pruebas de presentación con cliente Flask y transporte HTTP simulado."""
# Carga el modulo o los modulos os.
import os
# Carga el modulo o los modulos re.
import re
# Carga el modulo o los modulos secrets.
import secrets
# Carga el modulo o los modulos tempfile.
import tempfile
# Carga el modulo o los modulos unittest.
import unittest
# Importa Path desde pathlib para usar esas definiciones.
from pathlib import Path
# Importa patch desde unittest.mock para usar esas definiciones.
from unittest.mock import patch
# Carga el modulo o los modulos requests.
import requests

# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
os.environ['CLAVE_SESION'] = secrets.token_urlsafe(48)
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
os.environ['SESIONES_ARCHIVO'] = str(Path(tempfile.mkdtemp()) / 'sesiones.sqlite3')
# Importa app, sesiones desde app_v3 para usar esas definiciones.
from app_v3 import app, sesiones

# Define la clase FrontSeguro y agrupa su estado y operaciones.
class FrontSeguro(unittest.TestCase):
    # Define la funcion setUp con los parametros declarados; su bloque realiza esta operacion.
    def setUp(self):
        # Guarda en self.cliente el valor necesario para reutilizarlo en otros metodos.
        self.cliente = app.test_client()
        # Guarda en self.rol el valor necesario para reutilizarlo en otros metodos.
        self.rol = 'administrador'
        # Guarda en self.estado el valor necesario para reutilizarlo en otros metodos.
        self.estado = 200
        # Guarda en self.caida el valor necesario para reutilizarlo en otros metodos.
        self.caida = False
        # Guarda en self.jwt el valor necesario para reutilizarlo en otros metodos.
        self.jwt = secrets.token_urlsafe(64)
        # Guarda en self.llamadas el valor necesario para reutilizarlo en otros metodos.
        self.llamadas = []
        # Guarda en self.parche el valor necesario para reutilizarlo en otros metodos.
        self.parche = patch('cliente_api.requests.request', side_effect=self.transporte)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.parche.start()

    # Define la funcion tearDown con los parametros declarados; su bloque realiza esta operacion.
    def tearDown(self):
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.parche.stop()

    # Define la funcion transporte con los parametros declarados; su bloque realiza esta operacion.
    def transporte(self, metodo, url, **kwargs):
        # Carga el modulo o los modulos json.
        import json
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.llamadas.append((metodo, url, kwargs))
        # Ejecuta el bloque siguiente solo cuando se cumple: self.caida.
        if self.caida:
            # Lanza la excepcion indicada y detiene el flujo normal.
            raise requests.ConnectionError()
        # Asigna a respuesta el valor calculado a la derecha.
        respuesta = requests.Response()
        # Asigna a respuesta.status_code el valor calculado a la derecha.
        respuesta.status_code = self.estado if not url.endswith('/login') else 200
        # Ejecuta el bloque siguiente solo cuando se cumple: url.endswith('/login').
        if url.endswith('/login'):
            # Asigna a cuerpo el valor calculado a la derecha.
            cuerpo = {'access_token':self.jwt, 'expires_in':1800, 'usuario':{}}
        # Prueba esta condicion alternativa si las anteriores fueron falsas.
        elif url.endswith('/sesion'):
            # Asigna a cuerpo el valor calculado a la derecha.
            cuerpo = {'username':'PRUEBA', 'roles':[self.rol]}
        # Prueba esta condicion alternativa si las anteriores fueron falsas.
        elif url.endswith('/logout'):
            # Asigna a cuerpo el valor calculado a la derecha.
            cuerpo = {'estado':200}
        # Prueba esta condicion alternativa si las anteriores fueron falsas.
        elif '/usuario' in url:
            # Asigna a cuerpo el valor calculado a la derecha.
            cuerpo = {'datos':[{'id':1, 'username':'cuenta', 'email':'c@example.invalid', 'nombre_completo':None, 'activo':True}]}
        # Prueba esta condicion alternativa si las anteriores fueron falsas.
        elif '/rol_usuario' in url:
            # Asigna a cuerpo el valor calculado a la derecha.
            cuerpo = {'datos':[{'usuario_id':1, 'rol_id':1, 'activo':True}]}
        # Prueba esta condicion alternativa si las anteriores fueron falsas.
        elif '/rol' in url:
            # Asigna a cuerpo el valor calculado a la derecha.
            cuerpo = {'datos':[{'id':1, 'nombre':'consulta', 'descripcion':None, 'activo':True}]}
        # Prueba esta condicion alternativa si las anteriores fueron falsas.
        elif '/area_conocimiento' in url:
            # Asigna a cuerpo el valor calculado a la derecha.
            cuerpo = {'datos':[{'id':'PRUEBA', 'gran_area':'Ciencias', 'area':'Área', 'disciplina':'Disciplina'}]}
        # Define el caso alternativo cuando las condiciones anteriores no se cumplen.
        else:
            # Asigna a cuerpo el valor calculado a la derecha.
            cuerpo = {'datos':[]}
        # Asigna a respuesta._content el valor calculado a la derecha.
        respuesta._content = json.dumps(cuerpo).encode()
        # Devuelve al llamador el resultado de la expresion indicada.
        return respuesta

    # Define la funcion csrf con los parametros declarados; su bloque realiza esta operacion.
    def csrf(self, ruta='/login'):
        # Asigna a respuesta el valor calculado a la derecha.
        respuesta = self.cliente.get(ruta)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(respuesta.status_code, 200)
        # Devuelve al llamador el resultado de la expresion indicada.
        return re.search(rb'name="csrf_token" value="([^"]+)"', respuesta.data)[1].decode()

    # Define la funcion entrar con los parametros declarados; su bloque realiza esta operacion.
    def entrar(self):
        # Asigna a token el valor calculado a la derecha.
        token = self.csrf()
        # Asigna a respuesta el valor calculado a la derecha.
        respuesta = self.cliente.post('/login', data={'csrf_token':token, 'username':'PRUEBA', 'password':secrets.token_urlsafe(24)})
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(respuesta.status_code, 302)
        # Devuelve al llamador el resultado de la expresion indicada.
        return respuesta

    # Define la funcion test_login_csrf_cookie_y_rotacion con los parametros declarados; su bloque realiza esta operacion.
    def test_login_csrf_cookie_y_rotacion(self):
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.cliente.get('/docente').status_code, 302)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.cliente.post('/login', data={'username':'PRUEBA'}).status_code, 400)
        # Asigna a anterior el valor calculado a la derecha.
        anterior = self.csrf()
        # Asigna a respuesta el valor calculado a la derecha.
        respuesta = self.entrar()
        # Asigna a cookie el valor calculado a la derecha.
        cookie = respuesta.headers['Set-Cookie']
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertIn('HttpOnly', cookie)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertIn('SameSite=Lax', cookie)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertNotIn(self.jwt, cookie)
        # Abre el recurso y asegura su cierre al salir del bloque.
        with self.cliente.session_transaction() as sesion:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            self.assertNotIn('token', sesion)
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            self.assertNotIn('access_token', sesion)
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            self.assertNotEqual(sesion['csrf'], anterior)
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            self.assertEqual(sesiones.obtener(sesion['sid']), self.jwt)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(respuesta.headers['Cache-Control'], 'no-store')

    # Define la funcion test_consulta_solo_lectura_y_urls_directas con los parametros declarados; su bloque realiza esta operacion.
    def test_consulta_solo_lectura_y_urls_directas(self):
        # Guarda en self.rol el valor necesario para reutilizarlo en otros metodos.
        self.rol = 'consulta'
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.entrar()
        # Recorre los elementos de la coleccion indicada y ejecuta el bloque para cada uno.
        for ruta in ('/areas-de-conocimiento', '/docente', '/grupo-investigacion', '/semillero'):
            # Asigna a respuesta el valor calculado a la derecha.
            respuesta = self.cliente.get(ruta)
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            self.assertEqual(respuesta.status_code, 200)
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            self.assertNotIn(b'>Editar</a>', respuesta.data)
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            self.assertNotIn(b'Retirar ficha</button>', respuesta.data)
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            self.assertNotIn(b'/seguridad/usuarios', respuesta.data)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.cliente.get('/areas-de-conocimiento/nuevo').status_code, 403)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.cliente.get('/seguridad/usuarios').status_code, 403)
        # Asigna a csrf el valor calculado a la derecha.
        csrf = self.csrf('/areas-de-conocimiento')
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.cliente.post('/areas-de-conocimiento/1A01/eliminar', data={'csrf_token':csrf}).status_code, 403)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertFalse(any(m == 'DELETE' for m, _, _ in self.llamadas))

    # Define la funcion test_admin_todas_las_plantillas_y_csrf con los parametros declarados; su bloque realiza esta operacion.
    def test_admin_todas_las_plantillas_y_csrf(self):
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.entrar()
        # Recorre los elementos de la coleccion indicada y ejecuta el bloque para cada uno.
        for regla in app.url_map.iter_rules():
            # Ejecuta el bloque siguiente solo cuando se cumple: regla.arguments or 'GET' not in regla.methods or regla.endpoint == 'static'.
            if regla.arguments or 'GET' not in regla.methods or regla.endpoint == 'static':
                # Salta al siguiente ciclo de la repeticion.
                continue
            # Asigna a respuesta el valor calculado a la derecha.
            respuesta = self.cliente.get(regla.rule)
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            self.assertEqual(respuesta.status_code, 200, regla.rule)
            # Recorre los elementos de la coleccion indicada y ejecuta el bloque para cada uno.
            for formulario in re.findall(rb'<form\b.*?</form>', respuesta.data, re.S):
                # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                self.assertIn(b'name="csrf_token"', formulario, regla.rule)
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            self.assertNotIn(self.jwt.encode(), respuesta.data)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.cliente.post('/seguridad/usuarios', data={}).status_code, 400)

    # Define la funcion test_401_403_caida_y_vencimiento_local con los parametros declarados; su bloque realiza esta operacion.
    def test_401_403_caida_y_vencimiento_local(self):
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.entrar()
        # Guarda en self.estado el valor necesario para reutilizarlo en otros metodos.
        self.estado = 403
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.cliente.get('/docente').status_code, 403)
        # Guarda en self.estado el valor necesario para reutilizarlo en otros metodos.
        self.estado = 401
        # Asigna a respuesta el valor calculado a la derecha.
        respuesta = self.cliente.get('/docente')
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(respuesta.status_code, 302)
        # Abre el recurso y asegura su cierre al salir del bloque.
        with self.cliente.session_transaction() as sesion:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            self.assertNotIn('sid', sesion)
        # Guarda en self.estado el valor necesario para reutilizarlo en otros metodos.
        self.estado = 200
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.entrar()
        # Guarda en self.estado el valor necesario para reutilizarlo en otros metodos.
        self.estado = 500
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.cliente.get('/docente').status_code, 503)
        # Guarda en self.estado el valor necesario para reutilizarlo en otros metodos.
        self.estado = 200
        # Guarda en self.caida el valor necesario para reutilizarlo en otros metodos.
        self.caida = True
        # Asigna a respuesta el valor calculado a la derecha.
        respuesta = self.cliente.get('/docente')
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(respuesta.status_code, 503)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertNotIn(b'cuenta', respuesta.data)
        # Guarda en self.caida el valor necesario para reutilizarlo en otros metodos.
        self.caida = False
        # Abre el recurso y asegura su cierre al salir del bloque.
        with self.cliente.session_transaction() as sesion:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            sesiones.retirar(sesion['sid'])
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.cliente.get('/docente').status_code, 302)

    # Define la funcion test_logout_con_csrf_y_bearer_solo_servidor con los parametros declarados; su bloque realiza esta operacion.
    def test_logout_con_csrf_y_bearer_solo_servidor(self):
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.entrar()
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.cliente.get('/logout').status_code, 405)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.cliente.post('/logout').status_code, 400)
        # Asigna a csrf el valor calculado a la derecha.
        csrf = self.csrf('/docente')
        # Asigna a respuesta el valor calculado a la derecha.
        respuesta = self.cliente.post('/logout', data={'csrf_token':csrf})
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(respuesta.status_code, 302)
        # Abre el recurso y asegura su cierre al salir del bloque.
        with self.cliente.session_transaction() as sesion:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            self.assertNotIn('sid', sesion)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertTrue(any(url.endswith('/logout') and datos['headers']['Authorization'] == 'Bearer '+self.jwt for _,url,datos in self.llamadas))
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.cliente.get('/docente').status_code, 302)

# Ejecuta el bloque siguiente solo cuando se cumple: __name__ == '__main__'.
if __name__ == '__main__':
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    unittest.main(verbosity=2)
