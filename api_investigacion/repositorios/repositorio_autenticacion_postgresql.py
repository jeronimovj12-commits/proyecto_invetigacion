from sqlalchemy import text
from sqlalchemy.exc import IntegrityError, DBAPIError
from sqlalchemy.ext.asyncio import create_async_engine

from repositorios.conexion_postgresql import ConexionPostgreSQL
from seguridad.errores import ConflictoInicializacion


class RepositorioAutenticacionPostgreSQL(ConexionPostgreSQL):
    def _motor(self):
        if self._engine is None:
            self._engine = create_async_engine(self._cadena, isolation_level='SERIALIZABLE',
                                              hide_parameters=True)
        return self._engine

    # Una consulta obtiene identidad y roles desde el mismo snapshot de PostgreSQL.
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
    """

    async def _obtener(self, consulta: str, parametros: dict) -> dict | None:
        async with self._conexion() as conexion:
            fila = (await conexion.execute(text(consulta), parametros)).mappings().first()
            return dict(fila) if fila else None

    async def por_nombre(self, nombre: str) -> dict | None:
        return await self._obtener(self._consulta.format(condicion='u.username = :nombre'), {'nombre': nombre})

    async def por_id(self, usuario_id: int) -> dict | None:
        return await self._obtener(self._consulta.format(condicion='u.id = :id'), {'id': usuario_id})

    async def revocar(self, usuario_id: int, version: int) -> bool:
        try:
            async with self._conexion() as conexion:
                # Incremento condicional atómico: ni lectura-modificación en Python ni pérdida de incrementos.
                fila = await conexion.execute(text("""
                    UPDATE usuario SET version_sesion = version_sesion + 1,
                        fecha_actualizacion = CURRENT_TIMESTAMP
                    WHERE id = :id AND activo IS TRUE AND version_sesion = :version
                    RETURNING id
                """), {'id': usuario_id, 'version': version})
                return fila.first() is not None
        except DBAPIError as error:
            if getattr(error.orig, 'sqlstate', None) == '40001':
                return False  # Otro logout ya invalidó la versión presentada.
            raise

    async def crear_primero(self, nombre: str, correo: str, resumen: str) -> None:
        try:
            async with self._conexion() as conexion:
                # Serializa el bootstrap incluso frente a dos comandos simultáneos.
                await conexion.execute(text('LOCK TABLE usuario, rol, rol_usuario IN EXCLUSIVE MODE'))
                if (await conexion.execute(text('SELECT EXISTS (SELECT 1 FROM usuario)'))).scalar_one():
                    raise ConflictoInicializacion('Ya existen cuentas; la inicialización no modifica ninguna.')
                if (await conexion.execute(text("SELECT EXISTS (SELECT 1 FROM rol WHERE nombre IN ('administrador', 'consulta'))"))).scalar_one():
                    raise ConflictoInicializacion('Ya existen roles iniciales; no se sobrescriben ni reactivan.')
                roles = await conexion.execute(text("""
                    INSERT INTO rol (nombre, descripcion, activo)
                    VALUES ('administrador', 'Administración de investigación y seguridad', TRUE),
                           ('consulta', 'Solo lectura de investigación', TRUE)
                    RETURNING id, nombre
                """))
                administrador = next(f.id for f in roles if f.nombre == 'administrador')
                usuario = (await conexion.execute(text("""
                    INSERT INTO usuario (username, email, password, activo, version_sesion)
                    VALUES (:nombre, :correo, :resumen, TRUE, 0) RETURNING id
                """), {'nombre': nombre, 'correo': correo, 'resumen': resumen})).scalar_one()
                await conexion.execute(text('INSERT INTO rol_usuario (usuario_id, rol_id, activo) VALUES (:usuario, :rol, TRUE)'),
                                       {'usuario': usuario, 'rol': administrador})
        except IntegrityError:
            raise ConflictoInicializacion('Conflicto de datos; la transacción se revirtió sin sobrescribir.') from None
