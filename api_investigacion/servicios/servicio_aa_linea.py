"""La identidad de cada asociación se trata como una pareja indivisible."""

from repositorios.abstracciones.i_repositorio_aa_linea import IRepositorioAaLinea


class ServicioAaLinea:
    def __init__(self, repositorio: IRepositorioAaLinea):
        self._repositorio = repositorio

    async def listar(self, limite: int) -> list[dict]:
        if limite <= 0:
            raise ValueError("El límite debe ser mayor que cero.")
        return await self._repositorio.obtener_todos(limite)

    async def obtener(self, area_aplicacion: int, linea_investigacion: int) -> dict:
        fila = await self._repositorio.obtener_por_claves(area_aplicacion, linea_investigacion)
        if fila is None:
            raise LookupError("No existe el vínculo solicitado.")
        return fila

    async def crear(self, datos: dict) -> None:
        await self._repositorio.crear(datos)

    async def eliminar(self, area_aplicacion: int, linea_investigacion: int) -> int:
        filas = await self._repositorio.eliminar_logico(area_aplicacion, linea_investigacion)
        if filas == 0:
            raise LookupError("No existe el vínculo solicitado.")
        return filas
