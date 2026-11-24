"""La desasignación elimina solo la relación porque rol_usuario no tiene columna activo."""

from sqlalchemy import text

from repositorios.abstracciones.i_repositorio_rol_usuario import IRepositorioRolUsuario
from database import obtener_engine


class RepositorioRolUsuarioPostgreSQL(IRepositorioRolUsuario):
    def __init__(self):
        self._engine = obtener_engine()

    async def obtener_todos(self, limite: int) -> list[dict]:
        consulta = text(
            "SELECT ru.usuario_id, ru.rol_id FROM rol_usuario ru "
            "JOIN usuario u ON u.id = ru.usuario_id "
            "JOIN rol r ON r.id = ru.rol_id "
            "WHERE u.activo = TRUE AND r.activo = TRUE "
            "ORDER BY ru.usuario_id, ru.rol_id LIMIT :limite"
        )
        async with self._engine.connect() as conexion:
            resultado = await conexion.execute(consulta, {"limite": limite})
            return [dict(fila._mapping) for fila in resultado]

    async def obtener_por_claves(self, usuario_id: int, rol_id: int) -> dict | None:
        consulta = text(
            "SELECT ru.usuario_id, ru.rol_id FROM rol_usuario ru "
            "JOIN usuario u ON u.id = ru.usuario_id "
            "JOIN rol r ON r.id = ru.rol_id "
            "WHERE ru.usuario_id = :usuario_id AND ru.rol_id = :rol_id "
            "AND u.activo = TRUE AND r.activo = TRUE"
        )
        async with self._engine.connect() as conexion:
            resultado = await conexion.execute(
                consulta, {"usuario_id": usuario_id, "rol_id": rol_id}
            )
            fila = resultado.first()
            return dict(fila._mapping) if fila else None

    async def crear(self, datos: dict) -> int:
        consulta = text(
            "INSERT INTO rol_usuario (usuario_id, rol_id) "
            "SELECT :usuario_id, :rol_id "
            "WHERE EXISTS (SELECT 1 FROM usuario WHERE id = :usuario_id AND activo = TRUE) "
            "AND EXISTS (SELECT 1 FROM rol WHERE id = :rol_id AND activo = TRUE)"
        )
        async with self._engine.begin() as conexion:
            resultado = await conexion.execute(consulta, datos)
            return resultado.rowcount

    async def eliminar(self, usuario_id: int, rol_id: int) -> int:
        consulta = text(
            "DELETE FROM rol_usuario "
            "WHERE usuario_id = :usuario_id AND rol_id = :rol_id"
        )
        async with self._engine.begin() as conexion:
            resultado = await conexion.execute(
                consulta, {"usuario_id": usuario_id, "rol_id": rol_id}
            )
            return resultado.rowcount
