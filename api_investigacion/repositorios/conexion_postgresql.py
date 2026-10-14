"""Una transacción por operación de negocio, aislada por tarea asíncrona.

La lectura de referencias y la escritura deben compartir transacción para
que una desactivación concurrente no deje relaciones con padres inactivos.
PostgreSQL puede abortar una operación concurrente; nunca se confirma a medias.
"""
from contextlib import asynccontextmanager
from contextvars import ContextVar

from sqlalchemy.ext.asyncio import create_async_engine


class ConexionPostgreSQL:
    def __init__(self, cadena_conexion: str):
        self._cadena = cadena_conexion
        self._engine = None
        self._actual = ContextVar("conexion_actual", default=None)

    def _motor(self):
        if self._engine is None:
            self._engine = create_async_engine(self._cadena, isolation_level="SERIALIZABLE")
        return self._engine

    @asynccontextmanager
    async def transaccion(self):
        if self._actual.get() is not None:
            yield
            return
        async with self._motor().begin() as conexion:
            token = self._actual.set(conexion)
            try:
                yield
            finally:
                self._actual.reset(token)

    @asynccontextmanager
    async def _conexion(self):
        conexion = self._actual.get()
        if conexion is not None:
            yield conexion
        else:
            async with self._motor().begin() as conexion:
                yield conexion
