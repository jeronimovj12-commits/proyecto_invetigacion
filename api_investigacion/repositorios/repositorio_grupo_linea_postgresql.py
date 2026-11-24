"""La configuración fija de columnas permite reutilizar SQL seguro sin ORM."""

from repositorios.abstracciones.i_repositorio_grupo_linea import IRepositorioGrupoLinea
from repositorios.repositorio_postgresql_compuesto import RepositorioPostgreSQLCompuesto


class RepositorioGrupoLineaPostgreSQL(RepositorioPostgreSQLCompuesto, IRepositorioGrupoLinea):
    TABLA = "grupo_linea"
    CLAVES = ("grupo_investigacion", "linea_investigacion")
    COLUMNAS = CLAVES
    COLUMNAS_CREACION = CLAVES

    async def obtener_por_claves(self, grupo_investigacion: int, linea_investigacion: int):
        return await self._obtener_por_claves(grupo_investigacion, linea_investigacion)

    async def crear(self, datos: dict) -> None:
        await self._crear(datos)

    async def eliminar_logico(self, grupo_investigacion: int, linea_investigacion: int):
        return await self._eliminar_logico(grupo_investigacion, linea_investigacion)
