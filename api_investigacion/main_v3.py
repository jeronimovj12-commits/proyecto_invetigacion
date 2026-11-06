"""Arranque explícito de la entrega parcial v3. main:app sigue siendo v2."""
from main import app
from controllers.autenticacion_controller import router
from servicios.ensamblador_autenticacion import crear_servicio_autenticacion

# Validar configuración antes de aceptar solicitudes; sin secreto no hay arranque v3.
crear_servicio_autenticacion()
app.title = 'API Investigación — v3 parcial'
app.version = 'v3-parcial'
app.description = 'Login/sesión/logout disponibles. Las rutas de dominio aún NO están protegidas.'
app.include_router(router)
