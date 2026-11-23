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

## Continuación autorizada — 9 de noviembre de 2026

Los apartados anteriores son evidencia histórica del 5 de noviembre. Sus pendientes
y la prohibición de push quedaron sustituidos por el siguiente pedido real:

```text
Necesito completar la implementación de v3. Revisa primero git status, los commits actuales, la constitución y todos los documentos de v3_autenticacion. Conserva los cambios existentes. Trabaja en v3-desarrollo; v2 sigue abierta.

Audita lo implementado y completa únicamente lo que falta según los requisitos y las políticas ya documentadas:

- Login JWT, contraseñas con hash, vencimiento y logout con invalidación de sesiones.
- Creación segura del primer administrador.
- CRUD administrativo de usuarios, roles y asignaciones, con borrado lógico.
- Protección de todas las rutas de investigación y seguridad: administrador con los permisos acordados, consulta solo lectura y usuario sin roles sin acceso.
- Validación de permisos en la API, incluyendo solicitudes directas.
- Front Flask con login, logout, sesión, menú y acciones según permisos. Manejo de 401, 403 y vencimiento.
- Sesión del navegador y formularios protegidos adecuadamente, sin exponer JWT ni secretos.
- Arranque reproducible con Docker, migraciones y guía para instalaciones nuevas y existentes.

Respeta las capas e interfaces existentes y el SQL parametrizado. Revisa que la administración no permita perder accidentalmente el último administrador activo. No incorpores recuperación por correo, registro público ni funciones de v4.

Primero presenta una lista breve de lo que falta y continúa implementándolo. Ejecuta las verificaciones pertinentes y corrige los fallos. No declares pruebas manuales realizadas por mí.

Actualiza contratos, quickstart, tareas, checklist y GUIA_IA3.md con evidencia real. No edites los archivos reservados a mis compañeros:
- prueba_permisos_v3_equipo.py
- VERIFICACION_API_V3_EQUIPO.md
- VERIFICACION_FRONT_V3_EQUIPO.md

Crea commits por cambios funcionales reales, con títulos breves que expliquen el resultado. Evita commits vacíos y no incluyas secretos. Publica el avance en origin/v3-desarrollo sin force push.

Termina indicando los commits, pruebas ejecutadas, pendientes y comandos exactos para que mis compañeros arranquen y verifiquen la misma versión. No hagas merge a main ni crees el tag v3.
```

### Trabajo y decisiones reales

Git comenzó limpio en v3-desarrollo, tres commits por delante de origin:
ee05b39, 9c34ba9 y 7ed5594. Se conservaron. Se leyó la constitución y el spec kit,
y se informó la lista de faltantes antes de implementar: protección global, CRUD,
último administrador, Flask y arranque/evidencia. V2 permanece abierta.

Se añadió administración por interfaces y SQL parametrizado; bajas lógicas y
transacción con locks para conservar el último administrador. Los roles iniciales
no se renombran. Asignaciones conservan clave compuesta y retiro sin restitución.
Se mantuvo el bootstrap y autenticación anteriores, ampliando sus verificaciones.
La API protege peticiones directas y publica el esquema Bearer en OpenAPI.

Flask mantiene HTTP como única conexión con los datos del módulo. Guarda JWT en
SQLite local del servidor; la cookie firmada solo contiene identificador opaco,
CSRF y avisos. CSRF en login/logout y todos los POST; menú y rutas según permisos;
401 limpia sesión, 403 deniega y caída/500 de sesión presenta 503 sin investigación.
Se consultó documentación oficial de Flask y SQLAlchemy (4_research.md).

Docker Desktop estaba detenido; se inició para verificar. Python por alias no
funcionaba, se utilizó el Python instalado para ediciones y Docker para las suites.
Se preservaron secretos existentes y se añadió únicamente la clave de sesión local
faltante sin imprimirla. Dependencias v3 fijadas con las versiones verificadas.
La migración es ahora un servicio obligatorio previo a la API; v2 sigue independiente.

Se ejecutaron pruebas de autenticación, administración, migración, Flask, integración
real y capas v1/v2. Se corrigieron fallos del lector de respuestas 204 y semillas de
regresión que omitían campos obligatorios o excedían la longitud del código de área.
Una auditoría adicional de solo lectura detectó dos fallos corregidos: manejo de
500/JSON inesperado de sesión y Bearer ausente en OpenAPI para operaciones protegidas.
Los resultados finales y límites se registran en VERIFICACION_V3.md.

No se tocaron los tres archivos reservados. No se atribuyen pruebas manuales al
usuario ni al equipo. Pendientes: revisión humana del prompt oculto/navegador,
aportes, firmas y aceptación; sin merge a main ni tag v3. El push autorizado publica
avance, no cierre de versión. Se conservan las propuestas de enmienda pendientes
de ratificación; no se inventa aprobación del profesor.

## Commits de continuación

- 5454168: protege la API y administra usuarios y roles, con pruebas HTTP.
- 1e92ff1: sesión segura y administración en Flask, con pruebas de presentación.
- La automatización Docker, dependencias fijadas, pruebas integradas y esta evidencia
  se agrupan en «Automatiza arranque y verificación de v3». Consultar `git log -6 --oneline`
  para su identificador final y los tres commits anteriores conservados.


### Edición de asignaciones en la revisión final

Antes de finalizar se detectó que el alcance CRUD exigía también editar una
asignación activa. Se completaron PUT/PATCH y el formulario Flask: baja lógica
del par anterior y alta del nuevo en la misma transacción, sin reactivar pares
retirados. Se añadió cobertura de par idéntico, null/cuerpo vacío, origen retirado,
destino activo o retirado, rollback y protección del último administrador; también
edición real desde Flask. La matriz pasó a 92 operaciones y la suite administrativa
a cinco casos. El commit adicional se titula «Permite editar asignaciones sin borrar vínculos».
