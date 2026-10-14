"""SQL explícito y parametrizado para participa_grupo."""
from sqlalchemy import text
from repositorios.conexion_postgresql import ConexionPostgreSQL


class RepositorioParticipaGrupoPostgreSQL(ConexionPostgreSQL):
    async def obtener_todos(self, limite: int) -> list[dict]:
        async with self._conexion() as conexion:
            resultado = await conexion.execute(text("SELECT docente_cedula, grupo_investigacion_id, rol, fecha_inicio, fecha_fin FROM participa_grupo WHERE activo = TRUE LIMIT :limite"), {"limite": limite})
            return [dict(fila) for fila in resultado.mappings()]

    async def obtener_por_id(self, identidad: dict) -> dict | None:
        async with self._conexion() as conexion:
            resultado = await conexion.execute(text("SELECT docente_cedula, grupo_investigacion_id, rol, fecha_inicio, fecha_fin FROM participa_grupo WHERE docente_cedula = :docente_cedula AND grupo_investigacion_id = :grupo_investigacion_id AND activo = TRUE"), identidad)
            fila = resultado.mappings().first()
            return dict(fila) if fila is not None else None

    async def crear(self, datos: dict) -> None:
        async with self._conexion() as conexion:
            await conexion.execute(text("INSERT INTO participa_grupo (docente_cedula, grupo_investigacion_id, rol, fecha_inicio, fecha_fin, activo) VALUES (:docente_cedula, :grupo_investigacion_id, :rol, :fecha_inicio, :fecha_fin, TRUE)"), datos)

    async def actualizar(self, identidad: dict, datos: dict) -> int:
        permitidos = ('docente_cedula', 'grupo_investigacion_id', 'rol', 'fecha_inicio', 'fecha_fin')
        if not datos or any(campo not in permitidos for campo in datos):
            raise ValueError("Campos de actualización inválidos.")
        # Solo se componen nombres de columnas de una lista cerrada.
        asignaciones = ", ".join(f"{campo} = :{campo}" for campo in datos)
        parametros = {**datos, **{f"pk_{campo}": valor for campo, valor in identidad.items()}}
        async with self._conexion() as conexion:
            resultado = await conexion.execute(text(f"UPDATE participa_grupo SET {asignaciones} WHERE docente_cedula = :pk_docente_cedula AND grupo_investigacion_id = :pk_grupo_investigacion_id AND activo = TRUE"), parametros)
            return resultado.rowcount

    async def eliminar_logico(self, identidad: dict) -> int:
        async with self._conexion() as conexion:
            resultado = await conexion.execute(text("UPDATE participa_grupo SET activo = FALSE WHERE docente_cedula = :docente_cedula AND grupo_investigacion_id = :grupo_investigacion_id AND activo = TRUE"), identidad)
            return resultado.rowcount

    async def referencia_activa(self, campo: str, valor) -> bool:
        consultas = {'docente_cedula': 'SELECT 1 FROM docente WHERE cedula = :valor AND activo = TRUE', 'grupo_investigacion_id': 'SELECT 1 FROM grupo_investigacion WHERE id = :valor AND activo = TRUE'}
        if campo not in consultas:
            raise ValueError("La referencia no pertenece a esta tabla.")
        async with self._conexion() as conexion:
            resultado = await conexion.execute(text(consultas[campo]), {"valor": valor})
            return resultado.first() is not None

    async def tiene_dependientes(self, identidad: dict) -> bool:
        return False
