"""
Repositorio para PostgreSQL — la capa de DATOS.

SQLAlchemy async como EJECUTOR, no como ORM: el SQL se escribe a mano, queda
a la vista y SIEMPRE va parametrizado con `text()` y `:parametro`.

Todas las consultas filtran por activo = TRUE: el borrado es LÓGICO.
"""

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine


class RepositorioAreaConocimientoPostgreSQL:
    """Implementación concreta de IRepositorioAreaConocimiento."""

    # Las columnas se listan una sola vez: si mañana entra una, entra aquí.
    COLUMNAS = "id, gran_area, area, disciplina"

    def __init__(self, cadena_conexion: str):
        self._cadena_conexion = cadena_conexion
        self._engine: AsyncEngine | None = None

    def _obtener_engine(self) -> AsyncEngine:
        # Se crea la primera vez que se necesita: construir el repositorio no
        # abre conexiones.
        if self._engine is None:
            self._engine = create_async_engine(self._cadena_conexion)
        return self._engine

    async def obtener_todos(self, limite: int) -> list[dict]:
        sql = text(
            f"SELECT {self.COLUMNAS} FROM area_conocimiento "
            "WHERE activo = TRUE ORDER BY id LIMIT :limite"
        )
        async with self._obtener_engine().connect() as conexion:
            resultado = await conexion.execute(sql, {"limite": limite})
            return [dict(fila._mapping) for fila in resultado]

    async def obtener_por_id(self, id_area: str) -> dict | None:
        # Una fila inactiva responde como inexistente.
        sql = text(
            f"SELECT {self.COLUMNAS} FROM area_conocimiento "
            "WHERE id = :id AND activo = TRUE"
        )
        async with self._obtener_engine().connect() as conexion:
            resultado = await conexion.execute(sql, {"id": id_area})
            fila = resultado.first()
            return dict(fila._mapping) if fila else None

    async def crear(self, datos: dict) -> bool:
        sql = text(
            "INSERT INTO area_conocimiento (id, gran_area, area, disciplina, activo) "
            "VALUES (:id, :gran_area, :area, :disciplina, TRUE)"
        )
        async with self._obtener_engine().begin() as conexion:
            resultado = await conexion.execute(sql, datos)
            return resultado.rowcount == 1

    async def actualizar(self, id_area: str, datos: dict) -> int:
        # El PATCH escribe solo lo que llegó, así que la consulta se compone.
        # OJO: lo que se compone son NOMBRES DE COLUMNA de una lista cerrada
        # —las llaves del diccionario vienen de un modelo Pydantic, no del
        # usuario—; los VALORES siempre viajan como :parametro.
        asignaciones = ", ".join(f"{columna} = :{columna}" for columna in datos)
        sql = text(
            f"UPDATE area_conocimiento SET {asignaciones} "
            "WHERE id = :pk_id AND activo = TRUE"
        )
        async with self._obtener_engine().begin() as conexion:
            resultado = await conexion.execute(sql, {**datos, "pk_id": id_area})
            return resultado.rowcount

    async def eliminar_logico(self, id_area: str) -> int:
        # Borrado LÓGICO en una sola consulta: cero filas afectadas significa
        # "no existe o ya estaba inactiva", que es el 404 del contrato.
        sql = text(
            "UPDATE area_conocimiento SET activo = FALSE "
            "WHERE id = :id AND activo = TRUE"
        )
        async with self._obtener_engine().begin() as conexion:
            resultado = await conexion.execute(sql, {"id": id_area})
            return resultado.rowcount
