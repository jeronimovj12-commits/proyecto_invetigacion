"""El repositorio hereda SQL parametrizado con filtro activo del adaptador base."""

from repositorios.abstracciones.i_repositorio_rol import IRepositorioRol
from repositorios.repositorio_postgresql_base import RepositorioPostgreSQLBase


class RepositorioRolPostgreSQL(RepositorioPostgreSQLBase, IRepositorioRol):
    TABLA = "rol"
    CLAVE = "id"
    COLUMNAS = ("id", "nombre", "descripcion", "fecha_creacion")
    COLUMNAS_CREACION = ("nombre", "descripcion")
