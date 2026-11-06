class AutenticacionFallida(Exception):
    """Credenciales o token sin identidad vigente."""


class PermisoInsuficiente(Exception):
    """Identidad válida sin permiso concedido."""


class ConflictoInicializacion(Exception):
    """El comando inicial no puede sobrescribir datos previos."""
