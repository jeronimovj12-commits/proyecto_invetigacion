# Ejecuta la instruccion indicada dentro del flujo actual.
"""Define los errores de conflicto y ausencia para la administracion de seguridad."""
# Define la clase ConflictoSeguridad y agrupa su estado y operaciones.
class ConflictoSeguridad(Exception):
    # Deja el bloque intencionalmente vacio sin ejecutar una operacion.
    pass

# Define la clase SeguridadNoEncontrada y agrupa su estado y operaciones.
class SeguridadNoEncontrada(Exception):
    # Deja el bloque intencionalmente vacio sin ejecutar una operacion.
    pass
