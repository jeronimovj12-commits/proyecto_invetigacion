"""
ensamblador.py — El ÚNICO punto del sistema que decide qué motor se usa.

Los controladores llaman a `crear_servicio_area_conocimiento()` y reciben algo
que cumple la interfaz del servicio. No saben —ni tienen por qué saber— qué
repositorio hay detrás.

Hoy hay un solo motor. El día que entre un segundo, este archivo es el único
que cambia: esa es toda la gracia de tener la construcción en un solo sitio.
"""

import os

from repositorios.repositorio_area_conocimiento_postgresql import (
    RepositorioAreaConocimientoPostgreSQL,
)
from servicios.abstracciones.i_servicio_area_conocimiento import (
    IServicioAreaConocimiento,
)
from servicios.servicio_area_conocimiento import ServicioAreaConocimiento


_servicio_area_conocimiento: IServicioAreaConocimiento | None = None


def _cadena_conexion() -> str:
    cadena = os.environ.get("DB_POSTGRES")
    if not cadena:
        raise RuntimeError(
            "Falta la variable de entorno DB_POSTGRES con la cadena de conexión.")
    return cadena


def crear_servicio_area_conocimiento() -> IServicioAreaConocimiento:
    """Entrega una instancia compartida para reutilizar el pool de conexiones."""
    global _servicio_area_conocimiento
    if _servicio_area_conocimiento is None:
        _servicio_area_conocimiento = ServicioAreaConocimiento(
            RepositorioAreaConocimientoPostgreSQL(_cadena_conexion()))
    return _servicio_area_conocimiento


from repositorios.repositorio_docente_postgresql import RepositorioDocentePostgreSQL
from servicios.servicio_docente import ServicioDocente
from servicios.abstracciones.i_servicio_docente import IServicioDocente

_servicio_docente: IServicioDocente | None = None

def crear_servicio_docente() -> IServicioDocente:
    global _servicio_docente
    if _servicio_docente is None:
        _servicio_docente = ServicioDocente(RepositorioDocentePostgreSQL(_cadena_conexion()))
    return _servicio_docente


from repositorios.repositorio_grupo_investigacion_postgresql import RepositorioGrupoInvestigacionPostgreSQL
from servicios.servicio_grupo_investigacion import ServicioGrupoInvestigacion
from servicios.abstracciones.i_servicio_grupo_investigacion import IServicioGrupoInvestigacion

_servicio_grupo_investigacion: IServicioGrupoInvestigacion | None = None

def crear_servicio_grupo_investigacion() -> IServicioGrupoInvestigacion:
    global _servicio_grupo_investigacion
    if _servicio_grupo_investigacion is None:
        _servicio_grupo_investigacion = ServicioGrupoInvestigacion(RepositorioGrupoInvestigacionPostgreSQL(_cadena_conexion()))
    return _servicio_grupo_investigacion


from repositorios.repositorio_semillero_postgresql import RepositorioSemilleroPostgreSQL
from servicios.servicio_semillero import ServicioSemillero
from servicios.abstracciones.i_servicio_semillero import IServicioSemillero

_servicio_semillero: IServicioSemillero | None = None

def crear_servicio_semillero() -> IServicioSemillero:
    global _servicio_semillero
    if _servicio_semillero is None:
        _servicio_semillero = ServicioSemillero(RepositorioSemilleroPostgreSQL(_cadena_conexion()))
    return _servicio_semillero


from repositorios.repositorio_participa_semillero_postgresql import RepositorioParticipaSemilleroPostgreSQL
from servicios.servicio_participa_semillero import ServicioParticipaSemillero
from servicios.abstracciones.i_servicio_participa_semillero import IServicioParticipaSemillero

_servicio_participa_semillero: IServicioParticipaSemillero | None = None

def crear_servicio_participa_semillero() -> IServicioParticipaSemillero:
    global _servicio_participa_semillero
    if _servicio_participa_semillero is None:
        _servicio_participa_semillero = ServicioParticipaSemillero(RepositorioParticipaSemilleroPostgreSQL(_cadena_conexion()))
    return _servicio_participa_semillero


from repositorios.repositorio_participa_grupo_postgresql import RepositorioParticipaGrupoPostgreSQL
from servicios.servicio_participa_grupo import ServicioParticipaGrupo
from servicios.abstracciones.i_servicio_participa_grupo import IServicioParticipaGrupo

_servicio_participa_grupo: IServicioParticipaGrupo | None = None

def crear_servicio_participa_grupo() -> IServicioParticipaGrupo:
    global _servicio_participa_grupo
    if _servicio_participa_grupo is None:
        _servicio_participa_grupo = ServicioParticipaGrupo(RepositorioParticipaGrupoPostgreSQL(_cadena_conexion()))
    return _servicio_participa_grupo


from repositorios.repositorio_semillero_linea_postgresql import RepositorioSemilleroLineaPostgreSQL
from servicios.servicio_semillero_linea import ServicioSemilleroLinea
from servicios.abstracciones.i_servicio_semillero_linea import IServicioSemilleroLinea

_servicio_semillero_linea: IServicioSemilleroLinea | None = None

def crear_servicio_semillero_linea() -> IServicioSemilleroLinea:
    global _servicio_semillero_linea
    if _servicio_semillero_linea is None:
        _servicio_semillero_linea = ServicioSemilleroLinea(RepositorioSemilleroLineaPostgreSQL(_cadena_conexion()))
    return _servicio_semillero_linea


from repositorios.repositorio_grupo_linea_postgresql import RepositorioGrupoLineaPostgreSQL
from servicios.servicio_grupo_linea import ServicioGrupoLinea
from servicios.abstracciones.i_servicio_grupo_linea import IServicioGrupoLinea

_servicio_grupo_linea: IServicioGrupoLinea | None = None

def crear_servicio_grupo_linea() -> IServicioGrupoLinea:
    global _servicio_grupo_linea
    if _servicio_grupo_linea is None:
        _servicio_grupo_linea = ServicioGrupoLinea(RepositorioGrupoLineaPostgreSQL(_cadena_conexion()))
    return _servicio_grupo_linea


from repositorios.repositorio_ac_linea_postgresql import RepositorioAcLineaPostgreSQL
from servicios.servicio_ac_linea import ServicioAcLinea
from servicios.abstracciones.i_servicio_ac_linea import IServicioAcLinea

_servicio_ac_linea: IServicioAcLinea | None = None

def crear_servicio_ac_linea() -> IServicioAcLinea:
    global _servicio_ac_linea
    if _servicio_ac_linea is None:
        _servicio_ac_linea = ServicioAcLinea(RepositorioAcLineaPostgreSQL(_cadena_conexion()))
    return _servicio_ac_linea


from repositorios.repositorio_ods_linea_postgresql import RepositorioOdsLineaPostgreSQL
from servicios.servicio_ods_linea import ServicioOdsLinea
from servicios.abstracciones.i_servicio_ods_linea import IServicioOdsLinea

_servicio_ods_linea: IServicioOdsLinea | None = None

def crear_servicio_ods_linea() -> IServicioOdsLinea:
    global _servicio_ods_linea
    if _servicio_ods_linea is None:
        _servicio_ods_linea = ServicioOdsLinea(RepositorioOdsLineaPostgreSQL(_cadena_conexion()))
    return _servicio_ods_linea


from repositorios.repositorio_aa_linea_postgresql import RepositorioAaLineaPostgreSQL
from servicios.servicio_aa_linea import ServicioAaLinea
from servicios.abstracciones.i_servicio_aa_linea import IServicioAaLinea

_servicio_aa_linea: IServicioAaLinea | None = None

def crear_servicio_aa_linea() -> IServicioAaLinea:
    global _servicio_aa_linea
    if _servicio_aa_linea is None:
        _servicio_aa_linea = ServicioAaLinea(RepositorioAaLineaPostgreSQL(_cadena_conexion()))
    return _servicio_aa_linea


from repositorios.repositorio_universidad_postgresql import RepositorioUniversidadPostgreSQL
from servicios.servicio_universidad import ServicioUniversidad
from servicios.abstracciones.i_servicio_universidad import IServicioUniversidad

_servicio_universidad: IServicioUniversidad | None = None

def crear_servicio_universidad() -> IServicioUniversidad:
    global _servicio_universidad
    if _servicio_universidad is None:
        _servicio_universidad = ServicioUniversidad(RepositorioUniversidadPostgreSQL(_cadena_conexion()))
    return _servicio_universidad


from repositorios.repositorio_linea_investigacion_postgresql import RepositorioLineaInvestigacionPostgreSQL
from servicios.servicio_linea_investigacion import ServicioLineaInvestigacion
from servicios.abstracciones.i_servicio_linea_investigacion import IServicioLineaInvestigacion

_servicio_linea_investigacion: IServicioLineaInvestigacion | None = None

def crear_servicio_linea_investigacion() -> IServicioLineaInvestigacion:
    global _servicio_linea_investigacion
    if _servicio_linea_investigacion is None:
        _servicio_linea_investigacion = ServicioLineaInvestigacion(RepositorioLineaInvestigacionPostgreSQL(_cadena_conexion()))
    return _servicio_linea_investigacion


from repositorios.repositorio_objetivo_desarrollo_sostenible_postgresql import RepositorioObjetivoDesarrolloSosteniblePostgreSQL
from servicios.servicio_objetivo_desarrollo_sostenible import ServicioObjetivoDesarrolloSostenible
from servicios.abstracciones.i_servicio_objetivo_desarrollo_sostenible import IServicioObjetivoDesarrolloSostenible

_servicio_objetivo_desarrollo_sostenible: IServicioObjetivoDesarrolloSostenible | None = None

def crear_servicio_objetivo_desarrollo_sostenible() -> IServicioObjetivoDesarrolloSostenible:
    global _servicio_objetivo_desarrollo_sostenible
    if _servicio_objetivo_desarrollo_sostenible is None:
        _servicio_objetivo_desarrollo_sostenible = ServicioObjetivoDesarrolloSostenible(RepositorioObjetivoDesarrolloSosteniblePostgreSQL(_cadena_conexion()))
    return _servicio_objetivo_desarrollo_sostenible


from repositorios.repositorio_area_aplicacion_postgresql import RepositorioAreaAplicacionPostgreSQL
from servicios.servicio_area_aplicacion import ServicioAreaAplicacion
from servicios.abstracciones.i_servicio_area_aplicacion import IServicioAreaAplicacion

_servicio_area_aplicacion: IServicioAreaAplicacion | None = None

def crear_servicio_area_aplicacion() -> IServicioAreaAplicacion:
    global _servicio_area_aplicacion
    if _servicio_area_aplicacion is None:
        _servicio_area_aplicacion = ServicioAreaAplicacion(RepositorioAreaAplicacionPostgreSQL(_cadena_conexion()))
    return _servicio_area_aplicacion
