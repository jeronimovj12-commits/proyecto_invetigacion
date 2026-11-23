# Ejecuta la instruccion indicada dentro del flujo actual.
"""Flask real -> HTTP -> FastAPI -> PostgreSQL aislado, sin mocks de transporte."""
# Carga el modulo o los modulos json.
import json
# Importa Path desde pathlib para usar esas definiciones.
from pathlib import Path
# Carga el modulo o los modulos re.
import re
# Carga el modulo o los modulos secrets.
import secrets
# Carga el modulo o los modulos unittest.
import unittest
# Carga el modulo o los modulos requests.
import requests
# Importa app, sesiones desde app_v3 para usar esas definiciones.
from app_v3 import app, sesiones
# Importa URL_API desde cliente_api para usar esas definiciones.
from cliente_api import URL_API

# Define la clase IntegracionCompleta y agrupa su estado y operaciones.
class IntegracionCompleta(unittest.TestCase):
    # Define la funcion setUp con los parametros declarados; su bloque realiza esta operacion.
    def setUp(self):
        # Guarda en self.cliente el valor necesario para reutilizarlo en otros metodos.
        self.cliente = app.test_client()
        # Guarda en self.cuentas el valor necesario para reutilizarlo en otros metodos.
        self.cuentas = json.loads(Path('/fixture/cuentas.json').read_text())

    # Define la funcion csrf con los parametros declarados; su bloque realiza esta operacion.
    def csrf(self, ruta):
        # Asigna a respuesta el valor calculado a la derecha.
        respuesta = self.cliente.get(ruta)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(respuesta.status_code, 200, ruta)
        # Devuelve al llamador el resultado de la expresion indicada.
        return re.search(rb'name="csrf_token" value="([^"]+)"', respuesta.data)[1].decode()

    # Define la funcion entrar con los parametros declarados; su bloque realiza esta operacion.
    def entrar(self, rol):
        # Devuelve al llamador el resultado de la expresion indicada.
        return self.cliente.post('/login', data={**self.cuentas[rol], 'csrf_token':self.csrf('/login')})

    # Define la funcion post con los parametros declarados; su bloque realiza esta operacion.
    def post(self, ruta, datos, pagina=None):
        # Devuelve al llamador el resultado de la expresion indicada.
        return self.cliente.post(ruta, data={**datos, 'csrf_token':self.csrf(pagina or ruta)})

    # Define la funcion test_recorrido_real con los parametros declarados; su bloque realiza esta operacion.
    def test_recorrido_real(self):
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.entrar('consulta').status_code, 302)
        # Asigna a respuesta el valor calculado a la derecha.
        respuesta = self.cliente.get('/areas-de-conocimiento')
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(respuesta.status_code, 200)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertIn(b'1A01', respuesta.data)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertNotIn(b'>Editar</a>', respuesta.data)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.cliente.get('/seguridad/usuarios').status_code, 403)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.cliente.get('/areas-de-conocimiento/nuevo').status_code, 403)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.post('/logout', {}, '/').status_code, 302)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.entrar('administrador').status_code, 302)
        # Recorre los elementos de la coleccion indicada y ejecuta el bloque para cada uno.
        for regla in app.url_map.iter_rules():
            # Ejecuta el bloque siguiente solo cuando se cumple: not regla.arguments and 'GET' in regla.methods and regla.endpoint != 'static'.
            if not regla.arguments and 'GET' in regla.methods and regla.endpoint != 'static':
                # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                self.assertEqual(self.cliente.get(regla.rule).status_code, 200, regla.rule)
        # Asigna a nombre el valor calculado a la derecha.
        nombre = 'PRUEBA_' + secrets.token_hex(5)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.post('/seguridad/roles', {'nombre':nombre,'descripcion':'Integración'}).status_code, 302)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertIn(nombre.encode(), self.cliente.get('/seguridad/roles').data)
        # Asigna a clave el valor calculado a la derecha.
        clave = secrets.token_urlsafe(24)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.post('/seguridad/usuarios', {'username':nombre,'email':nombre+'@example.invalid','nombre_completo':'Prueba','password':clave}).status_code, 302)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertIn(nombre.encode(), self.cliente.get('/seguridad/usuarios').data)
        # Abre el recurso y asegura su cierre al salir del bloque.
        with self.cliente.session_transaction() as sesion:
            # Asigna a token el valor calculado a la derecha.
            token = sesiones.obtener(sesion['sid'])
        # Asigna a cabecera el valor calculado a la derecha.
        cabecera = {'Authorization':'Bearer '+token}
        # Asigna a usuarios el valor calculado a la derecha.
        usuarios = requests.get(URL_API+'/api/usuario', headers=cabecera, timeout=10).json()['datos']
        # Asigna a uid el valor calculado a la derecha.
        uid = next(u['id'] for u in usuarios if u['username']==nombre)
        # Asigna a roles el valor calculado a la derecha.
        roles = requests.get(URL_API+'/api/rol', headers=cabecera, timeout=10).json()['datos']
        # Asigna a rid el valor calculado a la derecha.
        rid = next(r['id'] for r in roles if r['nombre']=='consulta')
        # Asigna a admin el valor calculado a la derecha.
        admin = next(r['id'] for r in roles if r['nombre']=='administrador')
        # Asigna a rol_creado el valor calculado a la derecha.
        rol_creado = next(r['id'] for r in roles if r['nombre']==nombre)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.post('/seguridad/asignaciones', {'usuario_id':uid,'rol_id':rid}).status_code, 302)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(requests.post(URL_API+'/api/login', json={'username':nombre,'password':clave}, timeout=10).status_code, 200)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.post('/seguridad/asignaciones', {'id':f'{uid}/{rid}', 'usuario_id':uid, 'rol_id':rol_creado}).status_code, 302)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(requests.post(URL_API+'/api/login', json={'username':nombre,'password':clave}, timeout=10).status_code, 403)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(requests.get(URL_API+f'/api/rol_usuario/{uid}/{rid}', headers=cabecera, timeout=10).status_code, 404)
        # El error de último administrador se presenta dentro de la aplicación.
        # Asigna a respuesta el valor calculado a la derecha.
        respuesta = self.post(f'/seguridad/rol/{admin}/retirar', {}, '/seguridad/roles')
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(respuesta.status_code, 302)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertIn('sin administrador activo'.encode(), self.cliente.get('/seguridad/roles').data)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.post('/logout', {}, '/').status_code, 302)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(requests.get(URL_API+'/api/sesion', headers=cabecera, timeout=10).status_code, 401)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.cliente.get('/areas-de-conocimiento').status_code, 302)

# Ejecuta el bloque siguiente solo cuando se cumple: __name__ == '__main__'.
if __name__ == '__main__':
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    unittest.main(verbosity=2)
