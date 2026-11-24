"""El repositorio fija los nombres SQL y enlaza cada valor recibido como parámetro."""

from repositorios.abstracciones.i_repositorio_ods_linea import IRepositorioOdsLinea
from repositorios.repositorio_postgresql_compuesto import RepositorioPostgreSQLCompuesto


class RepositorioOdsLineaPostgreSQL(RepositorioPostgreSQLCompuesto, IRepositorioOdsLinea):
    TABLA = "ods_linea"
    CLAVES = ("linea_investigacion", "ods")
    COLUMNAS = CLAVES
    COLUMNAS_CREACION = CLAVES

    async def obtener_por_claves(self, linea_investigacion: int, ods: int):
        return await self._obtener_por_claves(linea_investigacion, ods)

    async def crear(self, datos: dict) -> None:
        await self._crear(datos)

    async def eliminar_logico(self, linea_investigacion: int, ods: int):
        return await self._eliminar_logico(linea_investigacion, ods)
