"""
Repositorio para PostgreSQL — la capa de DATOS.

SQLAlchemy async como EJECUTOR, no como ORM: el SQL se escribe a mano, queda
a la vista y SIEMPRE va parametrizado con `text()` y `:parametro`.

Todas las consultas filtran por activo = TRUE: el borrado es LÓGICO.
"""

# Importa text desde sqlalchemy para usar esas definiciones.
from sqlalchemy import text
# Importa ConexionPostgreSQL desde repositorios.conexion_postgresql para usar esas definiciones.
from repositorios.conexion_postgresql import ConexionPostgreSQL


# Define la clase RepositorioAreaConocimientoPostgreSQL y agrupa su estado y operaciones.
class RepositorioAreaConocimientoPostgreSQL(ConexionPostgreSQL):
    # Ejecuta la instruccion indicada dentro del flujo actual.
    """Implementación concreta de IRepositorioAreaConocimiento."""

    # Las columnas se listan una sola vez: si mañana entra una, entra aquí.
    # Asigna a COLUMNAS el valor calculado a la derecha.
    COLUMNAS = "id, gran_area, area, disciplina"

    # Define la funcion obtener_todos con los parametros declarados; su bloque realiza esta operacion.
    async def obtener_todos(self, limite: int) -> list[dict]:
        # Construye la consulta SQL que ejecutara este repositorio.
        sql = text(
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            f"SELECT {self.COLUMNAS} FROM area_conocimiento "
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            "WHERE activo = TRUE ORDER BY id LIMIT :limite"
        # Cierra la estructura abierta en las lineas anteriores.
        )
        # Abre el recurso asincronico y asegura su cierre al salir del bloque.
        async with self._conexion() as conexion:
            # Asigna a resultado el valor calculado a la derecha.
            resultado = await conexion.execute(sql, {"limite": limite})
            # Devuelve al llamador el resultado de la expresion indicada.
            return [dict(fila._mapping) for fila in resultado]

    # Define la funcion obtener_por_id con los parametros declarados; su bloque realiza esta operacion.
    async def obtener_por_id(self, id_area: str) -> dict | None:
        # Una fila inactiva responde como inexistente.
        # Construye la consulta SQL que ejecutara este repositorio.
        sql = text(
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            f"SELECT {self.COLUMNAS} FROM area_conocimiento "
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            "WHERE id = :id AND activo = TRUE"
        # Cierra la estructura abierta en las lineas anteriores.
        )
        # Abre el recurso asincronico y asegura su cierre al salir del bloque.
        async with self._conexion() as conexion:
            # Asigna a resultado el valor calculado a la derecha.
            resultado = await conexion.execute(sql, {"id": id_area})
            # Asigna a fila el valor calculado a la derecha.
            fila = resultado.first()
            # Devuelve al llamador el resultado de la expresion indicada.
            return dict(fila._mapping) if fila else None

    # Define la funcion crear con los parametros declarados; su bloque realiza esta operacion.
    async def crear(self, datos: dict) -> bool:
        # Construye la consulta SQL que ejecutara este repositorio.
        sql = text(
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            "INSERT INTO area_conocimiento (id, gran_area, area, disciplina, activo) "
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            "VALUES (:id, :gran_area, :area, :disciplina, TRUE)"
        # Cierra la estructura abierta en las lineas anteriores.
        )
        # Abre el recurso asincronico y asegura su cierre al salir del bloque.
        async with self._conexion() as conexion:
            # Asigna a resultado el valor calculado a la derecha.
            resultado = await conexion.execute(sql, datos)
            # Devuelve al llamador el resultado de la expresion indicada.
            return resultado.rowcount == 1

    # Define la funcion actualizar con los parametros declarados; su bloque realiza esta operacion.
    async def actualizar(self, id_area: str, datos: dict) -> int:
        # El PATCH escribe solo lo que llegó, así que la consulta se compone.
        # OJO: lo que se compone son NOMBRES DE COLUMNA de una lista cerrada
        # —las llaves del diccionario vienen de un modelo Pydantic, no del
        # usuario—; los VALORES siempre viajan como :parametro.
        # Asigna a asignaciones el valor calculado a la derecha.
        asignaciones = ", ".join(f"{columna} = :{columna}" for columna in datos)
        # Construye la consulta SQL que ejecutara este repositorio.
        sql = text(
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            f"UPDATE area_conocimiento SET {asignaciones} "
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            "WHERE id = :pk_id AND activo = TRUE"
        # Cierra la estructura abierta en las lineas anteriores.
        )
        # Abre el recurso asincronico y asegura su cierre al salir del bloque.
        async with self._conexion() as conexion:
            # Asigna a resultado el valor calculado a la derecha.
            resultado = await conexion.execute(sql, {**datos, "pk_id": id_area})
            # Devuelve al llamador el resultado de la expresion indicada.
            return resultado.rowcount

    # Define la funcion eliminar_logico con los parametros declarados; su bloque realiza esta operacion.
    async def eliminar_logico(self, id_area: str) -> int:
        # Borrado LÓGICO en una sola consulta: cero filas afectadas significa
        # "no existe o ya estaba inactiva", que es el 404 del contrato.
        # Construye la consulta SQL que ejecutara este repositorio.
        sql = text(
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            "UPDATE area_conocimiento SET activo = FALSE "
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            "WHERE id = :id AND activo = TRUE"
        # Cierra la estructura abierta en las lineas anteriores.
        )
        # Abre el recurso asincronico y asegura su cierre al salir del bloque.
        async with self._conexion() as conexion:
            # Asigna a resultado el valor calculado a la derecha.
            resultado = await conexion.execute(sql, {"id": id_area})
            # Devuelve al llamador el resultado de la expresion indicada.
            return resultado.rowcount

    # Define la funcion tiene_dependientes con los parametros declarados; su bloque realiza esta operacion.
    async def tiene_dependientes(self, id_area: str) -> bool:
        # Abre el recurso asincronico y asegura su cierre al salir del bloque.
        async with self._conexion() as conexion:
            # Asigna a resultado el valor calculado a la derecha.
            resultado = await conexion.execute(text("SELECT EXISTS (SELECT 1 FROM ac_linea WHERE area_conocimiento = :id AND activo = TRUE)"), {"id": id_area})
            # Devuelve al llamador el resultado de la expresion indicada.
            return bool(resultado.scalar())
