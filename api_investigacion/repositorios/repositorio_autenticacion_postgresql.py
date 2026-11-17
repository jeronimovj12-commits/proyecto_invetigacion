# Ejecuta la instruccion indicada dentro del flujo actual.
"""Repositorio PostgreSQL: ejecuta consultas parametrizadas y adapta filas de la base a datos de la aplicacion."""
# Importa text desde sqlalchemy para usar esas definiciones.
from sqlalchemy import text
# Importa IntegrityError, DBAPIError desde sqlalchemy.exc para usar esas definiciones.
from sqlalchemy.exc import IntegrityError, DBAPIError
# Importa create_async_engine desde sqlalchemy.ext.asyncio para usar esas definiciones.
from sqlalchemy.ext.asyncio import create_async_engine

# Importa ConexionPostgreSQL desde repositorios.conexion_postgresql para usar esas definiciones.
from repositorios.conexion_postgresql import ConexionPostgreSQL
# Importa ConflictoInicializacion desde seguridad.errores para usar esas definiciones.
from seguridad.errores import ConflictoInicializacion


# Define la clase RepositorioAutenticacionPostgreSQL y agrupa su estado y operaciones.
class RepositorioAutenticacionPostgreSQL(ConexionPostgreSQL):
    # Define la funcion _motor con los parametros declarados; su bloque realiza esta operacion.
    def _motor(self):
        # Ejecuta el bloque siguiente solo cuando se cumple: self._engine is None.
        if self._engine is None:
            # Guarda en self._engine el valor necesario para reutilizarlo en otros metodos.
            self._engine = create_async_engine(self._cadena, isolation_level='SERIALIZABLE',
                                              # Asigna a hide_parameters el valor calculado a la derecha.
                                              hide_parameters=True)
        # Devuelve al llamador el resultado de la expresion indicada.
        return self._engine

    # Una consulta obtiene identidad y roles desde el mismo snapshot de PostgreSQL.
    # Asigna a _consulta el valor calculado a la derecha.
    _consulta = """
        SELECT u.id, u.username, u.password, u.email, u.nombre_completo,
               u.activo, u.version_sesion,
               COALESCE(array_agg(r.nombre ORDER BY r.nombre)
                        FILTER (WHERE r.id IS NOT NULL), ARRAY[]::varchar[]) AS roles
        FROM usuario u
        LEFT JOIN rol_usuario ru ON ru.usuario_id = u.id AND ru.activo IS TRUE
        LEFT JOIN rol r ON r.id = ru.rol_id AND r.activo IS TRUE
        WHERE {condicion}
        GROUP BY u.id
    """  # Termina el literal multilinea y completa la instruccion que lo contiene.

    # Define la operacion _obtener y su cuerpo.
    async def _obtener(self, consulta: str, parametros: dict) -> dict | None:
        # Abre y gestiona el recurso asincronico durante este bloque.
        async with self._conexion() as conexion:
            # Asigna a fila el resultado calculado en esta instruccion.
            fila = (await conexion.execute(text(consulta), parametros)).mappings().first()
            # Devuelve el resultado de esta expresion al llamador.
            return dict(fila) if fila else None

    # Define la operacion por_nombre y su cuerpo.
    async def por_nombre(self, nombre: str) -> dict | None:
        # Devuelve el resultado de esta expresion al llamador.
        return await self._obtener(self._consulta.format(condicion='u.username = :nombre'), {'nombre': nombre})

    # Define la operacion por_id y su cuerpo.
    async def por_id(self, usuario_id: int) -> dict | None:
        # Devuelve el resultado de esta expresion al llamador.
        return await self._obtener(self._consulta.format(condicion='u.id = :id'), {'id': usuario_id})

    # Define la operacion revocar y su cuerpo.
    async def revocar(self, usuario_id: int, version: int) -> bool:
        # Ejecuta la instruccion indicada dentro del flujo actual.
        try:
            # Abre y gestiona el recurso asincronico durante este bloque.
            async with self._conexion() as conexion:
                # Incremento condicional atómico: ni lectura-modificación en Python ni pérdida de incrementos.
                fila = await conexion.execute(text("""
                    UPDATE usuario SET version_sesion = version_sesion + 1,
                        fecha_actualizacion = CURRENT_TIMESTAMP
                    WHERE id = :id AND activo IS TRUE AND version_sesion = :version
                    RETURNING id
                """), {'id': usuario_id, 'version': version})  # Termina el literal multilinea y completa la instruccion que lo contiene.
                # Devuelve el resultado de esta expresion al llamador.
                return fila.first() is not None
        # Ejecuta la instruccion indicada dentro del flujo actual.
        except DBAPIError as error:
            # Aplica la condicion indicada al flujo que sigue.
            if getattr(error.orig, 'sqlstate', None) == '40001':
                return False  # Otro logout ya invalidó la versión presentada.
            # Ejecuta la instruccion indicada dentro del flujo actual.
            raise

    # Define la operacion crear_primero y su cuerpo.
    async def crear_primero(self, nombre: str, correo: str, resumen: str) -> None:
        # Ejecuta la instruccion indicada dentro del flujo actual.
        try:
            # Abre y gestiona el recurso asincronico durante este bloque.
            async with self._conexion() as conexion:
                # Serializa el bootstrap incluso frente a dos comandos simultáneos.
                await conexion.execute(text('LOCK TABLE usuario, rol, rol_usuario IN EXCLUSIVE MODE'))
                # Aplica la condicion indicada al flujo que sigue.
                if (await conexion.execute(text('SELECT EXISTS (SELECT 1 FROM usuario)'))).scalar_one():
                    # Lanza la excepcion indicada y detiene el flujo normal.
                    raise ConflictoInicializacion('Ya existen cuentas; la inicialización no modifica ninguna.')
                # Aplica la condicion indicada al flujo que sigue.
                if (await conexion.execute(text("SELECT EXISTS (SELECT 1 FROM rol WHERE nombre IN ('administrador', 'consulta'))"))).scalar_one():
                    # Lanza la excepcion indicada y detiene el flujo normal.
                    raise ConflictoInicializacion('Ya existen roles iniciales; no se sobrescriben ni reactivan.')
                # La cadena multilinea siguiente contiene el texto o SQL que usa esta instruccion.
                roles = await conexion.execute(text("""
                    INSERT INTO rol (nombre, descripcion, activo)
                    VALUES ('administrador', 'Administración de investigación y seguridad', TRUE),
                           ('consulta', 'Solo lectura de investigación', TRUE)
                    RETURNING id, nombre
                """))  # Termina el literal multilinea y completa la instruccion que lo contiene.
                # Asigna a administrador el resultado calculado en esta instruccion.
                administrador = next(f.id for f in roles if f.nombre == 'administrador')
                # La cadena multilinea siguiente contiene el texto o SQL que usa esta instruccion.
                usuario = (await conexion.execute(text("""
                    INSERT INTO usuario (username, email, password, activo, version_sesion)
                    VALUES (:nombre, :correo, :resumen, TRUE, 0) RETURNING id
                """), {'nombre': nombre, 'correo': correo, 'resumen': resumen})).scalar_one()  # Termina el literal multilinea y completa la instruccion que lo contiene.
                # Espera que termine la operacion asincronica antes de continuar.
                await conexion.execute(text('INSERT INTO rol_usuario (usuario_id, rol_id, activo) VALUES (:usuario, :rol, TRUE)'),
                                       # Ejecuta la instruccion indicada dentro del flujo actual.
                                       {'usuario': usuario, 'rol': administrador})
        # Ejecuta la instruccion indicada dentro del flujo actual.
        except IntegrityError:
            # Lanza la excepcion indicada y detiene el flujo normal.
            raise ConflictoInicializacion('Conflicto de datos; la transacción se revirtió sin sobrescribir.') from None
