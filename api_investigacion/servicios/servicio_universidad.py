"""Negocio de universidades separado de HTTP y del motor por inyección de interfaz."""

from repositorios.abstracciones.i_repositorio_universidad import IRepositorioUniversidad
from servicios.servicio_base import ServicioBase


class ServicioUniversidad(ServicioBase):
    def __init__(self, repositorio: IRepositorioUniversidad):
        super().__init__(repositorio)
