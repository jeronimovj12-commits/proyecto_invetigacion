"""La contraseña solo aparece en modelos de entrada y no en contratos de lectura."""

from pydantic import BaseModel, ConfigDict, Field


class _Base(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")


class UsuarioCrear(_Base):
    username: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=8, max_length=72)
    email: str = Field(min_length=1, max_length=150)
    nombre_completo: str | None = Field(default=None, alias="nombreCompleto", max_length=200)


class UsuarioReemplazo(_Base):
    username: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=8, max_length=72)
    email: str = Field(min_length=1, max_length=150)
    nombre_completo: str | None = Field(alias="nombreCompleto", max_length=200)


class UsuarioActualizar(_Base):
    username: str | None = Field(default=None, min_length=1, max_length=100)
    password: str | None = Field(default=None, min_length=8, max_length=72)
    email: str | None = Field(default=None, min_length=1, max_length=150)
    nombre_completo: str | None = Field(default=None, alias="nombreCompleto", max_length=200)
