"""El controlador solo conecta el contrato HTTP con el servicio de grupo-línea."""

from controllers.controlador_relacion import crear_controlador_relacion
from models.grupo_linea import GrupoLineaCrear
from servicios.abstracciones.i_servicio_grupo_linea import IServicioGrupoLinea
from servicios.ensamblador import crear_servicio_grupo_linea


def _ensamblar() -> IServicioGrupoLinea:
    return crear_servicio_grupo_linea()


router = crear_controlador_relacion(
    "grupo_linea", "Relación grupo-línea",
    "grupo_investigacion", "linea_investigacion", int, int,
    {"grupo_investigacion": "grupoInvestigacion", "linea_investigacion": "lineaInvestigacion"},
    GrupoLineaCrear, _ensamblar,
)
