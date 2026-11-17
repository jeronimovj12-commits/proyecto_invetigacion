# Ejecuta la instruccion indicada dentro del flujo actual.
"""Ensamblador de seguridad: construye el servicio con sus dependencias concretas."""
# Importa lru_cache desde functools para usar esas definiciones.
from functools import lru_cache
# Carga el modulo o los modulos os.
import os
# Importa IServicioSeguridad desde servicios.abstracciones.i_servicio_seguridad para usar esas definiciones.
from servicios.abstracciones.i_servicio_seguridad import IServicioSeguridad
# Importa ServicioSeguridad desde servicios.servicio_seguridad para usar esas definiciones.
from servicios.servicio_seguridad import ServicioSeguridad
# Importa RepositorioSeguridadPostgreSQL desde repositorios.repositorio_seguridad_postgresql para usar esas definiciones.
from repositorios.repositorio_seguridad_postgresql import RepositorioSeguridadPostgreSQL
# Importa ClavesArgon2 desde seguridad.adaptadores para usar esas definiciones.
from seguridad.adaptadores import ClavesArgon2

# Aplica @lru_cache a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@lru_cache
# Define la funcion crear_servicio_seguridad con los parametros declarados; su bloque realiza esta operacion.
def crear_servicio_seguridad() -> IServicioSeguridad:
    # Devuelve al llamador el resultado de la expresion indicada.
    return ServicioSeguridad(RepositorioSeguridadPostgreSQL(os.environ['DB_POSTGRES']), ClavesArgon2())
