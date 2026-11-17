# Ejecuta la instruccion indicada dentro del flujo actual.
"""Contrato de repositorio: define las operaciones de almacenamiento requeridas por los servicios."""
# Importa Protocol desde typing para usar esas definiciones.
from typing import Protocol

# Define la clase IRepositorioSeguridad y agrupa su estado y operaciones.
class IRepositorioSeguridad(Protocol):
    # Define la funcion listar con los parametros declarados; su bloque realiza esta operacion.
    async def listar(self, recurso: str, claves: dict, limite: int) -> list[dict]: ...
    # Define la funcion guardar con los parametros declarados; su bloque realiza esta operacion.
    async def guardar(self, recurso: str, claves: dict, datos: dict, crear: bool) -> dict: ...
    # Define la funcion retirar con los parametros declarados; su bloque realiza esta operacion.
    async def retirar(self, recurso: str, claves: dict) -> None: ...
