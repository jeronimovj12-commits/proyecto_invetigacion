from repositorios.abstracciones.i_repositorio_ods_linea import IRepositorioOdsLinea


class ServicioOdsLinea:
    def __init__(self, repositorio: IRepositorioOdsLinea):
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

    async def _validar_referencias(self, datos: dict) -> None:
        for campo in ('linea_investigacion', 'ods'):
            if campo in datos and datos[campo] is not None:
                if not await self._repositorio.referencia_activa(campo, datos[campo]):
                    raise ValueError(f"La referencia {campo} no existe o está inactiva.")

    async def crear(self, datos: dict) -> None:
        async with self._repositorio.transaccion():
            await self._validar_referencias(datos)
            await self._repositorio.crear(datos)

    async def actualizar(self, identidad: dict, datos: dict) -> int:
        async with self._repositorio.transaccion():
            if not datos:
                raise ValueError("No se envió ningún campo para actualizar.")
            actual = await self.obtener(identidad)
            await self._validar_referencias({**actual, **datos})
            filas = await self._repositorio.actualizar(identidad, datos)
            if filas == 0:
                raise LookupError("El registro no existe o está inactivo.")
            return filas

    async def eliminar(self, identidad: dict) -> int:
        async with self._repositorio.transaccion():
            await self.obtener(identidad)
            if await self._repositorio.tiene_dependientes(identidad):
                raise ValueError("El registro tiene relaciones activas. Retire primero esas relaciones.")
            filas = await self._repositorio.eliminar_logico(identidad)
            if filas == 0:
                raise LookupError("El registro no existe o está inactivo.")
            return filas
