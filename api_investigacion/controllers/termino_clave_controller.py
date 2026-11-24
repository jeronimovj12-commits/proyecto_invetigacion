"""Router específico de términos; mantiene su clave natural de texto y alias de salida."""

from controllers.crud_controlador import crear_controlador
from models.termino_clave import TerminoClaveActualizar, TerminoClaveCrear, TerminoClaveReemplazo
from servicios.abstracciones.i_servicio_termino_clave import IServicioTerminoClave
from servicios.ensamblador import crear_servicio_termino_clave


def _ensamblar_terminos() -> IServicioTerminoClave:
    return crear_servicio_termino_clave()


router = crear_controlador(
    "termino_clave", "Término clave",
    {"termino": "termino", "termino_ingles": "terminoIngles"},
    str, TerminoClaveCrear, TerminoClaveReemplazo, TerminoClaveActualizar,
    _ensamblar_terminos,
)
