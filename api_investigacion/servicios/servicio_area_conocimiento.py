"""Negocio del catálogo de áreas, con repositorio inyectado para no exigir PostgreSQL al probar."""

from repositorios.abstracciones.i_repositorio_area_conocimiento import IRepositorioAreaConocimiento
from servicios.servicio_base import ServicioBase


class ServicioAreaConocimiento(ServicioBase):
    def __init__(self, repositorio: IRepositorioAreaConocimiento):
        super().__init__(repositorio)
