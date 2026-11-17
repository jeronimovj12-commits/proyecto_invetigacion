"""
Contrato del repositorio. El servicio depende de ESTA interfaz, nunca de una
clase concreta: por eso se le puede enchufar un repositorio de mentiras y
probarlo sin base de datos (inversión de dependencias).
"""

# Importa Protocol, AsyncContextManager desde typing para usar esas definiciones.
from typing import Protocol, AsyncContextManager


# Define la clase IRepositorioAreaConocimiento y agrupa su estado y operaciones.
class IRepositorioAreaConocimiento(Protocol):
    # Ejecuta la instruccion indicada dentro del flujo actual.
    """Las operaciones de datos de area_conocimiento."""

    # Define la funcion obtener_todos con los parametros declarados; su bloque realiza esta operacion.
    async def obtener_todos(self, limite: int) -> list[dict]:
        # Ejecuta la instruccion indicada dentro del flujo actual.
        """Hasta `limite` filas ACTIVAS, ordenadas por id."""
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        ...

    # Define la funcion obtener_por_id con los parametros declarados; su bloque realiza esta operacion.
    async def obtener_por_id(self, id_area: str) -> dict | None:
        # Ejecuta la instruccion indicada dentro del flujo actual.
        """La fila con ese id si está activa, o None."""
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        ...

    # Define la funcion crear con los parametros declarados; su bloque realiza esta operacion.
    async def crear(self, datos: dict) -> bool:
        # Ejecuta la instruccion indicada dentro del flujo actual.
        """Inserta. Devuelve True si quedó insertada."""
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        ...

    # Define la funcion actualizar con los parametros declarados; su bloque realiza esta operacion.
    async def actualizar(self, id_area: str, datos: dict) -> int:
        # Ejecuta la instruccion indicada dentro del flujo actual.
        """Escribe los campos de `datos`. Devuelve filas afectadas."""
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        ...

    # Define la funcion eliminar_logico con los parametros declarados; su bloque realiza esta operacion.
    async def eliminar_logico(self, id_area: str) -> int:
        """Marca activo = FALSE. Devuelve filas afectadas (0 = no existía
        o ya estaba inactiva)."""
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        ...

    # Define la funcion transaccion con los parametros declarados; su bloque realiza esta operacion.
    def transaccion(self) -> AsyncContextManager[None]: ...

    # Define la funcion tiene_dependientes con los parametros declarados; su bloque realiza esta operacion.
    async def tiene_dependientes(self, id_area: str) -> bool: ...
