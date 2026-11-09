from pydantic import BaseModel, ConfigDict, Field, SecretStr, model_validator

class Entrada(BaseModel):
    model_config = ConfigDict(extra='forbid', str_strip_whitespace=True)

class UsuarioCrear(Entrada):
    username: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=1, max_length=150)
    nombre_completo: str | None = Field(default=None, max_length=200)
    password: SecretStr = Field(min_length=12, max_length=1024)

class UsuarioEditar(Entrada):
    username: str | None = Field(default=None, min_length=1, max_length=100)
    email: str | None = Field(default=None, min_length=1, max_length=150)
    nombre_completo: str | None = Field(default=None, max_length=200)
    password: SecretStr | None = Field(default=None, min_length=12, max_length=1024)

    @model_validator(mode='after')
    def no_nulos(self):
        if any(getattr(self, c) is None for c in self.model_fields_set - {'nombre_completo'}):
            raise ValueError('Los campos obligatorios no admiten null.')
        return self

class RolCrear(Entrada):
    nombre: str = Field(min_length=1, max_length=100)
    descripcion: str | None = Field(default=None, max_length=2000)

class RolEditar(Entrada):
    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    descripcion: str | None = Field(default=None, max_length=2000)

    @model_validator(mode='after')
    def no_nulo(self):
        if 'nombre' in self.model_fields_set and self.nombre is None:
            raise ValueError('El nombre no admite null.')
        return self

class AsignacionCrear(Entrada):
    usuario_id: int = Field(gt=0)
    rol_id: int = Field(gt=0)


class AsignacionEditar(Entrada):
    usuario_id: int | None = Field(default=None, gt=0)
    rol_id: int | None = Field(default=None, gt=0)

    @model_validator(mode='after')
    def no_nulos(self):
        if any(getattr(self, c) is None for c in self.model_fields_set):
            raise ValueError('Los identificadores no admiten null.')
        return self
