"""Punto único de ensamblaje; las implementaciones concretas solo se eligen aquí."""

from repositorios.repositorio_area_aplicacion_postgresql import RepositorioAreaAplicacionPostgreSQL
from repositorios.repositorio_area_conocimiento_postgresql import RepositorioAreaConocimientoPostgreSQL
from repositorios.repositorio_docente_postgresql import RepositorioDocentePostgreSQL
from repositorios.repositorio_aa_linea_postgresql import RepositorioAaLineaPostgreSQL
from repositorios.repositorio_ac_linea_postgresql import RepositorioAcLineaPostgreSQL
from repositorios.repositorio_grupo_investigacion_postgresql import RepositorioGrupoInvestigacionPostgreSQL
from repositorios.repositorio_grupo_linea_postgresql import RepositorioGrupoLineaPostgreSQL
from repositorios.repositorio_linea_investigacion_postgresql import RepositorioLineaInvestigacionPostgreSQL
from repositorios.repositorio_objetivo_desarrollo_sostenible_postgresql import RepositorioObjetivoDesarrolloSosteniblePostgreSQL
from repositorios.repositorio_ods_linea_postgresql import RepositorioOdsLineaPostgreSQL
from repositorios.repositorio_participa_grupo_postgresql import RepositorioParticipaGrupoPostgreSQL
from repositorios.repositorio_participa_semillero_postgresql import RepositorioParticipaSemilleroPostgreSQL
from repositorios.repositorio_semillero_postgresql import RepositorioSemilleroPostgreSQL
from repositorios.repositorio_semillero_linea_postgresql import RepositorioSemilleroLineaPostgreSQL
from repositorios.repositorio_termino_clave_postgresql import RepositorioTerminoClavePostgreSQL
from repositorios.repositorio_universidad_postgresql import RepositorioUniversidadPostgreSQL
from repositorios.repositorio_rol_postgresql import RepositorioRolPostgreSQL
from repositorios.repositorio_rol_usuario_postgresql import RepositorioRolUsuarioPostgreSQL
from repositorios.repositorio_usuario_postgresql import RepositorioUsuarioPostgreSQL
from servicios.servicio_area_aplicacion import ServicioAreaAplicacion
from servicios.servicio_area_conocimiento import ServicioAreaConocimiento
from servicios.servicio_docente import ServicioDocente
from servicios.servicio_aa_linea import ServicioAaLinea
from servicios.servicio_ac_linea import ServicioAcLinea
from servicios.servicio_grupo_investigacion import ServicioGrupoInvestigacion
from servicios.servicio_grupo_linea import ServicioGrupoLinea
from servicios.servicio_linea_investigacion import ServicioLineaInvestigacion
from servicios.servicio_objetivo_desarrollo_sostenible import ServicioObjetivoDesarrolloSostenible
from servicios.servicio_ods_linea import ServicioOdsLinea
from servicios.servicio_participa_grupo import ServicioParticipaGrupo
from servicios.servicio_participa_semillero import ServicioParticipaSemillero
from servicios.servicio_semillero import ServicioSemillero
from servicios.servicio_semillero_linea import ServicioSemilleroLinea
from servicios.servicio_termino_clave import ServicioTerminoClave
from servicios.servicio_universidad import ServicioUniversidad
from servicios.servicio_rol import ServicioRol
from servicios.servicio_rol_usuario import ServicioRolUsuario
from servicios.servicio_usuario import ServicioUsuario


def crear_servicio_area_conocimiento():
    return ServicioAreaConocimiento(RepositorioAreaConocimientoPostgreSQL())


def crear_servicio_objetivo_desarrollo_sostenible():
    return ServicioObjetivoDesarrolloSostenible(RepositorioObjetivoDesarrolloSosteniblePostgreSQL())


def crear_servicio_area_aplicacion():
    return ServicioAreaAplicacion(RepositorioAreaAplicacionPostgreSQL())


def crear_servicio_termino_clave():
    return ServicioTerminoClave(RepositorioTerminoClavePostgreSQL())


def crear_servicio_universidad():
    return ServicioUniversidad(RepositorioUniversidadPostgreSQL())


def crear_servicio_linea_investigacion():
    return ServicioLineaInvestigacion(RepositorioLineaInvestigacionPostgreSQL())


def crear_servicio_docente():
    return ServicioDocente(RepositorioDocentePostgreSQL())


def crear_servicio_grupo_investigacion():
    return ServicioGrupoInvestigacion(RepositorioGrupoInvestigacionPostgreSQL())


def crear_servicio_semillero():
    return ServicioSemillero(RepositorioSemilleroPostgreSQL())


def crear_servicio_participa_grupo():
    return ServicioParticipaGrupo(RepositorioParticipaGrupoPostgreSQL())


def crear_servicio_participa_semillero():
    return ServicioParticipaSemillero(RepositorioParticipaSemilleroPostgreSQL())


def crear_servicio_grupo_linea():
    return ServicioGrupoLinea(RepositorioGrupoLineaPostgreSQL())


def crear_servicio_semillero_linea():
    return ServicioSemilleroLinea(RepositorioSemilleroLineaPostgreSQL())


def crear_servicio_ac_linea():
    return ServicioAcLinea(RepositorioAcLineaPostgreSQL())


def crear_servicio_ods_linea():
    return ServicioOdsLinea(RepositorioOdsLineaPostgreSQL())


def crear_servicio_aa_linea():
    return ServicioAaLinea(RepositorioAaLineaPostgreSQL())


def crear_servicio_rol():
    return ServicioRol(RepositorioRolPostgreSQL())


def crear_servicio_usuario():
    return ServicioUsuario(RepositorioUsuarioPostgreSQL())


def crear_servicio_rol_usuario():
    return ServicioRolUsuario(RepositorioRolUsuarioPostgreSQL())
