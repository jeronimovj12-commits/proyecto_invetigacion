from functools import lru_cache
import os
from servicios.abstracciones.i_servicio_seguridad import IServicioSeguridad
from servicios.servicio_seguridad import ServicioSeguridad
from repositorios.repositorio_seguridad_postgresql import RepositorioSeguridadPostgreSQL
from seguridad.adaptadores import ClavesArgon2

@lru_cache
def crear_servicio_seguridad() -> IServicioSeguridad:
    return ServicioSeguridad(RepositorioSeguridadPostgreSQL(os.environ['DB_POSTGRES']), ClavesArgon2())
