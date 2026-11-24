"""Repositorio PostgreSQL del catálogo; SQL común y parámetros aislados reducen divergencias."""

from repositorios.repositorio_postgresql_base import RepositorioPostgreSQLBase


class RepositorioAreaConocimientoPostgreSQL(RepositorioPostgreSQLBase):
    TABLA = "area_conocimiento"
    CLAVE = "id"
    COLUMNAS = ("id", "gran_area", "area", "disciplina")
    COLUMNAS_CREACION = COLUMNAS
