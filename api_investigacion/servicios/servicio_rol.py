"""La validación de cambios se mantiene en negocio y no en el controlador."""

from repositorios.abstracciones.i_repositorio_rol import IRepositorioRol
from servicios.abstracciones.i_servicio_rol import IServicioRol
from servicios.servicio_base import ServicioBase


class ServicioRol(ServicioBase, IServicioRol):
    def __init__(self, repositorio: IRepositorioRol):
        super().__init__(repositorio)

    async def actualizar(self, identificador: str | int, datos: dict) -> int:
        if "nombre" in datos and datos["nombre"] is None:
            raise ValueError("El nombre del rol no puede estar vacío.")
        return await super().actualizar(identificador, datos)
