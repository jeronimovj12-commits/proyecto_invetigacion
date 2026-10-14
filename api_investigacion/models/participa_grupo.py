from datetime import date
from pydantic import BaseModel, ConfigDict, Field, model_validator


class ParticipaGrupo(BaseModel):
    model_config = ConfigDict(extra="forbid")
    docente_cedula: int
    grupo_investigacion_id: int
    rol: str = Field(min_length=1, max_length=15)
    fecha_inicio: date
    fecha_fin: date | None

class ParticipaGrupoReemplazo(BaseModel):
    model_config = ConfigDict(extra="forbid")
    docente_cedula: int
    grupo_investigacion_id: int
    rol: str = Field(min_length=1, max_length=15)
    fecha_inicio: date
    fecha_fin: date | None

class ParticipaGrupoActualizar(BaseModel):
    model_config = ConfigDict(extra="forbid")
    docente_cedula: int | None = Field(default=None)
    grupo_investigacion_id: int | None = Field(default=None)
    rol: str | None = Field(default=None, min_length=1, max_length=15)
    fecha_inicio: date | None = Field(default=None)
    fecha_fin: date | None = Field(default=None)

    @model_validator(mode="after")
    def validar_nulos(self):
        for campo in self.model_fields_set:
            if campo in ('docente_cedula', 'grupo_investigacion_id', 'rol', 'fecha_inicio') and getattr(self, campo) is None:
                raise ValueError(f"El campo {campo} no admite nulo.")
        return self
