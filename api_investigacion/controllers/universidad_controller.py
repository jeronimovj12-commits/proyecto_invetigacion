"""Router específico de universidades; el tipo de la clave se fija al declarar el recurso."""

from controllers.crud_controlador import crear_controlador
from models.universidad import UniversidadActualizar, UniversidadCrear, UniversidadReemplazo
from servicios.abstracciones.i_servicio_universidad import IServicioUniversidad
from servicios.ensamblador import crear_servicio_universidad


def _ensamblar_universidades() -> IServicioUniversidad:
    return crear_servicio_universidad()


router = crear_controlador(
    "universidad", "Universidad",
    {"id": "id", "nombre": "nombre", "tipo": "tipo", "ciudad": "ciudad"},
    int, UniversidadCrear, UniversidadReemplazo, UniversidadActualizar,
    _ensamblar_universidades,
)
