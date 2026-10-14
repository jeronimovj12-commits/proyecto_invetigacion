"""
Servicio — la capa de NEGOCIO.

Depende solo de la interfaz del repositorio, así que no sabe qué motor hay
detrás: por eso se puede probar sin base de datos.

Comunica los problemas con excepciones, que el controlador traduce a códigos
HTTP. El servicio no sabe qué es un 404, y así debe ser.
"""

from repositorios.abstracciones.i_repositorio_area_conocimiento import (
    IRepositorioAreaConocimiento,
)


class ServicioAreaConocimiento:
    """Reglas de negocio del CRUD de area_conocimiento."""

    def __init__(self, repositorio: IRepositorioAreaConocimiento):
        self._repositorio = repositorio

    @staticmethod
    def _validar_id(id_area: str) -> str:
        id_area = (id_area or "").strip()
        if not id_area:
            raise ValueError("El id del área de conocimiento no puede estar vacío.")
        return id_area

    async def listar(self, limite: int) -> list[dict]:
        # La FORMA del dato es correcta (sí es un entero), así que esto es
        # 400 y no 422.
        if limite <= 0:
            raise ValueError("El límite debe ser un entero mayor que cero.")
        return await self._repositorio.obtener_todos(limite)

    async def obtener(self, id_area: str) -> dict:
        id_area = self._validar_id(id_area)
        fila = await self._repositorio.obtener_por_id(id_area)
        if fila is None:
            raise LookupError(
                f"No existe un área con el código {id_area}.")
        return fila

    async def crear(self, datos: dict) -> None:
        await self._repositorio.crear(datos)

    async def actualizar(self, id_area: str, datos: dict) -> int:
        id_area = self._validar_id(id_area)
        # Sin esta comprobación el repositorio devolvería 0 filas, que en
        # toda la demás lógica significa "no existe" — y responderíamos 404
        # en vez del 400 que exige el contrato para un cuerpo vacío.
        if not datos:
            raise ValueError("No se envió ningún campo para actualizar.")
        filas = await self._repositorio.actualizar(id_area, datos)
        if filas == 0:
            raise LookupError(
                f"No existe un área con el código {id_area}.")
        return filas

    async def eliminar(self, id_area: str) -> int:
        id_area = self._validar_id(id_area)
        async with self._repositorio.transaccion():
            await self.obtener(id_area)
            if await self._repositorio.tiene_dependientes(id_area):
                raise ValueError("El área tiene líneas activas relacionadas. Retire primero esas relaciones.")
            filas = await self._repositorio.eliminar_logico(id_area)
            if filas == 0:
                raise LookupError(f"No existe un área con el código {id_area}.")
            return filas
