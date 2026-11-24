"""Contratos de entrada de áreas de aplicación con límites iguales al esquema SQL."""

from pydantic import BaseModel, ConfigDict, Field


class _Base(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")


class AreaAplicacionCrear(_Base):
    id: int
    nombre: str = Field(min_length=1, max_length=150)


class AreaAplicacionReemplazo(_Base):
    nombre: str = Field(min_length=1, max_length=150)


class AreaAplicacionActualizar(_Base):
    nombre: str | None = Field(default=None, min_length=1, max_length=150)
