"""El parámetro de área sigue siendo texto para respetar el VARCHAR(6) original."""

from repositorios.abstracciones.i_repositorio_ac_linea import IRepositorioAcLinea
from repositorios.repositorio_postgresql_compuesto import RepositorioPostgreSQLCompuesto


class RepositorioAcLineaPostgreSQL(RepositorioPostgreSQLCompuesto, IRepositorioAcLinea):
    TABLA = "ac_linea"
    CLAVES = ("linea_investigacion", "area_conocimiento")
    COLUMNAS = CLAVES
    COLUMNAS_CREACION = CLAVES

    async def obtener_por_claves(self, linea_investigacion: int, area_conocimiento: str):
        return await self._obtener_por_claves(linea_investigacion, area_conocimiento)

    async def crear(self, datos: dict) -> None:
        await self._crear(datos)

    async def eliminar_logico(self, linea_investigacion: int, area_conocimiento: str):
        return await self._eliminar_logico(linea_investigacion, area_conocimiento)
