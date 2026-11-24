"""Router específico de ODS para que el contrato sea visible sin rutas por nombre variable."""

from controllers.crud_controlador import crear_controlador
from models.objetivo_desarrollo_sostenible import ObjetivoDesarrolloSostenibleActualizar, ObjetivoDesarrolloSostenibleCrear, ObjetivoDesarrolloSostenibleReemplazo
from servicios.abstracciones.i_servicio_objetivo_desarrollo_sostenible import IServicioObjetivoDesarrolloSostenible
from servicios.ensamblador import crear_servicio_objetivo_desarrollo_sostenible


def _ensamblar_objetivos() -> IServicioObjetivoDesarrolloSostenible:
    return crear_servicio_objetivo_desarrollo_sostenible()


router = crear_controlador(
    "objetivo_desarrollo_sostenible", "Objetivo de desarrollo sostenible",
    {"id": "id", "nombre": "nombre", "categoria": "categoria"},
    int, ObjetivoDesarrolloSostenibleCrear, ObjetivoDesarrolloSostenibleReemplazo,
    ObjetivoDesarrolloSostenibleActualizar, _ensamblar_objetivos,
)
