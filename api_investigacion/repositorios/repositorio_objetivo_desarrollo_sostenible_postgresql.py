"""SQL explícito y parametrizado para objetivo_desarrollo_sostenible."""
from sqlalchemy import text
from repositorios.conexion_postgresql import ConexionPostgreSQL


class RepositorioObjetivoDesarrolloSosteniblePostgreSQL(ConexionPostgreSQL):
    async def obtener_todos(self, limite: int) -> list[dict]:
        async with self._conexion() as conexion:
            resultado = await conexion.execute(text("SELECT id, nombre, categoria FROM objetivo_desarrollo_sostenible WHERE activo = TRUE LIMIT :limite"), {"limite": limite})
            return [dict(fila) for fila in resultado.mappings()]

    async def obtener_por_id(self, identidad: dict) -> dict | None:
        async with self._conexion() as conexion:
            resultado = await conexion.execute(text("SELECT id, nombre, categoria FROM objetivo_desarrollo_sostenible WHERE id = :id AND activo = TRUE"), identidad)
            fila = resultado.mappings().first()
            return dict(fila) if fila is not None else None
