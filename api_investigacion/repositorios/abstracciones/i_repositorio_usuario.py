"""Las operaciones de autenticación exponen la clave solo al servicio, nunca al controlador."""

from typing import Protocol

from repositorios.abstracciones.i_repositorio_base import IRepositorioBase


class IRepositorioUsuario(IRepositorioBase, Protocol):
    async def obtener_por_username(self, username: str) -> dict | None: ...
    async def obtener_roles_activos(self, usuario_id: int) -> list[str]: ...
    async def sembrar_datos_iniciales(self, roles: list[dict], usuarios: list[dict]) -> None: ...
