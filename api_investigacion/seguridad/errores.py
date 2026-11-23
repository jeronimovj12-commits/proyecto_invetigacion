# Ejecuta la instruccion indicada dentro del flujo actual.
"""Define errores de autenticacion y permisos que las capas superiores traducen a HTTP."""
# Define la clase AutenticacionFallida y agrupa su estado y operaciones.
class AutenticacionFallida(Exception):
    # Ejecuta la instruccion indicada dentro del flujo actual.
    """Credenciales o token sin identidad vigente."""


# Define la clase PermisoInsuficiente y agrupa su estado y operaciones.
class PermisoInsuficiente(Exception):
    # Ejecuta la instruccion indicada dentro del flujo actual.
    """Identidad válida sin permiso concedido."""


# Define la clase ConflictoInicializacion y agrupa su estado y operaciones.
class ConflictoInicializacion(Exception):
    # Ejecuta la instruccion indicada dentro del flujo actual.
    """El comando inicial no puede sobrescribir datos previos."""
