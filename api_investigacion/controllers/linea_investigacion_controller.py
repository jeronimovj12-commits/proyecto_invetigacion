"""Router específico de líneas; separarlo permite exponer su creación con clave generada."""

from controllers.crud_controlador import crear_controlador
from models.linea_investigacion import LineaInvestigacionActualizar, LineaInvestigacionCrear, LineaInvestigacionReemplazo
from servicios.abstracciones.i_servicio_linea_investigacion import IServicioLineaInvestigacion
from servicios.ensamblador import crear_servicio_linea_investigacion


def _ensamblar_lineas() -> IServicioLineaInvestigacion:
    return crear_servicio_linea_investigacion()


router = crear_controlador(
    "linea_investigacion", "Línea de investigación",
    {"id": "id", "nombre": "nombre", "descripcion": "descripcion"},
    int, LineaInvestigacionCrear, LineaInvestigacionReemplazo, LineaInvestigacionActualizar,
    _ensamblar_lineas,
)
