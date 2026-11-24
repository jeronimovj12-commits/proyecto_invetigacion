"""Router de semilleros con operaciones explícitas y clave primaria simple."""

from controllers.crud_controlador import crear_controlador
from models.semillero import SemilleroActualizar, SemilleroCrear, SemilleroReemplazo
from servicios.abstracciones.i_servicio_semillero import IServicioSemillero
from servicios.ensamblador import crear_servicio_semillero


def _ensamblar_semilleros() -> IServicioSemillero:
    return crear_servicio_semillero()


router = crear_controlador(
    "semillero", "Semillero",
    {
        "id": "id", "nombre": "nombre", "fecha_fundacion": "fechaFundacion",
        "grupo_investigacion": "grupoInvestigacion",
    },
    int, SemilleroCrear, SemilleroReemplazo, SemilleroActualizar,
    _ensamblar_semilleros,
)
