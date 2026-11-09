"""SQL manual: identificadores exclusivamente de listas internas; valores parametrizados."""
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine
from repositorios.conexion_postgresql import ConexionPostgreSQL
from seguridad.errores_administracion import ConflictoSeguridad, SeguridadNoEncontrada

CAMPOS = {
    'usuario': ('id', 'username', 'email', 'nombre_completo', 'activo'),
    'rol': ('id', 'nombre', 'descripcion', 'activo'),
    'rol_usuario': ('usuario_id', 'rol_id', 'activo'),
}
EDITABLES = {
    'usuario': ('username', 'email', 'nombre_completo', 'password'),
    'rol': ('nombre', 'descripcion'),
    'rol_usuario': ('usuario_id', 'rol_id'),
}

class RepositorioSeguridadPostgreSQL(ConexionPostgreSQL):
    def _motor(self):
        if self._engine is None:
            # El lock precede a la lectura: después de esperar se ve el último commit.
            self._engine = create_async_engine(self._cadena, isolation_level='READ COMMITTED', hide_parameters=True)
        return self._engine

    @staticmethod
    def _donde(recurso, claves):
        permitidas = ('usuario_id', 'rol_id') if recurso == 'rol_usuario' else ('id',)
        if set(claves) - set(permitidas):
            raise ValueError('Identificador inválido.')
        return ' AND '.join(c + ' = :' + c for c in claves) or 'TRUE'

    async def listar(self, recurso, claves, limite):
        campos = ', '.join(CAMPOS[recurso])
        donde = self._donde(recurso, claves)
        async with self._conexion() as conexion:
            resultado = await conexion.execute(text(f'SELECT {campos} FROM {recurso} WHERE activo IS TRUE AND {donde} ORDER BY {CAMPOS[recurso][0]} LIMIT :limite'), {**claves, 'limite': limite})
            filas = [dict(f) for f in resultado.mappings()]
            if claves and not filas:
                raise SeguridadNoEncontrada()
            return filas

    async def _bloquear(self, conexion):
        # Todas las mutaciones y bootstrap usan el mismo orden de tablas.
        await conexion.execute(text('LOCK TABLE usuario, rol, rol_usuario IN EXCLUSIVE MODE'))

    async def _administradores(self, conexion):
        return (await conexion.execute(text("""
            SELECT count(DISTINCT u.id) FROM usuario u
            JOIN rol_usuario ru ON ru.usuario_id=u.id AND ru.activo IS TRUE
            JOIN rol r ON r.id=ru.rol_id AND r.activo IS TRUE
            WHERE u.activo IS TRUE AND r.nombre='administrador'
        """))).scalar_one()

    async def _conservar_admin(self, conexion, anteriores):
        if anteriores and not await self._administradores(conexion):
            raise ConflictoSeguridad('La operación dejaría el sistema sin administrador activo.')

    async def guardar(self, recurso, claves, datos, crear):
        if set(datos) - set(EDITABLES[recurso]):
            raise ValueError('Campos inválidos.')
        campos = ', '.join(CAMPOS[recurso])
        try:
            async with self._conexion() as conexion:
                await self._bloquear(conexion)
                anteriores = await self._administradores(conexion)
                if recurso == 'rol_usuario':
                    if not crear:
                        if not datos:
                            raise ConflictoSeguridad('Envía al menos un campo.')
                        anterior = (await conexion.execute(text('SELECT usuario_id, rol_id, activo FROM rol_usuario WHERE usuario_id=:usuario_id AND rol_id=:rol_id AND activo IS TRUE'), claves)).mappings().first()
                        if anterior is None:
                            raise SeguridadNoEncontrada()
                        datos = {**claves, **datos}
                    for tabla, campo in (('usuario', 'usuario_id'), ('rol', 'rol_id')):
                        existe = (await conexion.execute(text(f'SELECT id FROM {tabla} WHERE id=:valor AND activo IS TRUE'), {'valor': datos[campo]})).first()
                        if not existe:
                            raise ConflictoSeguridad('La cuenta y el rol deben estar activos.')
                if not crear and recurso == 'rol':
                    nombre = (await conexion.execute(text('SELECT nombre FROM rol WHERE id=:id AND activo IS TRUE'), claves)).scalar_one_or_none()
                    if nombre in ('administrador', 'consulta') and datos.get('nombre', nombre) != nombre:
                        raise ConflictoSeguridad('Los nombres de los roles iniciales no se cambian.')
                if recurso == 'rol_usuario' and not crear:
                    if datos == claves:
                        return dict(anterior)
                    # Cambiar un par conserva la fila anterior como retirada. Si el
                    # destino existe o falla la regla del admin, todo hace rollback.
                    await conexion.execute(text('UPDATE rol_usuario SET activo=FALSE WHERE usuario_id=:usuario_id AND rol_id=:rol_id'), claves)
                if crear or recurso == 'rol_usuario':
                    columnas = ', '.join(datos)
                    valores = ', '.join(':' + c for c in datos)
                    sql = f'INSERT INTO {recurso} ({columnas}) VALUES ({valores}) RETURNING {campos}'
                    parametros = datos
                else:
                    donde = self._donde(recurso, claves)
                    cambios = ', '.join(c + '=:' + c for c in datos)
                    if not cambios:
                        raise ConflictoSeguridad('Envía al menos un campo.')
                    if recurso == 'usuario':
                        cambios += ', fecha_actualizacion=CURRENT_TIMESTAMP'
                        if 'password' in datos:
                            cambios += ', version_sesion=version_sesion+1'
                    sql = f'UPDATE {recurso} SET {cambios} WHERE {donde} AND activo IS TRUE RETURNING {campos}'
                    parametros = {**claves, **datos}
                fila = (await conexion.execute(text(sql), parametros)).mappings().first()
                if fila is None:
                    raise SeguridadNoEncontrada()
                await self._conservar_admin(conexion, anteriores)
                return dict(fila)
        except IntegrityError:
            raise ConflictoSeguridad('Datos duplicados o referencias inválidas; no se reactivan asignaciones retiradas.') from None

    async def retirar(self, recurso, claves):
        donde = self._donde(recurso, claves)
        async with self._conexion() as conexion:
            await self._bloquear(conexion)
            anteriores = await self._administradores(conexion)
            extra = ', version_sesion=version_sesion+1, fecha_actualizacion=CURRENT_TIMESTAMP' if recurso == 'usuario' else ''
            fila = (await conexion.execute(text(f'UPDATE {recurso} SET activo=FALSE{extra} WHERE {donde} AND activo IS TRUE RETURNING {CAMPOS[recurso][0]}'), claves)).first()
            if fila is None:
                raise SeguridadNoEncontrada()
            await self._conservar_admin(conexion, anteriores)
