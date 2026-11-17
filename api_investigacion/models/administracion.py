# Ejecuta la instruccion indicada dentro del flujo actual.
"""Modelos Pydantic: declaran la forma y las restricciones de los datos que entran o salen de la API."""
# Importa BaseModel, ConfigDict, Field, SecretStr, model_validator desde pydantic para usar esas definiciones.
from pydantic import BaseModel, ConfigDict, Field, SecretStr, model_validator

# Define la clase Entrada y agrupa su estado y operaciones.
class Entrada(BaseModel):
    # Asigna a model_config el valor calculado a la derecha.
    model_config = ConfigDict(extra='forbid', str_strip_whitespace=True)

# Define la clase UsuarioCrear y agrupa su estado y operaciones.
class UsuarioCrear(Entrada):
    # Declara el campo username y configura en Field el alias o limites que debe validar.
    username: str = Field(min_length=1, max_length=100)
    # Declara el campo email y configura en Field el alias o limites que debe validar.
    email: str = Field(min_length=1, max_length=150)
    # Declara el campo nombre_completo y configura en Field el alias o limites que debe validar.
    nombre_completo: str | None = Field(default=None, max_length=200)
    # Declara el campo password y configura en Field el alias o limites que debe validar.
    password: SecretStr = Field(min_length=12, max_length=1024)

# Define la clase UsuarioEditar y agrupa su estado y operaciones.
class UsuarioEditar(Entrada):
    # Declara el campo username y configura en Field el alias o limites que debe validar.
    username: str | None = Field(default=None, min_length=1, max_length=100)
    # Declara el campo email y configura en Field el alias o limites que debe validar.
    email: str | None = Field(default=None, min_length=1, max_length=150)
    # Declara el campo nombre_completo y configura en Field el alias o limites que debe validar.
    nombre_completo: str | None = Field(default=None, max_length=200)
    # Declara el campo password y configura en Field el alias o limites que debe validar.
    password: SecretStr | None = Field(default=None, min_length=12, max_length=1024)

    # Aplica @model_validator a la declaracion que sigue; en rutas, registra el endpoint HTTP.
    @model_validator(mode='after')
    # Define la funcion no_nulos con los parametros declarados; su bloque realiza esta operacion.
    def no_nulos(self):
        # Ejecuta el bloque siguiente solo cuando se cumple: any(getattr(self, c) is None for c in self.model_fields_set - {'nombre_completo'}).
        if any(getattr(self, c) is None for c in self.model_fields_set - {'nombre_completo'}):
            # Lanza la excepcion indicada y detiene el flujo normal.
            raise ValueError('Los campos obligatorios no admiten null.')
        # Devuelve al llamador el resultado de la expresion indicada.
        return self

# Define la clase RolCrear y agrupa su estado y operaciones.
class RolCrear(Entrada):
    # Declara el campo nombre y configura en Field el alias o limites que debe validar.
    nombre: str = Field(min_length=1, max_length=100)
    # Declara el campo descripcion y configura en Field el alias o limites que debe validar.
    descripcion: str | None = Field(default=None, max_length=2000)

# Define la clase RolEditar y agrupa su estado y operaciones.
class RolEditar(Entrada):
    # Declara el campo nombre y configura en Field el alias o limites que debe validar.
    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    # Declara el campo descripcion y configura en Field el alias o limites que debe validar.
    descripcion: str | None = Field(default=None, max_length=2000)

    # Aplica @model_validator a la declaracion que sigue; en rutas, registra el endpoint HTTP.
    @model_validator(mode='after')
    # Define la funcion no_nulo con los parametros declarados; su bloque realiza esta operacion.
    def no_nulo(self):
        # Ejecuta el bloque siguiente solo cuando se cumple: 'nombre' in self.model_fields_set and self.nombre is None.
        if 'nombre' in self.model_fields_set and self.nombre is None:
            # Lanza la excepcion indicada y detiene el flujo normal.
            raise ValueError('El nombre no admite null.')
        # Devuelve al llamador el resultado de la expresion indicada.
        return self

# Define la clase AsignacionCrear y agrupa su estado y operaciones.
class AsignacionCrear(Entrada):
    # Declara el campo usuario_id y configura en Field el alias o limites que debe validar.
    usuario_id: int = Field(gt=0)
    # Declara el campo rol_id y configura en Field el alias o limites que debe validar.
    rol_id: int = Field(gt=0)


# Define la clase AsignacionEditar y agrupa su estado y operaciones.
class AsignacionEditar(Entrada):
    # Declara el campo usuario_id y configura en Field el alias o limites que debe validar.
    usuario_id: int | None = Field(default=None, gt=0)
    # Declara el campo rol_id y configura en Field el alias o limites que debe validar.
    rol_id: int | None = Field(default=None, gt=0)

    # Aplica @model_validator a la declaracion que sigue; en rutas, registra el endpoint HTTP.
    @model_validator(mode='after')
    # Define la funcion no_nulos con los parametros declarados; su bloque realiza esta operacion.
    def no_nulos(self):
        # Ejecuta el bloque siguiente solo cuando se cumple: any(getattr(self, c) is None for c in self.model_fields_set).
        if any(getattr(self, c) is None for c in self.model_fields_set):
            # Lanza la excepcion indicada y detiene el flujo normal.
            raise ValueError('Los identificadores no admiten null.')
        # Devuelve al llamador el resultado de la expresion indicada.
        return self
