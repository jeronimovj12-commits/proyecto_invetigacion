"""
ensamblador.py — El ÚNICO punto del sistema que decide qué motor se usa.

Los controladores llaman a `crear_servicio_area_conocimiento()` y reciben algo
que cumple la interfaz del servicio. No saben —ni tienen por qué saber— qué
repositorio hay detrás.

Hoy hay un solo motor. El día que entre un segundo, este archivo es el único
que cambia: esa es toda la gracia de tener la construcción en un solo sitio.
"""

# Carga el modulo o los modulos os.
import os

# Importa ( desde repositorios.repositorio_area_conocimiento_postgresql para usar esas definiciones.
from repositorios.repositorio_area_conocimiento_postgresql import (
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    RepositorioAreaConocimientoPostgreSQL,
# Cierra la estructura abierta en las lineas anteriores.
)
# Importa ( desde servicios.abstracciones.i_servicio_area_conocimiento para usar esas definiciones.
from servicios.abstracciones.i_servicio_area_conocimiento import (
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    IServicioAreaConocimiento,
# Cierra la estructura abierta en las lineas anteriores.
)
# Importa ServicioAreaConocimiento desde servicios.servicio_area_conocimiento para usar esas definiciones.
from servicios.servicio_area_conocimiento import ServicioAreaConocimiento


# Asigna a _servicio_area_conocimiento el valor calculado a la derecha.
_servicio_area_conocimiento: IServicioAreaConocimiento | None = None


# Define la funcion _cadena_conexion con los parametros declarados; su bloque realiza esta operacion.
def _cadena_conexion() -> str:
    # Asigna a cadena el valor calculado a la derecha.
    cadena = os.environ.get("DB_POSTGRES") or os.environ.get("DATABASE_URL")
    # Ejecuta el bloque siguiente solo cuando se cumple: not cadena.
    if not cadena:
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise RuntimeError(
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            "Falta DB_POSTGRES o DATABASE_URL con la cadena de conexión.")
    # Devuelve al llamador el resultado de la expresion indicada.
    return cadena


# Define la funcion crear_servicio_area_conocimiento con los parametros declarados; su bloque realiza esta operacion.
def crear_servicio_area_conocimiento() -> IServicioAreaConocimiento:
    # Ejecuta la instruccion indicada dentro del flujo actual.
    """Entrega una instancia compartida para reutilizar el pool de conexiones."""
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    global _servicio_area_conocimiento
    # Ejecuta el bloque siguiente solo cuando se cumple: _servicio_area_conocimiento is None.
    if _servicio_area_conocimiento is None:
        # Asigna a _servicio_area_conocimiento el valor calculado a la derecha.
        _servicio_area_conocimiento = ServicioAreaConocimiento(
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            RepositorioAreaConocimientoPostgreSQL(_cadena_conexion()))
    # Devuelve al llamador el resultado de la expresion indicada.
    return _servicio_area_conocimiento


# Importa RepositorioDocentePostgreSQL desde repositorios.repositorio_docente_postgresql para usar esas definiciones.
from repositorios.repositorio_docente_postgresql import RepositorioDocentePostgreSQL
# Importa ServicioDocente desde servicios.servicio_docente para usar esas definiciones.
from servicios.servicio_docente import ServicioDocente
# Importa IServicioDocente desde servicios.abstracciones.i_servicio_docente para usar esas definiciones.
from servicios.abstracciones.i_servicio_docente import IServicioDocente

# Asigna a _servicio_docente el valor calculado a la derecha.
_servicio_docente: IServicioDocente | None = None

# Define la funcion crear_servicio_docente con los parametros declarados; su bloque realiza esta operacion.
def crear_servicio_docente() -> IServicioDocente:
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    global _servicio_docente
    # Ejecuta el bloque siguiente solo cuando se cumple: _servicio_docente is None.
    if _servicio_docente is None:
        # Asigna a _servicio_docente el valor calculado a la derecha.
        _servicio_docente = ServicioDocente(RepositorioDocentePostgreSQL(_cadena_conexion()))
    # Devuelve al llamador el resultado de la expresion indicada.
    return _servicio_docente


# Importa RepositorioGrupoInvestigacionPostgreSQL desde repositorios.repositorio_grupo_investigacion_postgresql para usar esas definiciones.
from repositorios.repositorio_grupo_investigacion_postgresql import RepositorioGrupoInvestigacionPostgreSQL
# Importa ServicioGrupoInvestigacion desde servicios.servicio_grupo_investigacion para usar esas definiciones.
from servicios.servicio_grupo_investigacion import ServicioGrupoInvestigacion
# Importa IServicioGrupoInvestigacion desde servicios.abstracciones.i_servicio_grupo_investigacion para usar esas definiciones.
from servicios.abstracciones.i_servicio_grupo_investigacion import IServicioGrupoInvestigacion

# Asigna a _servicio_grupo_investigacion el valor calculado a la derecha.
_servicio_grupo_investigacion: IServicioGrupoInvestigacion | None = None

# Define la funcion crear_servicio_grupo_investigacion con los parametros declarados; su bloque realiza esta operacion.
def crear_servicio_grupo_investigacion() -> IServicioGrupoInvestigacion:
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    global _servicio_grupo_investigacion
    # Ejecuta el bloque siguiente solo cuando se cumple: _servicio_grupo_investigacion is None.
    if _servicio_grupo_investigacion is None:
        # Asigna a _servicio_grupo_investigacion el valor calculado a la derecha.
        _servicio_grupo_investigacion = ServicioGrupoInvestigacion(RepositorioGrupoInvestigacionPostgreSQL(_cadena_conexion()))
    # Devuelve al llamador el resultado de la expresion indicada.
    return _servicio_grupo_investigacion


# Importa RepositorioSemilleroPostgreSQL desde repositorios.repositorio_semillero_postgresql para usar esas definiciones.
from repositorios.repositorio_semillero_postgresql import RepositorioSemilleroPostgreSQL
# Importa ServicioSemillero desde servicios.servicio_semillero para usar esas definiciones.
from servicios.servicio_semillero import ServicioSemillero
# Importa IServicioSemillero desde servicios.abstracciones.i_servicio_semillero para usar esas definiciones.
from servicios.abstracciones.i_servicio_semillero import IServicioSemillero

# Asigna a _servicio_semillero el valor calculado a la derecha.
_servicio_semillero: IServicioSemillero | None = None

# Define la funcion crear_servicio_semillero con los parametros declarados; su bloque realiza esta operacion.
def crear_servicio_semillero() -> IServicioSemillero:
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    global _servicio_semillero
    # Ejecuta el bloque siguiente solo cuando se cumple: _servicio_semillero is None.
    if _servicio_semillero is None:
        # Asigna a _servicio_semillero el valor calculado a la derecha.
        _servicio_semillero = ServicioSemillero(RepositorioSemilleroPostgreSQL(_cadena_conexion()))
    # Devuelve al llamador el resultado de la expresion indicada.
    return _servicio_semillero


# Importa RepositorioParticipaSemilleroPostgreSQL desde repositorios.repositorio_participa_semillero_postgresql para usar esas definiciones.
from repositorios.repositorio_participa_semillero_postgresql import RepositorioParticipaSemilleroPostgreSQL
# Importa ServicioParticipaSemillero desde servicios.servicio_participa_semillero para usar esas definiciones.
from servicios.servicio_participa_semillero import ServicioParticipaSemillero
# Importa IServicioParticipaSemillero desde servicios.abstracciones.i_servicio_participa_semillero para usar esas definiciones.
from servicios.abstracciones.i_servicio_participa_semillero import IServicioParticipaSemillero

# Asigna a _servicio_participa_semillero el valor calculado a la derecha.
_servicio_participa_semillero: IServicioParticipaSemillero | None = None

# Define la funcion crear_servicio_participa_semillero con los parametros declarados; su bloque realiza esta operacion.
def crear_servicio_participa_semillero() -> IServicioParticipaSemillero:
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    global _servicio_participa_semillero
    # Ejecuta el bloque siguiente solo cuando se cumple: _servicio_participa_semillero is None.
    if _servicio_participa_semillero is None:
        # Asigna a _servicio_participa_semillero el valor calculado a la derecha.
        _servicio_participa_semillero = ServicioParticipaSemillero(RepositorioParticipaSemilleroPostgreSQL(_cadena_conexion()))
    # Devuelve al llamador el resultado de la expresion indicada.
    return _servicio_participa_semillero


# Importa RepositorioParticipaGrupoPostgreSQL desde repositorios.repositorio_participa_grupo_postgresql para usar esas definiciones.
from repositorios.repositorio_participa_grupo_postgresql import RepositorioParticipaGrupoPostgreSQL
# Importa ServicioParticipaGrupo desde servicios.servicio_participa_grupo para usar esas definiciones.
from servicios.servicio_participa_grupo import ServicioParticipaGrupo
# Importa IServicioParticipaGrupo desde servicios.abstracciones.i_servicio_participa_grupo para usar esas definiciones.
from servicios.abstracciones.i_servicio_participa_grupo import IServicioParticipaGrupo

# Asigna a _servicio_participa_grupo el valor calculado a la derecha.
_servicio_participa_grupo: IServicioParticipaGrupo | None = None

# Define la funcion crear_servicio_participa_grupo con los parametros declarados; su bloque realiza esta operacion.
def crear_servicio_participa_grupo() -> IServicioParticipaGrupo:
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    global _servicio_participa_grupo
    # Ejecuta el bloque siguiente solo cuando se cumple: _servicio_participa_grupo is None.
    if _servicio_participa_grupo is None:
        # Asigna a _servicio_participa_grupo el valor calculado a la derecha.
        _servicio_participa_grupo = ServicioParticipaGrupo(RepositorioParticipaGrupoPostgreSQL(_cadena_conexion()))
    # Devuelve al llamador el resultado de la expresion indicada.
    return _servicio_participa_grupo


# Importa RepositorioSemilleroLineaPostgreSQL desde repositorios.repositorio_semillero_linea_postgresql para usar esas definiciones.
from repositorios.repositorio_semillero_linea_postgresql import RepositorioSemilleroLineaPostgreSQL
# Importa ServicioSemilleroLinea desde servicios.servicio_semillero_linea para usar esas definiciones.
from servicios.servicio_semillero_linea import ServicioSemilleroLinea
# Importa IServicioSemilleroLinea desde servicios.abstracciones.i_servicio_semillero_linea para usar esas definiciones.
from servicios.abstracciones.i_servicio_semillero_linea import IServicioSemilleroLinea

# Asigna a _servicio_semillero_linea el valor calculado a la derecha.
_servicio_semillero_linea: IServicioSemilleroLinea | None = None

# Define la funcion crear_servicio_semillero_linea con los parametros declarados; su bloque realiza esta operacion.
def crear_servicio_semillero_linea() -> IServicioSemilleroLinea:
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    global _servicio_semillero_linea
    # Ejecuta el bloque siguiente solo cuando se cumple: _servicio_semillero_linea is None.
    if _servicio_semillero_linea is None:
        # Asigna a _servicio_semillero_linea el valor calculado a la derecha.
        _servicio_semillero_linea = ServicioSemilleroLinea(RepositorioSemilleroLineaPostgreSQL(_cadena_conexion()))
    # Devuelve al llamador el resultado de la expresion indicada.
    return _servicio_semillero_linea


# Importa RepositorioGrupoLineaPostgreSQL desde repositorios.repositorio_grupo_linea_postgresql para usar esas definiciones.
from repositorios.repositorio_grupo_linea_postgresql import RepositorioGrupoLineaPostgreSQL
# Importa ServicioGrupoLinea desde servicios.servicio_grupo_linea para usar esas definiciones.
from servicios.servicio_grupo_linea import ServicioGrupoLinea
# Importa IServicioGrupoLinea desde servicios.abstracciones.i_servicio_grupo_linea para usar esas definiciones.
from servicios.abstracciones.i_servicio_grupo_linea import IServicioGrupoLinea

# Asigna a _servicio_grupo_linea el valor calculado a la derecha.
_servicio_grupo_linea: IServicioGrupoLinea | None = None

# Define la funcion crear_servicio_grupo_linea con los parametros declarados; su bloque realiza esta operacion.
def crear_servicio_grupo_linea() -> IServicioGrupoLinea:
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    global _servicio_grupo_linea
    # Ejecuta el bloque siguiente solo cuando se cumple: _servicio_grupo_linea is None.
    if _servicio_grupo_linea is None:
        # Asigna a _servicio_grupo_linea el valor calculado a la derecha.
        _servicio_grupo_linea = ServicioGrupoLinea(RepositorioGrupoLineaPostgreSQL(_cadena_conexion()))
    # Devuelve al llamador el resultado de la expresion indicada.
    return _servicio_grupo_linea


# Importa RepositorioAcLineaPostgreSQL desde repositorios.repositorio_ac_linea_postgresql para usar esas definiciones.
from repositorios.repositorio_ac_linea_postgresql import RepositorioAcLineaPostgreSQL
# Importa ServicioAcLinea desde servicios.servicio_ac_linea para usar esas definiciones.
from servicios.servicio_ac_linea import ServicioAcLinea
# Importa IServicioAcLinea desde servicios.abstracciones.i_servicio_ac_linea para usar esas definiciones.
from servicios.abstracciones.i_servicio_ac_linea import IServicioAcLinea

# Asigna a _servicio_ac_linea el valor calculado a la derecha.
_servicio_ac_linea: IServicioAcLinea | None = None

# Define la funcion crear_servicio_ac_linea con los parametros declarados; su bloque realiza esta operacion.
def crear_servicio_ac_linea() -> IServicioAcLinea:
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    global _servicio_ac_linea
    # Ejecuta el bloque siguiente solo cuando se cumple: _servicio_ac_linea is None.
    if _servicio_ac_linea is None:
        # Asigna a _servicio_ac_linea el valor calculado a la derecha.
        _servicio_ac_linea = ServicioAcLinea(RepositorioAcLineaPostgreSQL(_cadena_conexion()))
    # Devuelve al llamador el resultado de la expresion indicada.
    return _servicio_ac_linea


# Importa RepositorioOdsLineaPostgreSQL desde repositorios.repositorio_ods_linea_postgresql para usar esas definiciones.
from repositorios.repositorio_ods_linea_postgresql import RepositorioOdsLineaPostgreSQL
# Importa ServicioOdsLinea desde servicios.servicio_ods_linea para usar esas definiciones.
from servicios.servicio_ods_linea import ServicioOdsLinea
# Importa IServicioOdsLinea desde servicios.abstracciones.i_servicio_ods_linea para usar esas definiciones.
from servicios.abstracciones.i_servicio_ods_linea import IServicioOdsLinea

# Asigna a _servicio_ods_linea el valor calculado a la derecha.
_servicio_ods_linea: IServicioOdsLinea | None = None

# Define la funcion crear_servicio_ods_linea con los parametros declarados; su bloque realiza esta operacion.
def crear_servicio_ods_linea() -> IServicioOdsLinea:
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    global _servicio_ods_linea
    # Ejecuta el bloque siguiente solo cuando se cumple: _servicio_ods_linea is None.
    if _servicio_ods_linea is None:
        # Asigna a _servicio_ods_linea el valor calculado a la derecha.
        _servicio_ods_linea = ServicioOdsLinea(RepositorioOdsLineaPostgreSQL(_cadena_conexion()))
    # Devuelve al llamador el resultado de la expresion indicada.
    return _servicio_ods_linea


# Importa RepositorioAaLineaPostgreSQL desde repositorios.repositorio_aa_linea_postgresql para usar esas definiciones.
from repositorios.repositorio_aa_linea_postgresql import RepositorioAaLineaPostgreSQL
# Importa ServicioAaLinea desde servicios.servicio_aa_linea para usar esas definiciones.
from servicios.servicio_aa_linea import ServicioAaLinea
# Importa IServicioAaLinea desde servicios.abstracciones.i_servicio_aa_linea para usar esas definiciones.
from servicios.abstracciones.i_servicio_aa_linea import IServicioAaLinea

# Asigna a _servicio_aa_linea el valor calculado a la derecha.
_servicio_aa_linea: IServicioAaLinea | None = None

# Define la funcion crear_servicio_aa_linea con los parametros declarados; su bloque realiza esta operacion.
def crear_servicio_aa_linea() -> IServicioAaLinea:
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    global _servicio_aa_linea
    # Ejecuta el bloque siguiente solo cuando se cumple: _servicio_aa_linea is None.
    if _servicio_aa_linea is None:
        # Asigna a _servicio_aa_linea el valor calculado a la derecha.
        _servicio_aa_linea = ServicioAaLinea(RepositorioAaLineaPostgreSQL(_cadena_conexion()))
    # Devuelve al llamador el resultado de la expresion indicada.
    return _servicio_aa_linea


# Importa RepositorioUniversidadPostgreSQL desde repositorios.repositorio_universidad_postgresql para usar esas definiciones.
from repositorios.repositorio_universidad_postgresql import RepositorioUniversidadPostgreSQL
# Importa ServicioUniversidad desde servicios.servicio_universidad para usar esas definiciones.
from servicios.servicio_universidad import ServicioUniversidad
# Importa IServicioUniversidad desde servicios.abstracciones.i_servicio_universidad para usar esas definiciones.
from servicios.abstracciones.i_servicio_universidad import IServicioUniversidad

# Asigna a _servicio_universidad el valor calculado a la derecha.
_servicio_universidad: IServicioUniversidad | None = None

# Define la funcion crear_servicio_universidad con los parametros declarados; su bloque realiza esta operacion.
def crear_servicio_universidad() -> IServicioUniversidad:
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    global _servicio_universidad
    # Ejecuta el bloque siguiente solo cuando se cumple: _servicio_universidad is None.
    if _servicio_universidad is None:
        # Asigna a _servicio_universidad el valor calculado a la derecha.
        _servicio_universidad = ServicioUniversidad(RepositorioUniversidadPostgreSQL(_cadena_conexion()))
    # Devuelve al llamador el resultado de la expresion indicada.
    return _servicio_universidad


# Importa RepositorioLineaInvestigacionPostgreSQL desde repositorios.repositorio_linea_investigacion_postgresql para usar esas definiciones.
from repositorios.repositorio_linea_investigacion_postgresql import RepositorioLineaInvestigacionPostgreSQL
# Importa ServicioLineaInvestigacion desde servicios.servicio_linea_investigacion para usar esas definiciones.
from servicios.servicio_linea_investigacion import ServicioLineaInvestigacion
# Importa IServicioLineaInvestigacion desde servicios.abstracciones.i_servicio_linea_investigacion para usar esas definiciones.
from servicios.abstracciones.i_servicio_linea_investigacion import IServicioLineaInvestigacion

# Asigna a _servicio_linea_investigacion el valor calculado a la derecha.
_servicio_linea_investigacion: IServicioLineaInvestigacion | None = None

# Define la funcion crear_servicio_linea_investigacion con los parametros declarados; su bloque realiza esta operacion.
def crear_servicio_linea_investigacion() -> IServicioLineaInvestigacion:
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    global _servicio_linea_investigacion
    # Ejecuta el bloque siguiente solo cuando se cumple: _servicio_linea_investigacion is None.
    if _servicio_linea_investigacion is None:
        # Asigna a _servicio_linea_investigacion el valor calculado a la derecha.
        _servicio_linea_investigacion = ServicioLineaInvestigacion(RepositorioLineaInvestigacionPostgreSQL(_cadena_conexion()))
    # Devuelve al llamador el resultado de la expresion indicada.
    return _servicio_linea_investigacion


# Importa RepositorioObjetivoDesarrolloSosteniblePostgreSQL desde repositorios.repositorio_objetivo_desarrollo_sostenible_postgresql para usar esas definiciones.
from repositorios.repositorio_objetivo_desarrollo_sostenible_postgresql import RepositorioObjetivoDesarrolloSosteniblePostgreSQL
# Importa ServicioObjetivoDesarrolloSostenible desde servicios.servicio_objetivo_desarrollo_sostenible para usar esas definiciones.
from servicios.servicio_objetivo_desarrollo_sostenible import ServicioObjetivoDesarrolloSostenible
# Importa IServicioObjetivoDesarrolloSostenible desde servicios.abstracciones.i_servicio_objetivo_desarrollo_sostenible para usar esas definiciones.
from servicios.abstracciones.i_servicio_objetivo_desarrollo_sostenible import IServicioObjetivoDesarrolloSostenible

# Asigna a _servicio_objetivo_desarrollo_sostenible el valor calculado a la derecha.
_servicio_objetivo_desarrollo_sostenible: IServicioObjetivoDesarrolloSostenible | None = None

# Define la funcion crear_servicio_objetivo_desarrollo_sostenible con los parametros declarados; su bloque realiza esta operacion.
def crear_servicio_objetivo_desarrollo_sostenible() -> IServicioObjetivoDesarrolloSostenible:
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    global _servicio_objetivo_desarrollo_sostenible
    # Ejecuta el bloque siguiente solo cuando se cumple: _servicio_objetivo_desarrollo_sostenible is None.
    if _servicio_objetivo_desarrollo_sostenible is None:
        # Asigna a _servicio_objetivo_desarrollo_sostenible el valor calculado a la derecha.
        _servicio_objetivo_desarrollo_sostenible = ServicioObjetivoDesarrolloSostenible(RepositorioObjetivoDesarrolloSosteniblePostgreSQL(_cadena_conexion()))
    # Devuelve al llamador el resultado de la expresion indicada.
    return _servicio_objetivo_desarrollo_sostenible


# Importa RepositorioAreaAplicacionPostgreSQL desde repositorios.repositorio_area_aplicacion_postgresql para usar esas definiciones.
from repositorios.repositorio_area_aplicacion_postgresql import RepositorioAreaAplicacionPostgreSQL
# Importa ServicioAreaAplicacion desde servicios.servicio_area_aplicacion para usar esas definiciones.
from servicios.servicio_area_aplicacion import ServicioAreaAplicacion
# Importa IServicioAreaAplicacion desde servicios.abstracciones.i_servicio_area_aplicacion para usar esas definiciones.
from servicios.abstracciones.i_servicio_area_aplicacion import IServicioAreaAplicacion

# Asigna a _servicio_area_aplicacion el valor calculado a la derecha.
_servicio_area_aplicacion: IServicioAreaAplicacion | None = None

# Define la funcion crear_servicio_area_aplicacion con los parametros declarados; su bloque realiza esta operacion.
def crear_servicio_area_aplicacion() -> IServicioAreaAplicacion:
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    global _servicio_area_aplicacion
    # Ejecuta el bloque siguiente solo cuando se cumple: _servicio_area_aplicacion is None.
    if _servicio_area_aplicacion is None:
        # Asigna a _servicio_area_aplicacion el valor calculado a la derecha.
        _servicio_area_aplicacion = ServicioAreaAplicacion(RepositorioAreaAplicacionPostgreSQL(_cadena_conexion()))
    # Devuelve al llamador el resultado de la expresion indicada.
    return _servicio_area_aplicacion
