from datetime import date
from pydantic import BaseModel, ConfigDict, Field, model_validator


class GrupoLinea(BaseModel):
    model_config = ConfigDict(extra="forbid")
    grupo_investigacion: int
    linea_investigacion: int

class GrupoLineaReemplazo(BaseModel):
    model_config = ConfigDict(extra="forbid")
    grupo_investigacion: int
    linea_investigacion: int

class GrupoLineaActualizar(BaseModel):
    model_config = ConfigDict(extra="forbid")
    grupo_investigacion: int | None = Field(default=None)
    linea_investigacion: int | None = Field(default=None)

    @model_validator(mode="after")
    def validar_nulos(self):
        for campo in self.model_fields_set:
            if campo in ('grupo_investigacion', 'linea_investigacion') and getattr(self, campo) is None:
                raise ValueError(f"El campo {campo} no admite nulo.")
        return self
