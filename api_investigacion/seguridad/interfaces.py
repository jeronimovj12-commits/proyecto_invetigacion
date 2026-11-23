# Ejecuta la instruccion indicada dentro del flujo actual.
"""Puertos de seguridad; no dependen de HTTP ni PostgreSQL."""
# Importa Protocol desde typing para usar esas definiciones.
from typing import Protocol


# Define la clase IClaves y agrupa su estado y operaciones.
class IClaves(Protocol):
    # Define la funcion crear con los parametros declarados; su bloque realiza esta operacion.
    def crear(self, clave: str) -> str: ...
    # Define la funcion verificar con los parametros declarados; su bloque realiza esta operacion.
    def verificar(self, clave: str, resumen: str) -> bool: ...


# Define la clase ITokens y agrupa su estado y operaciones.
class ITokens(Protocol):
    # Asigna a segundos el valor calculado a la derecha.
    segundos: int
    # Define la funcion emitir con los parametros declarados; su bloque realiza esta operacion.
    def emitir(self, usuario_id: int, version: int) -> str: ...
    # Define la funcion validar con los parametros declarados; su bloque realiza esta operacion.
    def validar(self, token: str) -> dict: ...
