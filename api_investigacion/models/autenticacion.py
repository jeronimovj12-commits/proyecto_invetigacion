# Ejecuta la instruccion indicada dentro del flujo actual.
"""Modelos Pydantic: declaran la forma y las restricciones de los datos que entran o salen de la API."""
# Importa BaseModel, ConfigDict, Field, SecretStr desde pydantic para usar esas definiciones.
from pydantic import BaseModel, ConfigDict, Field, SecretStr


# Define la clase Login y agrupa su estado y operaciones.
class Login(BaseModel):
    # Asigna a model_config el valor calculado a la derecha.
    model_config = ConfigDict(extra='forbid')
    # Declara el campo username y configura en Field el alias o limites que debe validar.
    username: str = Field(min_length=1, max_length=100)
    # Declara el campo password y configura en Field el alias o limites que debe validar.
    password: SecretStr = Field(min_length=1, max_length=1024)


# Define la clase UsuarioSesion y agrupa su estado y operaciones.
class UsuarioSesion(BaseModel):
    # Asigna a id el valor calculado a la derecha.
    id: int
    # Asigna a username el valor calculado a la derecha.
    username: str
    # Asigna a email el valor calculado a la derecha.
    email: str
    # Asigna a nombre_completo el valor calculado a la derecha.
    nombre_completo: str | None
    # Asigna a roles el valor calculado a la derecha.
    roles: list[str]


# Define la clase TokenSesion y agrupa su estado y operaciones.
class TokenSesion(BaseModel):
    # Asigna a access_token el valor calculado a la derecha.
    access_token: str
    # Asigna a token_type el valor calculado a la derecha.
    token_type: str
    # Asigna a expires_in el valor calculado a la derecha.
    expires_in: int
    # Asigna a usuario el valor calculado a la derecha.
    usuario: UsuarioSesion


# Define la clase SesionCerrada y agrupa su estado y operaciones.
class SesionCerrada(BaseModel):
    # Asigna a estado el valor calculado a la derecha.
    estado: int = 200
    # Asigna a mensaje el valor calculado a la derecha.
    mensaje: str = 'Sesión cerrada en todos los dispositivos.'
