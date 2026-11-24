"""El protocolo mantiene el servicio de roles independiente del adaptador PostgreSQL."""

from typing import Protocol

from repositorios.abstracciones.i_repositorio_base import IRepositorioBase


class IRepositorioRol(IRepositorioBase, Protocol):
    pass
