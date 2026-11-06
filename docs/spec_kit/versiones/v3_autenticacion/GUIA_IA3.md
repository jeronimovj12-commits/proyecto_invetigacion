# Guía de IA — v3

## Alcance de este registro

Registra únicamente la solicitud de implementación disponible y el trabajo
comprobado en esta sesión. Los borradores iniciales ya existían al comenzar.
No se reconstruyen ni se inventan prompts anteriores o aprobación del profesor.

## Prompt real de implementación

```text
Avanza con la primera implementación del backend de v3 en v3-desarrollo. Mantén v2 abierta y conserva cualquier cambio existente.

Usa estas decisiones como políticas de esta implementación, diferenciándolas de los requisitos originales del profesor:
- Roles iniciales: administrador y consulta.
- Administrador: lectura y escritura de investigación y administración de seguridad.
- Consulta: únicamente lectura de investigación.
- Usuarios creados por administrador; sin registro público.
- Sesión de 30 minutos, configurable, sin refresh token.
- Logout invalida todas las sesiones del usuario mediante version_sesion.
- Asignaciones rol_usuario con borrado lógico.
- Recuperación automática por correo y restitución de asignaciones retiradas fuera de esta primera entrega.

Implementa esta primera parte:

1. Prepara migraciones SQL para version_sesion y activo en rol_usuario, revisando antes el esquema real. Conserva los registros existentes y detecta esquemas incompatibles. Prueba las migraciones en una base aislada; todavía no las apliques a mi base local compartida con v2.

2. Implementa la autenticación respetando controlador, servicio, repositorio e interfaces. Usa SQL parametrizado y las bibliotecas de seguridad apropiadas según documentación oficial actual. Contraseñas con Argon2; nunca implementes criptografía propia.

3. Implementa los contratos de login, consulta del usuario autenticado y logout. Valida firma, algoritmo permitido, vencimiento y los claims definidos en el contrato. Comprueba usuario activo, version_sesion y roles/asignaciones activos desde la base.

4. Logout debe incrementar version_sesion de forma atómica. Un token anterior debe dejar de funcionar incluso después de reiniciar la API.

5. Prepara un comando local para crear el primer administrador en una transacción. Contraseña mediante entrada oculta, sin credenciales predeterminadas. Ante cuentas existentes o conflictos, detente sin sobrescribir ni reactivar.

6. Secretos mediante configuración externa, sin valores reales en Git, logs ni respuestas. Documenta cómo generarlos y configurarlos. No muestres contraseñas, hashes ni JWT completos en el informe.

7. Prueba login correcto e incorrecto, usuario inactivo, token vencido o alterado, usuario sin roles y reutilización de token después del logout. Comprueba también que se excluyen roles y asignaciones inactivos. Distingue correctamente autenticación fallida de permisos insuficientes.

Esta entrega no incluye todavía las pantallas Flask, el CRUD administrativo ni aplicar protección a todas las rutas existentes. Déjalos explícitamente pendientes; no declares completa ni protegida toda la v3.

Actualiza especificación, contratos, tareas y GUIA_IA3.md con las decisiones y el trabajo real. Registra únicamente verificaciones ejecutadas.

Crea commits separados por cambios reales:
- "Prepara migraciones para sesiones y borrado lógico de asignaciones"
- "Implementa login JWT, consulta de sesión y logout"
- "Prueba credenciales, vencimiento y revocación de sesiones"

Al terminar, indica resultados, limitaciones y comandos exactos para probarlo localmente. No hagas push, merge ni tags.
```

## Fuentes, decisiones y resultado

Se revisó git status: v3-desarrollo estaba limpia. Se consultaron constitución,
borradores v3, capas existentes, SQL y metadatos de la base compartida, sin leer
contraseñas. Se consultaron la documentación oficial de FastAPI sobre JWT y
hash de contraseñas y la API de PyJWT (enlaces en 4_research.md). Se usaron
PyJWT 2.15.1 y pwdlib[argon2] 0.3.0; el hash se delega a Argon2id.

La migración añade únicamente las columnas autorizadas y una restricción de
versión no negativa, dentro de una transacción con validación previa. Se mantuvo
init.sql y no se aplicó la migración en investigacion_local. Las bases y volumen
v3 son independientes de los contenedores y volumen de v2.

El ensamblador nuevo construye interfaces y adaptadores; controladores no tocan
SQL y servicios no conocen HTTP. Solo el repositorio habla con PostgreSQL.
Se implementaron login/sesion/logout y un bootstrap local, sin CRUD público de
registro. Los claims y códigos reales están en 6_contracts.md. La función de
permisos expresa la política autorizada, pero aún no se aplica a todas las rutas.

La configuración real se generó con el generador aleatorio del sistema y quedó
solo en v3-local.env ignorado por Git; .env.example contiene marcadores. No se
copian secretos a este registro. El compose v2 y su arranque no se modificaron.

## Verificaciones realmente realizadas

- Migración en base aislada con filas previas: repetición, versiones e inactivos
  conservados y rechazo intencional de columna incompatible.
- Suite de 14 pruebas HTTP/política con base nueva, credenciales generadas en
  memoria, claims maliciosos, roles/asignaciones, logout concurrente y reinicio
  real del proceso API. Pasó. El bootstrap del servicio creó la primera cuenta
  y rechazó otra inicialización; el comando sin terminal fue rechazado.
- Regresión en memoria de capas v1 y las 12 pruebas de v2: pasaron.
- Consulta posterior de solo lectura: la base compartida sigue sin columnas v3
  y sin cuentas, roles ni asignaciones.

Detalle y comandos en VERIFICACION_V3.md y 7_quickstart.md. El prompt interactivo
oculto no fue recorrido manualmente. No se probaron pantallas inexistentes ni
se atribuyen a esta sesión las pruebas manuales históricas de v2.

## Pendientes y responsabilidades

El equipo debe revisar e integrar aportes, ratificar cambios documentales,
completar pruebas manuales y firmar. La IA no constituye aceptación del profesor.
Faltan middleware/protección de rutas existentes, CRUD administrativo, front,
prueba manual del bootstrap y aceptación integral de seguridad. La v2 sigue
abierta y la v3 no se considera completa ni totalmente protegida.
