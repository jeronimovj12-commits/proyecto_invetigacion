# Modelo de datos existente — v3

Fuente: db/init.sql y ProyectosDeAula/db_scripts/postgresql/investigacion.pg.sql.
Contrastado el 5 de noviembre de 2026 con information_schema.columns y
pg_constraint de investigacion_local, esquema public. Los apartados originales
describen la base compartida, cuyo esquema no se cambió; la migración aislada
de esta primera entrega se describe al final.
Tablas vacías: rol=0, usuario=0, rol_usuario=0; sin semillas en init.sql.

## rol

Una fila define un rol de autorización; no es el campo rol de las participaciones
de docentes de v2. PK: id. UNIQUE: nombre.

| Columna | Tipo real SQL | NULL | Default / función |
|---|---|---|---|
| id | integer (SERIAL) | No | Secuencia rol_id_seq; PK |
| nombre | varchar(100) | No | Nombre único |
| descripcion | text | Sí | Descripción |
| activo | boolean | Sí | true; permite NULL en SQL |
| fecha_creacion | timestamp without time zone | Sí | CURRENT_TIMESTAMP |

## usuario

Una fila representa una cuenta del sistema, no un docente. No hay FK a docente.
PK: id. UNIQUE independientes para username y email.

| Columna | Tipo real SQL | NULL | Default / función |
|---|---|---|---|
| id | integer (SERIAL) | No | Secuencia usuario_id_seq; PK |
| username | varchar(100) | No | Nombre de cuenta único |
| password | varchar(255) | No | Debe contener hash; SQL no impone formato criptográfico |
| email | varchar(150) | No | Correo único; SQL no valida formato |
| nombre_completo | varchar(200) | Sí | Nombre visible |
| activo | boolean | Sí | true; permite NULL en SQL |
| fecha_creacion | timestamp without time zone | Sí | CURRENT_TIMESTAMP |
| fecha_actualizacion | timestamp without time zone | Sí | CURRENT_TIMESTAMP solo al insertar; sin trigger de actualización |

No hay unicidad insensible a mayúsculas explícita ni política de normalización;
debe acordarse antes de implementar. No retornar password ni siquiera su hash.
Las fechas son sin zona horaria: acordar convención de interpretación; no
confundirlas con exp del JWT.

## rol_usuario

Una fila asigna un rol a una cuenta; relación muchos a muchos.
PK compuesta en orden: (usuario_id, rol_id).

| Columna | Tipo real SQL | NULL | Función |
|---|---|---|---|
| usuario_id | integer | No | FK usuario(id), ON DELETE CASCADE |
| rol_id | integer | No | FK rol(id), ON DELETE CASCADE |

Sin columna activo, fechas o identificador adicional. Las FK comprueban existencia,
no actividad; CASCADE solo opera ante borrado físico. La política constitucional
de borrado lógico no se implementa automáticamente con estas restricciones.
No se propone usar borrado físico silenciosamente: resolver antes del DELETE
individual. Ninguna migración forma parte de este trabajo.

## Diferencias entre esquema y reglas por implementar

- Proponer considerar activo exclusivamente cuando sea IS TRUE; NULL no concede
  acceso. API impediría modificar activo libremente o reactivar según política.
- Hash, credenciales correctas, expiración JWT, permisos y protección del último
  admin son reglas de aplicación; ninguna existe hoy por tener estas tablas.
- No hay tabla de permisos por recurso: una matriz acordada podría residir en
  política de aplicación, sin inventar nuevas tablas en este borrador.
- No hay campos para recuperación, revocación, renovación ni sesiones. Su alcance
  debe decidirse; no se presupone que JWT necesite almacenarse en usuario.
- Para usuario y rol puede marcarse activo=false sin borrar la fila; para quitar
  una asignación aislada falta resolver el conflicto descrito en 4_research.md.

Ejemplo conceptual (no datos insertados): usuario U con roles R1 y R2 ocupa
dos filas (U,R1) y (U,R2). Desactivar U bloquea ambas efectivamente, pero no
equivale a retirar R1 conservando R2. Esto explica por qué falta decidir el
retiro individual de rol_usuario.

## Ampliación autorizada y probada únicamente en bases aisladas

| Tabla / columna nueva | Tipo | NULL | Default | Uso |
|---|---|---|---|---|
| usuario.version_sesion | integer | No | 0 | CHECK >= 0; logout incrementa atómicamente y JWT exige coincidencia |
| rol_usuario.activo | boolean | No | TRUE | Filtrar asignaciones retiradas sin borrar la fila |

Archivo: db/migraciones/v3_001_sesiones_asignaciones.sql. No modifica init.sql,
claves compuestas ni FK; no reinicia secuencias y no reescribe hashes. La
repetición conserva versiones y estados inactivos. La restitución de una
asignación retirada queda fuera de la primera entrega: no hay endpoint que
reactive filas. Tampoco se implementó todavía el endpoint para retirarlas.

No se guarda JWT en PostgreSQL: solo la versión que permite invalidarlo.
Roles y asignaciones se leen desde la base; no se confía en permisos del token.
Véanse contratos implementados en 6_contracts.md y evidencia en VERIFICACION_V3.md.

## Actualización de implementación — 9 de noviembre de 2026

Los apartados anteriores conservan el diagnóstico del esquema original y la primera
entrega. El esquema v3 continúa añadiendo solo version_sesion y activo de asignación.
Ahora se implementan los endpoints administrativos y el retiro lógico. No hay
migraciones nuevas ni tablas del módulo adicionales para las pantallas.

Las lecturas administrativas omiten password y version_sesion. Las bajas de usuario
revocan sus sesiones; cambiar contraseña también. Nombres de roles iniciales
inmutables y transacción con bloqueo de las tres tablas impiden perder el último
administrador efectivo. Una asignación inactiva conserva su PK y no se restituye.

El front usa una tabla SQLite local de sesiones con id SHA-256 de identificador
aleatorio, token y vence. No pertenece al modelo PostgreSQL ni guarda investigación;
la cookie solo lleva identificador opaco firmado, CSRF y mensajes. La expiración
no se extiende al usar la aplicación. Se elimina la fila al cerrar sesión o al
limpiar una sesión inválida y se purgan vencidas al crear nuevas sesiones.
