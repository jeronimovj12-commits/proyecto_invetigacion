# Ejecuta la instruccion indicada dentro del flujo actual.
"""Contrato de servicio: define las operaciones que debe ofrecer la capa de negocio."""
# Importa Protocol desde typing para usar esas definiciones.
from typing import Protocol


# Define la clase IServicioAutenticacion y agrupa su estado y operaciones.
class IServicioAutenticacion(Protocol):
    # Define la funcion login con los parametros declarados; su bloque realiza esta operacion.
    async def login(self, nombre: str, clave: str) -> dict: ...
    # Define la funcion sesion con los parametros declarados; su bloque realiza esta operacion.
    async def sesion(self, token: str) -> dict: ...
    # Define la funcion logout con los parametros declarados; su bloque realiza esta operacion.
    async def logout(self, token: str) -> None: ...
    # Define la funcion crear_primero con los parametros declarados; su bloque realiza esta operacion.
    async def crear_primero(self, nombre: str, correo: str, clave: str) -> None: ...
