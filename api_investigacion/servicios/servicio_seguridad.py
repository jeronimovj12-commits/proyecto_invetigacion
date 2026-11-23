# Ejecuta la instruccion indicada dentro del flujo actual.
"""Servicio de negocio: coordina las reglas del caso de uso con los repositorios sin ejecutar SQL directamente."""
# Importa to_thread desde asyncio para usar esas definiciones.
from asyncio import to_thread
# Importa IRepositorioSeguridad desde repositorios.abstracciones.i_repositorio_seguridad para usar esas definiciones.
from repositorios.abstracciones.i_repositorio_seguridad import IRepositorioSeguridad
# Importa IClaves desde seguridad.interfaces para usar esas definiciones.
from seguridad.interfaces import IClaves

# Define la clase ServicioSeguridad y agrupa su estado y operaciones.
class ServicioSeguridad:
    # Define la funcion __init__ con los parametros declarados; su bloque realiza esta operacion.
    def __init__(self, repositorio: IRepositorioSeguridad, claves: IClaves):
        # Guarda en self._repositorio el valor necesario para reutilizarlo en otros metodos.
        self._repositorio = repositorio
        # Guarda en self._claves el valor necesario para reutilizarlo en otros metodos.
        self._claves = claves

    # Define la funcion listar con los parametros declarados; su bloque realiza esta operacion.
    async def listar(self, recurso, claves, limite):
        # Devuelve al llamador el resultado de la expresion indicada.
        return await self._repositorio.listar(recurso, claves, limite)

    # Define la funcion guardar con los parametros declarados; su bloque realiza esta operacion.
    async def guardar(self, recurso, claves, datos, crear=False):
        # Asigna a datos el valor calculado a la derecha.
        datos = dict(datos)
        # Ejecuta el bloque siguiente solo cuando se cumple: 'password' in datos.
        if 'password' in datos:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            datos['password'] = await to_thread(self._claves.crear, datos['password'].get_secret_value())
        # Devuelve al llamador el resultado de la expresion indicada.
        return await self._repositorio.guardar(recurso, claves, datos, crear)

    # Define la funcion retirar con los parametros declarados; su bloque realiza esta operacion.
    async def retirar(self, recurso, claves):
        # Espera que termine la operacion asincronica antes de continuar.
        await self._repositorio.retirar(recurso, claves)
