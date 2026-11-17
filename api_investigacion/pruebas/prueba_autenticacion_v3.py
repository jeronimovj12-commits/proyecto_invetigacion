# Ejecuta la instruccion indicada dentro del flujo actual.
"""Integración real, solo compose v3 aislado. No imprime claves, hashes o JWT."""
# Carga el modulo o los modulos asyncio.
import asyncio
# Carga el modulo o los modulos json.
import json
# Carga el modulo o los modulos os.
import os
# Importa Path desde pathlib para usar esas definiciones.
from pathlib import Path
# Carga el modulo o los modulos secrets.
import secrets
# Carga el modulo o los modulos subprocess.
import subprocess
# Carga el modulo o los modulos sys.
import sys
# Carga el modulo o los modulos time.
import time
# Carga el modulo o los modulos unittest.
import unittest
# Importa HTTPError, URLError desde urllib.error para usar esas definiciones.
from urllib.error import HTTPError, URLError
# Importa Request, urlopen desde urllib.request para usar esas definiciones.
from urllib.request import Request, urlopen
# Importa uuid4 desde uuid para usar esas definiciones.
from uuid import uuid4

# Carga el modulo o los modulos asyncpg.
import asyncpg
# Carga el modulo o los modulos jwt.
import jwt
# Importa text desde sqlalchemy para usar esas definiciones.
from sqlalchemy import text
# Importa make_url desde sqlalchemy.engine para usar esas definiciones.
from sqlalchemy.engine import make_url
# Importa create_async_engine desde sqlalchemy.ext.asyncio para usar esas definiciones.
from sqlalchemy.ext.asyncio import create_async_engine

# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
# Importa ClavesArgon2, ConfiguracionSeguridad, TokensJWT desde seguridad.adaptadores para usar esas definiciones.
from seguridad.adaptadores import ClavesArgon2, ConfiguracionSeguridad, TokensJWT
# Importa ConflictoInicializacion, PermisoInsuficiente desde seguridad.errores para usar esas definiciones.
from seguridad.errores import ConflictoInicializacion, PermisoInsuficiente
# Importa RepositorioAutenticacionPostgreSQL desde repositorios.repositorio_autenticacion_postgresql para usar esas definiciones.
from repositorios.repositorio_autenticacion_postgresql import RepositorioAutenticacionPostgreSQL
# Importa ServicioAutenticacion desde servicios.servicio_autenticacion para usar esas definiciones.
from servicios.servicio_autenticacion import ServicioAutenticacion

# Asigna a PROCESO el valor calculado a la derecha.
PROCESO = None
# Asigna a URL el valor calculado a la derecha.
URL = 'http://127.0.0.1:8031'
# Asigna a CONFIG el valor calculado a la derecha.
CONFIG = ConfiguracionSeguridad.desde_entorno()
# Asigna a CLAVES el valor calculado a la derecha.
CLAVES = ClavesArgon2()


# Define la funcion pedir con los parametros declarados; su bloque realiza esta operacion.
def pedir(metodo, ruta, datos=None, token=None):
    # Asigna a cabeceras el valor calculado a la derecha.
    cabeceras = {'Content-Type': 'application/json'}
    # Ejecuta el bloque siguiente solo cuando se cumple: token.
    if token:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        cabeceras['Authorization'] = 'Bearer ' + token
    # Asigna a peticion el valor calculado a la derecha.
    peticion = Request(URL + ruta, data=json.dumps(datos).encode() if datos is not None else None,
                      # Asigna a headers el valor calculado a la derecha.
                      headers=cabeceras, method=metodo)
    # Inicia un bloque cuya excepcion se manejara en los except siguientes.
    try:
        # Asigna a respuesta el valor calculado a la derecha.
        respuesta = urlopen(peticion, timeout=15)
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except HTTPError as error:
        # Asigna a respuesta el valor calculado a la derecha.
        respuesta = error
    # Abre el recurso y asegura su cierre al salir del bloque.
    with respuesta:
        # Asigna a contenido el valor calculado a la derecha.
        contenido = respuesta.read()
        # Asigna a cuerpo el valor calculado a la derecha.
        cuerpo = json.loads(contenido) if contenido else None
        # Devuelve al llamador el resultado de la expresion indicada.
        return respuesta.status, cuerpo, respuesta.headers


# Define la funcion arrancar con los parametros declarados; su bloque realiza esta operacion.
def arrancar():
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    global PROCESO
    # Asigna a PROCESO el valor calculado a la derecha.
    PROCESO = subprocess.Popen([sys.executable, '-m', 'uvicorn', 'main_v3:app',
                               # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                               '--host', '127.0.0.1', '--port', '8031', '--no-access-log'],
                              # Asigna a stdout el valor calculado a la derecha.
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # Recorre los elementos de la coleccion indicada y ejecuta el bloque para cada uno.
    for _ in range(100):
        # Ejecuta el bloque siguiente solo cuando se cumple: PROCESO.poll() is not None.
        if PROCESO.poll() is not None:
            # Lanza la excepcion indicada y detiene el flujo normal.
            raise RuntimeError('No arrancó la API de pruebas; salida omitida por seguridad.')
        # Inicia un bloque cuya excepcion se manejara en los except siguientes.
        try:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            pedir('GET', '/')
            # Termina la funcion sin devolver un valor.
            return
        # Captura la excepcion indicada para manejarla sin dejarla propagarse.
        except (URLError, ConnectionError):
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            time.sleep(0.1)
    # Lanza la excepcion indicada y detiene el flujo normal.
    raise RuntimeError('Tiempo agotado al arrancar API de pruebas.')


# Define la funcion detener con los parametros declarados; su bloque realiza esta operacion.
def detener():
    # Ejecuta el bloque siguiente solo cuando se cumple: PROCESO is not None.
    if PROCESO is not None:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        PROCESO.terminate()
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        PROCESO.wait(timeout=15)


# Define la funcion preparar con los parametros declarados; su bloque realiza esta operacion.
async def preparar():
    # Asigna a original el valor calculado a la derecha.
    original = make_url(os.environ['DB_POSTGRES'])
    # Ejecuta el bloque siguiente solo cuando se cumple: os.environ.get('PRUEBAS_V3') != '1' or original.host != 'postgres-v3' or original.database != 'investigacion_v3'.
    if os.environ.get('PRUEBAS_V3') != '1' or original.host != 'postgres-v3' or original.database != 'investigacion_v3':
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise RuntimeError('Solo se admite el compose aislado v3 con PRUEBAS_V3=1.')
    # El identificador lo genera el test, nunca una entrada del usuario.
    # Asigna a nombre el valor calculado a la derecha.
    nombre = 'pruebas_v3_' + uuid4().hex
    # Asigna a administrador el valor calculado a la derecha.
    administrador = await asyncpg.connect(original.set(drivername='postgresql', database='postgres').render_as_string(hide_password=False))
    # Espera que termine la operacion asincronica antes de continuar.
    await administrador.execute('CREATE DATABASE "' + nombre + '"')
    # Espera que termine la operacion asincronica antes de continuar.
    await administrador.close()
    # Asigna a cadena el valor calculado a la derecha.
    cadena = original.set(database=nombre).render_as_string(hide_password=False)
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    os.environ['DB_POSTGRES'] = cadena
    # Asigna a conexion el valor calculado a la derecha.
    conexion = await asyncpg.connect(make_url(cadena).set(drivername='postgresql').render_as_string(hide_password=False))
    # Espera que termine la operacion asincronica antes de continuar.
    await conexion.execute(Path('/db-v3/init.sql').read_text())
    # Asigna a migracion el valor calculado a la derecha.
    migracion = Path('/db-v3/migraciones/v3_001_sesiones_asignaciones.sql').read_text()
    # Asigna a migracion el valor calculado a la derecha.
    migracion = '\n'.join(linea for linea in migracion.splitlines() if not linea.startswith('\\'))
    # Espera que termine la operacion asincronica antes de continuar.
    await conexion.execute(migracion)
    # Espera que termine la operacion asincronica antes de continuar.
    await conexion.execute(migracion)
    # Espera que termine la operacion asincronica antes de continuar.
    await conexion.close()
    # Asigna a repositorio el valor calculado a la derecha.
    repositorio = RepositorioAutenticacionPostgreSQL(cadena)
    # Asigna a servicio el valor calculado a la derecha.
    servicio = ServicioAutenticacion(repositorio, CLAVES, TokensJWT(CONFIG))
    # Espera que termine la operacion asincronica antes de continuar.
    await servicio.crear_primero('PRUEBA_INICIAL', 'inicial@example.invalid', secrets.token_urlsafe(24))
    # Inicia un bloque cuya excepcion se manejara en los except siguientes.
    try:
        # Espera que termine la operacion asincronica antes de continuar.
        await servicio.crear_primero('OTRO_INICIAL', 'otro@example.invalid', secrets.token_urlsafe(24))
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except ConflictoInicializacion:
        # Deja el bloque intencionalmente vacio sin ejecutar una operacion.
        pass
    # Define el caso alternativo cuando las condiciones anteriores no se cumplen.
    else:
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise AssertionError('Bootstrap debió rechazar cuentas existentes.')
    # Espera que termine la operacion asincronica antes de continuar.
    await repositorio._motor().dispose()
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    print('Base de pruebas nueva:', nombre)
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    print('Migración repetida y bootstrap transaccional/conflicto: OK')


# Define la clase AutenticacionHTTP y agrupa su estado y operaciones.
class AutenticacionHTTP(unittest.IsolatedAsyncioTestCase):
    # Define la funcion asyncSetUp con los parametros declarados; su bloque realiza esta operacion.
    async def asyncSetUp(self):
        # Guarda en self.motor el valor necesario para reutilizarlo en otros metodos.
        self.motor = create_async_engine(os.environ['DB_POSTGRES'], hide_parameters=True)
        # Guarda en self.nombre el valor necesario para reutilizarlo en otros metodos.
        self.nombre = 'PRUEBA_' + uuid4().hex
        # Guarda en self.clave el valor necesario para reutilizarlo en otros metodos.
        self.clave = secrets.token_urlsafe(24)
        # Asigna a resumen el valor calculado a la derecha.
        resumen = await asyncio.to_thread(CLAVES.crear, self.clave)
        # Abre el recurso asincronico y asegura su cierre al salir del bloque.
        async with self.motor.begin() as c:
            # Guarda en self.usuario el valor necesario para reutilizarlo en otros metodos.
            self.usuario = (await c.execute(text("""
                INSERT INTO usuario(username,email,password,activo)
                VALUES (:n,:e,:h,TRUE) RETURNING id
            """), {'n': self.nombre, 'e': self.nombre + '@example.invalid', 'h': resumen})).scalar_one()  # Termina el literal multilinea y completa la instruccion que lo contiene.
            # La cadena multilinea siguiente contiene el texto o SQL que usa esta instruccion.
            await c.execute(text("""INSERT INTO rol_usuario(usuario_id,rol_id,activo)
                SELECT :id,id,TRUE FROM rol WHERE nombre='consulta'"""), {'id': self.usuario})  # Termina el literal multilinea y completa la instruccion que lo contiene.

    # Define la funcion asyncTearDown con los parametros declarados; su bloque realiza esta operacion.
    async def asyncTearDown(self):
        # Espera que termine la operacion asincronica antes de continuar.
        await self.motor.dispose()

    # Define la funcion sql con los parametros declarados; su bloque realiza esta operacion.
    async def sql(self, consulta, **parametros):
        # Abre el recurso asincronico y asegura su cierre al salir del bloque.
        async with self.motor.begin() as c:
            # Devuelve al llamador el resultado de la expresion indicada.
            return await c.execute(text(consulta), parametros)

    # Define la funcion login con los parametros declarados; su bloque realiza esta operacion.
    def login(self, **cambios):
        # Devuelve al llamador el resultado de la expresion indicada.
        return pedir('POST', '/api/login', {'username': self.nombre, 'password': self.clave, **cambios})

    # Define la funcion token con los parametros declarados; su bloque realiza esta operacion.
    def token(self):
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        estado, datos, _ = self.login()
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(estado, 200)
        # Devuelve al llamador el resultado de la expresion indicada.
        return datos['access_token']

    # Define la funcion firmar con los parametros declarados; su bloque realiza esta operacion.
    def firmar(self, cambios=None, quitar=None, algoritmo='HS256'):
        # Asigna a ahora el valor calculado a la derecha.
        ahora = int(time.time())
        # Asigna a datos el valor calculado a la derecha.
        datos = {'sub': str(self.usuario), 'version_sesion': 0, 'iat': ahora,
                 # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                 'exp': ahora + 60, 'iss': CONFIG.emisor, 'aud': CONFIG.audiencia}
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        datos.update(cambios or {})
        # Ejecuta el bloque siguiente solo cuando se cumple: quitar.
        if quitar:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            datos.pop(quitar)
        # Devuelve al llamador el resultado de la expresion indicada.
        return jwt.encode(datos, CONFIG.secreto, algorithm=algoritmo)

    # Define la funcion test_login_y_sesion_sin_datos_sensibles con los parametros declarados; su bloque realiza esta operacion.
    async def test_login_y_sesion_sin_datos_sensibles(self):
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        estado, datos, cabeceras = self.login()
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(estado, 200)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(datos['expires_in'], CONFIG.minutos * 60)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(cabeceras['Cache-Control'], 'no-store')
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertNotIn('password', datos['usuario'])
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertNotIn('version_sesion', datos['usuario'])
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertTrue('$argon2' not in json.dumps(datos), 'Respuesta con datos sensibles; contenido omitido.')
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        estado, sesion, _ = pedir('GET', '/api/sesion', token=datos['access_token'])
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(estado, 200)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(sesion['roles'], ['consulta'])
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(sesion['id'], self.usuario)

    # Define la funcion test_credenciales_incorrectas_e_inexistentes con los parametros declarados; su bloque realiza esta operacion.
    async def test_credenciales_incorrectas_e_inexistentes(self):
        # Asigna a a el valor calculado a la derecha.
        a = self.login(password=secrets.token_urlsafe(25))
        # Asigna a b el valor calculado a la derecha.
        b = self.login(username="' OR 1=1 --")
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(a[0], 401)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(b[0], 401)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(a[1], b[1])
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(a[2]['WWW-Authenticate'], 'Bearer')

    # Define la funcion test_usuario_inactivo_y_null con los parametros declarados; su bloque realiza esta operacion.
    async def test_usuario_inactivo_y_null(self):
        # Asigna a token el valor calculado a la derecha.
        token = self.token()
        # Recorre los elementos de la coleccion indicada y ejecuta el bloque para cada uno.
        for estado in (False, None):
            # Espera que termine la operacion asincronica antes de continuar.
            await self.sql('UPDATE usuario SET activo=:estado WHERE id=:id', estado=estado, id=self.usuario)
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            self.assertEqual(self.login()[0], 401)
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            self.assertEqual(pedir('GET', '/api/sesion', token=token)[0], 401)

    # Define la funcion test_sin_token_y_token_alterado con los parametros declarados; su bloque realiza esta operacion.
    async def test_sin_token_y_token_alterado(self):
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(pedir('GET', '/api/sesion')[0], 401)
        # Asigna a token el valor calculado a la derecha.
        token = self.token()
        # Asigna a partes el valor calculado a la derecha.
        partes = token.split('.')
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        partes[1] = ('A' if partes[1][0] != 'A' else 'B') + partes[1][1:]
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(pedir('GET', '/api/sesion', token='.'.join(partes))[0], 401)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(pedir('GET', '/api/sesion', token='malformado')[0], 401)

    # Define la funcion test_vencimiento_algoritmo_y_claims con los parametros declarados; su bloque realiza esta operacion.
    async def test_vencimiento_algoritmo_y_claims(self):
        # Asigna a ahora el valor calculado a la derecha.
        ahora = int(time.time())
        # Asigna a casos el valor calculado a la derecha.
        casos = [{'iat': ahora - 120, 'exp': ahora - 60}, {'iss': 'otro'}, {'aud': 'otra'},
                 # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                 {'sub': 'no-entero'}, {'version_sesion': True}, {'iat': ahora + 120},
                 # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                 {'exp': ahora + CONFIG.minutos * 60 + 600}, {'sub': str(2**63)}]
        # Recorre los elementos de la coleccion indicada y ejecuta el bloque para cada uno.
        for caso in casos:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            self.assertEqual(pedir('GET', '/api/sesion', token=self.firmar(caso))[0], 401)
        # Recorre los elementos de la coleccion indicada y ejecuta el bloque para cada uno.
        for campo in ('sub', 'version_sesion', 'iat', 'exp', 'iss', 'aud'):
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            self.assertEqual(pedir('GET', '/api/sesion', token=self.firmar(quitar=campo))[0], 401)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(pedir('GET', '/api/sesion', token=self.firmar(algoritmo='HS512'))[0], 401)

    # Define la funcion test_sin_roles_es_403_pero_puede_cerrar_sesion con los parametros declarados; su bloque realiza esta operacion.
    async def test_sin_roles_es_403_pero_puede_cerrar_sesion(self):
        # Asigna a token el valor calculado a la derecha.
        token = self.token()
        # Espera que termine la operacion asincronica antes de continuar.
        await self.sql('UPDATE rol_usuario SET activo=FALSE WHERE usuario_id=:id', id=self.usuario)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.login()[0], 403)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(pedir('GET', '/api/sesion', token=token)[0], 403)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(pedir('POST', '/api/logout', token=token)[0], 200)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(pedir('GET', '/api/sesion', token=token)[0], 401)

    # Define la funcion test_permisos_politica con los parametros declarados; su bloque realiza esta operacion.
    async def test_permisos_politica(self):
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        ServicioAutenticacion.comprobar_permiso({'roles': ['consulta']})
        # Recorre los elementos de la coleccion indicada y ejecuta el bloque para cada uno.
        for politica in ({'escritura': True}, {'seguridad': True}):
            # Abre el recurso y asegura su cierre al salir del bloque.
            with self.assertRaises(PermisoInsuficiente):
                # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                ServicioAutenticacion.comprobar_permiso({'roles': ['consulta']}, **politica)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        ServicioAutenticacion.comprobar_permiso({'roles': ['administrador']}, escritura=True, seguridad=True)

    # Define la funcion test_logout_revoca_todas_las_sesiones_y_persiste_reinicio con los parametros declarados; su bloque realiza esta operacion.
    async def test_logout_revoca_todas_las_sesiones_y_persiste_reinicio(self):
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        primero, segundo = self.token(), self.token()
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(pedir('POST', '/api/logout', token=primero)[0], 200)
        # Recorre los elementos de la coleccion indicada y ejecuta el bloque para cada uno.
        for token in (primero, segundo):
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            self.assertEqual(pedir('GET', '/api/sesion', token=token)[0], 401)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        detener()
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        arrancar()
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(pedir('GET', '/api/sesion', token=segundo)[0], 401)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(pedir('POST', '/api/logout', token=primero)[0], 401)
        # Asigna a version el valor calculado a la derecha.
        version = (await self.sql('SELECT version_sesion FROM usuario WHERE id=:id', id=self.usuario)).scalar_one()
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(version, 1)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(pedir('GET', '/api/sesion', token=self.token())[0], 200)

    # Define la funcion test_bootstrap_conflicto_conserva_cuentas con los parametros declarados; su bloque realiza esta operacion.
    async def test_bootstrap_conflicto_conserva_cuentas(self):
        # Asigna a repo el valor calculado a la derecha.
        repo = RepositorioAutenticacionPostgreSQL(os.environ['DB_POSTGRES'])
        # Asigna a servicio el valor calculado a la derecha.
        servicio = ServicioAutenticacion(repo, CLAVES, TokensJWT(CONFIG))
        # Asigna a antes el valor calculado a la derecha.
        antes = (await self.sql('SELECT count(*) FROM usuario')).scalar_one()
        # Abre el recurso y asegura su cierre al salir del bloque.
        with self.assertRaises(ConflictoInicializacion):
            # Espera que termine la operacion asincronica antes de continuar.
            await servicio.crear_primero('OTRO_ADMIN', 'otro@example.invalid', secrets.token_urlsafe(24))
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual((await self.sql('SELECT count(*) FROM usuario')).scalar_one(), antes)
        # Espera que termine la operacion asincronica antes de continuar.
        await repo._motor().dispose()

    # Define la funcion test_administrador_y_proteccion_global con los parametros declarados; su bloque realiza esta operacion.
    async def test_administrador_y_proteccion_global(self):
        # Espera que termine la operacion asincronica antes de continuar.
        await self.sql("""INSERT INTO rol_usuario(usuario_id,rol_id,activo)
            SELECT :id,id,TRUE FROM rol WHERE nombre='administrador'""", id=self.usuario)  # Termina el literal multilinea y completa la instruccion que lo contiene.
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        estado, datos, _ = self.login()
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(estado, 200)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(datos['usuario']['roles'], ['administrador', 'consulta'])
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(pedir('GET', '/api/sesion', token=datos['access_token'])[0], 200)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(pedir('GET', '/api/usuario')[0], 401)
        # Las colecciones de dominio también exigen Bearer.
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(pedir('GET', '/api/area_conocimiento')[0], 401)

    # Define la funcion test_validacion_no_expone_secretos con los parametros declarados; su bloque realiza esta operacion.
    async def test_validacion_no_expone_secretos(self):
        # Recorre los elementos de la coleccion indicada y ejecuta el bloque para cada uno.
        for cuerpo in ({'username': self.nombre}, {'username': self.nombre, 'password': self.clave, 'activo': True}):
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            estado, datos, _ = pedir('POST', '/api/login', cuerpo)
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            self.assertEqual(estado, 422)
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            self.assertTrue(self.clave not in json.dumps(datos), 'Respuesta con datos sensibles; contenido omitido.')
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertFalse(CLAVES.verificar(self.clave, 'texto-sin-hash'))
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertFalse(CLAVES.verificar(self.clave, '$argon2id$invalido'))

    # Define la funcion test_logouts_simultaneos_incremento_unico con los parametros declarados; su bloque realiza esta operacion.
    async def test_logouts_simultaneos_incremento_unico(self):
        # Asigna a token el valor calculado a la derecha.
        token = self.token()
        # Asigna a respuestas el valor calculado a la derecha.
        respuestas = await asyncio.gather(*[
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            asyncio.to_thread(pedir, 'POST', '/api/logout', token=token) for _ in range(2)])
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(sorted(r[0] for r in respuestas), [200, 401])
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual((await self.sql('SELECT version_sesion FROM usuario WHERE id=:id', id=self.usuario)).scalar_one(), 1)

    # Define la funcion test_firma_incorrecta_y_configuracion_externa con los parametros declarados; su bloque realiza esta operacion.
    async def test_firma_incorrecta_y_configuracion_externa(self):
        # Asigna a datos el valor calculado a la derecha.
        datos = TokensJWT(CONFIG).validar(self.token())
        # Asigna a otro el valor calculado a la derecha.
        otro = jwt.encode(datos, secrets.token_urlsafe(48), algorithm='HS256')
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(pedir('GET', '/api/sesion', token=otro)[0], 401)
        # Asigna a entorno el valor calculado a la derecha.
        entorno = {k: v for k, v in os.environ.items() if k != 'JWT_SECRET'}
        # Asigna a resultado el valor calculado a la derecha.
        resultado = await asyncio.to_thread(subprocess.run,
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            [sys.executable, '-c', 'import main_v3'], env=entorno, capture_output=True)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertNotEqual(resultado.returncode, 0)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertTrue(CONFIG.secreto.encode() not in resultado.stderr, 'Salida sensible; contenido omitido.')
        # Asigna a comando el valor calculado a la derecha.
        comando = await asyncio.to_thread(subprocess.run,
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            [sys.executable, '-m', 'comandos.crear_administrador'], input=b'', capture_output=True)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(comando.returncode, 1)

    # Define la funcion test_z_excluye_roles_y_asignaciones_inactivos con los parametros declarados; su bloque realiza esta operacion.
    async def test_z_excluye_roles_y_asignaciones_inactivos(self):
        # Espera que termine la operacion asincronica antes de continuar.
        await self.sql("""INSERT INTO rol_usuario(usuario_id,rol_id,activo)
            SELECT :id,id,FALSE FROM rol WHERE nombre='administrador'""", id=self.usuario)  # Termina el literal multilinea y completa la instruccion que lo contiene.
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.login()[1]['usuario']['roles'], ['consulta'])
        # Asigna a token el valor calculado a la derecha.
        token = self.token()
        # Espera que termine la operacion asincronica antes de continuar.
        await self.sql("UPDATE rol SET activo=FALSE WHERE nombre='consulta'")
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.login()[0], 403)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(pedir('GET', '/api/sesion', token=token)[0], 403)


# Ejecuta el bloque siguiente solo cuando se cumple: __name__ == '__main__'.
if __name__ == '__main__':
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    asyncio.run(preparar())
    # Inicia un bloque cuya excepcion se manejara en los except siguientes.
    try:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        arrancar()
        # Asigna a resultado el valor calculado a la derecha.
        resultado = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(AutenticacionHTTP))
    # Ejecuta este bloque al final, haya ocurrido o no una excepcion.
    finally:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        detener()
    # Lanza la excepcion indicada y detiene el flujo normal.
    raise SystemExit(0 if resultado.wasSuccessful() else 1)
