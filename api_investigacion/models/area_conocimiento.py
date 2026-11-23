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

from pydantic import BaseModel, Field


class AreaConocimiento(BaseModel):
    """POST /api/area_conocimiento — todos los campos son obligatorios."""

    # El id es TEXTO, no un entero: los datos del catálogo son códigos como
    # '1A01'. Ver la clarificación C1.
    id: str = Field(min_length=1, max_length=6)
    gran_area: str = Field(alias="granArea", min_length=1, max_length=60)
    area: str = Field(min_length=1, max_length=60)
    disciplina: str = Field(min_length=1, max_length=150)


class AreaConocimientoReemplazo(BaseModel):
    """PUT /api/area_conocimiento/{id} — reemplazo COMPLETO.

    Omitir un campo es 422, no "dejarlo como estaba": esa es la semántica
    de PUT.
    """

    gran_area: str = Field(alias="granArea", min_length=1, max_length=60)
    area: str = Field(min_length=1, max_length=60)
    disciplina: str = Field(min_length=1, max_length=150)


class AreaConocimientoActualizar(BaseModel):
    """PATCH /api/area_conocimiento/{id} — solo se modifican los enviados."""

    gran_area: str | None = Field(default=None, alias="granArea", min_length=1, max_length=60)
    area: str | None = Field(default=None, min_length=1, max_length=60)
    disciplina: str | None = Field(default=None, min_length=1, max_length=150)
