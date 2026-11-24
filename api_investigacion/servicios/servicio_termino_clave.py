"""Negocio de términos clave que conserva la clave natural como texto."""

from repositorios.abstracciones.i_repositorio_termino_clave import IRepositorioTerminoClave
from servicios.servicio_base import ServicioBase


class ServicioTerminoClave(ServicioBase):
    def __init__(self, repositorio: IRepositorioTerminoClave):
        super().__init__(repositorio)
