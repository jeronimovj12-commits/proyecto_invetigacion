"""
Contrato del servicio. El controlador depende de esta interfaz y traduce sus
excepciones: ValueError → 400 · LookupError → 404.
"""

from typing import Protocol


class IServicioAreaConocimiento(Protocol):
    """Las operaciones de negocio sobre area_conocimiento."""

    async def listar(self, limite: int) -> list[dict]:
        """Hasta `limite` filas activas. ValueError si limite <= 0."""
        ...

    async def obtener(self, id_area: str) -> dict:
        """La fila con ese id. LookupError si no existe o está inactiva."""
        ...

    async def crear(self, datos: dict) -> None:
        """Crea (los datos ya vienen validados por Pydantic)."""
        ...

    async def actualizar(self, id_area: str, datos: dict) -> int:
        """Escribe los campos enviados. ValueError si no llegó ninguno ·
        LookupError si no existe · devuelve filas afectadas."""
        ...

    async def eliminar(self, id_area: str) -> int:
        """Borrado LÓGICO. LookupError si no existe o ya estaba inactiva."""
        ...
