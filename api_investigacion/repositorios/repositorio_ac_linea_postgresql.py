"""SQL explícito y parametrizado para ac_linea."""
from sqlalchemy import text
from repositorios.conexion_postgresql import ConexionPostgreSQL


class RepositorioAcLineaPostgreSQL(ConexionPostgreSQL):
    async def obtener_todos(self, limite: int) -> list[dict]:
        async with self._conexion() as conexion:
            resultado = await conexion.execute(text("SELECT linea_investigacion, area_conocimiento FROM ac_linea WHERE activo = TRUE LIMIT :limite"), {"limite": limite})
            return [dict(fila) for fila in resultado.mappings()]

    async def obtener_por_id(self, identidad: dict) -> dict | None:
        async with self._conexion() as conexion:
            resultado = await conexion.execute(text("SELECT linea_investigacion, area_conocimiento FROM ac_linea WHERE linea_investigacion = :linea_investigacion AND area_conocimiento = :area_conocimiento AND activo = TRUE"), identidad)
            fila = resultado.mappings().first()
            return dict(fila) if fila is not None else None

    async def crear(self, datos: dict) -> None:
        async with self._conexion() as conexion:
            await conexion.execute(text("INSERT INTO ac_linea (linea_investigacion, area_conocimiento, activo) VALUES (:linea_investigacion, :area_conocimiento, TRUE)"), datos)

    async def actualizar(self, identidad: dict, datos: dict) -> int:
        permitidos = ('linea_investigacion', 'area_conocimiento')
        if not datos or any(campo not in permitidos for campo in datos):
            raise ValueError("Campos de actualización inválidos.")
        # Solo se componen nombres de columnas de una lista cerrada.
        asignaciones = ", ".join(f"{campo} = :{campo}" for campo in datos)
        parametros = {**datos, **{f"pk_{campo}": valor for campo, valor in identidad.items()}}
        async with self._conexion() as conexion:
            resultado = await conexion.execute(text(f"UPDATE ac_linea SET {asignaciones} WHERE linea_investigacion = :pk_linea_investigacion AND area_conocimiento = :pk_area_conocimiento AND activo = TRUE"), parametros)
            return resultado.rowcount

    async def eliminar_logico(self, identidad: dict) -> int:
        async with self._conexion() as conexion:
            resultado = await conexion.execute(text("UPDATE ac_linea SET activo = FALSE WHERE linea_investigacion = :linea_investigacion AND area_conocimiento = :area_conocimiento AND activo = TRUE"), identidad)
            return resultado.rowcount

    async def referencia_activa(self, campo: str, valor) -> bool:
        consultas = {'linea_investigacion': 'SELECT 1 FROM linea_investigacion WHERE id = :valor AND activo = TRUE', 'area_conocimiento': 'SELECT 1 FROM area_conocimiento WHERE id = :valor AND activo = TRUE'}
        if campo not in consultas:
            raise ValueError("La referencia no pertenece a esta tabla.")
        async with self._conexion() as conexion:
            resultado = await conexion.execute(text(consultas[campo]), {"valor": valor})
            return resultado.first() is not None

    async def tiene_dependientes(self, identidad: dict) -> bool:
        return False
