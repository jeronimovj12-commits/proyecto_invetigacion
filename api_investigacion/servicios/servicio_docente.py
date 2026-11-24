"""Reglas de docente permanecen desacopladas porque el repositorio se inyecta por contrato."""

from repositorios.abstracciones.i_repositorio_docente import IRepositorioDocente
from servicios.servicio_base import ServicioBase


class ServicioDocente(ServicioBase):
    def __init__(self, repositorio: IRepositorioDocente):
        super().__init__(repositorio)

    async def crear(self, datos: dict) -> int | None:
        resultado = await super().crear(datos)
        return resultado if isinstance(resultado, int) else None
