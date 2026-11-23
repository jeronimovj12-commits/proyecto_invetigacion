"""
Contrato del repositorio. El servicio depende de ESTA interfaz, nunca de una
clase concreta: por eso se le puede enchufar un repositorio de mentiras y
probarlo sin base de datos (inversión de dependencias).
"""

from typing import Protocol


class IRepositorioAreaConocimiento(Protocol):
    """Las operaciones de datos de area_conocimiento."""

    async def obtener_todos(self, limite: int) -> list[dict]:
        """Hasta `limite` filas ACTIVAS, ordenadas por id."""
        ...

    async def obtener_por_id(self, id_area: str) -> dict | None:
        """La fila con ese id si está activa, o None."""
        ...

    async def crear(self, datos: dict) -> bool:
        """Inserta. Devuelve True si quedó insertada."""
        ...

    async def actualizar(self, id_area: str, datos: dict) -> int:
        """Escribe los campos de `datos`. Devuelve filas afectadas."""
        ...

    async def eliminar_logico(self, id_area: str) -> int:
        """Marca activo = FALSE. Devuelve filas afectadas (0 = no existía
        o ya estaba inactiva)."""
        ...
