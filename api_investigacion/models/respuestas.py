"""Modelos de salida mantienen los alias camelCase del contrato sin contaminar SQL."""

from pydantic import BaseModel, ConfigDict, Field


class RespuestaActualizacion(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    estado: int
    mensaje: str
    filas_afectadas: int = Field(alias="filasAfectadas")


class RespuestaCreacion(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    estado: int
    mensaje: str
