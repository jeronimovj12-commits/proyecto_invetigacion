"""Adaptador SQL de participación en semilleros con borrado lógico sobre su clave doble."""

from repositorios.abstracciones.i_repositorio_participa_semillero import IRepositorioParticipaSemillero
from repositorios.repositorio_postgresql_compuesto import RepositorioPostgreSQLCompuesto


class RepositorioParticipaSemilleroPostgreSQL(RepositorioPostgreSQLCompuesto, IRepositorioParticipaSemillero):
    TABLA = "participa_semillero"
    CLAVES = ("docente", "semillero")
    COLUMNAS = (*CLAVES, "rol", "fecha_inicio", "fecha_fin")
    COLUMNAS_CREACION = COLUMNAS

    async def obtener_por_claves(self, docente: int, semillero: int):
        return await self._obtener_por_claves(docente, semillero)

    async def crear(self, datos: dict) -> None:
        await self._crear(datos)

    async def actualizar_por_claves(self, docente: int, semillero: int, datos: dict):
        return await self._actualizar_por_claves(docente, semillero, datos)

    async def eliminar_logico(self, docente: int, semillero: int):
        return await self._eliminar_logico(docente, semillero)
