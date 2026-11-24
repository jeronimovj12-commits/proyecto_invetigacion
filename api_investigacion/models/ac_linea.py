"""El código de área se mantiene textual porque así lo define la clave de la base."""

from pydantic import BaseModel, ConfigDict, Field


class AcLineaCrear(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    linea_investigacion: int = Field(alias="lineaInvestigacion")
    area_conocimiento: str = Field(alias="areaConocimiento", min_length=1, max_length=6)
