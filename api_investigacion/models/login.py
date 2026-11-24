"""El contrato de login restringe la entrada a las credenciales necesarias."""

from pydantic import BaseModel, ConfigDict, Field


class LoginCrear(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    username: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=1, max_length=72)
