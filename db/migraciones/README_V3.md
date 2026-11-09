# Migración v3 001

Solo ejecución explícita con psql -X -v ON_ERROR_STOP=1. No está montada en el
compose de v2 ni se modifica init.sql. V2 permanece abierta.

Añade usuario.version_sesion (integer NOT NULL DEFAULT 0, CHECK >= 0) y
rol_usuario.activo (boolean NOT NULL DEFAULT TRUE). Conserva claves, filas,
contraseñas y estados anteriores. Las asignaciones existentes comienzan activas;
los usuarios/roles inactivos siguen excluidos por sus propios estados.

Transacción única y bloqueo exclusivo breve: requiere ventana de mantenimiento
si algún día se aprueba para una base compartida. Una repetición compatible no
reinicia versiones ni reactiva asignaciones. Se rechazan columnas base, claves,
tipos, nulabilidad y defaults nuevos incompatibles. No es una reparación de
cualquier variante arbitraria del esquema. No hay rollback destructivo automático.

En la instalación aislada descrita en el quickstart v3:

```sh
docker compose -p investigacion-v3 --env-file v3-local.env -f docker-compose.v3.yml exec -T postgres-v3 psql -X -v ON_ERROR_STOP=1 -U investigacion_v3 -d investigacion_v3 -f /migraciones/v3_001_sesiones_asignaciones.sql
```

La base investigacion_local compartida con v2 **no debe recibir esta migración
en esta entrega**. La ampliación del esquema es política autorizada por el
usuario para v3, no una modificación atribuida al SQL original del profesor.

Verificación ejecutada el 5 de noviembre de 2026 en
prueba_migraciones_v3_20261105 del servicio postgres-v3 aislado: inicialización
con init.sql, una cuenta y un rol ficticios inactivos con asignación existente,
primera migración y repetición. Un bloque DO confirmó que la cuenta y su valor
previo se conservaron, version_sesion=7 no volvió a cero y la asignación retirada
no se reactivó. Al quitar NOT NULL de la columna nueva en esa base de prueba,
la migración falló explícitamente con salida no cero. Se conserva esa base con
la incompatibilidad intencional; no es la base de ejecución de la API.

## Arranque actualizado — 9 de noviembre de 2026

El compose v3 incluye ahora migrar-v3 como dependencia obligatoria previa a API.
En instalaciones nuevas y existentes aplica el mismo SQL idempotente con
ON_ERROR_STOP; si falla, la API no arranca. El compose v2 sigue sin incluirlo.
Respaldar antes de actualizar una instalación existente, detener escrituras y
seguir [quickstart v3](../../docs/spec_kit/versiones/v3_autenticacion/7_quickstart.md).
No volver a aplicar init.sql ni borrar volúmenes para actualizar.

La suite prueba_migracion_v3.py volvió a verificar filas anteriores inactivas,
version_sesion=7, asignación retirada, repetición y rechazo al eliminar NOT NULL.
Solo bases aleatorias de postgres-v3; no se migró investigacion_local compartida.
