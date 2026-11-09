"""SQL explícito y parametrizado para semillero."""
from sqlalchemy import text
from repositorios.conexion_postgresql import ConexionPostgreSQL


class RepositorioSemilleroPostgreSQL(ConexionPostgreSQL):
    async def obtener_todos(self, limite: int) -> list[dict]:
        async with self._conexion() as conexion:
            resultado = await conexion.execute(text("SELECT id, nombre, fecha_fundacion, grupo_investigacion FROM semillero WHERE activo = TRUE LIMIT :limite"), {"limite": limite})
            return [dict(fila) for fila in resultado.mappings()]

    async def obtener_por_id(self, identidad: dict) -> dict | None:
        async with self._conexion() as conexion:
            resultado = await conexion.execute(text("SELECT id, nombre, fecha_fundacion, grupo_investigacion FROM semillero WHERE id = :id AND activo = TRUE"), identidad)
            fila = resultado.mappings().first()
            return dict(fila) if fila is not None else None

    async def crear(self, datos: dict) -> None:
        async with self._conexion() as conexion:
            await conexion.execute(text("INSERT INTO semillero (id, nombre, fecha_fundacion, grupo_investigacion, activo) VALUES (:id, :nombre, :fecha_fundacion, :grupo_investigacion, TRUE)"), datos)

    async def actualizar(self, identidad: dict, datos: dict) -> int:
        permitidos = ('nombre', 'fecha_fundacion', 'grupo_investigacion')
        if not datos or any(campo not in permitidos for campo in datos):
            raise ValueError("Campos de actualización inválidos.")
        # Solo se componen nombres de columnas de una lista cerrada.
        asignaciones = ", ".join(f"{campo} = :{campo}" for campo in datos)
        parametros = {**datos, **{f"pk_{campo}": valor for campo, valor in identidad.items()}}
        async with self._conexion() as conexion:
            resultado = await conexion.execute(text(f"UPDATE semillero SET {asignaciones} WHERE id = :pk_id AND activo = TRUE"), parametros)
            return resultado.rowcount

    async def eliminar_logico(self, identidad: dict) -> int:
        async with self._conexion() as conexion:
            resultado = await conexion.execute(text("UPDATE semillero SET activo = FALSE WHERE id = :id AND activo = TRUE"), identidad)
            return resultado.rowcount

    async def referencia_activa(self, campo: str, valor) -> bool:
        consultas = {'grupo_investigacion': 'SELECT 1 FROM grupo_investigacion WHERE id = :valor AND activo = TRUE'}
        if campo not in consultas:
            raise ValueError("La referencia no pertenece a esta tabla.")
        async with self._conexion() as conexion:
            resultado = await conexion.execute(text(consultas[campo]), {"valor": valor})
            return resultado.first() is not None

    async def tiene_dependientes(self, identidad: dict) -> bool:
        async with self._conexion() as conexion:
            resultado = await conexion.execute(text("SELECT EXISTS (SELECT 1 FROM participa_semillero WHERE semillero = :id AND activo = TRUE) OR EXISTS (SELECT 1 FROM semillero_linea WHERE semillero = :id AND activo = TRUE)"), identidad)
            return bool(resultado.scalar())
