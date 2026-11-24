"""Adaptador SQL de participación en grupos; la actualización conserva la identidad de ambas claves."""

from repositorios.abstracciones.i_repositorio_participa_grupo import IRepositorioParticipaGrupo
from repositorios.repositorio_postgresql_compuesto import RepositorioPostgreSQLCompuesto


class RepositorioParticipaGrupoPostgreSQL(RepositorioPostgreSQLCompuesto, IRepositorioParticipaGrupo):
    TABLA = "participa_grupo"
    CLAVES = ("docente_cedula", "grupo_investigacion_id")
    COLUMNAS = (*CLAVES, "rol", "fecha_inicio", "fecha_fin")
    COLUMNAS_CREACION = COLUMNAS

    async def obtener_por_claves(self, docente_cedula: int, grupo_investigacion_id: int):
        return await self._obtener_por_claves(docente_cedula, grupo_investigacion_id)

    async def crear(self, datos: dict) -> None:
        await self._crear(datos)

    async def actualizar_por_claves(self, docente_cedula: int, grupo_investigacion_id: int, datos: dict):
        return await self._actualizar_por_claves(docente_cedula, grupo_investigacion_id, datos)

    async def eliminar_logico(self, docente_cedula: int, grupo_investigacion_id: int):
        return await self._eliminar_logico(docente_cedula, grupo_investigacion_id)
