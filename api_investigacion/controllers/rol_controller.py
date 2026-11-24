"""El adaptador reutiliza CRUD común y limita todas sus operaciones a ADMIN."""

from controllers.crud_controlador import crear_controlador
from models.rol import RolActualizar, RolCrear, RolReemplazo
from servicios.abstracciones.i_servicio_rol import IServicioRol
from servicios.ensamblador import crear_servicio_rol


def _ensamblar() -> IServicioRol:
    return crear_servicio_rol()


router = crear_controlador(
    "rol", "Rol",
    {"id": "id", "nombre": "nombre", "descripcion": "descripcion", "fecha_creacion": "fechaCreacion"},
    int, RolCrear, RolReemplazo, RolActualizar, _ensamblar,
    roles_lectura=("ADMIN",), roles_escritura=("ADMIN",),
)
