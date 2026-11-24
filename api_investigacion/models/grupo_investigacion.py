"""Contratos de grupos de investigación; se mantiene la errata SQL y se ofrece un alias claro al cliente."""

from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class _Base(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")


class GrupoInvestigacionCrear(_Base):
    id: int
    nombre: str = Field(min_length=1, max_length=60)
    url_gruplac: str | None = Field(default=None, alias="urlGruplac", max_length=128)
    categoria: str | None = Field(default=None, max_length=10)
    convocatoria: str | None = Field(default=None, max_length=10)
    fecha_fundacion: date = Field(alias="fechaFundacion")
    universidsad: int | None = Field(default=None, alias="universidad")
    interno: int = Field(ge=-32768, le=32767)
    ambito: str = Field(min_length=1, max_length=45)


class GrupoInvestigacionReemplazo(_Base):
    nombre: str = Field(min_length=1, max_length=60)
    url_gruplac: str | None = Field(alias="urlGruplac", max_length=128)
    categoria: str | None = Field(max_length=10)
    convocatoria: str | None = Field(max_length=10)
    fecha_fundacion: date = Field(alias="fechaFundacion")
    universidsad: int | None = Field(alias="universidad")
    interno: int = Field(ge=-32768, le=32767)
    ambito: str = Field(min_length=1, max_length=45)


class GrupoInvestigacionActualizar(_Base):
    nombre: str | None = Field(default=None, min_length=1, max_length=60)
    url_gruplac: str | None = Field(default=None, alias="urlGruplac", max_length=128)
    categoria: str | None = Field(default=None, max_length=10)
    convocatoria: str | None = Field(default=None, max_length=10)
    fecha_fundacion: date | None = Field(default=None, alias="fechaFundacion")
    universidsad: int | None = Field(default=None, alias="universidad")
    interno: int | None = Field(default=None, ge=-32768, le=32767)
    ambito: str | None = Field(default=None, min_length=1, max_length=45)
