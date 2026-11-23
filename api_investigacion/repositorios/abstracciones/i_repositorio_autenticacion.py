# Ejecuta la instruccion indicada dentro del flujo actual.
"""Contrato de repositorio: define las operaciones de almacenamiento requeridas por los servicios."""
# Importa Protocol desde typing para usar esas definiciones.
from typing import Protocol


# Define la clase IRepositorioAutenticacion y agrupa su estado y operaciones.
class IRepositorioAutenticacion(Protocol):
    # Define la funcion por_nombre con los parametros declarados; su bloque realiza esta operacion.
    async def por_nombre(self, nombre: str) -> dict | None: ...
    # Define la funcion por_id con los parametros declarados; su bloque realiza esta operacion.
    async def por_id(self, usuario_id: int) -> dict | None: ...
    # Define la funcion revocar con los parametros declarados; su bloque realiza esta operacion.
    async def revocar(self, usuario_id: int, version: int) -> bool: ...
    # Define la funcion crear_primero con los parametros declarados; su bloque realiza esta operacion.
    async def crear_primero(self, nombre: str, correo: str, resumen: str) -> None: ...
