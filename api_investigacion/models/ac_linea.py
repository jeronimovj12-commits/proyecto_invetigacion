from datetime import date
from pydantic import BaseModel, ConfigDict, Field, model_validator


class AcLinea(BaseModel):
    model_config = ConfigDict(extra="forbid")
    linea_investigacion: int
    area_conocimiento: str = Field(min_length=1, max_length=6)

class AcLineaReemplazo(BaseModel):
    model_config = ConfigDict(extra="forbid")
    linea_investigacion: int
    area_conocimiento: str = Field(min_length=1, max_length=6)

class AcLineaActualizar(BaseModel):
    model_config = ConfigDict(extra="forbid")
    linea_investigacion: int | None = Field(default=None)
    area_conocimiento: str | None = Field(default=None, min_length=1, max_length=6)

    @model_validator(mode="after")
    def validar_nulos(self):
        for campo in self.model_fields_set:
            if campo in ('linea_investigacion', 'area_conocimiento') and getattr(self, campo) is None:
                raise ValueError(f"El campo {campo} no admite nulo.")
        return self
