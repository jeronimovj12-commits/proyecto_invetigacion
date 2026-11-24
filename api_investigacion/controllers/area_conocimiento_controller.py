"""Router propio del catálogo de áreas; el nombre fijo conserva rutas REST explícitas."""

from controllers.crud_controlador import crear_controlador
from models.area_conocimiento import AreaConocimientoActualizar, AreaConocimientoCrear, AreaConocimientoReemplazo
from servicios.abstracciones.i_servicio_area_conocimiento import IServicioAreaConocimiento
from servicios.ensamblador import crear_servicio_area_conocimiento


def _ensamblar_area() -> IServicioAreaConocimiento:
    return crear_servicio_area_conocimiento()


router = crear_controlador(
    "area_conocimiento", "Área de conocimiento",
    {"id": "id", "gran_area": "granArea", "area": "area", "disciplina": "disciplina"},
    str, AreaConocimientoCrear, AreaConocimientoReemplazo, AreaConocimientoActualizar,
    _ensamblar_area,
)
