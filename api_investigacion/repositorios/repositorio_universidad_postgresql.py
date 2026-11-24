"""Repositorio PostgreSQL de universidades con columnas constantes y valores parametrizados."""

from repositorios.repositorio_postgresql_base import RepositorioPostgreSQLBase


class RepositorioUniversidadPostgreSQL(RepositorioPostgreSQLBase):
    TABLA = "universidad"
    CLAVE = "id"
    COLUMNAS = ("id", "nombre", "tipo", "ciudad")
    COLUMNAS_CREACION = COLUMNAS
