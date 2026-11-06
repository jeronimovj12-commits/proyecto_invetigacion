from pydantic import BaseModel, ConfigDict, Field, SecretStr


class Login(BaseModel):
    model_config = ConfigDict(extra='forbid')
    username: str = Field(min_length=1, max_length=100)
    password: SecretStr = Field(min_length=1, max_length=1024)


class UsuarioSesion(BaseModel):
    id: int
    username: str
    email: str
    nombre_completo: str | None
    roles: list[str]


class TokenSesion(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    usuario: UsuarioSesion


class SesionCerrada(BaseModel):
    estado: int = 200
    mensaje: str = 'Sesión cerrada en todos los dispositivos.'
