"""Repositorio PostgreSQL de objetivos con identidad primaria manual."""

from repositorios.repositorio_postgresql_base import RepositorioPostgreSQLBase


class RepositorioObjetivoDesarrolloSosteniblePostgreSQL(RepositorioPostgreSQLBase):
    TABLA = "objetivo_desarrollo_sostenible"
    CLAVE = "id"
    COLUMNAS = ("id", "nombre", "categoria")
    COLUMNAS_CREACION = COLUMNAS
