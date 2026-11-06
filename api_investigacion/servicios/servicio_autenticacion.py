from asyncio import to_thread
import secrets

from repositorios.abstracciones.i_repositorio_autenticacion import IRepositorioAutenticacion
from seguridad.interfaces import IClaves, ITokens
from seguridad.errores import AutenticacionFallida, PermisoInsuficiente


class ServicioAutenticacion:
    def __init__(self, repositorio: IRepositorioAutenticacion, claves: IClaves, tokens: ITokens):
        self._repositorio = repositorio
        self._claves = claves
        self._tokens = tokens
        # Cuenta inexistente también recorre una verificación Argon2 real.
        self._resumen_ficticio = claves.crear(secrets.token_urlsafe(32))

    @staticmethod
    def _publico(usuario: dict) -> dict:
        return {campo: usuario[campo] for campo in ('id', 'username', 'email', 'nombre_completo', 'roles')}

    @staticmethod
    def comprobar_permiso(usuario: dict, escritura: bool = False, seguridad: bool = False) -> None:
        roles = set(usuario['roles'])
        if 'administrador' in roles:
            return
        if 'consulta' in roles and not escritura and not seguridad:
            return
        raise PermisoInsuficiente()

    async def login(self, nombre: str, clave: str) -> dict:
        usuario = await self._repositorio.por_nombre(nombre)
        resumen = usuario['password'] if usuario else self._resumen_ficticio
        valido = await to_thread(self._claves.verificar, clave, resumen)
        if not valido or usuario is None or usuario['activo'] is not True:
            raise AutenticacionFallida()
        self.comprobar_permiso(usuario)
        return {'access_token': self._tokens.emitir(usuario['id'], usuario['version_sesion']),
                'token_type': 'bearer', 'expires_in': self._tokens.segundos,
                'usuario': self._publico(usuario)}

    async def _identidad(self, token: str) -> tuple[dict, dict]:
        datos = self._tokens.validar(token)
        usuario = await self._repositorio.por_id(int(datos['sub']))
        if (usuario is None or usuario['activo'] is not True
                or usuario['version_sesion'] != datos['version_sesion']):
            raise AutenticacionFallida()
        return usuario, datos

    async def sesion(self, token: str) -> dict:
        usuario, _ = await self._identidad(token)
        self.comprobar_permiso(usuario)
        return self._publico(usuario)

    async def logout(self, token: str) -> None:
        # Incluso quien perdió todos los roles puede invalidar sus propias sesiones.
        usuario, datos = await self._identidad(token)
        if not await self._repositorio.revocar(usuario['id'], datos['version_sesion']):
            raise AutenticacionFallida()

    async def crear_primero(self, nombre: str, correo: str, clave: str) -> None:
        if not nombre.strip() or len(nombre) > 100 or not correo.strip() or len(correo) > 150:
            raise ValueError('Nombre o correo inválidos.')
        if not 12 <= len(clave) <= 1024:
            raise ValueError('La contraseña debe tener entre 12 y 1024 caracteres.')
        resumen = await to_thread(self._claves.crear, clave)
        await self._repositorio.crear_primero(nombre, correo, resumen)
