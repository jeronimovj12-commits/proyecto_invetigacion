"""SQL para relaciones de clave compuesta; columnas configuradas son constantes, valores siempre enlazados."""

from sqlalchemy import text

from database import obtener_engine


class RepositorioPostgreSQLCompuesto:
    TABLA = ""
    CLAVES: tuple[str, str] = ("", "")
    COLUMNAS: tuple[str, ...] = ()
    COLUMNAS_CREACION: tuple[str, ...] = ()

    def __init__(self):
        self._engine = obtener_engine()

    async def obtener_todos(self, limite: int) -> list[dict]:
        columnas = ", ".join(self.COLUMNAS)
        primero, segundo = self.CLAVES
        consulta = text(
            f"SELECT {columnas} FROM {self.TABLA} "
            f"WHERE activo = TRUE ORDER BY {primero}, {segundo} LIMIT :limite"
        )
        async with self._engine.connect() as conexion:
            resultado = await conexion.execute(consulta, {"limite": limite})
            return [dict(fila._mapping) for fila in resultado]

    async def _obtener_por_claves(self, primera: int, segunda: int) -> dict | None:
        primero, segundo = self.CLAVES
        columnas = ", ".join(self.COLUMNAS)
        consulta = text(
            f"SELECT {columnas} FROM {self.TABLA} "
            f"WHERE {primero} = :clave_primera AND {segundo} = :clave_segunda "
            "AND activo = TRUE"
        )
        async with self._engine.connect() as conexion:
            resultado = await conexion.execute(
                consulta, {"clave_primera": primera, "clave_segunda": segunda}
            )
            fila = resultado.first()
            return dict(fila._mapping) if fila else None

    async def _crear(self, datos: dict) -> None:
        campos = self.COLUMNAS_CREACION
        nombres = ", ".join((*campos, "activo"))
        valores = ", ".join(f":{campo}" for campo in campos)
        consulta = text(
            f"INSERT INTO {self.TABLA} ({nombres}) VALUES ({valores}, TRUE)"
        )
        parametros = {campo: datos[campo] for campo in campos}
        async with self._engine.begin() as conexion:
            await conexion.execute(consulta, parametros)

    async def _actualizar_por_claves(self, primera: int, segunda: int, datos: dict) -> int:
        primero, segundo = self.CLAVES
        campos = tuple(campo for campo in self.COLUMNAS if campo not in self.CLAVES)
        cambios = tuple(campo for campo in campos if campo in datos)
        asignaciones = ", ".join(f"{campo} = :{campo}" for campo in cambios)
        consulta = text(
            f"UPDATE {self.TABLA} SET {asignaciones} "
            f"WHERE {primero} = :clave_primera AND {segundo} = :clave_segunda "
            "AND activo = TRUE"
        )
        parametros = {campo: datos[campo] for campo in cambios}
        parametros.update({"clave_primera": primera, "clave_segunda": segunda})
        async with self._engine.begin() as conexion:
            resultado = await conexion.execute(consulta, parametros)
            return resultado.rowcount

    async def _eliminar_logico(self, primera: int, segunda: int) -> int:
        primero, segundo = self.CLAVES
        consulta = text(
            f"UPDATE {self.TABLA} SET activo = FALSE "
            f"WHERE {primero} = :clave_primera AND {segundo} = :clave_segunda "
            "AND activo = TRUE"
        )
        async with self._engine.begin() as conexion:
            resultado = await conexion.execute(
                consulta, {"clave_primera": primera, "clave_segunda": segunda}
            )
            return resultado.rowcount
