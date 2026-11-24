"""Reglas de grupos usan el contrato del repositorio para permitir pruebas sin datos persistentes."""

from repositorios.abstracciones.i_repositorio_grupo_investigacion import IRepositorioGrupoInvestigacion
from servicios.servicio_base import ServicioBase


class ServicioGrupoInvestigacion(ServicioBase):
    def __init__(self, repositorio: IRepositorioGrupoInvestigacion):
        super().__init__(repositorio)

    async def crear(self, datos: dict) -> int | None:
        resultado = await super().crear(datos)
        return resultado if isinstance(resultado, int) else None
