"""Adaptador SQL de semilleros; la FK obligatoria se deja a la restricción referencial de PostgreSQL."""

from repositorios.abstracciones.i_repositorio_semillero import IRepositorioSemillero
from repositorios.repositorio_postgresql_base import RepositorioPostgreSQLBase


class RepositorioSemilleroPostgreSQL(RepositorioPostgreSQLBase, IRepositorioSemillero):
    TABLA = "semillero"
    CLAVE = "id"
    COLUMNAS = ("id", "nombre", "fecha_fundacion", "grupo_investigacion")
    COLUMNAS_CREACION = COLUMNAS
