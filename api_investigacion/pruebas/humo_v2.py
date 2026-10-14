"""Prueba integrada: ejecutarla dentro del contenedor de la API.
Crea fichas de prueba, prueba API/front y comprueba el borrado en PostgreSQL.
No se ejecuta al arrancar la aplicación.
"""
import asyncio
import json
import os
import random
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

CASOS = [{'tabla': 'docente', 'claves': ['cedula'], 'datos': {'cedula': '__ID__', 'nombres': 'Prueba v2', 'apellidos': 'Prueba v2', 'genero': 'Prueba v2', 'cargo': 'Prueba v2', 'fecha_nacimiento': '2026-01-01', 'correo': 'Prueba v2', 'telefono': 'Prueba v2', 'url_cvlac': 'Prueba v2', 'fecha_actualizacion': '2026-01-01', 'escalafon': 'Prueba v2', 'perfil': 'Prueba v2', 'cat_minciencia': None, 'conv_minciencia': 'Prueba v2', 'nacionalidaad': 'Prueba v2', 'linea_investigacion_principal': '__ID__'}, 'mutables': ['nombres', 'apellidos', 'genero', 'cargo', 'fecha_nacimiento', 'correo', 'telefono', 'url_cvlac', 'fecha_actualizacion', 'escalafon', 'perfil', 'cat_minciencia', 'conv_minciencia', 'nacionalidaad', 'linea_investigacion_principal'], 'fk': 'linea_investigacion_principal'}, {'tabla': 'grupo_investigacion', 'claves': ['id'], 'datos': {'id': '__ID__', 'nombre': 'Prueba v2', 'url_gruplac': None, 'categoria': None, 'convocatoria': None, 'fecha_fundacion': '2026-01-01', 'universidsad': '__ID__', 'interno': 1, 'ambito': 'Prueba v2'}, 'mutables': ['nombre', 'url_gruplac', 'categoria', 'convocatoria', 'fecha_fundacion', 'universidsad', 'interno', 'ambito'], 'fk': 'universidsad'}, {'tabla': 'semillero', 'claves': ['id'], 'datos': {'id': '__ID__', 'nombre': 'Prueba v2', 'fecha_fundacion': '2026-01-01', 'grupo_investigacion': '__ID__'}, 'mutables': ['nombre', 'fecha_fundacion', 'grupo_investigacion'], 'fk': 'grupo_investigacion'}, {'tabla': 'participa_semillero', 'claves': ['docente', 'semillero'], 'datos': {'docente': '__ID__', 'semillero': '__ID__', 'rol': 'Prueba v2', 'fecha_inicio': '2026-01-01', 'fecha_fin': None}, 'mutables': ['docente', 'semillero', 'rol', 'fecha_inicio', 'fecha_fin'], 'fk': 'docente'}, {'tabla': 'participa_grupo', 'claves': ['docente_cedula', 'grupo_investigacion_id'], 'datos': {'docente_cedula': '__ID__', 'grupo_investigacion_id': '__ID__', 'rol': 'Prueba v2', 'fecha_inicio': '2026-01-01', 'fecha_fin': None}, 'mutables': ['docente_cedula', 'grupo_investigacion_id', 'rol', 'fecha_inicio', 'fecha_fin'], 'fk': 'docente_cedula'}, {'tabla': 'semillero_linea', 'claves': ['semillero', 'linea_investigacion'], 'datos': {'semillero': '__ID__', 'linea_investigacion': '__ID__'}, 'mutables': ['semillero', 'linea_investigacion'], 'fk': 'semillero'}, {'tabla': 'grupo_linea', 'claves': ['grupo_investigacion', 'linea_investigacion'], 'datos': {'grupo_investigacion': '__ID__', 'linea_investigacion': '__ID__'}, 'mutables': ['grupo_investigacion', 'linea_investigacion'], 'fk': 'grupo_investigacion'}, {'tabla': 'ac_linea', 'claves': ['linea_investigacion', 'area_conocimiento'], 'datos': {'linea_investigacion': '__ID__', 'area_conocimiento': '1A01'}, 'mutables': ['linea_investigacion', 'area_conocimiento'], 'fk': 'linea_investigacion'}, {'tabla': 'ods_linea', 'claves': ['linea_investigacion', 'ods'], 'datos': {'linea_investigacion': '__ID__', 'ods': 1}, 'mutables': ['linea_investigacion', 'ods'], 'fk': 'linea_investigacion'}, {'tabla': 'aa_linea', 'claves': ['area_aplicacion', 'linea_investigacion'], 'datos': {'area_aplicacion': 1, 'linea_investigacion': '__ID__'}, 'mutables': ['area_aplicacion', 'linea_investigacion'], 'fk': 'area_aplicacion'}]


def pedir(metodo, ruta, datos=None, esperado=200):
    cuerpo = json.dumps(datos).encode() if datos is not None else None
    solicitud = Request("http://localhost:8025" + ruta, data=cuerpo, method=metodo,
                        headers={"Content-Type": "application/json"})
    try:
        respuesta = urlopen(solicitud, timeout=15)
    except HTTPError as respuesta_error:
        respuesta = respuesta_error
    with respuesta:
        contenido = respuesta.read().decode()
        assert respuesta.status == esperado, f"{metodo} {ruta}: {respuesta.status} != {esperado}: {contenido}"
        return json.loads(contenido) if contenido else None


async def main():
    numero = random.randint(1_000_000_000, 2_000_000_000)
    motor = create_async_engine(os.environ['DB_POSTGRES'])
    async with motor.begin() as conexion:
        await conexion.execute(text("INSERT INTO universidad (id, nombre, tipo, ciudad, activo) VALUES (:id, 'Universidad de PRUEBA V2', 'Prueba', 'Prueba', TRUE), (:inactiva, 'Universidad inactiva de PRUEBA V2', 'Prueba', 'Prueba', FALSE)"), {'id': numero, 'inactiva': numero-1})
        await conexion.execute(text("INSERT INTO linea_investigacion (id, nombre, descripcion, activo) VALUES (:id, 'Línea de PRUEBA V2', 'Registro exclusivo del smoke test', TRUE)"), {'id': numero})
    creados = []
    try:
        for caso in CASOS:
            tabla, claves = caso['tabla'], caso['claves']
            datos = {k: numero if v == '__ID__' else v for k,v in caso['datos'].items()}
            coleccion = '/api/' + tabla
            ruta = coleccion + '/' + '/'.join(str(datos[k]) for k in claves)
            pedir('POST', coleccion, datos)
            creados.append((caso, datos, ruta))
            fila = pedir('GET', ruta)
            pedir('POST', coleccion, datos, esperado=500)
            cuerpo = {k: datos[k] for k in caso['mutables']}
            pedir('PUT', ruta, cuerpo)
            pedir('PATCH', ruta, {}, esperado=400)
            pedir('PATCH', ruta, {caso['fk']: -999999999}, esperado=400)
            assert pedir('GET', ruta) == fila, f'PATCH inválido modificó {tabla}'
            if tabla == 'grupo_investigacion':
                pedir('PATCH', ruta, {'universidsad': numero-1}, esperado=400)
            pedir('PATCH', ruta, {caso['mutables'][0]: cuerpo[caso['mutables'][0]]})
            parcial = dict(cuerpo)
            parcial.pop(caso['mutables'][0])
            pedir('PUT', ruta, parcial, esperado=422)
            pagina = urlopen('http://front-flask:8078/' + tabla.replace('_','-') + '/nuevo', timeout=15).read().decode()
            assert '<select' in pagina and str(numero) in pagina, f'Desplegables ausentes en {tabla}'
            print('[OK]', tabla, 'API y desplegables')
        for tabla in ['docente','grupo_investigacion','semillero']:
            pedir('DELETE', '/api/' + tabla + '/' + str(numero), esperado=400)
        pedir('DELETE', '/api/area_conocimiento/1A01', esperado=400)
        for caso, datos, ruta in reversed(creados):
            pedir('DELETE', ruta)
            pedir('GET', ruta, esperado=404)
            pedir('DELETE', ruta, esperado=404)
            condiciones = ' AND '.join(k + ' = :' + k for k in caso['claves'])
            async with motor.connect() as conexion:
                valor = await conexion.scalar(text('SELECT activo FROM ' + caso['tabla'] + ' WHERE ' + condiciones), {k:datos[k] for k in caso['claves']})
                assert valor is False, f'No quedó el borrado lógico en {caso["tabla"]}'
            print('[OK]', caso['tabla'], 'fila conservada e inactiva')
        async with motor.begin() as conexion:
            await conexion.execute(text('UPDATE universidad SET activo = FALSE WHERE id = :id'), {'id': numero})
            await conexion.execute(text('UPDATE linea_investigacion SET activo = FALSE WHERE id = :id'), {'id': numero})
        print('Smoke test v2 completo. Identificador de las fichas de prueba:', numero)
    finally:
        await motor.dispose()


if __name__ == '__main__':
    asyncio.run(main())
