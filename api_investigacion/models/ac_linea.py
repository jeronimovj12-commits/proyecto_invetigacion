# Ejecuta la instruccion indicada dentro del flujo actual.
"""Modelos Pydantic: declaran la forma y las restricciones de los datos que entran o salen de la API."""
# Importa date desde datetime para usar esas definiciones.
from datetime import date
# Importa BaseModel, ConfigDict, Field, model_validator desde pydantic para usar esas definiciones.
from pydantic import BaseModel, ConfigDict, Field, model_validator


# Define la clase AcLinea y agrupa su estado y operaciones.
class AcLinea(BaseModel):
    # Asigna a model_config el valor calculado a la derecha.
    model_config = ConfigDict(extra="forbid")
    # Asigna a linea_investigacion el valor calculado a la derecha.
    linea_investigacion: int
    # Declara el campo area_conocimiento y configura en Field el alias o limites que debe validar.
    area_conocimiento: str = Field(min_length=1, max_length=6)

# Define la clase AcLineaReemplazo y agrupa su estado y operaciones.
class AcLineaReemplazo(BaseModel):
    # Asigna a model_config el valor calculado a la derecha.
    model_config = ConfigDict(extra="forbid")
    # Asigna a linea_investigacion el valor calculado a la derecha.
    linea_investigacion: int
    # Declara el campo area_conocimiento y configura en Field el alias o limites que debe validar.
    area_conocimiento: str = Field(min_length=1, max_length=6)

# Define la clase AcLineaActualizar y agrupa su estado y operaciones.
class AcLineaActualizar(BaseModel):
    # Asigna a model_config el valor calculado a la derecha.
    model_config = ConfigDict(extra="forbid")
    # Declara el campo linea_investigacion y configura en Field el alias o limites que debe validar.
    linea_investigacion: int | None = Field(default=None)
    # Declara el campo area_conocimiento y configura en Field el alias o limites que debe validar.
    area_conocimiento: str | None = Field(default=None, min_length=1, max_length=6)

    # Aplica @model_validator a la declaracion que sigue; en rutas, registra el endpoint HTTP.
    @model_validator(mode="after")
    # Define la funcion validar_nulos con los parametros declarados; su bloque realiza esta operacion.
    def validar_nulos(self):
        # Recorre los elementos de la coleccion indicada y ejecuta el bloque para cada uno.
        for campo in self.model_fields_set:
            # Ejecuta el bloque siguiente solo cuando se cumple: campo in ('linea_investigacion', 'area_conocimiento') and getattr(self, campo) is None.
            if campo in ('linea_investigacion', 'area_conocimiento') and getattr(self, campo) is None:
                # Lanza la excepcion indicada y detiene el flujo normal.
                raise ValueError(f"El campo {campo} no admite nulo.")
        # Devuelve al llamador el resultado de la expresion indicada.
        return self
