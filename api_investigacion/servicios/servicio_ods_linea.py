"""El servicio convierte resultados vacíos en excepciones de negocio uniformes."""

from repositorios.abstracciones.i_repositorio_ods_linea import IRepositorioOdsLinea


class ServicioOdsLinea:
    def __init__(self, repositorio: IRepositorioOdsLinea):
        self._repositorio = repositorio

    async def listar(self, limite: int) -> list[dict]:
        if limite <= 0:
            raise ValueError("El límite debe ser mayor que cero.")
        return await self._repositorio.obtener_todos(limite)

    async def obtener(self, linea_investigacion: int, ods: int) -> dict:
        fila = await self._repositorio.obtener_por_claves(linea_investigacion, ods)
        if fila is None:
            raise LookupError("No existe el vínculo solicitado.")
        return fila

    async def crear(self, datos: dict) -> None:
        await self._repositorio.crear(datos)

    async def eliminar(self, linea_investigacion: int, ods: int) -> int:
        filas = await self._repositorio.eliminar_logico(linea_investigacion, ods)
        if filas == 0:
            raise LookupError("No existe el vínculo solicitado.")
        return filas
