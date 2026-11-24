"""El controlador expresa la identidad compuesta en la ruta y delega la persistencia."""

from controllers.controlador_relacion import crear_controlador_relacion
from models.aa_linea import AaLineaCrear
from servicios.abstracciones.i_servicio_aa_linea import IServicioAaLinea
from servicios.ensamblador import crear_servicio_aa_linea


def _ensamblar() -> IServicioAaLinea:
    return crear_servicio_aa_linea()


router = crear_controlador_relacion(
    "aa_linea", "Relación área de aplicación-línea",
    "area_aplicacion", "linea_investigacion", int, int,
    {"area_aplicacion": "areaAplicacion", "linea_investigacion": "lineaInvestigacion"},
    AaLineaCrear, _ensamblar,
)
