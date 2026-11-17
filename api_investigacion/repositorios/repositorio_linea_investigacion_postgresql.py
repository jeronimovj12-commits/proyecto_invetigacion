# Ejecuta la instruccion indicada dentro del flujo actual.
"""SQL explícito y parametrizado para linea_investigacion."""
# Importa text desde sqlalchemy para usar esas definiciones.
from sqlalchemy import text
# Importa ConexionPostgreSQL desde repositorios.conexion_postgresql para usar esas definiciones.
from repositorios.conexion_postgresql import ConexionPostgreSQL


# Define la clase RepositorioLineaInvestigacionPostgreSQL y agrupa su estado y operaciones.
class RepositorioLineaInvestigacionPostgreSQL(ConexionPostgreSQL):
    # Define la funcion obtener_todos con los parametros declarados; su bloque realiza esta operacion.
    async def obtener_todos(self, limite: int) -> list[dict]:
        # Abre el recurso asincronico y asegura su cierre al salir del bloque.
        async with self._conexion() as conexion:
            # Asigna a resultado el valor calculado a la derecha.
            resultado = await conexion.execute(text("SELECT id, nombre, descripcion FROM linea_investigacion WHERE activo = TRUE LIMIT :limite"), {"limite": limite})
            # Devuelve al llamador el resultado de la expresion indicada.
            return [dict(fila) for fila in resultado.mappings()]

    # Define la funcion obtener_por_id con los parametros declarados; su bloque realiza esta operacion.
    async def obtener_por_id(self, identidad: dict) -> dict | None:
        # Abre el recurso asincronico y asegura su cierre al salir del bloque.
        async with self._conexion() as conexion:
            # Asigna a resultado el valor calculado a la derecha.
            resultado = await conexion.execute(text("SELECT id, nombre, descripcion FROM linea_investigacion WHERE id = :id AND activo = TRUE"), identidad)
            # Asigna a fila el valor calculado a la derecha.
            fila = resultado.mappings().first()
            # Devuelve al llamador el resultado de la expresion indicada.
            return dict(fila) if fila is not None else None
