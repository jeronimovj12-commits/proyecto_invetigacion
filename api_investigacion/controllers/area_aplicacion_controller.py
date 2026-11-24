"""Router específico de áreas de aplicación con rutas estáticas del contrato."""

from controllers.crud_controlador import crear_controlador
from models.area_aplicacion import AreaAplicacionActualizar, AreaAplicacionCrear, AreaAplicacionReemplazo
from servicios.abstracciones.i_servicio_area_aplicacion import IServicioAreaAplicacion
from servicios.ensamblador import crear_servicio_area_aplicacion


def _ensamblar_areas() -> IServicioAreaAplicacion:
    return crear_servicio_area_aplicacion()


router = crear_controlador(
    "area_aplicacion", "Área de aplicación",
    {"id": "id", "nombre": "nombre"},
    int, AreaAplicacionCrear, AreaAplicacionReemplazo, AreaAplicacionActualizar,
    _ensamblar_areas,
)
