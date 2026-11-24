"""Contratos del personal investigador; alias JSON separan el vocabulario público de columnas dadas."""

from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class _Base(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")


class DocenteCrear(_Base):
    cedula: int
    nombres: str = Field(min_length=1, max_length=60)
    apellidos: str = Field(min_length=1, max_length=60)
    genero: str = Field(min_length=1, max_length=12)
    cargo: str = Field(min_length=1, max_length=30)
    fecha_nacimiento: date = Field(alias="fechaNacimiento")
    correo: str = Field(min_length=1, max_length=70)
    telefono: str = Field(min_length=1, max_length=20)
    url_cvlac: str = Field(alias="urlCvlac", min_length=1, max_length=128)
    fecha_actualizacion: date = Field(alias="fechaActualizacion")
    escalafon: str = Field(min_length=1, max_length=45)
    perfil: str
    cat_minciencia: str | None = Field(default=None, alias="catMinciencia", max_length=45)
    conv_minciencia: str = Field(alias="convMinciencia", min_length=1, max_length=45)
    nacionalidaad: str = Field(alias="nacionalidad", min_length=1, max_length=45)
    linea_investigacion_principal: int | None = Field(
        default=None, alias="lineaInvestigacionPrincipal"
    )


class DocenteReemplazo(_Base):
    nombres: str = Field(min_length=1, max_length=60)
    apellidos: str = Field(min_length=1, max_length=60)
    genero: str = Field(min_length=1, max_length=12)
    cargo: str = Field(min_length=1, max_length=30)
    fecha_nacimiento: date = Field(alias="fechaNacimiento")
    correo: str = Field(min_length=1, max_length=70)
    telefono: str = Field(min_length=1, max_length=20)
    url_cvlac: str = Field(alias="urlCvlac", min_length=1, max_length=128)
    fecha_actualizacion: date = Field(alias="fechaActualizacion")
    escalafon: str = Field(min_length=1, max_length=45)
    perfil: str
    cat_minciencia: str | None = Field(alias="catMinciencia", max_length=45)
    conv_minciencia: str = Field(alias="convMinciencia", min_length=1, max_length=45)
    nacionalidaad: str = Field(alias="nacionalidad", min_length=1, max_length=45)
    linea_investigacion_principal: int | None = Field(alias="lineaInvestigacionPrincipal")


class DocenteActualizar(_Base):
    nombres: str | None = Field(default=None, min_length=1, max_length=60)
    apellidos: str | None = Field(default=None, min_length=1, max_length=60)
    genero: str | None = Field(default=None, min_length=1, max_length=12)
    cargo: str | None = Field(default=None, min_length=1, max_length=30)
    fecha_nacimiento: date | None = Field(default=None, alias="fechaNacimiento")
    correo: str | None = Field(default=None, min_length=1, max_length=70)
    telefono: str | None = Field(default=None, min_length=1, max_length=20)
    url_cvlac: str | None = Field(default=None, alias="urlCvlac", min_length=1, max_length=128)
    fecha_actualizacion: date | None = Field(default=None, alias="fechaActualizacion")
    escalafon: str | None = Field(default=None, min_length=1, max_length=45)
    perfil: str | None = None
    cat_minciencia: str | None = Field(default=None, alias="catMinciencia", max_length=45)
    conv_minciencia: str | None = Field(default=None, alias="convMinciencia", min_length=1, max_length=45)
    nacionalidaad: str | None = Field(default=None, alias="nacionalidad", min_length=1, max_length=45)
    linea_investigacion_principal: int | None = Field(
        default=None, alias="lineaInvestigacionPrincipal"
    )
