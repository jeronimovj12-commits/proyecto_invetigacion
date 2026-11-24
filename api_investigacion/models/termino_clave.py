"""Contratos de términos; la traducción es opcional y conserva su nulabilidad."""

from pydantic import BaseModel, ConfigDict, Field


class _Base(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")


class TerminoClaveCrear(_Base):
    termino: str = Field(min_length=1, max_length=30)
    termino_ingles: str | None = Field(default=None, alias="terminoIngles", max_length=30)


class TerminoClaveReemplazo(_Base):
    termino_ingles: str | None = Field(alias="terminoIngles", max_length=30)


class TerminoClaveActualizar(_Base):
    termino_ingles: str | None = Field(default=None, alias="terminoIngles", max_length=30)
