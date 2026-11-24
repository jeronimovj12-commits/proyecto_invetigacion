"""Contratos de semilleros; la relación obligatoria se tipa en la frontera antes de consultar la base."""

from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class _Base(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")


class SemilleroCrear(_Base):
    id: int
    nombre: str = Field(min_length=1, max_length=60)
    fecha_fundacion: date = Field(alias="fechaFundacion")
    grupo_investigacion: int = Field(alias="grupoInvestigacion")


class SemilleroReemplazo(_Base):
    nombre: str = Field(min_length=1, max_length=60)
    fecha_fundacion: date = Field(alias="fechaFundacion")
    grupo_investigacion: int = Field(alias="grupoInvestigacion")


class SemilleroActualizar(_Base):
    nombre: str | None = Field(default=None, min_length=1, max_length=60)
    fecha_fundacion: date | None = Field(default=None, alias="fechaFundacion")
    grupo_investigacion: int | None = Field(default=None, alias="grupoInvestigacion")
