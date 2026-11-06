"""Único punto que construye adaptadores concretos de esta entrega v3."""
import os
from functools import lru_cache

from repositorios.repositorio_autenticacion_postgresql import RepositorioAutenticacionPostgreSQL
from seguridad.adaptadores import ClavesArgon2, ConfiguracionSeguridad, TokensJWT
from servicios.abstracciones.i_servicio_autenticacion import IServicioAutenticacion
from servicios.servicio_autenticacion import ServicioAutenticacion


@lru_cache
def crear_servicio_autenticacion() -> IServicioAutenticacion:
    cadena = os.environ.get('DB_POSTGRES')
    if not cadena:
        raise RuntimeError('Falta DB_POSTGRES en el entorno.')
    configuracion = ConfiguracionSeguridad.desde_entorno()
    return ServicioAutenticacion(RepositorioAutenticacionPostgreSQL(cadena),
                                ClavesArgon2(), TokensJWT(configuracion))
