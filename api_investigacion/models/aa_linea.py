from datetime import date
from pydantic import BaseModel, ConfigDict, Field, model_validator


class AaLinea(BaseModel):
    model_config = ConfigDict(extra="forbid")
    area_aplicacion: int
    linea_investigacion: int

class AaLineaReemplazo(BaseModel):
    model_config = ConfigDict(extra="forbid")
    area_aplicacion: int
    linea_investigacion: int

class AaLineaActualizar(BaseModel):
    model_config = ConfigDict(extra="forbid")
    area_aplicacion: int | None = Field(default=None)
    linea_investigacion: int | None = Field(default=None)

    @model_validator(mode="after")
    def validar_nulos(self):
        for campo in self.model_fields_set:
            if campo in ('area_aplicacion', 'linea_investigacion') and getattr(self, campo) is None:
                raise ValueError(f"El campo {campo} no admite nulo.")
        return self
