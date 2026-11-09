"""Pruebas de presentación con cliente Flask y transporte HTTP simulado."""
import os
import re
import secrets
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import requests

os.environ['CLAVE_SESION'] = secrets.token_urlsafe(48)
os.environ['SESIONES_ARCHIVO'] = str(Path(tempfile.mkdtemp()) / 'sesiones.sqlite3')
from app_v3 import app, sesiones

class FrontSeguro(unittest.TestCase):
    def setUp(self):
        self.cliente = app.test_client()
        self.rol = 'administrador'
        self.estado = 200
        self.caida = False
        self.jwt = secrets.token_urlsafe(64)
        self.llamadas = []
        self.parche = patch('cliente_api.requests.request', side_effect=self.transporte)
        self.parche.start()

    def tearDown(self):
        self.parche.stop()

    def transporte(self, metodo, url, **kwargs):
        import json
        self.llamadas.append((metodo, url, kwargs))
        if self.caida:
            raise requests.ConnectionError()
        respuesta = requests.Response()
        respuesta.status_code = self.estado if not url.endswith('/login') else 200
        if url.endswith('/login'):
            cuerpo = {'access_token':self.jwt, 'expires_in':1800, 'usuario':{}}
        elif url.endswith('/sesion'):
            cuerpo = {'username':'PRUEBA', 'roles':[self.rol]}
        elif url.endswith('/logout'):
            cuerpo = {'estado':200}
        elif '/usuario' in url:
            cuerpo = {'datos':[{'id':1, 'username':'cuenta', 'email':'c@example.invalid', 'nombre_completo':None, 'activo':True}]}
        elif '/rol_usuario' in url:
            cuerpo = {'datos':[{'usuario_id':1, 'rol_id':1, 'activo':True}]}
        elif '/rol' in url:
            cuerpo = {'datos':[{'id':1, 'nombre':'consulta', 'descripcion':None, 'activo':True}]}
        elif '/area_conocimiento' in url:
            cuerpo = {'datos':[{'id':'PRUEBA', 'gran_area':'Ciencias', 'area':'Área', 'disciplina':'Disciplina'}]}
        else:
            cuerpo = {'datos':[]}
        respuesta._content = json.dumps(cuerpo).encode()
        return respuesta

    def csrf(self, ruta='/login'):
        respuesta = self.cliente.get(ruta)
        self.assertEqual(respuesta.status_code, 200)
        return re.search(rb'name="csrf_token" value="([^"]+)"', respuesta.data)[1].decode()

    def entrar(self):
        token = self.csrf()
        respuesta = self.cliente.post('/login', data={'csrf_token':token, 'username':'PRUEBA', 'password':secrets.token_urlsafe(24)})
        self.assertEqual(respuesta.status_code, 302)
        return respuesta

    def test_login_csrf_cookie_y_rotacion(self):
        self.assertEqual(self.cliente.get('/docente').status_code, 302)
        self.assertEqual(self.cliente.post('/login', data={'username':'PRUEBA'}).status_code, 400)
        anterior = self.csrf()
        respuesta = self.entrar()
        cookie = respuesta.headers['Set-Cookie']
        self.assertIn('HttpOnly', cookie)
        self.assertIn('SameSite=Lax', cookie)
        self.assertNotIn(self.jwt, cookie)
        with self.cliente.session_transaction() as sesion:
            self.assertNotIn('token', sesion)
            self.assertNotIn('access_token', sesion)
            self.assertNotEqual(sesion['csrf'], anterior)
            self.assertEqual(sesiones.obtener(sesion['sid']), self.jwt)
        self.assertEqual(respuesta.headers['Cache-Control'], 'no-store')

    def test_consulta_solo_lectura_y_urls_directas(self):
        self.rol = 'consulta'
        self.entrar()
        for ruta in ('/areas-de-conocimiento', '/docente', '/grupo-investigacion', '/semillero'):
            respuesta = self.cliente.get(ruta)
            self.assertEqual(respuesta.status_code, 200)
            self.assertNotIn(b'>Editar</a>', respuesta.data)
            self.assertNotIn(b'Retirar ficha</button>', respuesta.data)
            self.assertNotIn(b'/seguridad/usuarios', respuesta.data)
        self.assertEqual(self.cliente.get('/areas-de-conocimiento/nuevo').status_code, 403)
        self.assertEqual(self.cliente.get('/seguridad/usuarios').status_code, 403)
        csrf = self.csrf('/areas-de-conocimiento')
        self.assertEqual(self.cliente.post('/areas-de-conocimiento/1A01/eliminar', data={'csrf_token':csrf}).status_code, 403)
        self.assertFalse(any(m == 'DELETE' for m, _, _ in self.llamadas))

    def test_admin_todas_las_plantillas_y_csrf(self):
        self.entrar()
        for regla in app.url_map.iter_rules():
            if regla.arguments or 'GET' not in regla.methods or regla.endpoint == 'static':
                continue
            respuesta = self.cliente.get(regla.rule)
            self.assertEqual(respuesta.status_code, 200, regla.rule)
            for formulario in re.findall(rb'<form\b.*?</form>', respuesta.data, re.S):
                self.assertIn(b'name="csrf_token"', formulario, regla.rule)
            self.assertNotIn(self.jwt.encode(), respuesta.data)
        self.assertEqual(self.cliente.post('/seguridad/usuarios', data={}).status_code, 400)

    def test_401_403_caida_y_vencimiento_local(self):
        self.entrar()
        self.estado = 403
        self.assertEqual(self.cliente.get('/docente').status_code, 403)
        self.estado = 401
        respuesta = self.cliente.get('/docente')
        self.assertEqual(respuesta.status_code, 302)
        with self.cliente.session_transaction() as sesion:
            self.assertNotIn('sid', sesion)
        self.estado = 200
        self.entrar()
        self.estado = 500
        self.assertEqual(self.cliente.get('/docente').status_code, 503)
        self.estado = 200
        self.caida = True
        respuesta = self.cliente.get('/docente')
        self.assertEqual(respuesta.status_code, 503)
        self.assertNotIn(b'cuenta', respuesta.data)
        self.caida = False
        with self.cliente.session_transaction() as sesion:
            sesiones.retirar(sesion['sid'])
        self.assertEqual(self.cliente.get('/docente').status_code, 302)

    def test_logout_con_csrf_y_bearer_solo_servidor(self):
        self.entrar()
        self.assertEqual(self.cliente.get('/logout').status_code, 405)
        self.assertEqual(self.cliente.post('/logout').status_code, 400)
        csrf = self.csrf('/docente')
        respuesta = self.cliente.post('/logout', data={'csrf_token':csrf})
        self.assertEqual(respuesta.status_code, 302)
        with self.cliente.session_transaction() as sesion:
            self.assertNotIn('sid', sesion)
        self.assertTrue(any(url.endswith('/logout') and datos['headers']['Authorization'] == 'Bearer '+self.jwt for _,url,datos in self.llamadas))
        self.assertEqual(self.cliente.get('/docente').status_code, 302)

if __name__ == '__main__':
    unittest.main(verbosity=2)
