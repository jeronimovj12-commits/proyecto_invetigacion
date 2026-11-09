from asyncio import to_thread
from repositorios.abstracciones.i_repositorio_seguridad import IRepositorioSeguridad
from seguridad.interfaces import IClaves

class ServicioSeguridad:
    def __init__(self, repositorio: IRepositorioSeguridad, claves: IClaves):
        self._repositorio = repositorio
        self._claves = claves

    async def listar(self, recurso, claves, limite):
        return await self._repositorio.listar(recurso, claves, limite)

    async def guardar(self, recurso, claves, datos, crear=False):
        datos = dict(datos)
        if 'password' in datos:
            datos['password'] = await to_thread(self._claves.crear, datos['password'].get_secret_value())
        return await self._repositorio.guardar(recurso, claves, datos, crear)

    async def retirar(self, recurso, claves):
        await self._repositorio.retirar(recurso, claves)
