"""SQL explícito y parametrizado para docente."""
from sqlalchemy import text
from repositorios.conexion_postgresql import ConexionPostgreSQL


class RepositorioDocentePostgreSQL(ConexionPostgreSQL):
    async def obtener_todos(self, limite: int) -> list[dict]:
        async with self._conexion() as conexion:
            resultado = await conexion.execute(text("SELECT cedula, nombres, apellidos, genero, cargo, fecha_nacimiento, correo, telefono, url_cvlac, fecha_actualizacion, escalafon, perfil, cat_minciencia, conv_minciencia, nacionalidaad, linea_investigacion_principal FROM docente WHERE activo = TRUE LIMIT :limite"), {"limite": limite})
            return [dict(fila) for fila in resultado.mappings()]

    async def obtener_por_id(self, identidad: dict) -> dict | None:
        async with self._conexion() as conexion:
            resultado = await conexion.execute(text("SELECT cedula, nombres, apellidos, genero, cargo, fecha_nacimiento, correo, telefono, url_cvlac, fecha_actualizacion, escalafon, perfil, cat_minciencia, conv_minciencia, nacionalidaad, linea_investigacion_principal FROM docente WHERE cedula = :cedula AND activo = TRUE"), identidad)
            fila = resultado.mappings().first()
            return dict(fila) if fila is not None else None

    async def crear(self, datos: dict) -> None:
        async with self._conexion() as conexion:
            await conexion.execute(text("INSERT INTO docente (cedula, nombres, apellidos, genero, cargo, fecha_nacimiento, correo, telefono, url_cvlac, fecha_actualizacion, escalafon, perfil, cat_minciencia, conv_minciencia, nacionalidaad, linea_investigacion_principal, activo) VALUES (:cedula, :nombres, :apellidos, :genero, :cargo, :fecha_nacimiento, :correo, :telefono, :url_cvlac, :fecha_actualizacion, :escalafon, :perfil, :cat_minciencia, :conv_minciencia, :nacionalidaad, :linea_investigacion_principal, TRUE)"), datos)

    async def actualizar(self, identidad: dict, datos: dict) -> int:
        permitidos = ('nombres', 'apellidos', 'genero', 'cargo', 'fecha_nacimiento', 'correo', 'telefono', 'url_cvlac', 'fecha_actualizacion', 'escalafon', 'perfil', 'cat_minciencia', 'conv_minciencia', 'nacionalidaad', 'linea_investigacion_principal')
        if not datos or any(campo not in permitidos for campo in datos):
            raise ValueError("Campos de actualización inválidos.")
        # Solo se componen nombres de columnas de una lista cerrada.
        asignaciones = ", ".join(f"{campo} = :{campo}" for campo in datos)
        parametros = {**datos, **{f"pk_{campo}": valor for campo, valor in identidad.items()}}
        async with self._conexion() as conexion:
            resultado = await conexion.execute(text(f"UPDATE docente SET {asignaciones} WHERE cedula = :pk_cedula AND activo = TRUE"), parametros)
            return resultado.rowcount

    async def eliminar_logico(self, identidad: dict) -> int:
        async with self._conexion() as conexion:
            resultado = await conexion.execute(text("UPDATE docente SET activo = FALSE WHERE cedula = :cedula AND activo = TRUE"), identidad)
            return resultado.rowcount

    async def referencia_activa(self, campo: str, valor) -> bool:
        consultas = {'linea_investigacion_principal': 'SELECT 1 FROM linea_investigacion WHERE id = :valor AND activo = TRUE'}
        if campo not in consultas:
            raise ValueError("La referencia no pertenece a esta tabla.")
        async with self._conexion() as conexion:
            resultado = await conexion.execute(text(consultas[campo]), {"valor": valor})
            return resultado.first() is not None

    async def tiene_dependientes(self, identidad: dict) -> bool:
        async with self._conexion() as conexion:
            resultado = await conexion.execute(text("SELECT EXISTS (SELECT 1 FROM participa_semillero WHERE docente = :cedula AND activo = TRUE) OR EXISTS (SELECT 1 FROM participa_grupo WHERE docente_cedula = :cedula AND activo = TRUE)"), identidad)
            return bool(resultado.scalar())
