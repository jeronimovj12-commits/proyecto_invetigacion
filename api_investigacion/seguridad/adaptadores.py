"""Argon2 y JWT delegados a bibliotecas; nunca criptografía propia."""
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone

import jwt
from pwdlib import PasswordHash
from pwdlib.exceptions import UnknownHashError

from seguridad.errores import AutenticacionFallida


@dataclass(frozen=True)
class ConfiguracionSeguridad:
    secreto: str = field(repr=False)
    emisor: str
    audiencia: str
    minutos: int = 30

    def __post_init__(self):
        if len(self.secreto.encode()) < 32 or self.secreto.startswith('REEMPLAZAR'):
            raise ValueError('JWT_SECRET debe ser un secreto externo aleatorio de al menos 32 bytes.')
        if not self.emisor or not self.audiencia or not 1 <= self.minutos <= 1440:
            raise ValueError('Emisor, audiencia o duración JWT inválidos.')

    @classmethod
    def desde_entorno(cls):
        try:
            return cls(os.environ['JWT_SECRET'], os.environ['JWT_ISSUER'],
                       os.environ['JWT_AUDIENCE'], int(os.environ.get('JWT_MINUTOS', '30')))
        except (KeyError, ValueError):
            raise RuntimeError('Configuración externa de seguridad ausente o inválida.') from None


class ClavesArgon2:
    def __init__(self):
        self._claves = PasswordHash.recommended()

    def crear(self, clave: str) -> str:
        return self._claves.hash(clave)

    def verificar(self, clave: str, resumen: str) -> bool:
        # No se aceptan hashes legados o texto plano por accidente.
        if not resumen.startswith('$argon2id$'):
            return False
        try:
            return self._claves.verify(clave, resumen)
        except (UnknownHashError, ValueError):
            return False


class TokensJWT:
    def __init__(self, configuracion: ConfiguracionSeguridad):
        self._config = configuracion
        self.segundos = configuracion.minutos * 60

    def emitir(self, usuario_id: int, version: int) -> str:
        ahora = int(datetime.now(timezone.utc).timestamp())
        return jwt.encode({'sub': str(usuario_id), 'version_sesion': version,
                           'iat': ahora, 'exp': ahora + self.segundos,
                           'iss': self._config.emisor, 'aud': self._config.audiencia},
                          self._config.secreto, algorithm='HS256')

    def validar(self, token: str) -> dict:
        try:
            datos = jwt.decode(token, self._config.secreto, algorithms=['HS256'],
                               issuer=self._config.emisor, audience=self._config.audiencia,
                               options={'require': ['sub', 'version_sesion', 'iat', 'exp', 'iss', 'aud'],
                                        'strict_aud': True})
            if (not isinstance(datos['sub'], str) or not datos['sub'].isascii()
                    or not datos['sub'].isdigit() or not 0 < int(datos['sub']) <= 2147483647
                    or type(datos['version_sesion']) is not int or datos['version_sesion'] < 0
                    or type(datos['iat']) is not int or type(datos['exp']) is not int
                    or datos['exp'] <= datos['iat'] or datos['exp'] - datos['iat'] > self.segundos):
                raise AutenticacionFallida()
            return datos
        except jwt.InvalidTokenError:
            raise AutenticacionFallida() from None
