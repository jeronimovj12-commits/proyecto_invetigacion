"""Una transacción por operación de negocio, aislada por tarea asíncrona.

La lectura de referencias y la escritura deben compartir transacción para
que una desactivación concurrente no deje relaciones con padres inactivos.
PostgreSQL puede abortar una operación concurrente; nunca se confirma a medias.
"""
# Importa asynccontextmanager desde contextlib para usar esas definiciones.
from contextlib import asynccontextmanager
# Importa ContextVar desde contextvars para usar esas definiciones.
from contextvars import ContextVar

# Importa create_async_engine desde sqlalchemy.ext.asyncio para usar esas definiciones.
from sqlalchemy.ext.asyncio import create_async_engine


# Define la clase ConexionPostgreSQL y agrupa su estado y operaciones.
class ConexionPostgreSQL:
    # Define la funcion __init__ con los parametros declarados; su bloque realiza esta operacion.
    def __init__(self, cadena_conexion: str):
        # Guarda en self._cadena el valor necesario para reutilizarlo en otros metodos.
        self._cadena = cadena_conexion
        # Guarda en self._engine el valor necesario para reutilizarlo en otros metodos.
        self._engine = None
        # Guarda en self._actual el valor necesario para reutilizarlo en otros metodos.
        self._actual = ContextVar("conexion_actual", default=None)

    # Define la funcion _motor con los parametros declarados; su bloque realiza esta operacion.
    def _motor(self):
        # Ejecuta el bloque siguiente solo cuando se cumple: self._engine is None.
        if self._engine is None:
            # Guarda en self._engine el valor necesario para reutilizarlo en otros metodos.
            self._engine = create_async_engine(self._cadena, isolation_level="SERIALIZABLE")
        # Devuelve al llamador el resultado de la expresion indicada.
        return self._engine

    # Aplica @asynccontextmanager a la declaracion que sigue; en rutas, registra el endpoint HTTP.
    @asynccontextmanager
    # Define la funcion transaccion con los parametros declarados; su bloque realiza esta operacion.
    async def transaccion(self):
        # Ejecuta el bloque siguiente solo cuando se cumple: self._actual.get() is not None.
        if self._actual.get() is not None:
            # Entrega un valor al iterador y conserva el estado de la funcion.
            yield
            # Termina la funcion sin devolver un valor.
            return
        # Abre el recurso asincronico y asegura su cierre al salir del bloque.
        async with self._motor().begin() as conexion:
            # Asigna a token el valor calculado a la derecha.
            token = self._actual.set(conexion)
            # Inicia un bloque cuya excepcion se manejara en los except siguientes.
            try:
                # Entrega un valor al iterador y conserva el estado de la funcion.
                yield
            # Ejecuta este bloque al final, haya ocurrido o no una excepcion.
            finally:
                # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                self._actual.reset(token)

    # Aplica @asynccontextmanager a la declaracion que sigue; en rutas, registra el endpoint HTTP.
    @asynccontextmanager
    # Define la funcion _conexion con los parametros declarados; su bloque realiza esta operacion.
    async def _conexion(self):
        # Asigna a conexion el valor calculado a la derecha.
        conexion = self._actual.get()
        # Ejecuta el bloque siguiente solo cuando se cumple: conexion is not None.
        if conexion is not None:
            # Entrega un valor al iterador y conserva el estado de la funcion.
            yield conexion
        # Define el caso alternativo cuando las condiciones anteriores no se cumplen.
        else:
            # Abre el recurso asincronico y asegura su cierre al salir del bloque.
            async with self._motor().begin() as conexion:
                # Entrega un valor al iterador y conserva el estado de la funcion.
                yield conexion
