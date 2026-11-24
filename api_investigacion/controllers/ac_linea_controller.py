"""El tipo de ruta textual conserva el identificador original del área de conocimiento."""

from controllers.controlador_relacion import crear_controlador_relacion
from models.ac_linea import AcLineaCrear
from servicios.abstracciones.i_servicio_ac_linea import IServicioAcLinea
from servicios.ensamblador import crear_servicio_ac_linea


def _ensamblar() -> IServicioAcLinea:
    return crear_servicio_ac_linea()


router = crear_controlador_relacion(
    "ac_linea", "Relación área de conocimiento-línea",
    "linea_investigacion", "area_conocimiento", int, str,
    {"linea_investigacion": "lineaInvestigacion", "area_conocimiento": "areaConocimiento"},
    AcLineaCrear, _ensamblar,
)
