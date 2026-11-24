"""Ejecución SQL parametrizada; solo identificadores fijos se componen para mantener SQL auditable."""

from sqlalchemy import text

from database import obtener_engine


class RepositorioPostgreSQLBase:
    TABLA = ""
    CLAVE = ""
    COLUMNAS: tuple[str, ...] = ()
    COLUMNAS_CREACION: tuple[str, ...] = ()

    def __init__(self):
        self._engine = obtener_engine()

    async def obtener_todos(self, limite: int) -> list[dict]:
        columnas = ", ".join(self.COLUMNAS)
        consulta = text(
            f"SELECT {columnas} FROM {self.TABLA} "
            f"WHERE activo = TRUE ORDER BY {self.CLAVE} LIMIT :limite"
        )
        async with self._engine.connect() as conexion:
            resultado = await conexion.execute(consulta, {"limite": limite})
            return [dict(fila._mapping) for fila in resultado]

    async def obtener_por_id(self, identificador: str | int) -> dict | None:
        columnas = ", ".join(self.COLUMNAS)
        consulta = text(
            f"SELECT {columnas} FROM {self.TABLA} "
            f"WHERE {self.CLAVE} = :identificador AND activo = TRUE"
        )
        async with self._engine.connect() as conexion:
            resultado = await conexion.execute(consulta, {"identificador": identificador})
            fila = resultado.first()
            return dict(fila._mapping) if fila else None

    async def crear(self, datos: dict) -> str | int | None:
        campos = self.COLUMNAS_CREACION
        nombres = ", ".join((*campos, "activo"))
        valores = ", ".join(f":{campo}" for campo in campos)
        consulta = text(
            f"INSERT INTO {self.TABLA} ({nombres}) VALUES ({valores}, TRUE) "
            f"RETURNING {self.CLAVE}"
        )
        parametros = {campo: datos[campo] for campo in campos}
        async with self._engine.begin() as conexion:
            resultado = await conexion.execute(consulta, parametros)
            return resultado.scalar_one()

    async def actualizar(self, identificador: str | int, datos: dict) -> int:
        campos = tuple(campo for campo in self.COLUMNAS if campo != self.CLAVE)
        cambios = tuple(campo for campo in campos if campo in datos)
        asignaciones = ", ".join(f"{campo} = :{campo}" for campo in cambios)
        consulta = text(
            f"UPDATE {self.TABLA} SET {asignaciones} "
            f"WHERE {self.CLAVE} = :identificador AND activo = TRUE"
        )
        parametros = {campo: datos[campo] for campo in cambios}
        parametros["identificador"] = identificador
        async with self._engine.begin() as conexion:
            resultado = await conexion.execute(consulta, parametros)
            return resultado.rowcount

    async def eliminar_logico(self, identificador: str | int) -> int:
        consulta = text(
            f"UPDATE {self.TABLA} SET activo = FALSE "
            f"WHERE {self.CLAVE} = :identificador AND activo = TRUE"
        )
        async with self._engine.begin() as conexion:
            resultado = await conexion.execute(consulta, {"identificador": identificador})
            return resultado.rowcount
