"""Contratos de participación en grupos; la clave compuesta se identifica en la ruta y el POST."""

from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class _Base(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")


class ParticipaGrupoCrear(_Base):
    docente_cedula: int = Field(alias="docenteCedula")
    grupo_investigacion_id: int = Field(alias="grupoInvestigacionId")
    rol: str = Field(min_length=1, max_length=15)
    fecha_inicio: date = Field(alias="fechaInicio")
    fecha_fin: date | None = Field(default=None, alias="fechaFin")


class ParticipaGrupoReemplazo(_Base):
    rol: str = Field(min_length=1, max_length=15)
    fecha_inicio: date = Field(alias="fechaInicio")
    fecha_fin: date | None = Field(alias="fechaFin")


class ParticipaGrupoActualizar(_Base):
    rol: str | None = Field(default=None, min_length=1, max_length=15)
    fecha_inicio: date | None = Field(default=None, alias="fechaInicio")
    fecha_fin: date | None = Field(default=None, alias="fechaFin")
