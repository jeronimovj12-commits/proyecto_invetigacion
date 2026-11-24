"""Las reglas de búsqueda y borrado permanecen fuera del controlador HTTP."""

from repositorios.abstracciones.i_repositorio_grupo_linea import IRepositorioGrupoLinea


class ServicioGrupoLinea:
    def __init__(self, repositorio: IRepositorioGrupoLinea):
        self._repositorio = repositorio

    async def listar(self, limite: int) -> list[dict]:
        if limite <= 0:
            raise ValueError("El límite debe ser mayor que cero.")
        return await self._repositorio.obtener_todos(limite)

    async def obtener(self, grupo_investigacion: int, linea_investigacion: int) -> dict:
        fila = await self._repositorio.obtener_por_claves(grupo_investigacion, linea_investigacion)
        if fila is None:
            raise LookupError("No existe el vínculo solicitado.")
        return fila

    async def crear(self, datos: dict) -> None:
        await self._repositorio.crear(datos)

    async def eliminar(self, grupo_investigacion: int, linea_investigacion: int) -> int:
        filas = await self._repositorio.eliminar_logico(grupo_investigacion, linea_investigacion)
        if filas == 0:
            raise LookupError("No existe el vínculo solicitado.")
        return filas
