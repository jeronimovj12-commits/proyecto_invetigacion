"""El alias camelCase conserva un JSON cómodo sin alterar los nombres SQL."""

from pydantic import BaseModel, ConfigDict, Field


class GrupoLineaCrear(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    grupo_investigacion: int = Field(alias="grupoInvestigacion")
    linea_investigacion: int = Field(alias="lineaInvestigacion")
