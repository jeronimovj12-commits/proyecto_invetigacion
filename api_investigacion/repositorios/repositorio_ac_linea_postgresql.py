# Ejecuta la instruccion indicada dentro del flujo actual.
"""SQL explícito y parametrizado para ac_linea."""
# Importa text desde sqlalchemy para usar esas definiciones.
from sqlalchemy import text
# Importa ConexionPostgreSQL desde repositorios.conexion_postgresql para usar esas definiciones.
from repositorios.conexion_postgresql import ConexionPostgreSQL


# Define la clase RepositorioAcLineaPostgreSQL y agrupa su estado y operaciones.
class RepositorioAcLineaPostgreSQL(ConexionPostgreSQL):
    # Define la funcion obtener_todos con los parametros declarados; su bloque realiza esta operacion.
    async def obtener_todos(self, limite: int) -> list[dict]:
        # Abre el recurso asincronico y asegura su cierre al salir del bloque.
        async with self._conexion() as conexion:
            # Asigna a resultado el valor calculado a la derecha.
            resultado = await conexion.execute(text("SELECT linea_investigacion, area_conocimiento FROM ac_linea WHERE activo = TRUE LIMIT :limite"), {"limite": limite})
            # Devuelve al llamador el resultado de la expresion indicada.
            return [dict(fila) for fila in resultado.mappings()]

    # Define la funcion obtener_por_id con los parametros declarados; su bloque realiza esta operacion.
    async def obtener_por_id(self, identidad: dict) -> dict | None:
        # Abre el recurso asincronico y asegura su cierre al salir del bloque.
        async with self._conexion() as conexion:
            # Asigna a resultado el valor calculado a la derecha.
            resultado = await conexion.execute(text("SELECT linea_investigacion, area_conocimiento FROM ac_linea WHERE linea_investigacion = :linea_investigacion AND area_conocimiento = :area_conocimiento AND activo = TRUE"), identidad)
            # Asigna a fila el valor calculado a la derecha.
            fila = resultado.mappings().first()
            # Devuelve al llamador el resultado de la expresion indicada.
            return dict(fila) if fila is not None else None

    # Define la funcion crear con los parametros declarados; su bloque realiza esta operacion.
    async def crear(self, datos: dict) -> None:
        # Abre el recurso asincronico y asegura su cierre al salir del bloque.
        async with self._conexion() as conexion:
            # Espera que termine la operacion asincronica antes de continuar.
            await conexion.execute(text("INSERT INTO ac_linea (linea_investigacion, area_conocimiento, activo) VALUES (:linea_investigacion, :area_conocimiento, TRUE)"), datos)

    # Define la funcion actualizar con los parametros declarados; su bloque realiza esta operacion.
    async def actualizar(self, identidad: dict, datos: dict) -> int:
        # Asigna a permitidos el valor calculado a la derecha.
        permitidos = ('linea_investigacion', 'area_conocimiento')
        # Ejecuta el bloque siguiente solo cuando se cumple: not datos or any(campo not in permitidos for campo in datos).
        if not datos or any(campo not in permitidos for campo in datos):
            # Lanza la excepcion indicada y detiene el flujo normal.
            raise ValueError("Campos de actualización inválidos.")
        # Solo se componen nombres de columnas de una lista cerrada.
        # Asigna a asignaciones el valor calculado a la derecha.
        asignaciones = ", ".join(f"{campo} = :{campo}" for campo in datos)
        # Asigna a parametros el valor calculado a la derecha.
        parametros = {**datos, **{f"pk_{campo}": valor for campo, valor in identidad.items()}}
        # Abre el recurso asincronico y asegura su cierre al salir del bloque.
        async with self._conexion() as conexion:
            # Asigna a resultado el valor calculado a la derecha.
            resultado = await conexion.execute(text(f"UPDATE ac_linea SET {asignaciones} WHERE linea_investigacion = :pk_linea_investigacion AND area_conocimiento = :pk_area_conocimiento AND activo = TRUE"), parametros)
            # Devuelve al llamador el resultado de la expresion indicada.
            return resultado.rowcount

    # Define la funcion eliminar_logico con los parametros declarados; su bloque realiza esta operacion.
    async def eliminar_logico(self, identidad: dict) -> int:
        # Abre el recurso asincronico y asegura su cierre al salir del bloque.
        async with self._conexion() as conexion:
            # Asigna a resultado el valor calculado a la derecha.
            resultado = await conexion.execute(text("UPDATE ac_linea SET activo = FALSE WHERE linea_investigacion = :linea_investigacion AND area_conocimiento = :area_conocimiento AND activo = TRUE"), identidad)
            # Devuelve al llamador el resultado de la expresion indicada.
            return resultado.rowcount

    # Define la funcion referencia_activa con los parametros declarados; su bloque realiza esta operacion.
    async def referencia_activa(self, campo: str, valor) -> bool:
        # Asigna a consultas el valor calculado a la derecha.
        consultas = {'linea_investigacion': 'SELECT 1 FROM linea_investigacion WHERE id = :valor AND activo = TRUE', 'area_conocimiento': 'SELECT 1 FROM area_conocimiento WHERE id = :valor AND activo = TRUE'}
        # Ejecuta el bloque siguiente solo cuando se cumple: campo not in consultas.
        if campo not in consultas:
            # Lanza la excepcion indicada y detiene el flujo normal.
            raise ValueError("La referencia no pertenece a esta tabla.")
        # Abre el recurso asincronico y asegura su cierre al salir del bloque.
        async with self._conexion() as conexion:
            # Asigna a resultado el valor calculado a la derecha.
            resultado = await conexion.execute(text(consultas[campo]), {"valor": valor})
            # Devuelve al llamador el resultado de la expresion indicada.
            return resultado.first() is not None

    # Define la funcion tiene_dependientes con los parametros declarados; su bloque realiza esta operacion.
    async def tiene_dependientes(self, identidad: dict) -> bool:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False
