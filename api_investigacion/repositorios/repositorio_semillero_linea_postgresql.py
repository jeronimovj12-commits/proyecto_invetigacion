"""La tabla y las columnas son constantes; los valores SQL siempre se enlazan."""

from repositorios.abstracciones.i_repositorio_semillero_linea import IRepositorioSemilleroLinea
from repositorios.repositorio_postgresql_compuesto import RepositorioPostgreSQLCompuesto


class RepositorioSemilleroLineaPostgreSQL(RepositorioPostgreSQLCompuesto, IRepositorioSemilleroLinea):
    TABLA = "semillero_linea"
    CLAVES = ("semillero", "linea_investigacion")
    COLUMNAS = CLAVES
    COLUMNAS_CREACION = CLAVES

    async def obtener_por_claves(self, semillero: int, linea_investigacion: int):
        return await self._obtener_por_claves(semillero, linea_investigacion)

    async def crear(self, datos: dict) -> None:
        await self._crear(datos)

    async def eliminar_logico(self, semillero: int, linea_investigacion: int):
        return await self._eliminar_logico(semillero, linea_investigacion)
