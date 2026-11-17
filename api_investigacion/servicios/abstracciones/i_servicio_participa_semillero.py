# Ejecuta la instruccion indicada dentro del flujo actual.
"""Contrato de servicio: define las operaciones que debe ofrecer la capa de negocio."""
# Importa Protocol desde typing para usar esas definiciones.
from typing import Protocol


# Define la clase IServicioParticipaSemillero y agrupa su estado y operaciones.
class IServicioParticipaSemillero(Protocol):
    # Define la funcion listar con los parametros declarados; su bloque realiza esta operacion.
    async def listar(self, limite: int) -> list[dict]: ...
    # Define la funcion obtener con los parametros declarados; su bloque realiza esta operacion.
    async def obtener(self, identidad: dict) -> dict: ...
    # Define la funcion crear con los parametros declarados; su bloque realiza esta operacion.
    async def crear(self, datos: dict) -> None: ...
    # Define la funcion actualizar con los parametros declarados; su bloque realiza esta operacion.
    async def actualizar(self, identidad: dict, datos: dict) -> int: ...
    # Define la funcion eliminar con los parametros declarados; su bloque realiza esta operacion.
    async def eliminar(self, identidad: dict) -> int: ...
