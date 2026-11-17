"""Prueba integrada: ejecutarla dentro del contenedor de la API.
Crea fichas de prueba, prueba API/front y comprueba el borrado en PostgreSQL.
No se ejecuta al arrancar la aplicación.
"""
# Carga el modulo o los modulos asyncio.
import asyncio
# Carga el modulo o los modulos json.
import json
# Carga el modulo o los modulos os.
import os
# Carga el modulo o los modulos random.
import random
# Importa Request, urlopen desde urllib.request para usar esas definiciones.
from urllib.request import Request, urlopen
# Importa HTTPError desde urllib.error para usar esas definiciones.
from urllib.error import HTTPError
# Importa text desde sqlalchemy para usar esas definiciones.
from sqlalchemy import text
# Importa create_async_engine desde sqlalchemy.ext.asyncio para usar esas definiciones.
from sqlalchemy.ext.asyncio import create_async_engine

# Asigna a CASOS el valor calculado a la derecha.
CASOS = [{'tabla': 'docente', 'claves': ['cedula'], 'datos': {'cedula': '__ID__', 'nombres': 'Prueba v2', 'apellidos': 'Prueba v2', 'genero': 'Prueba v2', 'cargo': 'Prueba v2', 'fecha_nacimiento': '2026-01-01', 'correo': 'Prueba v2', 'telefono': 'Prueba v2', 'url_cvlac': 'Prueba v2', 'fecha_actualizacion': '2026-01-01', 'escalafon': 'Prueba v2', 'perfil': 'Prueba v2', 'cat_minciencia': None, 'conv_minciencia': 'Prueba v2', 'nacionalidaad': 'Prueba v2', 'linea_investigacion_principal': '__ID__'}, 'mutables': ['nombres', 'apellidos', 'genero', 'cargo', 'fecha_nacimiento', 'correo', 'telefono', 'url_cvlac', 'fecha_actualizacion', 'escalafon', 'perfil', 'cat_minciencia', 'conv_minciencia', 'nacionalidaad', 'linea_investigacion_principal'], 'fk': 'linea_investigacion_principal'}, {'tabla': 'grupo_investigacion', 'claves': ['id'], 'datos': {'id': '__ID__', 'nombre': 'Prueba v2', 'url_gruplac': None, 'categoria': None, 'convocatoria': None, 'fecha_fundacion': '2026-01-01', 'universidsad': '__ID__', 'interno': 1, 'ambito': 'Prueba v2'}, 'mutables': ['nombre', 'url_gruplac', 'categoria', 'convocatoria', 'fecha_fundacion', 'universidsad', 'interno', 'ambito'], 'fk': 'universidsad'}, {'tabla': 'semillero', 'claves': ['id'], 'datos': {'id': '__ID__', 'nombre': 'Prueba v2', 'fecha_fundacion': '2026-01-01', 'grupo_investigacion': '__ID__'}, 'mutables': ['nombre', 'fecha_fundacion', 'grupo_investigacion'], 'fk': 'grupo_investigacion'}, {'tabla': 'participa_semillero', 'claves': ['docente', 'semillero'], 'datos': {'docente': '__ID__', 'semillero': '__ID__', 'rol': 'Prueba v2', 'fecha_inicio': '2026-01-01', 'fecha_fin': None}, 'mutables': ['docente', 'semillero', 'rol', 'fecha_inicio', 'fecha_fin'], 'fk': 'docente'}, {'tabla': 'participa_grupo', 'claves': ['docente_cedula', 'grupo_investigacion_id'], 'datos': {'docente_cedula': '__ID__', 'grupo_investigacion_id': '__ID__', 'rol': 'Prueba v2', 'fecha_inicio': '2026-01-01', 'fecha_fin': None}, 'mutables': ['docente_cedula', 'grupo_investigacion_id', 'rol', 'fecha_inicio', 'fecha_fin'], 'fk': 'docente_cedula'}, {'tabla': 'semillero_linea', 'claves': ['semillero', 'linea_investigacion'], 'datos': {'semillero': '__ID__', 'linea_investigacion': '__ID__'}, 'mutables': ['semillero', 'linea_investigacion'], 'fk': 'semillero'}, {'tabla': 'grupo_linea', 'claves': ['grupo_investigacion', 'linea_investigacion'], 'datos': {'grupo_investigacion': '__ID__', 'linea_investigacion': '__ID__'}, 'mutables': ['grupo_investigacion', 'linea_investigacion'], 'fk': 'grupo_investigacion'}, {'tabla': 'ac_linea', 'claves': ['linea_investigacion', 'area_conocimiento'], 'datos': {'linea_investigacion': '__ID__', 'area_conocimiento': '1A01'}, 'mutables': ['linea_investigacion', 'area_conocimiento'], 'fk': 'linea_investigacion'}, {'tabla': 'ods_linea', 'claves': ['linea_investigacion', 'ods'], 'datos': {'linea_investigacion': '__ID__', 'ods': 1}, 'mutables': ['linea_investigacion', 'ods'], 'fk': 'linea_investigacion'}, {'tabla': 'aa_linea', 'claves': ['area_aplicacion', 'linea_investigacion'], 'datos': {'area_aplicacion': 1, 'linea_investigacion': '__ID__'}, 'mutables': ['area_aplicacion', 'linea_investigacion'], 'fk': 'area_aplicacion'}]


# Define la funcion pedir con los parametros declarados; su bloque realiza esta operacion.
def pedir(metodo, ruta, datos=None, esperado=200):
    # Asigna a cuerpo el valor calculado a la derecha.
    cuerpo = json.dumps(datos).encode() if datos is not None else None
    # Asigna a solicitud el valor calculado a la derecha.
    solicitud = Request("http://localhost:8025" + ruta, data=cuerpo, method=metodo,
                        # Asigna a headers el valor calculado a la derecha.
                        headers={"Content-Type": "application/json"})
    # Inicia un bloque cuya excepcion se manejara en los except siguientes.
    try:
        # Asigna a respuesta el valor calculado a la derecha.
        respuesta = urlopen(solicitud, timeout=15)
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except HTTPError as respuesta_error:
        # Asigna a respuesta el valor calculado a la derecha.
        respuesta = respuesta_error
    # Abre el recurso y asegura su cierre al salir del bloque.
    with respuesta:
        # Asigna a contenido el valor calculado a la derecha.
        contenido = respuesta.read().decode()
        # Verifica la condicion; falla si el resultado no es verdadero.
        assert respuesta.status == esperado, f"{metodo} {ruta}: {respuesta.status} != {esperado}: {contenido}"
        # Devuelve al llamador el resultado de la expresion indicada.
        return json.loads(contenido) if contenido else None


# Define la funcion main con los parametros declarados; su bloque realiza esta operacion.
async def main():
    # Asigna a numero el valor calculado a la derecha.
    numero = random.randint(1_000_000_000, 2_000_000_000)
    # Asigna a motor el valor calculado a la derecha.
    motor = create_async_engine(os.environ['DB_POSTGRES'])
    # Abre el recurso asincronico y asegura su cierre al salir del bloque.
    async with motor.begin() as conexion:
        # Espera que termine la operacion asincronica antes de continuar.
        await conexion.execute(text("INSERT INTO universidad (id, nombre, tipo, ciudad, activo) VALUES (:id, 'Universidad de PRUEBA V2', 'Prueba', 'Prueba', TRUE), (:inactiva, 'Universidad inactiva de PRUEBA V2', 'Prueba', 'Prueba', FALSE)"), {'id': numero, 'inactiva': numero-1})
        # Espera que termine la operacion asincronica antes de continuar.
        await conexion.execute(text("INSERT INTO linea_investigacion (id, nombre, descripcion, activo) VALUES (:id, 'Línea de PRUEBA V2', 'Registro exclusivo del smoke test', TRUE)"), {'id': numero})
    # Asigna a creados el valor calculado a la derecha.
    creados = []
    # Inicia un bloque cuya excepcion se manejara en los except siguientes.
    try:
        # Recorre los elementos de la coleccion indicada y ejecuta el bloque para cada uno.
        for caso in CASOS:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            tabla, claves = caso['tabla'], caso['claves']
            # Asigna a datos el valor calculado a la derecha.
            datos = {k: numero if v == '__ID__' else v for k,v in caso['datos'].items()}
            # Asigna a coleccion el valor calculado a la derecha.
            coleccion = '/api/' + tabla
            # Asigna a ruta el valor calculado a la derecha.
            ruta = coleccion + '/' + '/'.join(str(datos[k]) for k in claves)
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            pedir('POST', coleccion, datos)
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            creados.append((caso, datos, ruta))
            # Asigna a fila el valor calculado a la derecha.
            fila = pedir('GET', ruta)
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            pedir('POST', coleccion, datos, esperado=500)
            # Asigna a cuerpo el valor calculado a la derecha.
            cuerpo = {k: datos[k] for k in caso['mutables']}
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            pedir('PUT', ruta, cuerpo)
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            pedir('PATCH', ruta, {}, esperado=400)
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            pedir('PATCH', ruta, {caso['fk']: -999999999}, esperado=400)
            # Verifica la condicion; falla si el resultado no es verdadero.
            assert pedir('GET', ruta) == fila, f'PATCH inválido modificó {tabla}'
            # Ejecuta el bloque siguiente solo cuando se cumple: tabla == 'grupo_investigacion'.
            if tabla == 'grupo_investigacion':
                # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                pedir('PATCH', ruta, {'universidsad': numero-1}, esperado=400)
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            pedir('PATCH', ruta, {caso['mutables'][0]: cuerpo[caso['mutables'][0]]})
            # Asigna a parcial el valor calculado a la derecha.
            parcial = dict(cuerpo)
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            parcial.pop(caso['mutables'][0])
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            pedir('PUT', ruta, parcial, esperado=422)
            # Asigna a pagina el valor calculado a la derecha.
            pagina = urlopen('http://front-flask:8078/' + tabla.replace('_','-') + '/nuevo', timeout=15).read().decode()
            # Verifica la condicion; falla si el resultado no es verdadero.
            assert '<select' in pagina and str(numero) in pagina, f'Desplegables ausentes en {tabla}'
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            print('[OK]', tabla, 'API y desplegables')
        # Recorre los elementos de la coleccion indicada y ejecuta el bloque para cada uno.
        for tabla in ['docente','grupo_investigacion','semillero']:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            pedir('DELETE', '/api/' + tabla + '/' + str(numero), esperado=400)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        pedir('DELETE', '/api/area_conocimiento/1A01', esperado=400)
        # Recorre los elementos de la coleccion indicada y ejecuta el bloque para cada uno.
        for caso, datos, ruta in reversed(creados):
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            pedir('DELETE', ruta)
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            pedir('GET', ruta, esperado=404)
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            pedir('DELETE', ruta, esperado=404)
            # Asigna a condiciones el valor calculado a la derecha.
            condiciones = ' AND '.join(k + ' = :' + k for k in caso['claves'])
            # Abre el recurso asincronico y asegura su cierre al salir del bloque.
            async with motor.connect() as conexion:
                # Asigna a valor el valor calculado a la derecha.
                valor = await conexion.scalar(text('SELECT activo FROM ' + caso['tabla'] + ' WHERE ' + condiciones), {k:datos[k] for k in caso['claves']})
                # Verifica la condicion; falla si el resultado no es verdadero.
                assert valor is False, f'No quedó el borrado lógico en {caso["tabla"]}'
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            print('[OK]', caso['tabla'], 'fila conservada e inactiva')
        # Abre el recurso asincronico y asegura su cierre al salir del bloque.
        async with motor.begin() as conexion:
            # Espera que termine la operacion asincronica antes de continuar.
            await conexion.execute(text('UPDATE universidad SET activo = FALSE WHERE id = :id'), {'id': numero})
            # Espera que termine la operacion asincronica antes de continuar.
            await conexion.execute(text('UPDATE linea_investigacion SET activo = FALSE WHERE id = :id'), {'id': numero})
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        print('Smoke test v2 completo. Identificador de las fichas de prueba:', numero)
    # Ejecuta este bloque al final, haya ocurrido o no una excepcion.
    finally:
        # Espera que termine la operacion asincronica antes de continuar.
        await motor.dispose()


# Ejecuta el bloque siguiente solo cuando se cumple: __name__ == '__main__'.
if __name__ == '__main__':
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    asyncio.run(main())
