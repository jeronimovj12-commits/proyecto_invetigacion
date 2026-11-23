# Ejecuta la instruccion indicada dentro del flujo actual.
"""Servicio de negocio: coordina las reglas del caso de uso con los repositorios sin ejecutar SQL directamente."""
# Importa to_thread desde asyncio para usar esas definiciones.
from asyncio import to_thread
# Carga el modulo o los modulos secrets.
import secrets

# Importa IRepositorioAutenticacion desde repositorios.abstracciones.i_repositorio_autenticacion para usar esas definiciones.
from repositorios.abstracciones.i_repositorio_autenticacion import IRepositorioAutenticacion
# Importa IClaves, ITokens desde seguridad.interfaces para usar esas definiciones.
from seguridad.interfaces import IClaves, ITokens
# Importa AutenticacionFallida, PermisoInsuficiente desde seguridad.errores para usar esas definiciones.
from seguridad.errores import AutenticacionFallida, PermisoInsuficiente


# Define la clase ServicioAutenticacion y agrupa su estado y operaciones.
class ServicioAutenticacion:
    # Define la funcion __init__ con los parametros declarados; su bloque realiza esta operacion.
    def __init__(self, repositorio: IRepositorioAutenticacion, claves: IClaves, tokens: ITokens):
        # Guarda en self._repositorio el valor necesario para reutilizarlo en otros metodos.
        self._repositorio = repositorio
        # Guarda en self._claves el valor necesario para reutilizarlo en otros metodos.
        self._claves = claves
        # Guarda en self._tokens el valor necesario para reutilizarlo en otros metodos.
        self._tokens = tokens
        # Cuenta inexistente también recorre una verificación Argon2 real.
        # El tiempo de login no revela si el nombre consultado existe.
        # Guarda en self._resumen_ficticio el valor necesario para reutilizarlo en otros metodos.
        self._resumen_ficticio = claves.crear(secrets.token_urlsafe(32))

    # Aplica @staticmethod a la declaracion que sigue; en rutas, registra el endpoint HTTP.
    @staticmethod
    # Define la funcion _publico con los parametros declarados; su bloque realiza esta operacion.
    def _publico(usuario: dict) -> dict:
        # Devuelve al llamador el resultado de la expresion indicada.
        return {campo: usuario[campo] for campo in ('id', 'username', 'email', 'nombre_completo', 'roles')}

    # Aplica @staticmethod a la declaracion que sigue; en rutas, registra el endpoint HTTP.
    @staticmethod
    # Define la funcion comprobar_permiso con los parametros declarados; su bloque realiza esta operacion.
    def comprobar_permiso(usuario: dict, escritura: bool = False, seguridad: bool = False) -> None:
        # Consulta puede leer; administrador puede operar y administrar seguridad.
        # Asigna a roles el valor calculado a la derecha.
        roles = set(usuario['roles'])
        # Ejecuta el bloque siguiente solo cuando se cumple: 'administrador' in roles.
        if 'administrador' in roles:
            # Termina la funcion sin devolver un valor.
            return
        # Ejecuta el bloque siguiente solo cuando se cumple: 'consulta' in roles and not escritura and not seguridad.
        if 'consulta' in roles and not escritura and not seguridad:
            # Termina la funcion sin devolver un valor.
            return
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise PermisoInsuficiente()

    # Define la funcion login con los parametros declarados; su bloque realiza esta operacion.
    async def login(self, nombre: str, clave: str) -> dict:
        # Asigna a usuario el valor calculado a la derecha.
        usuario = await self._repositorio.por_nombre(nombre)
        # Asigna a resumen el valor calculado a la derecha.
        resumen = usuario['password'] if usuario else self._resumen_ficticio
        # Argon2 consume CPU; to_thread evita bloquear el ciclo asincronico de la API.
        # Asigna a valido el valor calculado a la derecha.
        valido = await to_thread(self._claves.verificar, clave, resumen)
        # Ejecuta el bloque siguiente solo cuando se cumple: not valido or usuario is None or usuario['activo'] is not True.
        if not valido or usuario is None or usuario['activo'] is not True:
            # Lanza la excepcion indicada y detiene el flujo normal.
            raise AutenticacionFallida()
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.comprobar_permiso(usuario)
        # Devuelve al llamador el resultado de la expresion indicada.
        return {'access_token': self._tokens.emitir(usuario['id'], usuario['version_sesion']),
                # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                'token_type': 'bearer', 'expires_in': self._tokens.segundos,
                # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                'usuario': self._publico(usuario)}

    # Define la funcion _identidad con los parametros declarados; su bloque realiza esta operacion.
    async def _identidad(self, token: str) -> tuple[dict, dict]:
        # Asigna a datos el valor calculado a la derecha.
        datos = self._tokens.validar(token)
        # Asigna a usuario el valor calculado a la derecha.
        usuario = await self._repositorio.por_id(int(datos['sub']))
        # Incrementar version_sesion invalida los JWT emitidos antes del cambio.
        # Ejecuta el bloque siguiente solo cuando se cumple: (usuario is None or usuario['activo'] is not True.
        if (usuario is None or usuario['activo'] is not True
                # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                or usuario['version_sesion'] != datos['version_sesion']):
            # Lanza la excepcion indicada y detiene el flujo normal.
            raise AutenticacionFallida()
        # Devuelve al llamador el resultado de la expresion indicada.
        return usuario, datos

    # Define la funcion sesion con los parametros declarados; su bloque realiza esta operacion.
    async def sesion(self, token: str) -> dict:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        usuario, _ = await self._identidad(token)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.comprobar_permiso(usuario)
        # Devuelve al llamador el resultado de la expresion indicada.
        return self._publico(usuario)

    # Define la funcion logout con los parametros declarados; su bloque realiza esta operacion.
    async def logout(self, token: str) -> None:
        # Incluso quien perdió todos los roles puede invalidar sus propias sesiones.
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        usuario, datos = await self._identidad(token)
        # Ejecuta el bloque siguiente solo cuando se cumple: not await self._repositorio.revocar(usuario['id'], datos['version_sesion']).
        if not await self._repositorio.revocar(usuario['id'], datos['version_sesion']):
            # Lanza la excepcion indicada y detiene el flujo normal.
            raise AutenticacionFallida()

    # Define la funcion crear_primero con los parametros declarados; su bloque realiza esta operacion.
    async def crear_primero(self, nombre: str, correo: str, clave: str) -> None:
        # Ejecuta el bloque siguiente solo cuando se cumple: not nombre.strip() or len(nombre) > 100 or not correo.strip() or len(correo) > 150.
        if not nombre.strip() or len(nombre) > 100 or not correo.strip() or len(correo) > 150:
            # Lanza la excepcion indicada y detiene el flujo normal.
            raise ValueError('Nombre o correo inválidos.')
        # Ejecuta el bloque siguiente solo cuando se cumple: not 12 <= len(clave) <= 1024.
        if not 12 <= len(clave) <= 1024:
            # Lanza la excepcion indicada y detiene el flujo normal.
            raise ValueError('La contraseña debe tener entre 12 y 1024 caracteres.')
        # Asigna a resumen el valor calculado a la derecha.
        resumen = await to_thread(self._claves.crear, clave)
        # Espera que termine la operacion asincronica antes de continuar.
        await self._repositorio.crear_primero(nombre, correo, resumen)
