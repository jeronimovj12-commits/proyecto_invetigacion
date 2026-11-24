"""La identidad del vínculo se expresa con las dos claves compuestas originales."""

from repositorios.abstracciones.i_repositorio_aa_linea import IRepositorioAaLinea
from repositorios.repositorio_postgresql_compuesto import RepositorioPostgreSQLCompuesto


class RepositorioAaLineaPostgreSQL(RepositorioPostgreSQLCompuesto, IRepositorioAaLinea):
    TABLA = "aa_linea"
    CLAVES = ("area_aplicacion", "linea_investigacion")
    COLUMNAS = CLAVES
    COLUMNAS_CREACION = CLAVES

    async def obtener_por_claves(self, area_aplicacion: int, linea_investigacion: int):
        return await self._obtener_por_claves(area_aplicacion, linea_investigacion)

    async def crear(self, datos: dict) -> None:
        await self._crear(datos)

    async def eliminar_logico(self, area_aplicacion: int, linea_investigacion: int):
        return await self._eliminar_logico(area_aplicacion, linea_investigacion)
