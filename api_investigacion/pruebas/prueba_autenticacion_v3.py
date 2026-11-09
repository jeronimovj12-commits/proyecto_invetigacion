"""Integración real, solo compose v3 aislado. No imprime claves, hashes o JWT."""
import asyncio
import json
import os
from pathlib import Path
import secrets
import subprocess
import sys
import time
import unittest
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from uuid import uuid4

import asyncpg
import jwt
from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from seguridad.adaptadores import ClavesArgon2, ConfiguracionSeguridad, TokensJWT
from seguridad.errores import ConflictoInicializacion, PermisoInsuficiente
from repositorios.repositorio_autenticacion_postgresql import RepositorioAutenticacionPostgreSQL
from servicios.servicio_autenticacion import ServicioAutenticacion

PROCESO = None
URL = 'http://127.0.0.1:8031'
CONFIG = ConfiguracionSeguridad.desde_entorno()
CLAVES = ClavesArgon2()


def pedir(metodo, ruta, datos=None, token=None):
    cabeceras = {'Content-Type': 'application/json'}
    if token:
        cabeceras['Authorization'] = 'Bearer ' + token
    peticion = Request(URL + ruta, data=json.dumps(datos).encode() if datos is not None else None,
                      headers=cabeceras, method=metodo)
    try:
        respuesta = urlopen(peticion, timeout=15)
    except HTTPError as error:
        respuesta = error
    with respuesta:
        contenido = respuesta.read()
        cuerpo = json.loads(contenido) if contenido else None
        return respuesta.status, cuerpo, respuesta.headers


def arrancar():
    global PROCESO
    PROCESO = subprocess.Popen([sys.executable, '-m', 'uvicorn', 'main_v3:app',
                               '--host', '127.0.0.1', '--port', '8031', '--no-access-log'],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(100):
        if PROCESO.poll() is not None:
            raise RuntimeError('No arrancó la API de pruebas; salida omitida por seguridad.')
        try:
            pedir('GET', '/')
            return
        except (URLError, ConnectionError):
            time.sleep(0.1)
    raise RuntimeError('Tiempo agotado al arrancar API de pruebas.')


def detener():
    if PROCESO is not None:
        PROCESO.terminate()
        PROCESO.wait(timeout=15)


async def preparar():
    original = make_url(os.environ['DB_POSTGRES'])
    if os.environ.get('PRUEBAS_V3') != '1' or original.host != 'postgres-v3' or original.database != 'investigacion_v3':
        raise RuntimeError('Solo se admite el compose aislado v3 con PRUEBAS_V3=1.')
    # El identificador lo genera el test, nunca una entrada del usuario.
    nombre = 'pruebas_v3_' + uuid4().hex
    administrador = await asyncpg.connect(original.set(drivername='postgresql', database='postgres').render_as_string(hide_password=False))
    await administrador.execute('CREATE DATABASE "' + nombre + '"')
    await administrador.close()
    cadena = original.set(database=nombre).render_as_string(hide_password=False)
    os.environ['DB_POSTGRES'] = cadena
    conexion = await asyncpg.connect(make_url(cadena).set(drivername='postgresql').render_as_string(hide_password=False))
    await conexion.execute(Path('/db-v3/init.sql').read_text())
    migracion = Path('/db-v3/migraciones/v3_001_sesiones_asignaciones.sql').read_text()
    migracion = '\n'.join(linea for linea in migracion.splitlines() if not linea.startswith('\\'))
    await conexion.execute(migracion)
    await conexion.execute(migracion)
    await conexion.close()
    repositorio = RepositorioAutenticacionPostgreSQL(cadena)
    servicio = ServicioAutenticacion(repositorio, CLAVES, TokensJWT(CONFIG))
    await servicio.crear_primero('PRUEBA_INICIAL', 'inicial@example.invalid', secrets.token_urlsafe(24))
    try:
        await servicio.crear_primero('OTRO_INICIAL', 'otro@example.invalid', secrets.token_urlsafe(24))
    except ConflictoInicializacion:
        pass
    else:
        raise AssertionError('Bootstrap debió rechazar cuentas existentes.')
    await repositorio._motor().dispose()
    print('Base de pruebas nueva:', nombre)
    print('Migración repetida y bootstrap transaccional/conflicto: OK')


class AutenticacionHTTP(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.motor = create_async_engine(os.environ['DB_POSTGRES'], hide_parameters=True)
        self.nombre = 'PRUEBA_' + uuid4().hex
        self.clave = secrets.token_urlsafe(24)
        resumen = await asyncio.to_thread(CLAVES.crear, self.clave)
        async with self.motor.begin() as c:
            self.usuario = (await c.execute(text("""
                INSERT INTO usuario(username,email,password,activo)
                VALUES (:n,:e,:h,TRUE) RETURNING id
            """), {'n': self.nombre, 'e': self.nombre + '@example.invalid', 'h': resumen})).scalar_one()
            await c.execute(text("""INSERT INTO rol_usuario(usuario_id,rol_id,activo)
                SELECT :id,id,TRUE FROM rol WHERE nombre='consulta'"""), {'id': self.usuario})

    async def asyncTearDown(self):
        await self.motor.dispose()

    async def sql(self, consulta, **parametros):
        async with self.motor.begin() as c:
            return await c.execute(text(consulta), parametros)

    def login(self, **cambios):
        return pedir('POST', '/api/login', {'username': self.nombre, 'password': self.clave, **cambios})

    def token(self):
        estado, datos, _ = self.login()
        self.assertEqual(estado, 200)
        return datos['access_token']

    def firmar(self, cambios=None, quitar=None, algoritmo='HS256'):
        ahora = int(time.time())
        datos = {'sub': str(self.usuario), 'version_sesion': 0, 'iat': ahora,
                 'exp': ahora + 60, 'iss': CONFIG.emisor, 'aud': CONFIG.audiencia}
        datos.update(cambios or {})
        if quitar:
            datos.pop(quitar)
        return jwt.encode(datos, CONFIG.secreto, algorithm=algoritmo)

    async def test_login_y_sesion_sin_datos_sensibles(self):
        estado, datos, cabeceras = self.login()
        self.assertEqual(estado, 200)
        self.assertEqual(datos['expires_in'], CONFIG.minutos * 60)
        self.assertEqual(cabeceras['Cache-Control'], 'no-store')
        self.assertNotIn('password', datos['usuario'])
        self.assertNotIn('version_sesion', datos['usuario'])
        self.assertTrue('$argon2' not in json.dumps(datos), 'Respuesta con datos sensibles; contenido omitido.')
        estado, sesion, _ = pedir('GET', '/api/sesion', token=datos['access_token'])
        self.assertEqual(estado, 200)
        self.assertEqual(sesion['roles'], ['consulta'])
        self.assertEqual(sesion['id'], self.usuario)

    async def test_credenciales_incorrectas_e_inexistentes(self):
        a = self.login(password=secrets.token_urlsafe(25))
        b = self.login(username="' OR 1=1 --")
        self.assertEqual(a[0], 401)
        self.assertEqual(b[0], 401)
        self.assertEqual(a[1], b[1])
        self.assertEqual(a[2]['WWW-Authenticate'], 'Bearer')

    async def test_usuario_inactivo_y_null(self):
        token = self.token()
        for estado in (False, None):
            await self.sql('UPDATE usuario SET activo=:estado WHERE id=:id', estado=estado, id=self.usuario)
            self.assertEqual(self.login()[0], 401)
            self.assertEqual(pedir('GET', '/api/sesion', token=token)[0], 401)

    async def test_sin_token_y_token_alterado(self):
        self.assertEqual(pedir('GET', '/api/sesion')[0], 401)
        token = self.token()
        partes = token.split('.')
        partes[1] = ('A' if partes[1][0] != 'A' else 'B') + partes[1][1:]
        self.assertEqual(pedir('GET', '/api/sesion', token='.'.join(partes))[0], 401)
        self.assertEqual(pedir('GET', '/api/sesion', token='malformado')[0], 401)

    async def test_vencimiento_algoritmo_y_claims(self):
        ahora = int(time.time())
        casos = [{'iat': ahora - 120, 'exp': ahora - 60}, {'iss': 'otro'}, {'aud': 'otra'},
                 {'sub': 'no-entero'}, {'version_sesion': True}, {'iat': ahora + 120},
                 {'exp': ahora + CONFIG.minutos * 60 + 600}, {'sub': str(2**63)}]
        for caso in casos:
            self.assertEqual(pedir('GET', '/api/sesion', token=self.firmar(caso))[0], 401)
        for campo in ('sub', 'version_sesion', 'iat', 'exp', 'iss', 'aud'):
            self.assertEqual(pedir('GET', '/api/sesion', token=self.firmar(quitar=campo))[0], 401)
        self.assertEqual(pedir('GET', '/api/sesion', token=self.firmar(algoritmo='HS512'))[0], 401)

    async def test_sin_roles_es_403_pero_puede_cerrar_sesion(self):
        token = self.token()
        await self.sql('UPDATE rol_usuario SET activo=FALSE WHERE usuario_id=:id', id=self.usuario)
        self.assertEqual(self.login()[0], 403)
        self.assertEqual(pedir('GET', '/api/sesion', token=token)[0], 403)
        self.assertEqual(pedir('POST', '/api/logout', token=token)[0], 200)
        self.assertEqual(pedir('GET', '/api/sesion', token=token)[0], 401)

    async def test_permisos_politica(self):
        ServicioAutenticacion.comprobar_permiso({'roles': ['consulta']})
        for politica in ({'escritura': True}, {'seguridad': True}):
            with self.assertRaises(PermisoInsuficiente):
                ServicioAutenticacion.comprobar_permiso({'roles': ['consulta']}, **politica)
        ServicioAutenticacion.comprobar_permiso({'roles': ['administrador']}, escritura=True, seguridad=True)

    async def test_logout_revoca_todas_las_sesiones_y_persiste_reinicio(self):
        primero, segundo = self.token(), self.token()
        self.assertEqual(pedir('POST', '/api/logout', token=primero)[0], 200)
        for token in (primero, segundo):
            self.assertEqual(pedir('GET', '/api/sesion', token=token)[0], 401)
        detener()
        arrancar()
        self.assertEqual(pedir('GET', '/api/sesion', token=segundo)[0], 401)
        self.assertEqual(pedir('POST', '/api/logout', token=primero)[0], 401)
        version = (await self.sql('SELECT version_sesion FROM usuario WHERE id=:id', id=self.usuario)).scalar_one()
        self.assertEqual(version, 1)
        self.assertEqual(pedir('GET', '/api/sesion', token=self.token())[0], 200)

    async def test_bootstrap_conflicto_conserva_cuentas(self):
        repo = RepositorioAutenticacionPostgreSQL(os.environ['DB_POSTGRES'])
        servicio = ServicioAutenticacion(repo, CLAVES, TokensJWT(CONFIG))
        antes = (await self.sql('SELECT count(*) FROM usuario')).scalar_one()
        with self.assertRaises(ConflictoInicializacion):
            await servicio.crear_primero('OTRO_ADMIN', 'otro@example.invalid', secrets.token_urlsafe(24))
        self.assertEqual((await self.sql('SELECT count(*) FROM usuario')).scalar_one(), antes)
        await repo._motor().dispose()

    async def test_administrador_y_proteccion_global(self):
        await self.sql("""INSERT INTO rol_usuario(usuario_id,rol_id,activo)
            SELECT :id,id,TRUE FROM rol WHERE nombre='administrador'""", id=self.usuario)
        estado, datos, _ = self.login()
        self.assertEqual(estado, 200)
        self.assertEqual(datos['usuario']['roles'], ['administrador', 'consulta'])
        self.assertEqual(pedir('GET', '/api/sesion', token=datos['access_token'])[0], 200)
        self.assertEqual(pedir('GET', '/api/usuario')[0], 401)
        # Las colecciones de dominio también exigen Bearer.
        self.assertEqual(pedir('GET', '/api/area_conocimiento')[0], 401)

    async def test_validacion_no_expone_secretos(self):
        for cuerpo in ({'username': self.nombre}, {'username': self.nombre, 'password': self.clave, 'activo': True}):
            estado, datos, _ = pedir('POST', '/api/login', cuerpo)
            self.assertEqual(estado, 422)
            self.assertTrue(self.clave not in json.dumps(datos), 'Respuesta con datos sensibles; contenido omitido.')
        self.assertFalse(CLAVES.verificar(self.clave, 'texto-sin-hash'))
        self.assertFalse(CLAVES.verificar(self.clave, '$argon2id$invalido'))

    async def test_logouts_simultaneos_incremento_unico(self):
        token = self.token()
        respuestas = await asyncio.gather(*[
            asyncio.to_thread(pedir, 'POST', '/api/logout', token=token) for _ in range(2)])
        self.assertEqual(sorted(r[0] for r in respuestas), [200, 401])
        self.assertEqual((await self.sql('SELECT version_sesion FROM usuario WHERE id=:id', id=self.usuario)).scalar_one(), 1)

    async def test_firma_incorrecta_y_configuracion_externa(self):
        datos = TokensJWT(CONFIG).validar(self.token())
        otro = jwt.encode(datos, secrets.token_urlsafe(48), algorithm='HS256')
        self.assertEqual(pedir('GET', '/api/sesion', token=otro)[0], 401)
        entorno = {k: v for k, v in os.environ.items() if k != 'JWT_SECRET'}
        resultado = await asyncio.to_thread(subprocess.run,
            [sys.executable, '-c', 'import main_v3'], env=entorno, capture_output=True)
        self.assertNotEqual(resultado.returncode, 0)
        self.assertTrue(CONFIG.secreto.encode() not in resultado.stderr, 'Salida sensible; contenido omitido.')
        comando = await asyncio.to_thread(subprocess.run,
            [sys.executable, '-m', 'comandos.crear_administrador'], input=b'', capture_output=True)
        self.assertEqual(comando.returncode, 1)

    async def test_z_excluye_roles_y_asignaciones_inactivos(self):
        await self.sql("""INSERT INTO rol_usuario(usuario_id,rol_id,activo)
            SELECT :id,id,FALSE FROM rol WHERE nombre='administrador'""", id=self.usuario)
        self.assertEqual(self.login()[1]['usuario']['roles'], ['consulta'])
        token = self.token()
        await self.sql("UPDATE rol SET activo=FALSE WHERE nombre='consulta'")
        self.assertEqual(self.login()[0], 403)
        self.assertEqual(pedir('GET', '/api/sesion', token=token)[0], 403)


if __name__ == '__main__':
    asyncio.run(preparar())
    try:
        arrancar()
        resultado = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(AutenticacionHTTP))
    finally:
        detener()
    raise SystemExit(0 if resultado.wasSuccessful() else 1)
