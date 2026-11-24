"""El servicio comunica vínculos ausentes con excepciones para traducirlos a HTTP."""

from repositorios.abstracciones.i_repositorio_rol_usuario import IRepositorioRolUsuario
from servicios.abstracciones.i_servicio_rol_usuario import IServicioRolUsuario


class ServicioRolUsuario:
    def __init__(self, repositorio: IRepositorioRolUsuario):
        self._repositorio = repositorio

    async def listar(self, limite: int) -> list[dict]:
        if limite <= 0:
            raise ValueError("El límite debe ser mayor que cero.")
        return await self._repositorio.obtener_todos(limite)

    async def obtener(self, usuario_id: int, rol_id: int) -> dict:
        fila = await self._repositorio.obtener_por_claves(usuario_id, rol_id)
        if fila is None:
            raise LookupError("No existe la asignación solicitada.")
        return fila

    async def crear(self, datos: dict) -> None:
        filas = await self._repositorio.crear(datos)
        if filas == 0:
            raise LookupError("El usuario y el rol deben existir y estar activos.")

    async def eliminar(self, usuario_id: int, rol_id: int) -> int:
        filas = await self._repositorio.eliminar(usuario_id, rol_id)
        if filas == 0:
            raise LookupError("No existe la asignación solicitada.")
        return filas
