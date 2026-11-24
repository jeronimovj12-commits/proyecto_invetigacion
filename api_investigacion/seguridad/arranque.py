"""El arranque llama al servicio para sembrar cuentas sin acoplarse al motor SQL."""

from servicios.ensamblador import crear_servicio_usuario


ROLES_INICIALES = (
    {"nombre": "ADMIN", "descripcion": "Administración del sistema."},
    {"nombre": "INVESTIGADOR", "descripcion": "Consulta y edición de investigación."},
    {"nombre": "CONSULTOR", "descripcion": "Consulta de información."},
)

USUARIOS_INICIALES = (
    {
        "username": "admin",
        "password": "Admin123*",
        "email": "admin@umv.edu.co",
        "nombre_completo": "Administración UMV",
        "rol": "ADMIN",
    },
    {
        "username": "juanjoherrera",
        "password": "Invest123*",
        "email": "juanjo@umv.edu.co",
        "nombre_completo": "Juanjo Herrera",
        "rol": "INVESTIGADOR",
    },
    {
        "username": "consultor",
        "password": "Consult123*",
        "email": "consultor@umv.edu.co",
        "nombre_completo": "Consultor UMV",
        "rol": "CONSULTOR",
    },
)


async def sembrar_datos_iniciales() -> None:
    await crear_servicio_usuario().sembrar_datos_iniciales(
        list(ROLES_INICIALES), list(USUARIOS_INICIALES)
    )
