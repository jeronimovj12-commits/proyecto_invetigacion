"""El controlador concreta rutas de ODS-línea sin filtrar SQL ni detalles del motor."""

from controllers.controlador_relacion import crear_controlador_relacion
from models.ods_linea import OdsLineaCrear
from servicios.abstracciones.i_servicio_ods_linea import IServicioOdsLinea
from servicios.ensamblador import crear_servicio_ods_linea


def _ensamblar() -> IServicioOdsLinea:
    return crear_servicio_ods_linea()


router = crear_controlador_relacion(
    "ods_linea", "Relación ODS-línea",
    "linea_investigacion", "ods", int, int,
    {"linea_investigacion": "lineaInvestigacion", "ods": "ods"},
    OdsLineaCrear, _ensamblar,
)
