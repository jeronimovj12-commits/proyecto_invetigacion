"""Router dedicado a docente; el parámetro público conserva el nombre de su clave primaria."""

from controllers.crud_controlador import crear_controlador
from models.docente import DocenteActualizar, DocenteCrear, DocenteReemplazo
from servicios.abstracciones.i_servicio_docente import IServicioDocente
from servicios.ensamblador import crear_servicio_docente


def _ensamblar_docentes() -> IServicioDocente:
    return crear_servicio_docente()


router = crear_controlador(
    "docente", "Docente",
    {
        "cedula": "cedula", "nombres": "nombres", "apellidos": "apellidos",
        "genero": "genero", "cargo": "cargo", "fecha_nacimiento": "fechaNacimiento",
        "correo": "correo", "telefono": "telefono", "url_cvlac": "urlCvlac",
        "fecha_actualizacion": "fechaActualizacion", "escalafon": "escalafon",
        "perfil": "perfil", "cat_minciencia": "catMinciencia",
        "conv_minciencia": "convMinciencia", "nacionalidaad": "nacionalidad",
        "linea_investigacion_principal": "lineaInvestigacionPrincipal",
    },
    int, DocenteCrear, DocenteReemplazo, DocenteActualizar, _ensamblar_docentes,
    nombre_parametro="cedula",
)
