"""Rutas de participación en grupos exponen ambos componentes de clave para no ocultar su identidad."""

from controllers.controlador_compuesto import crear_controlador_compuesto
from models.participa_grupo import ParticipaGrupoActualizar, ParticipaGrupoCrear, ParticipaGrupoReemplazo
from servicios.abstracciones.i_servicio_participa_grupo import IServicioParticipaGrupo
from servicios.ensamblador import crear_servicio_participa_grupo


def _ensamblar_participaciones() -> IServicioParticipaGrupo:
    return crear_servicio_participa_grupo()


router = crear_controlador_compuesto(
    "participa_grupo", "Participación en grupo",
    "docente_cedula", "grupo_investigacion_id",
    {
        "docente_cedula": "docenteCedula",
        "grupo_investigacion_id": "grupoInvestigacionId",
        "rol": "rol", "fecha_inicio": "fechaInicio", "fecha_fin": "fechaFin",
    },
    ParticipaGrupoCrear, ParticipaGrupoReemplazo, ParticipaGrupoActualizar,
    _ensamblar_participaciones,
)
