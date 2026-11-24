"""Negocio del catálogo de objetivos; las reglas comunes se comparten y su contrato sigue específico."""

from repositorios.abstracciones.i_repositorio_objetivo_desarrollo_sostenible import IRepositorioObjetivoDesarrolloSostenible
from servicios.servicio_base import ServicioBase


class ServicioObjetivoDesarrolloSostenible(ServicioBase):
    def __init__(self, repositorio: IRepositorioObjetivoDesarrolloSostenible):
        super().__init__(repositorio)
