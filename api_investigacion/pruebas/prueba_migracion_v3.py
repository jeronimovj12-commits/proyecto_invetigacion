# Ejecuta la instruccion indicada dentro del flujo actual.
"""Migración con datos previos, repetición y rechazo de esquema incompatible."""
# Carga el modulo o los modulos asyncio.
import asyncio
# Carga el modulo o los modulos os.
import os
# Importa Path desde pathlib para usar esas definiciones.
from pathlib import Path
# Importa uuid4 desde uuid para usar esas definiciones.
from uuid import uuid4
# Carga el modulo o los modulos asyncpg.
import asyncpg
# Importa make_url desde sqlalchemy.engine para usar esas definiciones.
from sqlalchemy.engine import make_url

# Define la funcion ejecutar con los parametros declarados; su bloque realiza esta operacion.
async def ejecutar():
    # Asigna a original el valor calculado a la derecha.
    original = make_url(os.environ['DB_POSTGRES'])
    # Ejecuta el bloque siguiente solo cuando se cumple: os.environ.get('PRUEBAS_V3') != '1' or original.host != 'postgres-v3' or original.database != 'investigacion_v3'.
    if os.environ.get('PRUEBAS_V3') != '1' or original.host != 'postgres-v3' or original.database != 'investigacion_v3':
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise RuntimeError('Solo entorno v3 aislado.')
    # Asigna a nombre el valor calculado a la derecha.
    nombre = 'pruebas_migracion_v3_' + uuid4().hex
    # Asigna a c el valor calculado a la derecha.
    c = await asyncpg.connect(original.set(drivername='postgresql', database='postgres').render_as_string(hide_password=False))
    # Espera que termine la operacion asincronica antes de continuar.
    await c.execute('CREATE DATABASE "'+nombre+'"')
    # Espera que termine la operacion asincronica antes de continuar.
    await c.close()
    # Asigna a c el valor calculado a la derecha.
    c = await asyncpg.connect(original.set(drivername='postgresql', database=nombre).render_as_string(hide_password=False))
    # Inicia un bloque cuya excepcion se manejara en los except siguientes.
    try:
        # Espera que termine la operacion asincronica antes de continuar.
        await c.execute(Path('/db-v3/init.sql').read_text())
        # Espera que termine la operacion asincronica antes de continuar.
        await c.execute("INSERT INTO usuario(username,email,password,activo) VALUES ('PREVIO','previo@example.invalid','sin-acceso',FALSE)")
        # Espera que termine la operacion asincronica antes de continuar.
        await c.execute("INSERT INTO rol(nombre,activo) VALUES ('PREVIO',FALSE)")
        # Espera que termine la operacion asincronica antes de continuar.
        await c.execute('INSERT INTO rol_usuario(usuario_id,rol_id) VALUES (1,1)')
        # Construye la consulta SQL que ejecutara este repositorio.
        sql = '\n'.join(l for l in Path('/db-v3/migraciones/v3_001_sesiones_asignaciones.sql').read_text().splitlines() if not l.startswith('\\'))
        # Espera que termine la operacion asincronica antes de continuar.
        await c.execute(sql)
        # Espera que termine la operacion asincronica antes de continuar.
        await c.execute('UPDATE usuario SET version_sesion=7; UPDATE rol_usuario SET activo=FALSE')
        # Espera que termine la operacion asincronica antes de continuar.
        await c.execute(sql)
        # Asigna a fila el valor calculado a la derecha.
        fila = await c.fetchrow('SELECT activo,version_sesion FROM usuario WHERE id=1')
        # Verifica la condicion; falla si el resultado no es verdadero.
        assert fila['activo'] is False and fila['version_sesion'] == 7
        # Verifica la condicion; falla si el resultado no es verdadero.
        assert await c.fetchval('SELECT activo FROM rol_usuario WHERE usuario_id=1') is False
        # Espera que termine la operacion asincronica antes de continuar.
        await c.execute('ALTER TABLE rol_usuario ALTER COLUMN activo DROP NOT NULL')
        # Inicia un bloque cuya excepcion se manejara en los except siguientes.
        try:
            # Espera que termine la operacion asincronica antes de continuar.
            await c.execute(sql)
        # Captura la excepcion indicada para manejarla sin dejarla propagarse.
        except asyncpg.PostgresError:
            # Espera que termine la operacion asincronica antes de continuar.
            await c.execute('ROLLBACK')
        # Define el caso alternativo cuando las condiciones anteriores no se cumplen.
        else:
            # Lanza la excepcion indicada y detiene el flujo normal.
            raise AssertionError('No rechazó esquema incompatible.')
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        print('Migración: datos previos, repetición y rechazo incompatible OK. Base:',nombre)
    # Ejecuta este bloque al final, haya ocurrido o no una excepcion.
    finally:
        # Espera que termine la operacion asincronica antes de continuar.
        await c.close()

# Ejecuta el bloque siguiente solo cuando se cumple: __name__ == '__main__'.
if __name__ == '__main__':
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    asyncio.run(ejecutar())
