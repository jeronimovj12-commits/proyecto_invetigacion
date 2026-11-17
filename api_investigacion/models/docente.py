# Ejecuta la instruccion indicada dentro del flujo actual.
"""Modelos Pydantic: declaran la forma y las restricciones de los datos que entran o salen de la API."""
# Importa date desde datetime para usar esas definiciones.
from datetime import date
# Importa BaseModel, ConfigDict, Field, model_validator desde pydantic para usar esas definiciones.
from pydantic import BaseModel, ConfigDict, Field, model_validator


# Define la clase Docente y agrupa su estado y operaciones.
class Docente(BaseModel):
    # Asigna a model_config el valor calculado a la derecha.
    model_config = ConfigDict(extra="forbid")
    # Asigna a cedula el valor calculado a la derecha.
    cedula: int
    # Declara el campo nombres y configura en Field el alias o limites que debe validar.
    nombres: str = Field(min_length=1, max_length=60)
    # Declara el campo apellidos y configura en Field el alias o limites que debe validar.
    apellidos: str = Field(min_length=1, max_length=60)
    # Declara el campo genero y configura en Field el alias o limites que debe validar.
    genero: str = Field(min_length=1, max_length=12)
    # Declara el campo cargo y configura en Field el alias o limites que debe validar.
    cargo: str = Field(min_length=1, max_length=30)
    # Asigna a fecha_nacimiento el valor calculado a la derecha.
    fecha_nacimiento: date
    # Declara el campo correo y configura en Field el alias o limites que debe validar.
    correo: str = Field(min_length=1, max_length=70)
    # Declara el campo telefono y configura en Field el alias o limites que debe validar.
    telefono: str = Field(min_length=1, max_length=20)
    # Declara el campo url_cvlac y configura en Field el alias o limites que debe validar.
    url_cvlac: str = Field(min_length=1, max_length=128)
    # Asigna a fecha_actualizacion el valor calculado a la derecha.
    fecha_actualizacion: date
    # Declara el campo escalafon y configura en Field el alias o limites que debe validar.
    escalafon: str = Field(min_length=1, max_length=45)
    # Declara el campo perfil y configura en Field el alias o limites que debe validar.
    perfil: str = Field(min_length=1)
    # Declara el campo cat_minciencia y configura en Field el alias o limites que debe validar.
    cat_minciencia: str | None = Field(min_length=1, max_length=45)
    # Declara el campo conv_minciencia y configura en Field el alias o limites que debe validar.
    conv_minciencia: str = Field(min_length=1, max_length=45)
    # Declara el campo nacionalidaad y configura en Field el alias o limites que debe validar.
    nacionalidaad: str = Field(min_length=1, max_length=45)
    # Asigna a linea_investigacion_principal el valor calculado a la derecha.
    linea_investigacion_principal: int | None

# Define la clase DocenteReemplazo y agrupa su estado y operaciones.
class DocenteReemplazo(BaseModel):
    # Asigna a model_config el valor calculado a la derecha.
    model_config = ConfigDict(extra="forbid")
    # Declara el campo nombres y configura en Field el alias o limites que debe validar.
    nombres: str = Field(min_length=1, max_length=60)
    # Declara el campo apellidos y configura en Field el alias o limites que debe validar.
    apellidos: str = Field(min_length=1, max_length=60)
    # Declara el campo genero y configura en Field el alias o limites que debe validar.
    genero: str = Field(min_length=1, max_length=12)
    # Declara el campo cargo y configura en Field el alias o limites que debe validar.
    cargo: str = Field(min_length=1, max_length=30)
    # Asigna a fecha_nacimiento el valor calculado a la derecha.
    fecha_nacimiento: date
    # Declara el campo correo y configura en Field el alias o limites que debe validar.
    correo: str = Field(min_length=1, max_length=70)
    # Declara el campo telefono y configura en Field el alias o limites que debe validar.
    telefono: str = Field(min_length=1, max_length=20)
    # Declara el campo url_cvlac y configura en Field el alias o limites que debe validar.
    url_cvlac: str = Field(min_length=1, max_length=128)
    # Asigna a fecha_actualizacion el valor calculado a la derecha.
    fecha_actualizacion: date
    # Declara el campo escalafon y configura en Field el alias o limites que debe validar.
    escalafon: str = Field(min_length=1, max_length=45)
    # Declara el campo perfil y configura en Field el alias o limites que debe validar.
    perfil: str = Field(min_length=1)
    # Declara el campo cat_minciencia y configura en Field el alias o limites que debe validar.
    cat_minciencia: str | None = Field(min_length=1, max_length=45)
    # Declara el campo conv_minciencia y configura en Field el alias o limites que debe validar.
    conv_minciencia: str = Field(min_length=1, max_length=45)
    # Declara el campo nacionalidaad y configura en Field el alias o limites que debe validar.
    nacionalidaad: str = Field(min_length=1, max_length=45)
    # Asigna a linea_investigacion_principal el valor calculado a la derecha.
    linea_investigacion_principal: int | None

# Define la clase DocenteActualizar y agrupa su estado y operaciones.
class DocenteActualizar(BaseModel):
    # Asigna a model_config el valor calculado a la derecha.
    model_config = ConfigDict(extra="forbid")
    # Declara el campo nombres y configura en Field el alias o limites que debe validar.
    nombres: str | None = Field(default=None, min_length=1, max_length=60)
    # Declara el campo apellidos y configura en Field el alias o limites que debe validar.
    apellidos: str | None = Field(default=None, min_length=1, max_length=60)
    # Declara el campo genero y configura en Field el alias o limites que debe validar.
    genero: str | None = Field(default=None, min_length=1, max_length=12)
    # Declara el campo cargo y configura en Field el alias o limites que debe validar.
    cargo: str | None = Field(default=None, min_length=1, max_length=30)
    # Declara el campo fecha_nacimiento y configura en Field el alias o limites que debe validar.
    fecha_nacimiento: date | None = Field(default=None)
    # Declara el campo correo y configura en Field el alias o limites que debe validar.
    correo: str | None = Field(default=None, min_length=1, max_length=70)
    # Declara el campo telefono y configura en Field el alias o limites que debe validar.
    telefono: str | None = Field(default=None, min_length=1, max_length=20)
    # Declara el campo url_cvlac y configura en Field el alias o limites que debe validar.
    url_cvlac: str | None = Field(default=None, min_length=1, max_length=128)
    # Declara el campo fecha_actualizacion y configura en Field el alias o limites que debe validar.
    fecha_actualizacion: date | None = Field(default=None)
    # Declara el campo escalafon y configura en Field el alias o limites que debe validar.
    escalafon: str | None = Field(default=None, min_length=1, max_length=45)
    # Declara el campo perfil y configura en Field el alias o limites que debe validar.
    perfil: str | None = Field(default=None, min_length=1)
    # Declara el campo cat_minciencia y configura en Field el alias o limites que debe validar.
    cat_minciencia: str | None = Field(default=None, min_length=1, max_length=45)
    # Declara el campo conv_minciencia y configura en Field el alias o limites que debe validar.
    conv_minciencia: str | None = Field(default=None, min_length=1, max_length=45)
    # Declara el campo nacionalidaad y configura en Field el alias o limites que debe validar.
    nacionalidaad: str | None = Field(default=None, min_length=1, max_length=45)
    # Declara el campo linea_investigacion_principal y configura en Field el alias o limites que debe validar.
    linea_investigacion_principal: int | None = Field(default=None)

    # Aplica @model_validator a la declaracion que sigue; en rutas, registra el endpoint HTTP.
    @model_validator(mode="after")
    # Define la funcion validar_nulos con los parametros declarados; su bloque realiza esta operacion.
    def validar_nulos(self):
        # Recorre los elementos de la coleccion indicada y ejecuta el bloque para cada uno.
        for campo in self.model_fields_set:
            # Ejecuta el bloque siguiente solo cuando se cumple: campo in ('nombres', 'apellidos', 'genero', 'cargo', 'fecha_nacimiento', 'correo', 'telefono', 'url_cvlac', 'fecha_actualizacion', 'escalafon', 'perfil', 'conv_minciencia', 'nacionalidaad') and getattr(self, campo) is None.
            if campo in ('nombres', 'apellidos', 'genero', 'cargo', 'fecha_nacimiento', 'correo', 'telefono', 'url_cvlac', 'fecha_actualizacion', 'escalafon', 'perfil', 'conv_minciencia', 'nacionalidaad') and getattr(self, campo) is None:
                # Lanza la excepcion indicada y detiene el flujo normal.
                raise ValueError(f"El campo {campo} no admite nulo.")
        # Devuelve al llamador el resultado de la expresion indicada.
        return self
