# Ejecuta la instruccion indicada dentro del flujo actual.
"""Modelos Pydantic: declaran la forma y las restricciones de los datos que entran o salen de la API."""
# Importa date desde datetime para usar esas definiciones.
from datetime import date
# Importa BaseModel, ConfigDict, Field, model_validator desde pydantic para usar esas definiciones.
from pydantic import BaseModel, ConfigDict, Field, model_validator


# Define la clase GrupoInvestigacion y agrupa su estado y operaciones.
class GrupoInvestigacion(BaseModel):
    # Asigna a model_config el valor calculado a la derecha.
    model_config = ConfigDict(extra="forbid")
    # Asigna a id el valor calculado a la derecha.
    id: int
    # Declara el campo nombre y configura en Field el alias o limites que debe validar.
    nombre: str = Field(min_length=1, max_length=60)
    # Declara el campo url_gruplac y configura en Field el alias o limites que debe validar.
    url_gruplac: str | None = Field(min_length=1, max_length=128)
    # Declara el campo categoria y configura en Field el alias o limites que debe validar.
    categoria: str | None = Field(min_length=1, max_length=10)
    # Declara el campo convocatoria y configura en Field el alias o limites que debe validar.
    convocatoria: str | None = Field(min_length=1, max_length=10)
    # Asigna a fecha_fundacion el valor calculado a la derecha.
    fecha_fundacion: date
    # Asigna a universidsad el valor calculado a la derecha.
    universidsad: int | None
    # Asigna a interno el valor calculado a la derecha.
    interno: int
    # Declara el campo ambito y configura en Field el alias o limites que debe validar.
    ambito: str = Field(min_length=1, max_length=45)

# Define la clase GrupoInvestigacionReemplazo y agrupa su estado y operaciones.
class GrupoInvestigacionReemplazo(BaseModel):
    # Asigna a model_config el valor calculado a la derecha.
    model_config = ConfigDict(extra="forbid")
    # Declara el campo nombre y configura en Field el alias o limites que debe validar.
    nombre: str = Field(min_length=1, max_length=60)
    # Declara el campo url_gruplac y configura en Field el alias o limites que debe validar.
    url_gruplac: str | None = Field(min_length=1, max_length=128)
    # Declara el campo categoria y configura en Field el alias o limites que debe validar.
    categoria: str | None = Field(min_length=1, max_length=10)
    # Declara el campo convocatoria y configura en Field el alias o limites que debe validar.
    convocatoria: str | None = Field(min_length=1, max_length=10)
    # Asigna a fecha_fundacion el valor calculado a la derecha.
    fecha_fundacion: date
    # Asigna a universidsad el valor calculado a la derecha.
    universidsad: int | None
    # Asigna a interno el valor calculado a la derecha.
    interno: int
    # Declara el campo ambito y configura en Field el alias o limites que debe validar.
    ambito: str = Field(min_length=1, max_length=45)

# Define la clase GrupoInvestigacionActualizar y agrupa su estado y operaciones.
class GrupoInvestigacionActualizar(BaseModel):
    # Asigna a model_config el valor calculado a la derecha.
    model_config = ConfigDict(extra="forbid")
    # Declara el campo nombre y configura en Field el alias o limites que debe validar.
    nombre: str | None = Field(default=None, min_length=1, max_length=60)
    # Declara el campo url_gruplac y configura en Field el alias o limites que debe validar.
    url_gruplac: str | None = Field(default=None, min_length=1, max_length=128)
    # Declara el campo categoria y configura en Field el alias o limites que debe validar.
    categoria: str | None = Field(default=None, min_length=1, max_length=10)
    # Declara el campo convocatoria y configura en Field el alias o limites que debe validar.
    convocatoria: str | None = Field(default=None, min_length=1, max_length=10)
    # Declara el campo fecha_fundacion y configura en Field el alias o limites que debe validar.
    fecha_fundacion: date | None = Field(default=None)
    # Declara el campo universidsad y configura en Field el alias o limites que debe validar.
    universidsad: int | None = Field(default=None)
    # Declara el campo interno y configura en Field el alias o limites que debe validar.
    interno: int | None = Field(default=None)
    # Declara el campo ambito y configura en Field el alias o limites que debe validar.
    ambito: str | None = Field(default=None, min_length=1, max_length=45)

    # Aplica @model_validator a la declaracion que sigue; en rutas, registra el endpoint HTTP.
    @model_validator(mode="after")
    # Define la funcion validar_nulos con los parametros declarados; su bloque realiza esta operacion.
    def validar_nulos(self):
        # Recorre los elementos de la coleccion indicada y ejecuta el bloque para cada uno.
        for campo in self.model_fields_set:
            # Ejecuta el bloque siguiente solo cuando se cumple: campo in ('nombre', 'fecha_fundacion', 'interno', 'ambito') and getattr(self, campo) is None.
            if campo in ('nombre', 'fecha_fundacion', 'interno', 'ambito') and getattr(self, campo) is None:
                # Lanza la excepcion indicada y detiene el flujo normal.
                raise ValueError(f"El campo {campo} no admite nulo.")
        # Devuelve al llamador el resultado de la expresion indicada.
        return self
