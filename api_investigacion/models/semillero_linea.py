"""El contrato público usa alias explícitos y deja la persistencia en snake_case."""

from pydantic import BaseModel, ConfigDict, Field


class SemilleroLineaCrear(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    semillero: int = Field(alias="semillero")
    linea_investigacion: int = Field(alias="lineaInvestigacion")
