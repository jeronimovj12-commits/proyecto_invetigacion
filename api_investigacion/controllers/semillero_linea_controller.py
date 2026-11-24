"""El servicio mantiene la lógica fuera de este adaptador específico de rutas."""

from controllers.controlador_relacion import crear_controlador_relacion
from models.semillero_linea import SemilleroLineaCrear
from servicios.abstracciones.i_servicio_semillero_linea import IServicioSemilleroLinea
from servicios.ensamblador import crear_servicio_semillero_linea


def _ensamblar() -> IServicioSemilleroLinea:
    return crear_servicio_semillero_linea()


router = crear_controlador_relacion(
    "semillero_linea", "Relación semillero-línea",
    "semillero", "linea_investigacion", int, int,
    {"semillero": "semillero", "linea_investigacion": "lineaInvestigacion"},
    SemilleroLineaCrear, _ensamblar,
)
