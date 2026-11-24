"""Reglas de participación en semillero tratan la pareja de claves como una identidad inseparable."""

from repositorios.abstracciones.i_repositorio_participa_semillero import IRepositorioParticipaSemillero


class ServicioParticipaSemillero:
    def __init__(self, repositorio: IRepositorioParticipaSemillero):
        self._repositorio = repositorio

    async def listar(self, limite: int) -> list[dict]:
        if limite <= 0:
            raise ValueError("El límite debe ser mayor que cero.")
        return await self._repositorio.obtener_todos(limite)

    async def obtener(self, docente: int, semillero: int) -> dict:
        fila = await self._repositorio.obtener_por_claves(docente, semillero)
        if fila is None:
            raise LookupError("No existe la participación solicitada.")
        return fila

    async def crear(self, datos: dict) -> None:
        await self._repositorio.crear(datos)

    async def actualizar(self, docente: int, semillero: int, datos: dict) -> int:
        if not datos:
            raise ValueError("No se envió ningún campo para actualizar.")
        filas = await self._repositorio.actualizar_por_claves(docente, semillero, datos)
        if filas == 0:
            raise LookupError("No existe la participación solicitada.")
        return filas

    async def eliminar(self, docente: int, semillero: int) -> int:
        filas = await self._repositorio.eliminar_logico(docente, semillero)
        if filas == 0:
            raise LookupError("No existe la participación solicitada.")
        return filas
