"""Adaptador SQL de docente; la lista blanca de columnas preserva la errata de esquema sin aceptar SQL externo."""

from repositorios.abstracciones.i_repositorio_docente import IRepositorioDocente
from repositorios.repositorio_postgresql_base import RepositorioPostgreSQLBase


class RepositorioDocentePostgreSQL(RepositorioPostgreSQLBase, IRepositorioDocente):
    TABLA = "docente"
    CLAVE = "cedula"
    COLUMNAS = (
        "cedula", "nombres", "apellidos", "genero", "cargo", "fecha_nacimiento",
        "correo", "telefono", "url_cvlac", "fecha_actualizacion", "escalafon",
        "perfil", "cat_minciencia", "conv_minciencia", "nacionalidaad",
        "linea_investigacion_principal",
    )
    COLUMNAS_CREACION = COLUMNAS
