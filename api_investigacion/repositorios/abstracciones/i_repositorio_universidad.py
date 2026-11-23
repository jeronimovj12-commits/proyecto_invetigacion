# Ejecuta la instruccion indicada dentro del flujo actual.
"""Contrato de repositorio: define las operaciones de almacenamiento requeridas por los servicios."""
# Importa Protocol desde typing para usar esas definiciones.
from typing import Protocol


# Define la clase IRepositorioUniversidad y agrupa su estado y operaciones.
class IRepositorioUniversidad(Protocol):
    # Define la funcion obtener_todos con los parametros declarados; su bloque realiza esta operacion.
    async def obtener_todos(self, limite: int) -> list[dict]: ...
    # Define la funcion obtener_por_id con los parametros declarados; su bloque realiza esta operacion.
    async def obtener_por_id(self, identidad: dict) -> dict | None: ...
