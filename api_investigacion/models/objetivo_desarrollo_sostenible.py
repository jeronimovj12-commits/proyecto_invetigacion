"""Contratos de entrada ODS; esquemas separados expresan el reemplazo y el cambio parcial."""

from pydantic import BaseModel, ConfigDict, Field


class _Base(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")


class ObjetivoDesarrolloSostenibleCrear(_Base):
    id: int
    nombre: str = Field(min_length=1, max_length=60)
    categoria: str = Field(min_length=1, max_length=45)


class ObjetivoDesarrolloSostenibleReemplazo(_Base):
    nombre: str = Field(min_length=1, max_length=60)
    categoria: str = Field(min_length=1, max_length=45)


class ObjetivoDesarrolloSostenibleActualizar(_Base):
    nombre: str | None = Field(default=None, min_length=1, max_length=60)
    categoria: str | None = Field(default=None, min_length=1, max_length=45)
