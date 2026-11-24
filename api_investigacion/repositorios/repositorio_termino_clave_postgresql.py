"""Repositorio PostgreSQL de términos; la clave textual se conserva en las consultas parametrizadas."""

from repositorios.repositorio_postgresql_base import RepositorioPostgreSQLBase


class RepositorioTerminoClavePostgreSQL(RepositorioPostgreSQLBase):
    TABLA = "termino_clave"
    CLAVE = "termino"
    COLUMNAS = ("termino", "termino_ingles")
    COLUMNAS_CREACION = COLUMNAS
