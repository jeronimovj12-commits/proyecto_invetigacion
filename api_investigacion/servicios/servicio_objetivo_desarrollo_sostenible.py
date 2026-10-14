from repositorios.abstracciones.i_repositorio_objetivo_desarrollo_sostenible import IRepositorioObjetivoDesarrolloSostenible


class ServicioObjetivoDesarrolloSostenible:
    def __init__(self, repositorio: IRepositorioObjetivoDesarrolloSostenible):
        self._repositorio = repositorio

    async def listar(self, limite: int) -> list[dict]:
        if limite <= 0:
            raise ValueError("El límite debe ser mayor que cero.")
        return await self._repositorio.obtener_todos(limite)

    async def obtener(self, identidad: dict) -> dict:
        fila = await self._repositorio.obtener_por_id(identidad)
        if fila is None:
            raise LookupError("El registro no existe o está inactivo.")
        return fila
