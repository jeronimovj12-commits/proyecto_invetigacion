"""La clave de área no se transforma porque forma parte de una PK VARCHAR."""

from repositorios.abstracciones.i_repositorio_ac_linea import IRepositorioAcLinea


class ServicioAcLinea:
    def __init__(self, repositorio: IRepositorioAcLinea):
        self._repositorio = repositorio

    async def listar(self, limite: int) -> list[dict]:
        if limite <= 0:
            raise ValueError("El límite debe ser mayor que cero.")
        return await self._repositorio.obtener_todos(limite)

    async def obtener(self, linea_investigacion: int, area_conocimiento: str) -> dict:
        fila = await self._repositorio.obtener_por_claves(linea_investigacion, area_conocimiento)
        if fila is None:
            raise LookupError("No existe el vínculo solicitado.")
        return fila

    async def crear(self, datos: dict) -> None:
        await self._repositorio.crear(datos)

    async def eliminar(self, linea_investigacion: int, area_conocimiento: str) -> int:
        filas = await self._repositorio.eliminar_logico(linea_investigacion, area_conocimiento)
        if filas == 0:
            raise LookupError("No existe el vínculo solicitado.")
        return filas
