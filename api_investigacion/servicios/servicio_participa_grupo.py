"""Reglas para una clave compuesta validan el cuerpo antes de pedir la operación al repositorio."""

from repositorios.abstracciones.i_repositorio_participa_grupo import IRepositorioParticipaGrupo


class ServicioParticipaGrupo:
    def __init__(self, repositorio: IRepositorioParticipaGrupo):
        self._repositorio = repositorio

    async def listar(self, limite: int) -> list[dict]:
        if limite <= 0:
            raise ValueError("El límite debe ser mayor que cero.")
        return await self._repositorio.obtener_todos(limite)

    async def obtener(self, docente_cedula: int, grupo_investigacion_id: int) -> dict:
        fila = await self._repositorio.obtener_por_claves(docente_cedula, grupo_investigacion_id)
        if fila is None:
            raise LookupError("No existe la participación solicitada.")
        return fila

    async def crear(self, datos: dict) -> None:
        await self._repositorio.crear(datos)

    async def actualizar(self, docente_cedula: int, grupo_investigacion_id: int, datos: dict) -> int:
        if not datos:
            raise ValueError("No se envió ningún campo para actualizar.")
        filas = await self._repositorio.actualizar_por_claves(
            docente_cedula, grupo_investigacion_id, datos
        )
        if filas == 0:
            raise LookupError("No existe la participación solicitada.")
        return filas

    async def eliminar(self, docente_cedula: int, grupo_investigacion_id: int) -> int:
        filas = await self._repositorio.eliminar_logico(docente_cedula, grupo_investigacion_id)
        if filas == 0:
            raise LookupError("No existe la participación solicitada.")
        return filas
