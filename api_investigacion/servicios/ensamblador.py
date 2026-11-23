"""
ensamblador.py — El ÚNICO punto del sistema que decide qué motor se usa.

Los controladores llaman a `crear_servicio_area_conocimiento()` y reciben algo
que cumple la interfaz del servicio. No saben —ni tienen por qué saber— qué
repositorio hay detrás.

Hoy hay un solo motor. El día que entre un segundo, este archivo es el único
que cambia: esa es toda la gracia de tener la construcción en un solo sitio.
"""

import os

from repositorios.repositorio_area_conocimiento_postgresql import (
    RepositorioAreaConocimientoPostgreSQL,
)
from servicios.abstracciones.i_servicio_area_conocimiento import (
    IServicioAreaConocimiento,
)
from servicios.servicio_area_conocimiento import ServicioAreaConocimiento


_servicio_area_conocimiento: IServicioAreaConocimiento | None = None


def _cadena_conexion() -> str:
    cadena = os.environ.get("DB_POSTGRES")
    if not cadena:
        raise RuntimeError(
            "Falta la variable de entorno DB_POSTGRES con la cadena de conexión.")
    return cadena


def crear_servicio_area_conocimiento() -> IServicioAreaConocimiento:
    """Entrega una instancia compartida para reutilizar el pool de conexiones."""
    global _servicio_area_conocimiento
    if _servicio_area_conocimiento is None:
        _servicio_area_conocimiento = ServicioAreaConocimiento(
            RepositorioAreaConocimientoPostgreSQL(_cadena_conexion()))
    return _servicio_area_conocimiento
