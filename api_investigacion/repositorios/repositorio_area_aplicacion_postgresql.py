"""Repositorio PostgreSQL de áreas de aplicación con SQL compartido y claves fijas."""

from repositorios.repositorio_postgresql_base import RepositorioPostgreSQLBase


class RepositorioAreaAplicacionPostgreSQL(RepositorioPostgreSQLBase):
    TABLA = "area_aplicacion"
    CLAVE = "id"
    COLUMNAS = ("id", "nombre")
    COLUMNAS_CREACION = COLUMNAS
