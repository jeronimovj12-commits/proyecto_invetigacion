# Ejecuta la instruccion indicada dentro del flujo actual.
"""Modelos Pydantic: declaran la forma y las restricciones de los datos que entran o salen de la API."""
# Importa date desde datetime para usar esas definiciones.
from datetime import date
# Importa BaseModel, ConfigDict, Field, model_validator desde pydantic para usar esas definiciones.
from pydantic import BaseModel, ConfigDict, Field, model_validator


# Define la clase ParticipaGrupo y agrupa su estado y operaciones.
class ParticipaGrupo(BaseModel):
    # Asigna a model_config el valor calculado a la derecha.
    model_config = ConfigDict(extra="forbid")
    # Asigna a docente_cedula el valor calculado a la derecha.
    docente_cedula: int
    # Asigna a grupo_investigacion_id el valor calculado a la derecha.
    grupo_investigacion_id: int
    # Declara el campo rol y configura en Field el alias o limites que debe validar.
    rol: str = Field(min_length=1, max_length=15)
    # Asigna a fecha_inicio el valor calculado a la derecha.
    fecha_inicio: date
    # Asigna a fecha_fin el valor calculado a la derecha.
    fecha_fin: date | None

# Define la clase ParticipaGrupoReemplazo y agrupa su estado y operaciones.
class ParticipaGrupoReemplazo(BaseModel):
    # Asigna a model_config el valor calculado a la derecha.
    model_config = ConfigDict(extra="forbid")
    # Asigna a docente_cedula el valor calculado a la derecha.
    docente_cedula: int
    # Asigna a grupo_investigacion_id el valor calculado a la derecha.
    grupo_investigacion_id: int
    # Declara el campo rol y configura en Field el alias o limites que debe validar.
    rol: str = Field(min_length=1, max_length=15)
    # Asigna a fecha_inicio el valor calculado a la derecha.
    fecha_inicio: date
    # Asigna a fecha_fin el valor calculado a la derecha.
    fecha_fin: date | None

# Define la clase ParticipaGrupoActualizar y agrupa su estado y operaciones.
class ParticipaGrupoActualizar(BaseModel):
    # Asigna a model_config el valor calculado a la derecha.
    model_config = ConfigDict(extra="forbid")
    # Declara el campo docente_cedula y configura en Field el alias o limites que debe validar.
    docente_cedula: int | None = Field(default=None)
    # Declara el campo grupo_investigacion_id y configura en Field el alias o limites que debe validar.
    grupo_investigacion_id: int | None = Field(default=None)
    # Declara el campo rol y configura en Field el alias o limites que debe validar.
    rol: str | None = Field(default=None, min_length=1, max_length=15)
    # Declara el campo fecha_inicio y configura en Field el alias o limites que debe validar.
    fecha_inicio: date | None = Field(default=None)
    # Declara el campo fecha_fin y configura en Field el alias o limites que debe validar.
    fecha_fin: date | None = Field(default=None)

    # Aplica @model_validator a la declaracion que sigue; en rutas, registra el endpoint HTTP.
    @model_validator(mode="after")
    # Define la funcion validar_nulos con los parametros declarados; su bloque realiza esta operacion.
    def validar_nulos(self):
        # Recorre los elementos de la coleccion indicada y ejecuta el bloque para cada uno.
        for campo in self.model_fields_set:
            # Ejecuta el bloque siguiente solo cuando se cumple: campo in ('docente_cedula', 'grupo_investigacion_id', 'rol', 'fecha_inicio') and getattr(self, campo) is None.
            if campo in ('docente_cedula', 'grupo_investigacion_id', 'rol', 'fecha_inicio') and getattr(self, campo) is None:
                # Lanza la excepcion indicada y detiene el flujo normal.
                raise ValueError(f"El campo {campo} no admite nulo.")
        # Devuelve al llamador el resultado de la expresion indicada.
        return self
