"""La asignación se identifica por sus dos claves y no tiene estado activo propio."""

from pydantic import BaseModel, ConfigDict, Field


class RolUsuarioCrear(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    usuario_id: int = Field(alias="usuarioId")
    rol_id: int = Field(alias="rolId")
