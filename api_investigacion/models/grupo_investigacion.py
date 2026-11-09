from datetime import date
from pydantic import BaseModel, ConfigDict, Field, model_validator


class GrupoInvestigacion(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: int
    nombre: str = Field(min_length=1, max_length=60)
    url_gruplac: str | None = Field(min_length=1, max_length=128)
    categoria: str | None = Field(min_length=1, max_length=10)
    convocatoria: str | None = Field(min_length=1, max_length=10)
    fecha_fundacion: date
    universidsad: int | None
    interno: int
    ambito: str = Field(min_length=1, max_length=45)

class GrupoInvestigacionReemplazo(BaseModel):
    model_config = ConfigDict(extra="forbid")
    nombre: str = Field(min_length=1, max_length=60)
    url_gruplac: str | None = Field(min_length=1, max_length=128)
    categoria: str | None = Field(min_length=1, max_length=10)
    convocatoria: str | None = Field(min_length=1, max_length=10)
    fecha_fundacion: date
    universidsad: int | None
    interno: int
    ambito: str = Field(min_length=1, max_length=45)

class GrupoInvestigacionActualizar(BaseModel):
    model_config = ConfigDict(extra="forbid")
    nombre: str | None = Field(default=None, min_length=1, max_length=60)
    url_gruplac: str | None = Field(default=None, min_length=1, max_length=128)
    categoria: str | None = Field(default=None, min_length=1, max_length=10)
    convocatoria: str | None = Field(default=None, min_length=1, max_length=10)
    fecha_fundacion: date | None = Field(default=None)
    universidsad: int | None = Field(default=None)
    interno: int | None = Field(default=None)
    ambito: str | None = Field(default=None, min_length=1, max_length=45)

    @model_validator(mode="after")
    def validar_nulos(self):
        for campo in self.model_fields_set:
            if campo in ('nombre', 'fecha_fundacion', 'interno', 'ambito') and getattr(self, campo) is None:
                raise ValueError(f"El campo {campo} no admite nulo.")
        return self
