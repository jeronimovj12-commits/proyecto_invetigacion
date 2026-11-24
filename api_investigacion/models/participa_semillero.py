"""Contratos de participación en semilleros; Pydantic hace obligatorios ambos componentes de la clave."""

from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class _Base(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")


class ParticipaSemilleroCrear(_Base):
    docente: int
    semillero: int
    rol: str = Field(min_length=1, max_length=15)
    fecha_inicio: date = Field(alias="fechaInicio")
    fecha_fin: date | None = Field(default=None, alias="fechaFin")


class ParticipaSemilleroReemplazo(_Base):
    rol: str = Field(min_length=1, max_length=15)
    fecha_inicio: date = Field(alias="fechaInicio")
    fecha_fin: date | None = Field(alias="fechaFin")


class ParticipaSemilleroActualizar(_Base):
    rol: str | None = Field(default=None, min_length=1, max_length=15)
    fecha_inicio: date | None = Field(default=None, alias="fechaInicio")
    fecha_fin: date | None = Field(default=None, alias="fechaFin")
