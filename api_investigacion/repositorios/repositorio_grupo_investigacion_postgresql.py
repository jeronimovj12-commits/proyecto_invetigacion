"""SQL explícito y parametrizado para grupo_investigacion."""
from sqlalchemy import text
from repositorios.conexion_postgresql import ConexionPostgreSQL


class RepositorioGrupoInvestigacionPostgreSQL(ConexionPostgreSQL):
    async def obtener_todos(self, limite: int) -> list[dict]:
        async with self._conexion() as conexion:
            resultado = await conexion.execute(text("SELECT id, nombre, url_gruplac, categoria, convocatoria, fecha_fundacion, universidsad, interno, ambito FROM grupo_investigacion WHERE activo = TRUE LIMIT :limite"), {"limite": limite})
            return [dict(fila) for fila in resultado.mappings()]

    async def obtener_por_id(self, identidad: dict) -> dict | None:
        async with self._conexion() as conexion:
            resultado = await conexion.execute(text("SELECT id, nombre, url_gruplac, categoria, convocatoria, fecha_fundacion, universidsad, interno, ambito FROM grupo_investigacion WHERE id = :id AND activo = TRUE"), identidad)
            fila = resultado.mappings().first()
            return dict(fila) if fila is not None else None

    async def crear(self, datos: dict) -> None:
        async with self._conexion() as conexion:
            await conexion.execute(text("INSERT INTO grupo_investigacion (id, nombre, url_gruplac, categoria, convocatoria, fecha_fundacion, universidsad, interno, ambito, activo) VALUES (:id, :nombre, :url_gruplac, :categoria, :convocatoria, :fecha_fundacion, :universidsad, :interno, :ambito, TRUE)"), datos)

    async def actualizar(self, identidad: dict, datos: dict) -> int:
        permitidos = ('nombre', 'url_gruplac', 'categoria', 'convocatoria', 'fecha_fundacion', 'universidsad', 'interno', 'ambito')
        if not datos or any(campo not in permitidos for campo in datos):
            raise ValueError("Campos de actualización inválidos.")
        # Solo se componen nombres de columnas de una lista cerrada.
        asignaciones = ", ".join(f"{campo} = :{campo}" for campo in datos)
        parametros = {**datos, **{f"pk_{campo}": valor for campo, valor in identidad.items()}}
        async with self._conexion() as conexion:
            resultado = await conexion.execute(text(f"UPDATE grupo_investigacion SET {asignaciones} WHERE id = :pk_id AND activo = TRUE"), parametros)
            return resultado.rowcount

    async def eliminar_logico(self, identidad: dict) -> int:
        async with self._conexion() as conexion:
            resultado = await conexion.execute(text("UPDATE grupo_investigacion SET activo = FALSE WHERE id = :id AND activo = TRUE"), identidad)
            return resultado.rowcount

    async def referencia_activa(self, campo: str, valor) -> bool:
        consultas = {'universidsad': 'SELECT 1 FROM universidad WHERE id = :valor AND activo = TRUE'}
        if campo not in consultas:
            raise ValueError("La referencia no pertenece a esta tabla.")
        async with self._conexion() as conexion:
            resultado = await conexion.execute(text(consultas[campo]), {"valor": valor})
            return resultado.first() is not None

    async def tiene_dependientes(self, identidad: dict) -> bool:
        async with self._conexion() as conexion:
            resultado = await conexion.execute(text("SELECT EXISTS (SELECT 1 FROM semillero WHERE grupo_investigacion = :id AND activo = TRUE) OR EXISTS (SELECT 1 FROM participa_grupo WHERE grupo_investigacion_id = :id AND activo = TRUE) OR EXISTS (SELECT 1 FROM grupo_linea WHERE grupo_investigacion = :id AND activo = TRUE)"), identidad)
            return bool(resultado.scalar())
