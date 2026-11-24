"""Los alias hacen explícita la frontera JSON sin cambiar columnas PostgreSQL."""

from pydantic import BaseModel, ConfigDict, Field


class _Base(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")


class RolCrear(_Base):
    nombre: str = Field(min_length=1, max_length=100)
    descripcion: str | None = None


class RolReemplazo(_Base):
    nombre: str = Field(min_length=1, max_length=100)
    descripcion: str | None


class RolActualizar(_Base):
    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    descripcion: str | None = None
