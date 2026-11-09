"""Flask real -> HTTP -> FastAPI -> PostgreSQL aislado, sin mocks de transporte."""
import json
from pathlib import Path
import re
import secrets
import unittest
import requests
from app_v3 import app, sesiones
from cliente_api import URL_API

class IntegracionCompleta(unittest.TestCase):
    def setUp(self):
        self.cliente = app.test_client()
        self.cuentas = json.loads(Path('/fixture/cuentas.json').read_text())

    def csrf(self, ruta):
        respuesta = self.cliente.get(ruta)
        self.assertEqual(respuesta.status_code, 200, ruta)
        return re.search(rb'name="csrf_token" value="([^"]+)"', respuesta.data)[1].decode()

    def entrar(self, rol):
        return self.cliente.post('/login', data={**self.cuentas[rol], 'csrf_token':self.csrf('/login')})

    def post(self, ruta, datos, pagina=None):
        return self.cliente.post(ruta, data={**datos, 'csrf_token':self.csrf(pagina or ruta)})

    def test_recorrido_real(self):
        self.assertEqual(self.entrar('consulta').status_code, 302)
        respuesta = self.cliente.get('/areas-de-conocimiento')
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn(b'1A01', respuesta.data)
        self.assertNotIn(b'>Editar</a>', respuesta.data)
        self.assertEqual(self.cliente.get('/seguridad/usuarios').status_code, 403)
        self.assertEqual(self.cliente.get('/areas-de-conocimiento/nuevo').status_code, 403)
        self.assertEqual(self.post('/logout', {}, '/').status_code, 302)
        self.assertEqual(self.entrar('administrador').status_code, 302)
        for regla in app.url_map.iter_rules():
            if not regla.arguments and 'GET' in regla.methods and regla.endpoint != 'static':
                self.assertEqual(self.cliente.get(regla.rule).status_code, 200, regla.rule)
        nombre = 'PRUEBA_' + secrets.token_hex(5)
        self.assertEqual(self.post('/seguridad/roles', {'nombre':nombre,'descripcion':'Integración'}).status_code, 302)
        self.assertIn(nombre.encode(), self.cliente.get('/seguridad/roles').data)
        clave = secrets.token_urlsafe(24)
        self.assertEqual(self.post('/seguridad/usuarios', {'username':nombre,'email':nombre+'@example.invalid','nombre_completo':'Prueba','password':clave}).status_code, 302)
        self.assertIn(nombre.encode(), self.cliente.get('/seguridad/usuarios').data)
        with self.cliente.session_transaction() as sesion:
            token = sesiones.obtener(sesion['sid'])
        cabecera = {'Authorization':'Bearer '+token}
        usuarios = requests.get(URL_API+'/api/usuario', headers=cabecera, timeout=10).json()['datos']
        uid = next(u['id'] for u in usuarios if u['username']==nombre)
        roles = requests.get(URL_API+'/api/rol', headers=cabecera, timeout=10).json()['datos']
        rid = next(r['id'] for r in roles if r['nombre']=='consulta')
        admin = next(r['id'] for r in roles if r['nombre']=='administrador')
        self.assertEqual(self.post('/seguridad/asignaciones', {'usuario_id':uid,'rol_id':rid}).status_code, 302)
        self.assertEqual(requests.post(URL_API+'/api/login', json={'username':nombre,'password':clave}, timeout=10).status_code, 200)
        # El error de último administrador se presenta dentro de la aplicación.
        respuesta = self.post(f'/seguridad/rol/{admin}/retirar', {}, '/seguridad/roles')
        self.assertEqual(respuesta.status_code, 302)
        self.assertIn('sin administrador activo'.encode(), self.cliente.get('/seguridad/roles').data)
        self.assertEqual(self.post('/logout', {}, '/').status_code, 302)
        self.assertEqual(requests.get(URL_API+'/api/sesion', headers=cabecera, timeout=10).status_code, 401)
        self.assertEqual(self.cliente.get('/areas-de-conocimiento').status_code, 302)

if __name__ == '__main__':
    unittest.main(verbosity=2)
