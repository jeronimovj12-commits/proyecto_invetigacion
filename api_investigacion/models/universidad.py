"""Contratos de universidades con campos completos en PUT y opcionales en PATCH."""

from pydantic import BaseModel, ConfigDict, Field


class _Base(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")


class UniversidadCrear(_Base):
    id: int
    nombre: str = Field(min_length=1, max_length=60)
    tipo: str = Field(min_length=1, max_length=45)
    ciudad: str = Field(min_length=1, max_length=45)


class UniversidadReemplazo(_Base):
    nombre: str = Field(min_length=1, max_length=60)
    tipo: str = Field(min_length=1, max_length=45)
    ciudad: str = Field(min_length=1, max_length=45)


class UniversidadActualizar(_Base):
    nombre: str | None = Field(default=None, min_length=1, max_length=60)
    tipo: str | None = Field(default=None, min_length=1, max_length=45)
    ciudad: str | None = Field(default=None, min_length=1, max_length=45)
