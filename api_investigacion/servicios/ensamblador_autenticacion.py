# Ejecuta la instruccion indicada dentro del flujo actual.
"""Único punto que construye adaptadores concretos de esta entrega v3."""
# Carga el modulo o los modulos os.
import os
# Importa lru_cache desde functools para usar esas definiciones.
from functools import lru_cache

# Importa RepositorioAutenticacionPostgreSQL desde repositorios.repositorio_autenticacion_postgresql para usar esas definiciones.
from repositorios.repositorio_autenticacion_postgresql import RepositorioAutenticacionPostgreSQL
# Importa ClavesArgon2, ConfiguracionSeguridad, TokensJWT desde seguridad.adaptadores para usar esas definiciones.
from seguridad.adaptadores import ClavesArgon2, ConfiguracionSeguridad, TokensJWT
# Importa IServicioAutenticacion desde servicios.abstracciones.i_servicio_autenticacion para usar esas definiciones.
from servicios.abstracciones.i_servicio_autenticacion import IServicioAutenticacion
# Importa ServicioAutenticacion desde servicios.servicio_autenticacion para usar esas definiciones.
from servicios.servicio_autenticacion import ServicioAutenticacion


# Aplica @lru_cache a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@lru_cache
# Define la funcion crear_servicio_autenticacion con los parametros declarados; su bloque realiza esta operacion.
def crear_servicio_autenticacion() -> IServicioAutenticacion:
    # Asigna a cadena el valor calculado a la derecha.
    cadena = os.environ.get('DB_POSTGRES')
    # Ejecuta el bloque siguiente solo cuando se cumple: not cadena.
    if not cadena:
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise RuntimeError('Falta DB_POSTGRES en el entorno.')
    # Asigna a configuracion el valor calculado a la derecha.
    configuracion = ConfiguracionSeguridad.desde_entorno()
    # Devuelve al llamador el resultado de la expresion indicada.
    return ServicioAutenticacion(RepositorioAutenticacionPostgreSQL(cadena),
                                # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                                ClavesArgon2(), TokensJWT(configuracion))
