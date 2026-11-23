"""
Contrato del servicio. El controlador depende de esta interfaz y traduce sus
excepciones: ValueError → 400 · LookupError → 404.
"""

# Importa Protocol desde typing para usar esas definiciones.
from typing import Protocol


# Define la clase IServicioAreaConocimiento y agrupa su estado y operaciones.
class IServicioAreaConocimiento(Protocol):
    # Ejecuta la instruccion indicada dentro del flujo actual.
    """Las operaciones de negocio sobre area_conocimiento."""

    # Define la funcion listar con los parametros declarados; su bloque realiza esta operacion.
    async def listar(self, limite: int) -> list[dict]:
        # Ejecuta la instruccion indicada dentro del flujo actual.
        """Hasta `limite` filas activas. ValueError si limite <= 0."""
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        ...

    # Define la funcion obtener con los parametros declarados; su bloque realiza esta operacion.
    async def obtener(self, id_area: str) -> dict:
        # Ejecuta la instruccion indicada dentro del flujo actual.
        """La fila con ese id. LookupError si no existe o está inactiva."""
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        ...

    # Define la funcion crear con los parametros declarados; su bloque realiza esta operacion.
    async def crear(self, datos: dict) -> None:
        # Ejecuta la instruccion indicada dentro del flujo actual.
        """Crea (los datos ya vienen validados por Pydantic)."""
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        ...

    # Define la funcion actualizar con los parametros declarados; su bloque realiza esta operacion.
    async def actualizar(self, id_area: str, datos: dict) -> int:
        """Escribe los campos enviados. ValueError si no llegó ninguno ·
        LookupError si no existe · devuelve filas afectadas."""
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        ...

    # Define la funcion eliminar con los parametros declarados; su bloque realiza esta operacion.
    async def eliminar(self, id_area: str) -> int:
        # Ejecuta la instruccion indicada dentro del flujo actual.
        """Borrado LÓGICO. LookupError si no existe o ya estaba inactiva."""
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        ...
