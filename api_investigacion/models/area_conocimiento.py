"""Contratos de entrada de áreas; separar verbos permite que PUT sea íntegro y PATCH parcial."""

from pydantic import BaseModel, ConfigDict, Field


class _Base(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")


class AreaConocimientoCrear(_Base):
    id: str = Field(min_length=1, max_length=6)
    gran_area: str = Field(alias="granArea", min_length=1, max_length=60)
    area: str = Field(min_length=1, max_length=60)
    disciplina: str = Field(min_length=1, max_length=150)


class AreaConocimientoReemplazo(_Base):
    gran_area: str = Field(alias="granArea", min_length=1, max_length=60)
    area: str = Field(min_length=1, max_length=60)
    disciplina: str = Field(min_length=1, max_length=150)


class AreaConocimientoActualizar(_Base):
    gran_area: str | None = Field(default=None, alias="granArea", min_length=1, max_length=60)
    area: str | None = Field(default=None, min_length=1, max_length=60)
    disciplina: str | None = Field(default=None, min_length=1, max_length=150)
