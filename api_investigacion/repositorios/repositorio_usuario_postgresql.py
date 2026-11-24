"""Las lecturas omiten password; solo consultas internas de autenticación acceden al hash."""

from sqlalchemy import text

from repositorios.abstracciones.i_repositorio_usuario import IRepositorioUsuario
from repositorios.repositorio_postgresql_base import RepositorioPostgreSQLBase


class RepositorioUsuarioPostgreSQL(RepositorioPostgreSQLBase, IRepositorioUsuario):
    TABLA = "usuario"
    CLAVE = "id"
    COLUMNAS = (
        "id", "username", "email", "nombre_completo",
        "fecha_creacion", "fecha_actualizacion",
    )
    COLUMNAS_CREACION = ("username", "password", "email", "nombre_completo")

    async def obtener_por_username(self, username: str) -> dict | None:
        consulta = text(
            "SELECT id, username, password, email, nombre_completo, activo "
            "FROM usuario WHERE username = :username"
        )
        async with self._engine.connect() as conexion:
            resultado = await conexion.execute(consulta, {"username": username})
            fila = resultado.first()
            return dict(fila._mapping) if fila else None

    async def obtener_roles_activos(self, usuario_id: int) -> list[str]:
        consulta = text(
            "SELECT r.nombre FROM rol_usuario ru "
            "JOIN usuario u ON u.id = ru.usuario_id "
            "JOIN rol r ON r.id = ru.rol_id "
            "WHERE ru.usuario_id = :usuario_id AND u.activo = TRUE AND r.activo = TRUE "
            "ORDER BY r.nombre"
        )
        async with self._engine.connect() as conexion:
            resultado = await conexion.execute(consulta, {"usuario_id": usuario_id})
            return [fila.nombre for fila in resultado]

    async def actualizar(self, identificador: str | int, datos: dict) -> int:
        campos_permitidos = ("username", "password", "email", "nombre_completo")
        cambios = tuple(campo for campo in campos_permitidos if campo in datos)
        asignaciones = ", ".join(f"{campo} = :{campo}" for campo in cambios)
        consulta = text(
            f"UPDATE usuario SET {asignaciones}, fecha_actualizacion = CURRENT_TIMESTAMP "
            "WHERE id = :identificador AND activo = TRUE"
        )
        parametros = {campo: datos[campo] for campo in cambios}
        parametros["identificador"] = identificador
        async with self._engine.begin() as conexion:
            resultado = await conexion.execute(consulta, parametros)
            return resultado.rowcount

    async def sembrar_datos_iniciales(self, roles: list[dict], usuarios: list[dict]) -> None:
        consulta_rol = text(
            "INSERT INTO rol (nombre, descripcion, activo) "
            "VALUES (:nombre, :descripcion, TRUE) ON CONFLICT (nombre) DO NOTHING"
        )
        consulta_usuario = text(
            "INSERT INTO usuario (username, password, email, nombre_completo, activo) "
            "VALUES (:username, :password, :email, :nombre_completo, TRUE) "
            "ON CONFLICT DO NOTHING"
        )
        consulta_asignacion = text(
            "INSERT INTO rol_usuario (usuario_id, rol_id) "
            "SELECT u.id, r.id FROM usuario u CROSS JOIN rol r "
            "WHERE u.username = :username AND r.nombre = :rol "
            "ON CONFLICT (usuario_id, rol_id) DO NOTHING"
        )
        async with self._engine.begin() as conexion:
            for rol in roles:
                await conexion.execute(consulta_rol, rol)
            for usuario in usuarios:
                await conexion.execute(consulta_usuario, {
                    campo: usuario[campo]
                    for campo in ("username", "password", "email", "nombre_completo")
                })
                await conexion.execute(
                    consulta_asignacion,
                    {"username": usuario["username"], "rol": usuario["rol"]},
                )
                consulta_usuario_existente = text(
                    "SELECT id FROM usuario WHERE username = :username"
                )
                existente = await conexion.execute(
                    consulta_usuario_existente, {"username": usuario["username"]}
                )
                if existente.first() is None:
                    raise RuntimeError(
                        f"No se pudo garantizar la cuenta inicial {usuario['username']}."
                    )
