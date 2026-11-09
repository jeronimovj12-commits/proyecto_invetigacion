from datetime import date
from pydantic import BaseModel, ConfigDict, Field, model_validator


class ParticipaSemillero(BaseModel):
    model_config = ConfigDict(extra="forbid")
    docente: int
    semillero: int
    rol: str = Field(min_length=1, max_length=15)
    fecha_inicio: date
    fecha_fin: date | None

class ParticipaSemilleroReemplazo(BaseModel):
    model_config = ConfigDict(extra="forbid")
    docente: int
    semillero: int
    rol: str = Field(min_length=1, max_length=15)
    fecha_inicio: date
    fecha_fin: date | None

class ParticipaSemilleroActualizar(BaseModel):
    model_config = ConfigDict(extra="forbid")
    docente: int | None = Field(default=None)
    semillero: int | None = Field(default=None)
    rol: str | None = Field(default=None, min_length=1, max_length=15)
    fecha_inicio: date | None = Field(default=None)
    fecha_fin: date | None = Field(default=None)

    @model_validator(mode="after")
    def validar_nulos(self):
        for campo in self.model_fields_set:
            if campo in ('docente', 'semillero', 'rol', 'fecha_inicio') and getattr(self, campo) is None:
                raise ValueError(f"El campo {campo} no admite nulo.")
        return self
