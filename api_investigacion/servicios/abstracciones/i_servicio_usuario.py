"""La interfaz de usuario separa autenticación del transporte HTTP."""

from typing import Protocol

from servicios.abstracciones.i_servicio_base import IServicioBase


class IServicioUsuario(IServicioBase, Protocol):
    async def autenticar(self, username: str, password: str) -> dict | None: ...
    async def obtener_identidad_activa(self, usuario_id: int) -> dict | None: ...
    async def sembrar_datos_iniciales(self, roles: list[dict], usuarios: list[dict]) -> None: ...
