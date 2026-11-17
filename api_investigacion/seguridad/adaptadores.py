# Ejecuta la instruccion indicada dentro del flujo actual.
"""Argon2 y JWT delegados a bibliotecas; nunca criptografía propia."""
# Carga el modulo o los modulos os.
import os
# Importa dataclass, field desde dataclasses para usar esas definiciones.
from dataclasses import dataclass, field
# Importa datetime, timezone desde datetime para usar esas definiciones.
from datetime import datetime, timezone

# Carga el modulo o los modulos jwt.
import jwt
# Importa PasswordHash desde pwdlib para usar esas definiciones.
from pwdlib import PasswordHash
# Importa UnknownHashError desde pwdlib.exceptions para usar esas definiciones.
from pwdlib.exceptions import UnknownHashError

# Importa AutenticacionFallida desde seguridad.errores para usar esas definiciones.
from seguridad.errores import AutenticacionFallida


# Aplica @dataclass a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@dataclass(frozen=True)
# Define la clase ConfiguracionSeguridad y agrupa su estado y operaciones.
class ConfiguracionSeguridad:
    # Asigna a secreto el valor calculado a la derecha.
    secreto: str = field(repr=False)
    # Asigna a emisor el valor calculado a la derecha.
    emisor: str
    # Asigna a audiencia el valor calculado a la derecha.
    audiencia: str
    # Asigna a minutos el valor calculado a la derecha.
    minutos: int = 30

    # Define la funcion __post_init__ con los parametros declarados; su bloque realiza esta operacion.
    def __post_init__(self):
        # Ejecuta el bloque siguiente solo cuando se cumple: len(self.secreto.encode()) < 32 or self.secreto.startswith('REEMPLAZAR').
        if len(self.secreto.encode()) < 32 or self.secreto.startswith('REEMPLAZAR'):
            # Lanza la excepcion indicada y detiene el flujo normal.
            raise ValueError('JWT_SECRET debe ser un secreto externo aleatorio de al menos 32 bytes.')
        # Ejecuta el bloque siguiente solo cuando se cumple: not self.emisor or not self.audiencia or not 1 <= self.minutos <= 1440.
        if not self.emisor or not self.audiencia or not 1 <= self.minutos <= 1440:
            # Lanza la excepcion indicada y detiene el flujo normal.
            raise ValueError('Emisor, audiencia o duración JWT inválidos.')

    # Aplica @classmethod a la declaracion que sigue; en rutas, registra el endpoint HTTP.
    @classmethod
    # Define la funcion desde_entorno con los parametros declarados; su bloque realiza esta operacion.
    def desde_entorno(cls):
        # Inicia un bloque cuya excepcion se manejara en los except siguientes.
        try:
            # Devuelve al llamador el resultado de la expresion indicada.
            return cls(os.environ['JWT_SECRET'], os.environ['JWT_ISSUER'],
                       # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                       os.environ['JWT_AUDIENCE'], int(os.environ.get('JWT_MINUTOS', '30')))
        # Captura la excepcion indicada para manejarla sin dejarla propagarse.
        except (KeyError, ValueError):
            # Lanza la excepcion indicada y detiene el flujo normal.
            raise RuntimeError('Configuración externa de seguridad ausente o inválida.') from None


# Define la clase ClavesArgon2 y agrupa su estado y operaciones.
class ClavesArgon2:
    # Define la funcion __init__ con los parametros declarados; su bloque realiza esta operacion.
    def __init__(self):
        # Guarda en self._claves el valor necesario para reutilizarlo en otros metodos.
        self._claves = PasswordHash.recommended()

    # Define la funcion crear con los parametros declarados; su bloque realiza esta operacion.
    def crear(self, clave: str) -> str:
        # Devuelve al llamador el resultado de la expresion indicada.
        return self._claves.hash(clave)

    # Define la funcion verificar con los parametros declarados; su bloque realiza esta operacion.
    def verificar(self, clave: str, resumen: str) -> bool:
        # No se aceptan hashes legados o texto plano por accidente.
        # Ejecuta el bloque siguiente solo cuando se cumple: not resumen.startswith('$argon2id$').
        if not resumen.startswith('$argon2id$'):
            # Devuelve al llamador el resultado de la expresion indicada.
            return False
        # Inicia un bloque cuya excepcion se manejara en los except siguientes.
        try:
            # Devuelve al llamador el resultado de la expresion indicada.
            return self._claves.verify(clave, resumen)
        # Captura la excepcion indicada para manejarla sin dejarla propagarse.
        except (UnknownHashError, ValueError):
            # Devuelve al llamador el resultado de la expresion indicada.
            return False


# Define la clase TokensJWT y agrupa su estado y operaciones.
class TokensJWT:
    # Define la funcion __init__ con los parametros declarados; su bloque realiza esta operacion.
    def __init__(self, configuracion: ConfiguracionSeguridad):
        # Guarda en self._config el valor necesario para reutilizarlo en otros metodos.
        self._config = configuracion
        # Guarda en self.segundos el valor necesario para reutilizarlo en otros metodos.
        self.segundos = configuracion.minutos * 60

    # Define la funcion emitir con los parametros declarados; su bloque realiza esta operacion.
    def emitir(self, usuario_id: int, version: int) -> str:
        # Asigna a ahora el valor calculado a la derecha.
        ahora = int(datetime.now(timezone.utc).timestamp())
        # La version permite revocar los JWT anteriores sin guardar cada token.
        # Devuelve al llamador el resultado de la expresion indicada.
        return jwt.encode({'sub': str(usuario_id), 'version_sesion': version,
                           # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                           'iat': ahora, 'exp': ahora + self.segundos,
                           # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                           'iss': self._config.emisor, 'aud': self._config.audiencia},
                          # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                          self._config.secreto, algorithm='HS256')

    # Define la funcion validar con los parametros declarados; su bloque realiza esta operacion.
    def validar(self, token: str) -> dict:
        # Inicia un bloque cuya excepcion se manejara en los except siguientes.
        try:
            # La biblioteca valida firma, algoritmo, emisor, audiencia y vencimiento.
            # Asigna a datos el valor calculado a la derecha.
            datos = jwt.decode(token, self._config.secreto, algorithms=['HS256'],
                               # Asigna a issuer el valor calculado a la derecha.
                               issuer=self._config.emisor, audience=self._config.audiencia,
                               # Asigna a options el valor calculado a la derecha.
                               options={'require': ['sub', 'version_sesion', 'iat', 'exp', 'iss', 'aud'],
                                        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                                        'strict_aud': True})
            # Tambien se revisan tipos y limites de los claims que consume la aplicacion.
            # Ejecuta el bloque siguiente solo cuando se cumple: (not isinstance(datos['sub'], str) or not datos['sub'].isascii().
            if (not isinstance(datos['sub'], str) or not datos['sub'].isascii()
                    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                    or not datos['sub'].isdigit() or not 0 < int(datos['sub']) <= 2147483647
                    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                    or type(datos['version_sesion']) is not int or datos['version_sesion'] < 0
                    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                    or type(datos['iat']) is not int or type(datos['exp']) is not int
                    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                    or datos['exp'] <= datos['iat'] or datos['exp'] - datos['iat'] > self.segundos):
                # Lanza la excepcion indicada y detiene el flujo normal.
                raise AutenticacionFallida()
            # Devuelve al llamador el resultado de la expresion indicada.
            return datos
        # Captura la excepcion indicada para manejarla sin dejarla propagarse.
        except jwt.InvalidTokenError:
            # Lanza la excepcion indicada y detiene el flujo normal.
            raise AutenticacionFallida() from None
