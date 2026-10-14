from datetime import date
from pydantic import BaseModel, ConfigDict, Field, model_validator


class Docente(BaseModel):
    model_config = ConfigDict(extra="forbid")
    cedula: int
    nombres: str = Field(min_length=1, max_length=60)
    apellidos: str = Field(min_length=1, max_length=60)
    genero: str = Field(min_length=1, max_length=12)
    cargo: str = Field(min_length=1, max_length=30)
    fecha_nacimiento: date
    correo: str = Field(min_length=1, max_length=70)
    telefono: str = Field(min_length=1, max_length=20)
    url_cvlac: str = Field(min_length=1, max_length=128)
    fecha_actualizacion: date
    escalafon: str = Field(min_length=1, max_length=45)
    perfil: str = Field(min_length=1)
    cat_minciencia: str | None = Field(min_length=1, max_length=45)
    conv_minciencia: str = Field(min_length=1, max_length=45)
    nacionalidaad: str = Field(min_length=1, max_length=45)
    linea_investigacion_principal: int | None

class DocenteReemplazo(BaseModel):
    model_config = ConfigDict(extra="forbid")
    nombres: str = Field(min_length=1, max_length=60)
    apellidos: str = Field(min_length=1, max_length=60)
    genero: str = Field(min_length=1, max_length=12)
    cargo: str = Field(min_length=1, max_length=30)
    fecha_nacimiento: date
    correo: str = Field(min_length=1, max_length=70)
    telefono: str = Field(min_length=1, max_length=20)
    url_cvlac: str = Field(min_length=1, max_length=128)
    fecha_actualizacion: date
    escalafon: str = Field(min_length=1, max_length=45)
    perfil: str = Field(min_length=1)
    cat_minciencia: str | None = Field(min_length=1, max_length=45)
    conv_minciencia: str = Field(min_length=1, max_length=45)
    nacionalidaad: str = Field(min_length=1, max_length=45)
    linea_investigacion_principal: int | None

class DocenteActualizar(BaseModel):
    model_config = ConfigDict(extra="forbid")
    nombres: str | None = Field(default=None, min_length=1, max_length=60)
    apellidos: str | None = Field(default=None, min_length=1, max_length=60)
    genero: str | None = Field(default=None, min_length=1, max_length=12)
    cargo: str | None = Field(default=None, min_length=1, max_length=30)
    fecha_nacimiento: date | None = Field(default=None)
    correo: str | None = Field(default=None, min_length=1, max_length=70)
    telefono: str | None = Field(default=None, min_length=1, max_length=20)
    url_cvlac: str | None = Field(default=None, min_length=1, max_length=128)
    fecha_actualizacion: date | None = Field(default=None)
    escalafon: str | None = Field(default=None, min_length=1, max_length=45)
    perfil: str | None = Field(default=None, min_length=1)
    cat_minciencia: str | None = Field(default=None, min_length=1, max_length=45)
    conv_minciencia: str | None = Field(default=None, min_length=1, max_length=45)
    nacionalidaad: str | None = Field(default=None, min_length=1, max_length=45)
    linea_investigacion_principal: int | None = Field(default=None)

    @model_validator(mode="after")
    def validar_nulos(self):
        for campo in self.model_fields_set:
            if campo in ('nombres', 'apellidos', 'genero', 'cargo', 'fecha_nacimiento', 'correo', 'telefono', 'url_cvlac', 'fecha_actualizacion', 'escalafon', 'perfil', 'conv_minciencia', 'nacionalidaad') and getattr(self, campo) is None:
                raise ValueError(f"El campo {campo} no admite nulo.")
        return self
