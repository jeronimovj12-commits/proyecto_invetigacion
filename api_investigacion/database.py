"""Conexión compartida; la URL viene del entorno para no acoplar credenciales al código."""

import os

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

_engine: AsyncEngine | None = None


def obtener_engine() -> AsyncEngine:
    # La conexión se crea al primer uso para que las pruebas de servicios no dependan del motor.
    global _engine
    if _engine is None:
        url = os.environ.get("DATABASE_URL")
        if not url:
            raise RuntimeError("La variable de entorno DATABASE_URL es obligatoria.")
        _engine = create_async_engine(url, pool_pre_ping=True)
    return _engine
