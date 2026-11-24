"""El hash se omite de GET y de errores SQL para que nunca salga del límite de persistencia."""

from controllers.crud_controlador import crear_controlador
from models.usuario import UsuarioActualizar, UsuarioCrear, UsuarioReemplazo
from servicios.abstracciones.i_servicio_usuario import IServicioUsuario
from servicios.ensamblador import crear_servicio_usuario


def _ensamblar() -> IServicioUsuario:
    return crear_servicio_usuario()


router = crear_controlador(
    "usuario", "Usuario",
    {
        "id": "id",
        "username": "username",
        "email": "email",
        "nombre_completo": "nombreCompleto",
        "fecha_creacion": "fechaCreacion",
        "fecha_actualizacion": "fechaActualizacion",
    },
    int, UsuarioCrear, UsuarioReemplazo, UsuarioActualizar, _ensamblar,
    roles_lectura=("ADMIN",), roles_escritura=("ADMIN",),
    ocultar_detalle_error=True,
)
