"""Reglas de semillero delegan integridad de la relación al motor y mantienen errores de negocio independientes."""

from repositorios.abstracciones.i_repositorio_semillero import IRepositorioSemillero
from servicios.servicio_base import ServicioBase


class ServicioSemillero(ServicioBase):
    def __init__(self, repositorio: IRepositorioSemillero):
        super().__init__(repositorio)

    async def crear(self, datos: dict) -> int | None:
        resultado = await super().crear(datos)
        return resultado if isinstance(resultado, int) else None
