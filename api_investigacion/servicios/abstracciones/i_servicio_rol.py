"""El contrato permite compartir la política CRUD sin revelar SQL al controlador."""

from typing import Protocol

from servicios.abstracciones.i_servicio_base import IServicioBase


class IServicioRol(IServicioBase, Protocol):
    pass
