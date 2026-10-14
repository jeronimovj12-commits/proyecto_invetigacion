from repositorios.abstracciones.i_repositorio_linea_investigacion import IRepositorioLineaInvestigacion


class ServicioLineaInvestigacion:
    def __init__(self, repositorio: IRepositorioLineaInvestigacion):
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
