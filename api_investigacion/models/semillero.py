from datetime import date
from pydantic import BaseModel, ConfigDict, Field, model_validator


class Semillero(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: int
    nombre: str = Field(min_length=1, max_length=60)
    fecha_fundacion: date
    grupo_investigacion: int

class SemilleroReemplazo(BaseModel):
    model_config = ConfigDict(extra="forbid")
    nombre: str = Field(min_length=1, max_length=60)
    fecha_fundacion: date
    grupo_investigacion: int

class SemilleroActualizar(BaseModel):
    model_config = ConfigDict(extra="forbid")
    nombre: str | None = Field(default=None, min_length=1, max_length=60)
    fecha_fundacion: date | None = Field(default=None)
    grupo_investigacion: int | None = Field(default=None)

    @model_validator(mode="after")
    def validar_nulos(self):
        for campo in self.model_fields_set:
            if campo in ('nombre', 'fecha_fundacion', 'grupo_investigacion') and getattr(self, campo) is None:
                raise ValueError(f"El campo {campo} no admite nulo.")
        return self
