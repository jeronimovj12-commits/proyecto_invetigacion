from datetime import date
from pydantic import BaseModel, ConfigDict, Field, model_validator


class OdsLinea(BaseModel):
    model_config = ConfigDict(extra="forbid")
    linea_investigacion: int
    ods: int

class OdsLineaReemplazo(BaseModel):
    model_config = ConfigDict(extra="forbid")
    linea_investigacion: int
    ods: int

class OdsLineaActualizar(BaseModel):
    model_config = ConfigDict(extra="forbid")
    linea_investigacion: int | None = Field(default=None)
    ods: int | None = Field(default=None)

    @model_validator(mode="after")
    def validar_nulos(self):
        for campo in self.model_fields_set:
            if campo in ('linea_investigacion', 'ods') and getattr(self, campo) is None:
                raise ValueError(f"El campo {campo} no admite nulo.")
        return self
