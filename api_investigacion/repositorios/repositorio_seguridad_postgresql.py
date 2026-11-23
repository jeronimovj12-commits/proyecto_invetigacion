# Ejecuta la instruccion indicada dentro del flujo actual.
"""SQL manual: identificadores exclusivamente de listas internas; valores parametrizados."""
# Importa text desde sqlalchemy para usar esas definiciones.
from sqlalchemy import text
# Importa IntegrityError desde sqlalchemy.exc para usar esas definiciones.
from sqlalchemy.exc import IntegrityError
# Importa create_async_engine desde sqlalchemy.ext.asyncio para usar esas definiciones.
from sqlalchemy.ext.asyncio import create_async_engine
# Importa ConexionPostgreSQL desde repositorios.conexion_postgresql para usar esas definiciones.
from repositorios.conexion_postgresql import ConexionPostgreSQL
# Importa ConflictoSeguridad, SeguridadNoEncontrada desde seguridad.errores_administracion para usar esas definiciones.
from seguridad.errores_administracion import ConflictoSeguridad, SeguridadNoEncontrada

# Asigna a CAMPOS el valor calculado a la derecha.
CAMPOS = {
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    'usuario': ('id', 'username', 'email', 'nombre_completo', 'activo'),
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    'rol': ('id', 'nombre', 'descripcion', 'activo'),
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    'rol_usuario': ('usuario_id', 'rol_id', 'activo'),
# Cierra la estructura abierta en las lineas anteriores.
}
# Asigna a EDITABLES el valor calculado a la derecha.
EDITABLES = {
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    'usuario': ('username', 'email', 'nombre_completo', 'password'),
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    'rol': ('nombre', 'descripcion'),
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    'rol_usuario': ('usuario_id', 'rol_id'),
# Cierra la estructura abierta en las lineas anteriores.
}

# Define la clase RepositorioSeguridadPostgreSQL y agrupa su estado y operaciones.
class RepositorioSeguridadPostgreSQL(ConexionPostgreSQL):
    # Define la funcion _motor con los parametros declarados; su bloque realiza esta operacion.
    def _motor(self):
        # Ejecuta el bloque siguiente solo cuando se cumple: self._engine is None.
        if self._engine is None:
            # El lock precede a la lectura: después de esperar se ve el último commit.
            # Guarda en self._engine el valor necesario para reutilizarlo en otros metodos.
            self._engine = create_async_engine(self._cadena, isolation_level='READ COMMITTED', hide_parameters=True)
        # Devuelve al llamador el resultado de la expresion indicada.
        return self._engine

    # Aplica @staticmethod a la declaracion que sigue; en rutas, registra el endpoint HTTP.
    @staticmethod
    # Define la funcion _donde con los parametros declarados; su bloque realiza esta operacion.
    def _donde(recurso, claves):
        # Asigna a permitidas el valor calculado a la derecha.
        permitidas = ('usuario_id', 'rol_id') if recurso == 'rol_usuario' else ('id',)
        # Ejecuta el bloque siguiente solo cuando se cumple: set(claves) - set(permitidas).
        if set(claves) - set(permitidas):
            # Lanza la excepcion indicada y detiene el flujo normal.
            raise ValueError('Identificador inválido.')
        # Devuelve al llamador el resultado de la expresion indicada.
        return ' AND '.join(c + ' = :' + c for c in claves) or 'TRUE'

    # Define la funcion listar con los parametros declarados; su bloque realiza esta operacion.
    async def listar(self, recurso, claves, limite):
        # Asigna a campos el valor calculado a la derecha.
        campos = ', '.join(CAMPOS[recurso])
        # Asigna a donde el valor calculado a la derecha.
        donde = self._donde(recurso, claves)
        # Abre el recurso asincronico y asegura su cierre al salir del bloque.
        async with self._conexion() as conexion:
            # Asigna a resultado el valor calculado a la derecha.
            resultado = await conexion.execute(text(f'SELECT {campos} FROM {recurso} WHERE activo IS TRUE AND {donde} ORDER BY {CAMPOS[recurso][0]} LIMIT :limite'), {**claves, 'limite': limite})
            # Asigna a filas el valor calculado a la derecha.
            filas = [dict(f) for f in resultado.mappings()]
            # Ejecuta el bloque siguiente solo cuando se cumple: claves and not filas.
            if claves and not filas:
                # Lanza la excepcion indicada y detiene el flujo normal.
                raise SeguridadNoEncontrada()
            # Devuelve al llamador el resultado de la expresion indicada.
            return filas

    # Define la funcion _bloquear con los parametros declarados; su bloque realiza esta operacion.
    async def _bloquear(self, conexion):
        # Todas las mutaciones y bootstrap usan el mismo orden de tablas.
        # Espera que termine la operacion asincronica antes de continuar.
        await conexion.execute(text('LOCK TABLE usuario, rol, rol_usuario IN EXCLUSIVE MODE'))

    # Define la funcion _administradores con los parametros declarados; su bloque realiza esta operacion.
    async def _administradores(self, conexion):
        # Devuelve al llamador el resultado de la expresion indicada.
        return (await conexion.execute(text("""
            SELECT count(DISTINCT u.id) FROM usuario u
            JOIN rol_usuario ru ON ru.usuario_id=u.id AND ru.activo IS TRUE
            JOIN rol r ON r.id=ru.rol_id AND r.activo IS TRUE
            WHERE u.activo IS TRUE AND r.nombre='administrador'
        """))).scalar_one()  # Termina el literal multilinea y completa la instruccion que lo contiene.

    # Define la operacion _conservar_admin y su cuerpo.
    async def _conservar_admin(self, conexion, anteriores):
        # Aplica la condicion indicada al flujo que sigue.
        if anteriores and not await self._administradores(conexion):
            # Lanza la excepcion indicada y detiene el flujo normal.
            raise ConflictoSeguridad('La operación dejaría el sistema sin administrador activo.')

    # Define la operacion guardar y su cuerpo.
    async def guardar(self, recurso, claves, datos, crear):
        # Aplica la condicion indicada al flujo que sigue.
        if set(datos) - set(EDITABLES[recurso]):
            # Lanza la excepcion indicada y detiene el flujo normal.
            raise ValueError('Campos inválidos.')
        # Asigna a campos el resultado calculado en esta instruccion.
        campos = ', '.join(CAMPOS[recurso])
        # Ejecuta la instruccion indicada dentro del flujo actual.
        try:
            # Abre y gestiona el recurso asincronico durante este bloque.
            async with self._conexion() as conexion:
                # Espera que termine la operacion asincronica antes de continuar.
                await self._bloquear(conexion)
                # Asigna a anteriores el resultado calculado en esta instruccion.
                anteriores = await self._administradores(conexion)
                # Aplica la condicion indicada al flujo que sigue.
                if recurso == 'rol_usuario':
                    # Aplica la condicion indicada al flujo que sigue.
                    if not crear:
                        # Aplica la condicion indicada al flujo que sigue.
                        if not datos:
                            # Lanza la excepcion indicada y detiene el flujo normal.
                            raise ConflictoSeguridad('Envía al menos un campo.')
                        # Asigna a anterior el resultado calculado en esta instruccion.
                        anterior = (await conexion.execute(text('SELECT usuario_id, rol_id, activo FROM rol_usuario WHERE usuario_id=:usuario_id AND rol_id=:rol_id AND activo IS TRUE'), claves)).mappings().first()
                        # Aplica la condicion indicada al flujo que sigue.
                        if anterior is None:
                            # Lanza la excepcion indicada y detiene el flujo normal.
                            raise SeguridadNoEncontrada()
                        # Asigna a datos el resultado calculado en esta instruccion.
                        datos = {**claves, **datos}
                    # Itera sobre los elementos indicados.
                    for tabla, campo in (('usuario', 'usuario_id'), ('rol', 'rol_id')):
                        # Asigna a existe el resultado calculado en esta instruccion.
                        existe = (await conexion.execute(text(f'SELECT id FROM {tabla} WHERE id=:valor AND activo IS TRUE'), {'valor': datos[campo]})).first()
                        # Aplica la condicion indicada al flujo que sigue.
                        if not existe:
                            # Lanza la excepcion indicada y detiene el flujo normal.
                            raise ConflictoSeguridad('La cuenta y el rol deben estar activos.')
                # Aplica la condicion indicada al flujo que sigue.
                if not crear and recurso == 'rol':
                    # Asigna a nombre el resultado calculado en esta instruccion.
                    nombre = (await conexion.execute(text('SELECT nombre FROM rol WHERE id=:id AND activo IS TRUE'), claves)).scalar_one_or_none()
                    # Aplica la condicion indicada al flujo que sigue.
                    if nombre in ('administrador', 'consulta') and datos.get('nombre', nombre) != nombre:
                        # Lanza la excepcion indicada y detiene el flujo normal.
                        raise ConflictoSeguridad('Los nombres de los roles iniciales no se cambian.')
                # Aplica la condicion indicada al flujo que sigue.
                if recurso == 'rol_usuario' and not crear:
                    # Aplica la condicion indicada al flujo que sigue.
                    if datos == claves:
                        # Devuelve el resultado de esta expresion al llamador.
                        return dict(anterior)
                    # Cambiar un par conserva la fila anterior como retirada. Si el
                    # destino existe o falla la regla del admin, todo hace rollback.
                    await conexion.execute(text('UPDATE rol_usuario SET activo=FALSE WHERE usuario_id=:usuario_id AND rol_id=:rol_id'), claves)
                # Aplica la condicion indicada al flujo que sigue.
                if crear or recurso == 'rol_usuario':
                    # Asigna a columnas el resultado calculado en esta instruccion.
                    columnas = ', '.join(datos)
                    # Asigna a valores el resultado calculado en esta instruccion.
                    valores = ', '.join(':' + c for c in datos)
                    # Asigna a sql el resultado calculado en esta instruccion.
                    sql = f'INSERT INTO {recurso} ({columnas}) VALUES ({valores}) RETURNING {campos}'
                    # Asigna a parametros el resultado calculado en esta instruccion.
                    parametros = datos
                # Ejecuta la instruccion indicada dentro del flujo actual.
                else:
                    # Asigna a donde el resultado calculado en esta instruccion.
                    donde = self._donde(recurso, claves)
                    # Asigna a cambios el resultado calculado en esta instruccion.
                    cambios = ', '.join(c + '=:' + c for c in datos)
                    # Aplica la condicion indicada al flujo que sigue.
                    if not cambios:
                        # Lanza la excepcion indicada y detiene el flujo normal.
                        raise ConflictoSeguridad('Envía al menos un campo.')
                    # Aplica la condicion indicada al flujo que sigue.
                    if recurso == 'usuario':
                        # Ejecuta la instruccion indicada dentro del flujo actual.
                        cambios += ', fecha_actualizacion=CURRENT_TIMESTAMP'
                        # Aplica la condicion indicada al flujo que sigue.
                        if 'password' in datos:
                            # Ejecuta la instruccion indicada dentro del flujo actual.
                            cambios += ', version_sesion=version_sesion+1'
                    # Asigna a sql el resultado calculado en esta instruccion.
                    sql = f'UPDATE {recurso} SET {cambios} WHERE {donde} AND activo IS TRUE RETURNING {campos}'
                    # Asigna a parametros el resultado calculado en esta instruccion.
                    parametros = {**claves, **datos}
                # Asigna a fila el resultado calculado en esta instruccion.
                fila = (await conexion.execute(text(sql), parametros)).mappings().first()
                # Aplica la condicion indicada al flujo que sigue.
                if fila is None:
                    # Lanza la excepcion indicada y detiene el flujo normal.
                    raise SeguridadNoEncontrada()
                # Espera que termine la operacion asincronica antes de continuar.
                await self._conservar_admin(conexion, anteriores)
                # Devuelve el resultado de esta expresion al llamador.
                return dict(fila)
        # Ejecuta la instruccion indicada dentro del flujo actual.
        except IntegrityError:
            # Lanza la excepcion indicada y detiene el flujo normal.
            raise ConflictoSeguridad('Datos duplicados o referencias inválidas; no se reactivan asignaciones retiradas.') from None

    # Define la operacion retirar y su cuerpo.
    async def retirar(self, recurso, claves):
        # Asigna a donde el resultado calculado en esta instruccion.
        donde = self._donde(recurso, claves)
        # Abre y gestiona el recurso asincronico durante este bloque.
        async with self._conexion() as conexion:
            # Espera que termine la operacion asincronica antes de continuar.
            await self._bloquear(conexion)
            # Asigna a anteriores el resultado calculado en esta instruccion.
            anteriores = await self._administradores(conexion)
            # Asigna a extra el resultado calculado en esta instruccion.
            extra = ', version_sesion=version_sesion+1, fecha_actualizacion=CURRENT_TIMESTAMP' if recurso == 'usuario' else ''
            # Asigna a fila el resultado calculado en esta instruccion.
            fila = (await conexion.execute(text(f'UPDATE {recurso} SET activo=FALSE{extra} WHERE {donde} AND activo IS TRUE RETURNING {CAMPOS[recurso][0]}'), claves)).first()
            # Aplica la condicion indicada al flujo que sigue.
            if fila is None:
                # Lanza la excepcion indicada y detiene el flujo normal.
                raise SeguridadNoEncontrada()
            # Espera que termine la operacion asincronica antes de continuar.
            await self._conservar_admin(conexion, anteriores)
