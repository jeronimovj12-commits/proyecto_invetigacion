# Ejecuta la instruccion indicada dentro del flujo actual.
"""SQL explícito y parametrizado para participa_semillero."""
# Importa text desde sqlalchemy para usar esas definiciones.
from sqlalchemy import text
# Importa ConexionPostgreSQL desde repositorios.conexion_postgresql para usar esas definiciones.
from repositorios.conexion_postgresql import ConexionPostgreSQL


# Define la clase RepositorioParticipaSemilleroPostgreSQL y agrupa su estado y operaciones.
class RepositorioParticipaSemilleroPostgreSQL(ConexionPostgreSQL):
    # Define la funcion obtener_todos con los parametros declarados; su bloque realiza esta operacion.
    async def obtener_todos(self, limite: int) -> list[dict]:
        # Abre el recurso asincronico y asegura su cierre al salir del bloque.
        async with self._conexion() as conexion:
            # Asigna a resultado el valor calculado a la derecha.
            resultado = await conexion.execute(text("SELECT docente, semillero, rol, fecha_inicio, fecha_fin FROM participa_semillero WHERE activo = TRUE LIMIT :limite"), {"limite": limite})
            # Devuelve al llamador el resultado de la expresion indicada.
            return [dict(fila) for fila in resultado.mappings()]

    # Define la funcion obtener_por_id con los parametros declarados; su bloque realiza esta operacion.
    async def obtener_por_id(self, identidad: dict) -> dict | None:
        # Abre el recurso asincronico y asegura su cierre al salir del bloque.
        async with self._conexion() as conexion:
            # Asigna a resultado el valor calculado a la derecha.
            resultado = await conexion.execute(text("SELECT docente, semillero, rol, fecha_inicio, fecha_fin FROM participa_semillero WHERE docente = :docente AND semillero = :semillero AND activo = TRUE"), identidad)
            # Asigna a fila el valor calculado a la derecha.
            fila = resultado.mappings().first()
            # Devuelve al llamador el resultado de la expresion indicada.
            return dict(fila) if fila is not None else None

    # Define la funcion crear con los parametros declarados; su bloque realiza esta operacion.
    async def crear(self, datos: dict) -> None:
        # Abre el recurso asincronico y asegura su cierre al salir del bloque.
        async with self._conexion() as conexion:
            # Espera que termine la operacion asincronica antes de continuar.
            await conexion.execute(text("INSERT INTO participa_semillero (docente, semillero, rol, fecha_inicio, fecha_fin, activo) VALUES (:docente, :semillero, :rol, :fecha_inicio, :fecha_fin, TRUE)"), datos)

    # Define la funcion actualizar con los parametros declarados; su bloque realiza esta operacion.
    async def actualizar(self, identidad: dict, datos: dict) -> int:
        # Asigna a permitidos el valor calculado a la derecha.
        permitidos = ('docente', 'semillero', 'rol', 'fecha_inicio', 'fecha_fin')
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
            resultado = await conexion.execute(text(f"UPDATE participa_semillero SET {asignaciones} WHERE docente = :pk_docente AND semillero = :pk_semillero AND activo = TRUE"), parametros)
            # Devuelve al llamador el resultado de la expresion indicada.
            return resultado.rowcount

    # Define la funcion eliminar_logico con los parametros declarados; su bloque realiza esta operacion.
    async def eliminar_logico(self, identidad: dict) -> int:
        # Abre el recurso asincronico y asegura su cierre al salir del bloque.
        async with self._conexion() as conexion:
            # Asigna a resultado el valor calculado a la derecha.
            resultado = await conexion.execute(text("UPDATE participa_semillero SET activo = FALSE WHERE docente = :docente AND semillero = :semillero AND activo = TRUE"), identidad)
            # Devuelve al llamador el resultado de la expresion indicada.
            return resultado.rowcount

    # Define la funcion referencia_activa con los parametros declarados; su bloque realiza esta operacion.
    async def referencia_activa(self, campo: str, valor) -> bool:
        # Asigna a consultas el valor calculado a la derecha.
        consultas = {'docente': 'SELECT 1 FROM docente WHERE cedula = :valor AND activo = TRUE', 'semillero': 'SELECT 1 FROM semillero WHERE id = :valor AND activo = TRUE'}
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
