"""Negocio de áreas de aplicación; la interfaz inyectada permite una prueba aislada del motor."""

from repositorios.abstracciones.i_repositorio_area_aplicacion import IRepositorioAreaAplicacion
from servicios.servicio_base import ServicioBase


class ServicioAreaAplicacion(ServicioBase):
    def __init__(self, repositorio: IRepositorioAreaAplicacion):
        super().__init__(repositorio)
