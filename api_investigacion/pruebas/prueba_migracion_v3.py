"""Migración con datos previos, repetición y rechazo de esquema incompatible."""
import asyncio
import os
from pathlib import Path
from uuid import uuid4
import asyncpg
from sqlalchemy.engine import make_url

async def ejecutar():
    original = make_url(os.environ['DB_POSTGRES'])
    if os.environ.get('PRUEBAS_V3') != '1' or original.host != 'postgres-v3' or original.database != 'investigacion_v3':
        raise RuntimeError('Solo entorno v3 aislado.')
    nombre = 'pruebas_migracion_v3_' + uuid4().hex
    c = await asyncpg.connect(original.set(drivername='postgresql', database='postgres').render_as_string(hide_password=False))
    await c.execute('CREATE DATABASE "'+nombre+'"')
    await c.close()
    c = await asyncpg.connect(original.set(drivername='postgresql', database=nombre).render_as_string(hide_password=False))
    try:
        await c.execute(Path('/db-v3/init.sql').read_text())
        await c.execute("INSERT INTO usuario(username,email,password,activo) VALUES ('PREVIO','previo@example.invalid','sin-acceso',FALSE)")
        await c.execute("INSERT INTO rol(nombre,activo) VALUES ('PREVIO',FALSE)")
        await c.execute('INSERT INTO rol_usuario(usuario_id,rol_id) VALUES (1,1)')
        sql = '\n'.join(l for l in Path('/db-v3/migraciones/v3_001_sesiones_asignaciones.sql').read_text().splitlines() if not l.startswith('\\'))
        await c.execute(sql)
        await c.execute('UPDATE usuario SET version_sesion=7; UPDATE rol_usuario SET activo=FALSE')
        await c.execute(sql)
        fila = await c.fetchrow('SELECT activo,version_sesion FROM usuario WHERE id=1')
        assert fila['activo'] is False and fila['version_sesion'] == 7
        assert await c.fetchval('SELECT activo FROM rol_usuario WHERE usuario_id=1') is False
        await c.execute('ALTER TABLE rol_usuario ALTER COLUMN activo DROP NOT NULL')
        try:
            await c.execute(sql)
        except asyncpg.PostgresError:
            await c.execute('ROLLBACK')
        else:
            raise AssertionError('No rechazó esquema incompatible.')
        print('Migración: datos previos, repetición y rechazo incompatible OK. Base:',nombre)
    finally:
        await c.close()

if __name__ == '__main__':
    asyncio.run(ejecutar())
