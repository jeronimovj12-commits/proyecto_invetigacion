"""Rutas de participación en semilleros mantienen visibles las dos claves foráneas del vínculo."""

from controllers.controlador_compuesto import crear_controlador_compuesto
from models.participa_semillero import ParticipaSemilleroActualizar, ParticipaSemilleroCrear, ParticipaSemilleroReemplazo
from servicios.abstracciones.i_servicio_participa_semillero import IServicioParticipaSemillero
from servicios.ensamblador import crear_servicio_participa_semillero


def _ensamblar_participaciones() -> IServicioParticipaSemillero:
    return crear_servicio_participa_semillero()


router = crear_controlador_compuesto(
    "participa_semillero", "Participación en semillero",
    "docente", "semillero",
    {
        "docente": "docente", "semillero": "semillero", "rol": "rol",
        "fecha_inicio": "fechaInicio", "fecha_fin": "fechaFin",
    },
    ParticipaSemilleroCrear, ParticipaSemilleroReemplazo,
    ParticipaSemilleroActualizar, _ensamblar_participaciones,
)
