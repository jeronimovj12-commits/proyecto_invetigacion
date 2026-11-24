"""Los alias hacen explícito el contrato JSON aunque «ods» no cambie de capitalización."""

from pydantic import BaseModel, ConfigDict, Field


class OdsLineaCrear(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    linea_investigacion: int = Field(alias="lineaInvestigacion")
    ods: int = Field(alias="ods")
