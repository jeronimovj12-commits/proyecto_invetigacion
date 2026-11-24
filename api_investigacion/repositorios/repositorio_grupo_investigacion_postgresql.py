"""Adaptador SQL de grupos; usar el nombre físico exacto evita romper la base entregada."""

from repositorios.abstracciones.i_repositorio_grupo_investigacion import IRepositorioGrupoInvestigacion
from repositorios.repositorio_postgresql_base import RepositorioPostgreSQLBase


class RepositorioGrupoInvestigacionPostgreSQL(RepositorioPostgreSQLBase, IRepositorioGrupoInvestigacion):
    TABLA = "grupo_investigacion"
    CLAVE = "id"
    COLUMNAS = (
        "id", "nombre", "url_gruplac", "categoria", "convocatoria",
        "fecha_fundacion", "universidsad", "interno", "ambito",
    )
    COLUMNAS_CREACION = COLUMNAS
