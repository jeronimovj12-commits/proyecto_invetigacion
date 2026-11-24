"""Router de grupos de investigación; traduce universidad pública a la columna SQL heredada."""

from controllers.crud_controlador import crear_controlador
from models.grupo_investigacion import GrupoInvestigacionActualizar, GrupoInvestigacionCrear, GrupoInvestigacionReemplazo
from servicios.abstracciones.i_servicio_grupo_investigacion import IServicioGrupoInvestigacion
from servicios.ensamblador import crear_servicio_grupo_investigacion


def _ensamblar_grupos() -> IServicioGrupoInvestigacion:
    return crear_servicio_grupo_investigacion()


router = crear_controlador(
    "grupo_investigacion", "Grupo de investigación",
    {
        "id": "id", "nombre": "nombre", "url_gruplac": "urlGruplac",
        "categoria": "categoria", "convocatoria": "convocatoria",
        "fecha_fundacion": "fechaFundacion", "universidsad": "universidad",
        "interno": "interno", "ambito": "ambito",
    },
    int, GrupoInvestigacionCrear, GrupoInvestigacionReemplazo,
    GrupoInvestigacionActualizar, _ensamblar_grupos,
)
