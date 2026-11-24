"""El servicio hashea cada contraseña antes de que el repositorio reciba datos."""

from repositorios.abstracciones.i_repositorio_usuario import IRepositorioUsuario
from seguridad.jwt_handler import hashear_contrasena, verificar_contrasena
from servicios.abstracciones.i_servicio_usuario import IServicioUsuario
from servicios.servicio_base import ServicioBase


class ServicioUsuario(ServicioBase, IServicioUsuario):
    def __init__(self, repositorio: IRepositorioUsuario):
        super().__init__(repositorio)
        self._repositorio_usuario = repositorio

    async def crear(self, datos: dict) -> int:
        datos_seguros = dict(datos)
        datos_seguros["password"] = hashear_contrasena(datos_seguros["password"])
        identificador = await self._repositorio_usuario.crear(datos_seguros)
        return int(identificador)

    async def actualizar(self, identificador: str | int, datos: dict) -> int:
        cambios = dict(datos)
        if cambios.get("username") is None and "username" in cambios:
            raise ValueError("El nombre de usuario no puede estar vacío.")
        if cambios.get("email") is None and "email" in cambios:
            raise ValueError("El correo no puede estar vacío.")
        if "password" in cambios:
            if cambios["password"] is None:
                cambios.pop("password")
            else:
                cambios["password"] = hashear_contrasena(cambios["password"])
        return await super().actualizar(identificador, cambios)

    async def autenticar(self, username: str, password: str) -> dict | None:
        registro = await self._repositorio_usuario.obtener_por_username(username)
        if registro is None or not registro["activo"]:
            return None
        if not verificar_contrasena(password, registro["password"]):
            return None
        return {
            "id": registro["id"],
            "username": registro["username"],
            "email": registro["email"],
            "nombre_completo": registro["nombre_completo"],
            "roles": await self._repositorio_usuario.obtener_roles_activos(registro["id"]),
        }

    async def obtener_identidad_activa(self, usuario_id: int) -> dict | None:
        try:
            usuario = await self._repositorio_usuario.obtener_por_id(usuario_id)
        except LookupError:
            return None
        return {
            **usuario,
            "roles": await self._repositorio_usuario.obtener_roles_activos(usuario_id),
        }

    async def sembrar_datos_iniciales(self, roles: list[dict], usuarios: list[dict]) -> None:
        cuentas = []
        for usuario in usuarios:
            cuenta = dict(usuario)
            cuenta["password"] = hashear_contrasena(cuenta["password"])
            cuentas.append(cuenta)
        await self._repositorio_usuario.sembrar_datos_iniciales(roles, cuentas)
