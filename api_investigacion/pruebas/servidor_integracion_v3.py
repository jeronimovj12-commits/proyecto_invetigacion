"""Servidor efímero de integración: crea su propia base y credenciales de prueba."""
import asyncio
import json
import os
from pathlib import Path
import secrets
import subprocess
import sys
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
import prueba_autenticacion_v3 as base

async def preparar():
    await base.preparar()
    clave_admin = secrets.token_urlsafe(24)
    clave_consulta = secrets.token_urlsafe(24)
    motor = create_async_engine(os.environ['DB_POSTGRES'], hide_parameters=True)
    async with motor.begin() as c:
        await c.execute(text('UPDATE usuario SET password=:h WHERE id=1'), {'h':base.CLAVES.crear(clave_admin)})
        uid = (await c.execute(text("INSERT INTO usuario(username,email,password) VALUES ('CONSULTA_INTEGRACION','consulta@example.invalid',:h) RETURNING id"), {'h':base.CLAVES.crear(clave_consulta)})).scalar_one()
        await c.execute(text("INSERT INTO rol_usuario(usuario_id,rol_id) SELECT :uid,id FROM rol WHERE nombre='consulta'"), {'uid':uid})
    await motor.dispose()
    ruta = Path('/fixture/cuentas.json')
    ruta.write_text(json.dumps({'administrador':{'username':'PRUEBA_INICIAL','password':clave_admin},
                                'consulta':{'username':'CONSULTA_INTEGRACION','password':clave_consulta}}))
    ruta.chmod(0o600)

if __name__ == '__main__':
    asyncio.run(preparar())
    raise SystemExit(subprocess.call([sys.executable, '-m', 'uvicorn', 'main_v3:app', '--host','0.0.0.0','--port','8031','--no-access-log']))
