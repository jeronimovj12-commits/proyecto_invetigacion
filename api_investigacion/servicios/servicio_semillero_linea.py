"""Las reglas de existencia y límite se aplican antes de depender de la base."""

from repositorios.abstracciones.i_repositorio_semillero_linea import IRepositorioSemilleroLinea


class ServicioSemilleroLinea:
    def __init__(self, repositorio: IRepositorioSemilleroLinea):
        self._repositorio = repositorio

    async def listar(self, limite: int) -> list[dict]:
        if limite <= 0:
            raise ValueError("El límite debe ser mayor que cero.")
        return await self._repositorio.obtener_todos(limite)

    async def obtener(self, semillero: int, linea_investigacion: int) -> dict:
        fila = await self._repositorio.obtener_por_claves(semillero, linea_investigacion)
        if fila is None:
            raise LookupError("No existe el vínculo solicitado.")
        return fila

    async def crear(self, datos: dict) -> None:
        await self._repositorio.crear(datos)

    async def eliminar(self, semillero: int, linea_investigacion: int) -> int:
        filas = await self._repositorio.eliminar_logico(semillero, linea_investigacion)
        if filas == 0:
            raise LookupError("No existe el vínculo solicitado.")
        return filas
