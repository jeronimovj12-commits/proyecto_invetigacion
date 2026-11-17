# Ejecuta la instruccion indicada dentro del flujo actual.
"""Servidor efímero de integración: crea su propia base y credenciales de prueba."""
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
# Importa text desde sqlalchemy para usar esas definiciones.
from sqlalchemy import text
# Importa create_async_engine desde sqlalchemy.ext.asyncio para usar esas definiciones.
from sqlalchemy.ext.asyncio import create_async_engine
# Carga el modulo o los modulos prueba_autenticacion_v3 as base.
import prueba_autenticacion_v3 as base

# Define la funcion preparar con los parametros declarados; su bloque realiza esta operacion.
async def preparar():
    # Espera que termine la operacion asincronica antes de continuar.
    await base.preparar()
    # Asigna a clave_admin el valor calculado a la derecha.
    clave_admin = secrets.token_urlsafe(24)
    # Asigna a clave_consulta el valor calculado a la derecha.
    clave_consulta = secrets.token_urlsafe(24)
    # Asigna a motor el valor calculado a la derecha.
    motor = create_async_engine(os.environ['DB_POSTGRES'], hide_parameters=True)
    # Abre el recurso asincronico y asegura su cierre al salir del bloque.
    async with motor.begin() as c:
        # Espera que termine la operacion asincronica antes de continuar.
        await c.execute(text('UPDATE usuario SET password=:h WHERE id=1'), {'h':base.CLAVES.crear(clave_admin)})
        # Asigna a uid el valor calculado a la derecha.
        uid = (await c.execute(text("INSERT INTO usuario(username,email,password) VALUES ('CONSULTA_INTEGRACION','consulta@example.invalid',:h) RETURNING id"), {'h':base.CLAVES.crear(clave_consulta)})).scalar_one()
        # Espera que termine la operacion asincronica antes de continuar.
        await c.execute(text("INSERT INTO rol_usuario(usuario_id,rol_id) SELECT :uid,id FROM rol WHERE nombre='consulta'"), {'uid':uid})
    # Espera que termine la operacion asincronica antes de continuar.
    await motor.dispose()
    # Asigna a ruta el valor calculado a la derecha.
    ruta = Path('/fixture/cuentas.json')
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ruta.write_text(json.dumps({'administrador':{'username':'PRUEBA_INICIAL','password':clave_admin},
                                # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                                'consulta':{'username':'CONSULTA_INTEGRACION','password':clave_consulta}}))
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ruta.chmod(0o600)

# Ejecuta el bloque siguiente solo cuando se cumple: __name__ == '__main__'.
if __name__ == '__main__':
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    asyncio.run(preparar())
    # Lanza la excepcion indicada y detiene el flujo normal.
    raise SystemExit(subprocess.call([sys.executable, '-m', 'uvicorn', 'main_v3:app', '--host','0.0.0.0','--port','8031','--no-access-log']))
