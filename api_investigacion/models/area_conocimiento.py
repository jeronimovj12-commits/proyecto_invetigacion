"""
Modelos Pydantic de area_conocimiento — la FRONTERA DE ENTRADA de la API.

Aquí no hay ni un solo `if` de validación: se DECLARA la forma correcta de
los datos y Pydantic valida al construir el objeto. Un cuerpo inválido muere
en 422 antes de tocar el servicio o la base.

Hay UN modelo por semántica HTTP:
- AreaConocimiento           → POST : el recurso completo, con su código.
- AreaConocimientoReemplazo  → PUT  : reemplazo completo (el id va en la URL).
- AreaConocimientoActualizar → PATCH: parcial, todos los campos opcionales.
"""

# Importa BaseModel, Field desde pydantic para usar esas definiciones.
from pydantic import BaseModel, Field


# Define la clase AreaConocimiento y agrupa su estado y operaciones.
class AreaConocimiento(BaseModel):
    # Ejecuta la instruccion indicada dentro del flujo actual.
    """POST /api/area_conocimiento — todos los campos son obligatorios."""

    # El id es TEXTO, no un entero: los datos del catálogo son códigos como
    # '1A01'. Ver la clarificación C1.
    # Declara el campo id y configura en Field el alias o limites que debe validar.
    id: str = Field(min_length=1, max_length=6)
    # Declara el campo gran_area y configura en Field el alias o limites que debe validar.
    gran_area: str = Field(alias="granArea", min_length=1, max_length=60)
    # Declara el campo area y configura en Field el alias o limites que debe validar.
    area: str = Field(min_length=1, max_length=60)
    # Declara el campo disciplina y configura en Field el alias o limites que debe validar.
    disciplina: str = Field(min_length=1, max_length=150)


# Define la clase AreaConocimientoReemplazo y agrupa su estado y operaciones.
class AreaConocimientoReemplazo(BaseModel):
    """PUT /api/area_conocimiento/{id} — reemplazo COMPLETO.

    Omitir un campo es 422, no "dejarlo como estaba": esa es la semántica
    de PUT.
    """

    # Declara el campo gran_area y configura en Field el alias o limites que debe validar.
    gran_area: str = Field(alias="granArea", min_length=1, max_length=60)
    # Declara el campo area y configura en Field el alias o limites que debe validar.
    area: str = Field(min_length=1, max_length=60)
    # Declara el campo disciplina y configura en Field el alias o limites que debe validar.
    disciplina: str = Field(min_length=1, max_length=150)


# Define la clase AreaConocimientoActualizar y agrupa su estado y operaciones.
class AreaConocimientoActualizar(BaseModel):
    # Ejecuta la instruccion indicada dentro del flujo actual.
    """PATCH /api/area_conocimiento/{id} — solo se modifican los enviados."""

    # Declara el campo gran_area y configura en Field el alias o limites que debe validar.
    gran_area: str | None = Field(default=None, alias="granArea", min_length=1, max_length=60)
    # Declara el campo area y configura en Field el alias o limites que debe validar.
    area: str | None = Field(default=None, min_length=1, max_length=60)
    # Declara el campo disciplina y configura en Field el alias o limites que debe validar.
    disciplina: str | None = Field(default=None, min_length=1, max_length=150)
