"""Negocio de líneas; delega la generación automática de clave al adaptador de datos."""

from repositorios.abstracciones.i_repositorio_linea_investigacion import IRepositorioLineaInvestigacion
from servicios.servicio_base import ServicioBase


class ServicioLineaInvestigacion(ServicioBase):
    def __init__(self, repositorio: IRepositorioLineaInvestigacion):
        super().__init__(repositorio)
