"""Los alias separan el formato del cliente de los nombres persistidos."""

from pydantic import BaseModel, ConfigDict, Field


class AaLineaCrear(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    area_aplicacion: int = Field(alias="areaAplicacion")
    linea_investigacion: int = Field(alias="lineaInvestigacion")
