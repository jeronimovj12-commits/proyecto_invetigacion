"""Reglas compartidas sin HTTP; así se pueden validar las decisiones de negocio con dobles en memoria."""

from repositorios.abstracciones.i_repositorio_base import IRepositorioBase


class ServicioBase:
    def __init__(self, repositorio: IRepositorioBase):
        self._repositorio = repositorio

    @staticmethod
    def _validar_identificador(identificador: str | int) -> str | int:
        if isinstance(identificador, str) and not identificador.strip():
            raise ValueError("La clave no puede estar vacía.")
        return identificador

    async def listar(self, limite: int) -> list[dict]:
        if limite <= 0:
            raise ValueError("El límite debe ser mayor que cero.")
        return await self._repositorio.obtener_todos(limite)

    async def obtener(self, identificador: str | int) -> dict:
        identificador = self._validar_identificador(identificador)
        fila = await self._repositorio.obtener_por_id(identificador)
        if fila is None:
            raise LookupError(f"No existe el registro {identificador}.")
        return fila

    async def crear(self, datos: dict) -> str | int | None:
        return await self._repositorio.crear(datos)

    async def actualizar(self, identificador: str | int, datos: dict) -> int:
        identificador = self._validar_identificador(identificador)
        if not datos:
            raise ValueError("No se envió ningún campo para actualizar.")
        filas = await self._repositorio.actualizar(identificador, datos)
        if filas == 0:
            raise LookupError(f"No existe el registro {identificador}.")
        return filas

    async def eliminar(self, identificador: str | int) -> int:
        identificador = self._validar_identificador(identificador)
        filas = await self._repositorio.eliminar_logico(identificador)
        if filas == 0:
            raise LookupError(f"No existe el registro {identificador}.")
        return filas
