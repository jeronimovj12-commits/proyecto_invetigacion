"""Contratos de líneas; se omite la clave al crear porque PostgreSQL la genera."""

from pydantic import BaseModel, ConfigDict, Field


class _Base(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")


class LineaInvestigacionCrear(_Base):
    nombre: str = Field(min_length=1, max_length=45)
    descripcion: str = Field(min_length=1, max_length=256)


class LineaInvestigacionReemplazo(_Base):
    nombre: str = Field(min_length=1, max_length=45)
    descripcion: str = Field(min_length=1, max_length=256)


class LineaInvestigacionActualizar(_Base):
    nombre: str | None = Field(default=None, min_length=1, max_length=45)
    descripcion: str | None = Field(default=None, min_length=1, max_length=256)
