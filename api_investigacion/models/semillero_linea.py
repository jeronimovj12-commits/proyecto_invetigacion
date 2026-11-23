# Ejecuta la instruccion indicada dentro del flujo actual.
"""Modelos Pydantic: declaran la forma y las restricciones de los datos que entran o salen de la API."""
# Importa date desde datetime para usar esas definiciones.
from datetime import date
# Importa BaseModel, ConfigDict, Field, model_validator desde pydantic para usar esas definiciones.
from pydantic import BaseModel, ConfigDict, Field, model_validator


# Define la clase SemilleroLinea y agrupa su estado y operaciones.
class SemilleroLinea(BaseModel):
    # Asigna a model_config el valor calculado a la derecha.
    model_config = ConfigDict(extra="forbid")
    # Asigna a semillero el valor calculado a la derecha.
    semillero: int
    # Asigna a linea_investigacion el valor calculado a la derecha.
    linea_investigacion: int

# Define la clase SemilleroLineaReemplazo y agrupa su estado y operaciones.
class SemilleroLineaReemplazo(BaseModel):
    # Asigna a model_config el valor calculado a la derecha.
    model_config = ConfigDict(extra="forbid")
    # Asigna a semillero el valor calculado a la derecha.
    semillero: int
    # Asigna a linea_investigacion el valor calculado a la derecha.
    linea_investigacion: int

# Define la clase SemilleroLineaActualizar y agrupa su estado y operaciones.
class SemilleroLineaActualizar(BaseModel):
    # Asigna a model_config el valor calculado a la derecha.
    model_config = ConfigDict(extra="forbid")
    # Declara el campo semillero y configura en Field el alias o limites que debe validar.
    semillero: int | None = Field(default=None)
    # Declara el campo linea_investigacion y configura en Field el alias o limites que debe validar.
    linea_investigacion: int | None = Field(default=None)

    # Aplica @model_validator a la declaracion que sigue; en rutas, registra el endpoint HTTP.
    @model_validator(mode="after")
    # Define la funcion validar_nulos con los parametros declarados; su bloque realiza esta operacion.
    def validar_nulos(self):
        # Recorre los elementos de la coleccion indicada y ejecuta el bloque para cada uno.
        for campo in self.model_fields_set:
            # Ejecuta el bloque siguiente solo cuando se cumple: campo in ('semillero', 'linea_investigacion') and getattr(self, campo) is None.
            if campo in ('semillero', 'linea_investigacion') and getattr(self, campo) is None:
                # Lanza la excepcion indicada y detiene el flujo normal.
                raise ValueError(f"El campo {campo} no admite nulo.")
        # Devuelve al llamador el resultado de la expresion indicada.
        return self
