"""Permisos HTTP v3 y reglas de sesión con repositorio falso."""
import asyncio
import json
import re
import secrets
import time
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import prueba_autenticacion_v3 as base
from seguridad.adaptadores import TokensJWT
from seguridad.errores import AutenticacionFallida, PermisoInsuficiente
from servicios.servicio_autenticacion import ServicioAutenticacion


def pedir_con_cabeceras(metodo, ruta, datos=None, cabeceras=None):
    encabezados = {'Content-Type': 'application/json', **(cabeceras or {})}
    peticion = Request(
        base.URL + ruta,
        data=json.dumps(datos).encode() if datos is not None else None,
        headers=encabezados,
        method=metodo,
    )
    try:
        respuesta = urlopen(peticion, timeout=15)
    except HTTPError as error:
        respuesta = error
    with respuesta:
        contenido = respuesta.read()
        cuerpo = json.loads(contenido) if contenido else None
        return respuesta.status, cuerpo, respuesta.headers


class RepositorioFalso:
    def __init__(self, usuario):
        self.usuario = usuario

    async def por_nombre(self, nombre):
        return self.usuario if nombre == self.usuario['username'] else None

    async def por_id(self, usuario_id):
        return self.usuario if usuario_id == self.usuario['id'] else None

    async def revocar(self, usuario_id, version):
        if usuario_id != self.usuario['id'] or version != self.usuario['version_sesion']:
            return False
        self.usuario['version_sesion'] += 1
        return True


class ClavesFalsas:
    def crear(self, clave):
        return 'hash-falso'

    def verificar(self, clave, resumen):
        return clave == 'clave-correcta' and resumen == 'hash-falso'


class TokensFalsos:
    segundos = 60

    def emitir(self, usuario_id, version):
        return f'token:{usuario_id}:{version}'

    def validar(self, token):
        partes = token.split(':')
        if len(partes) != 3 or partes[0] != 'token':
            raise AutenticacionFallida()
        try:
            usuario_id, version = int(partes[1]), int(partes[2])
        except ValueError:
            raise AutenticacionFallida() from None
        return {'sub': str(usuario_id), 'version_sesion': version}


class ReglasConRepositorioFalso(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.usuario = {
            'id': 42, 'username': 'FALSO', 'password': 'hash-falso',
            'email': 'falso@example.invalid', 'nombre_completo': None,
            'activo': True, 'version_sesion': 0, 'roles': ['consulta'],
        }
        self.repositorio = RepositorioFalso(self.usuario)
        self.servicio = ServicioAutenticacion(self.repositorio, ClavesFalsas(), TokensFalsos())

    async def test_login_lectura_y_logout_revoca_version(self):
        resultado = await self.servicio.login('FALSO', 'clave-correcta')
        self.assertEqual(resultado['access_token'], 'token:42:0')
        self.assertEqual((await self.servicio.sesion('token:42:0'))['roles'], ['consulta'])
        await self.servicio.logout('token:42:0')
        self.assertEqual(self.usuario['version_sesion'], 1)
        with self.assertRaises(AutenticacionFallida):
            await self.servicio.sesion('token:42:0')

    async def test_usuario_inactivo_y_sin_rol_no_autentican(self):
        self.usuario['activo'] = False
        with self.assertRaises(AutenticacionFallida):
            await self.servicio.sesion('token:42:0')
        self.usuario['activo'] = True
        self.usuario['roles'] = []  # rol o asignación inactivos no aparecen en la identidad
        with self.assertRaises(PermisoInsuficiente):
            await self.servicio.sesion('token:42:0')


class PermisosEquipoHTTP(base.AutenticacionHTTP):
    def test_token_en_url_o_cookie_no_autentica(self):
        token = self.token()
        estado_url = pedir_con_cabeceras(
            'GET', f'/api/area_conocimiento?access_token={token}'
        )[0]
        estado_cookie = pedir_con_cabeceras(
            'GET', '/api/area_conocimiento', cabeceras={'Cookie': f'access_token={token}'}
        )[0]
        self.assertEqual(estado_url, 401)
        self.assertEqual(estado_cookie, 401)

    def test_sin_token_alterado_vencido_y_revocado(self):
        self.assertEqual(base.pedir('GET', '/api/sesion')[0], 401)
        self.assertEqual(base.pedir('GET', '/api/area_conocimiento')[0], 401)

        primero = self.token()
        partes = primero.split('.')
        partes[1] = ('A' if partes[1][0] != 'A' else 'B') + partes[1][1:]
        self.assertEqual(base.pedir('GET', '/api/sesion', token='.'.join(partes))[0], 401)

        ahora = int(time.time())
        vencido = self.firmar({'iat': ahora - 120, 'exp': ahora - 60})
        self.assertEqual(base.pedir('GET', '/api/sesion', token=vencido)[0], 401)

        segundo = self.token()
        self.assertEqual(base.pedir('POST', '/api/logout', token=primero)[0], 200)
        for token in (primero, segundo):
            self.assertEqual(base.pedir('GET', '/api/sesion', token=token)[0], 401)
            self.assertEqual(base.pedir('GET', '/api/area_conocimiento', token=token)[0], 401)

    def test_matriz_consulta_solo_lee_y_administrador_accede(self):
        contrato = base.pedir('GET', '/openapi.json')[1]
        token_consulta = self.token()
        token_administrador = TokensJWT(base.CONFIG).emitir(1, 0)
        operaciones = 0

        for ruta, metodos in contrato['paths'].items():
            if not ruta.startswith('/api/') or ruta in ('/api/login', '/api/logout', '/api/sesion'):
                continue
            ruta_real = re.sub(r'\{[^}]+\}', '999999', ruta)
            es_seguridad = ruta.split('/')[2] in ('usuario', 'rol', 'rol_usuario')
            for metodo, operacion in metodos.items():
                if metodo not in ('get', 'post', 'put', 'patch', 'delete'):
                    continue
                operaciones += 1
                self.assertEqual(operacion.get('security'), [{'HTTPBearer': []}], ruta)
                datos = None if metodo == 'get' else {}

                estado_consulta = base.pedir(metodo.upper(), ruta_real, datos, token_consulta)[0]
                if es_seguridad or metodo != 'get':
                    self.assertEqual(estado_consulta, 403, f'{metodo.upper()} {ruta}')
                else:
                    self.assertIn(estado_consulta, (200, 204, 404, 422), f'{metodo.upper()} {ruta}')

                estado_administrador = base.pedir(metodo.upper(), ruta_real, datos, token_administrador)[0]
                self.assertNotIn(estado_administrador, (401, 403), f'{metodo.upper()} {ruta}')

        self.assertGreater(operaciones, 60)
        print('Operaciones con permisos verificados:', operaciones)

    async def test_rechazos_no_modifican_datos(self):
        token = self.token()
        consulta_id = (await self.sql("SELECT id FROM rol WHERE nombre='consulta'")).scalar_one()
        nombre = 'BLOQUEADO_' + secrets.token_hex(4)
        codigo = 'T' + secrets.token_hex(2).upper()

        async def fotografia():
            valores = {}
            for tabla in ('usuario', 'rol', 'rol_usuario', 'area_conocimiento'):
                valores[tabla] = (await self.sql(f'SELECT count(*) FROM {tabla}')).scalar_one()
            valores['email'] = (await self.sql(
                'SELECT email FROM usuario WHERE id=:id', id=self.usuario
            )).scalar_one()
            valores['nombre_rol'] = (await self.sql(
                'SELECT nombre FROM rol WHERE id=:id', id=consulta_id
            )).scalar_one()
            valores['asignacion_activa'] = (await self.sql(
                'SELECT activo FROM rol_usuario WHERE usuario_id=:uid AND rol_id=:rid',
                uid=self.usuario, rid=consulta_id
            )).scalar_one()
            return valores

        antes = await fotografia()
        intentos = (
            ('POST', '/api/usuario', {'username': nombre, 'email': nombre+'@example.invalid', 'password': secrets.token_urlsafe(18)}),
            ('PATCH', f'/api/usuario/{self.usuario}', {'email': 'cambio@example.invalid'}),
            ('POST', '/api/rol', {'nombre': nombre, 'descripcion': 'No autorizado'}),
            ('PATCH', f'/api/rol/{consulta_id}', {'nombre': nombre}),
            ('POST', '/api/rol_usuario', {'usuario_id': self.usuario, 'rol_id': consulta_id}),
            ('DELETE', f'/api/rol_usuario/{self.usuario}/{consulta_id}', None),
            ('POST', '/api/area_conocimiento', {'id': codigo, 'granArea': 'Prueba', 'area': 'Prueba', 'disciplina': 'Prueba'}),
        )
        for metodo, ruta, datos in intentos:
            self.assertEqual(base.pedir(metodo, ruta, datos, token)[0], 403, f'{metodo} {ruta}')
        self.assertEqual(await fotografia(), antes)
        self.assertEqual((await self.sql(
            'SELECT count(*) FROM area_conocimiento WHERE id=:id', id=codigo
        )).scalar_one(), 0)

    async def test_usuario_rol_y_asignacion_inactivos_no_autorizan(self):
        token = self.token()
        consulta_id = (await self.sql("SELECT id FROM rol WHERE nombre='consulta'")).scalar_one()

        await self.sql('UPDATE usuario SET activo=FALSE WHERE id=:id', id=self.usuario)
        self.assertEqual(base.pedir('GET', '/api/sesion', token=token)[0], 401)
        await self.sql('UPDATE usuario SET activo=TRUE WHERE id=:id', id=self.usuario)

        await self.sql('UPDATE rol SET activo=FALSE WHERE id=:id', id=consulta_id)
        self.assertEqual(base.pedir('GET', '/api/sesion', token=token)[0], 403)
        await self.sql('UPDATE rol SET activo=TRUE WHERE id=:id', id=consulta_id)

        await self.sql('UPDATE rol_usuario SET activo=FALSE WHERE usuario_id=:uid AND rol_id=:rid', uid=self.usuario, rid=consulta_id)
        self.assertEqual(base.pedir('GET', '/api/sesion', token=token)[0], 403)
        self.assertEqual(base.pedir('GET', '/api/area_conocimiento', token=token)[0], 403)

    async def test_administrador_realiza_crud_de_seguridad_permitido(self):
        token = TokensJWT(base.CONFIG).emitir(1, 0)
        nombre = 'ADMIN_' + secrets.token_hex(4)
        clave = secrets.token_urlsafe(18)

        estado, rol, _ = base.pedir('POST', '/api/rol', {'nombre': nombre, 'descripcion': 'Prueba'}, token)
        self.assertEqual(estado, 201)
        rid = rol['id']
        self.assertEqual(base.pedir('GET', f'/api/rol/{rid}', token=token)[0], 200)
        self.assertEqual(base.pedir('PATCH', f'/api/rol/{rid}', {'descripcion': 'Actualizado'}, token)[0], 200)

        estado, usuario, _ = base.pedir('POST', '/api/usuario', {
            'username': nombre, 'email': nombre+'@example.invalid', 'password': clave,
        }, token)
        self.assertEqual(estado, 201)
        uid = usuario['id']
        self.assertEqual(base.pedir('GET', f'/api/usuario/{uid}', token=token)[0], 200)
        consulta_id = (await self.sql("SELECT id FROM rol WHERE nombre='consulta'")).scalar_one()
        relacion = {'usuario_id': uid, 'rol_id': consulta_id}
        self.assertEqual(base.pedir('POST', '/api/rol_usuario', relacion, token)[0], 201)
        self.assertEqual(base.pedir('GET', f'/api/rol_usuario/{uid}/{consulta_id}', token=token)[0], 200)
        self.assertEqual(base.pedir('DELETE', f'/api/rol_usuario/{uid}/{consulta_id}', token=token)[0], 200)
        self.assertEqual(base.pedir('DELETE', f'/api/usuario/{uid}', token=token)[0], 200)
        self.assertEqual(base.pedir('DELETE', f'/api/rol/{rid}', token=token)[0], 200)


if __name__ == '__main__':
    asyncio.run(base.preparar())
    try:
        base.arrancar()
        suite = unittest.TestSuite()
        for clase in (ReglasConRepositorioFalso, PermisosEquipoHTTP):
            nombres = [nombre for nombre in clase.__dict__ if nombre.startswith('test_')]
            suite.addTests(clase(nombre) for nombre in nombres)
        resultado = unittest.TextTestRunner(verbosity=2).run(suite)
    finally:
        base.detener()
    raise SystemExit(0 if resultado.wasSuccessful() else 1)
