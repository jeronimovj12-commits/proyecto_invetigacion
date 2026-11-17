# Ejecuta la instruccion indicada dentro del flujo actual.
"""Define excepciones para sesion terminada y acceso denegado en el front Flask."""
# Define la clase SesionTerminada y agrupa su estado y operaciones.
class SesionTerminada(Exception):
    # Deja el bloque intencionalmente vacio sin ejecutar una operacion.
    pass

# Define la clase AccesoDenegado y agrupa su estado y operaciones.
class AccesoDenegado(Exception):
    # Deja el bloque intencionalmente vacio sin ejecutar una operacion.
    pass
