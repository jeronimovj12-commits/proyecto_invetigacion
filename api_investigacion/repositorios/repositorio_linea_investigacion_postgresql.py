"""Repositorio PostgreSQL de líneas; omite la clave en INSERT para que la genere la base."""

from repositorios.repositorio_postgresql_base import RepositorioPostgreSQLBase


class RepositorioLineaInvestigacionPostgreSQL(RepositorioPostgreSQLBase):
    TABLA = "linea_investigacion"
    CLAVE = "id"
    COLUMNAS = ("id", "nombre", "descripcion")
    COLUMNAS_CREACION = ("nombre", "descripcion")
