# Especificación — primera entrega backend v3

Estado: implementación parcial en v3-desarrollo, 5 de noviembre de 2026.
V2 continúa abierta: pruebas manuales restantes, integración de aportes de
compañeros y firmas pendientes. No hay merge, tags ni cierre de versión.

## Requisitos originales confirmados

- [Módulo Investigación §3](../../../../ProyectosDeAula/docs/modulo_investigacion.md):
  POST /api/login con JWT, autenticación/autorización, menú por roles, CRUD de
  usuario/rol/rol_usuario solo para administradores y logout; consulta no escribe.
- [Metodología §2, §5 y §6](../../../../ProyectosDeAula/docs/0_METODOLOGIA.md):
  sesiones, Bearer desde el front, contraseñas hasheadas, secretos externos y
  regresión de versiones previas.
- [Constitución](../../1_constitution.md): interfaces entre capas, SQL
  parametrizado sin ORM, front separado por HTTP y borrado lógico.

Las fuentes no fijan los dos roles iniciales, 30 minutos, Argon2, HS256 ni
version_sesion. Son decisiones del usuario para esta implementación.

## Políticas autorizadas para esta entrega

| Tema | Política de implementación |
|---|---|
| Roles | administrador lee/escribe investigación y seguridad; consulta solo lee investigación |
| Identidad | Usuario activo, version_sesion coincidente y roles/asignaciones activos leídos desde PostgreSQL por solicitud |
| Permisos | Sin roles iniciales efectivos: 403; credencial/token inválido, inactividad o versión revocada: 401 |
| Alta | Primer administrador mediante comando local; futuro CRUD solo por admin; no registro público |
| Contraseña | Argon2id mediante pwdlib; entrada oculta y sin valores predeterminados |
| Sesión | 30 minutos configurables; HS256; sin refresh token ni renovación automática |
| Logout | Incremento atómico y persistente de version_sesion: invalida todas las sesiones anteriores del usuario |
| Asignaciones | Columna activo para borrado lógico; no restitución de retiradas en esta entrega |
| Recuperación | Correo automático fuera de esta entrega |

## Alcance realmente implementado

Migración explícita con precondiciones; interfaces, servicio, repositorio y
adaptadores de seguridad; POST /api/login, GET /api/sesion y POST /api/logout;
comando local transaccional del primer administrador; pruebas HTTP con base
nueva y reinicio de la API de prueba. Contratos exactos en 6_contracts.md.

El arranque v3 es `main_v3:app`, con compose independiente, PostgreSQL propio y
puerto local 8026. `main:app` y el compose de v2 permanecen sin modificar.
La base compartida investigacion_local no recibió las migraciones.

## Límites y pendientes explícitos

**Las rutas existentes de investigación todavía NO están protegidas**, incluso
si se consultan a través del arranque parcial v3. La función de política de
permisos no equivale a middleware global. No hay pantallas Flask de seguridad,
CRUD administrativo, registro público ni recuperación por correo. No hay todavía
endpoint para retirar asignaciones: se preparó el esquema y su filtro efectivo.
No usar este backend parcial como sistema completamente protegido.

Quedan pendientes protección de cada recurso/verbo, control del último admin,
limitación de intentos de login, tratamiento de claves/secretos comprometidos,
front, aceptación del equipo y revisión manual. No se asume conformidad total
con la rúbrica por aprobar pruebas automáticas parciales.

## Secuencia y cambios respecto de la constitución

Art. 1, mapa y metodología exigen cerrar la versión anterior antes de la siguiente.
Se registra la instrucción explícita del usuario de adelantar primero documentación
y ahora esta primera implementación sin cerrar v2. No se atribuye aprobación
al profesor ni se altera el estado de v2.

Conforme al art. 11, en 4_research.md quedan descritos el motivo y consecuencias
de añadir columnas (art. 5), bibliotecas de seguridad (art. 2) y 401/403 (art. 10).
El usuario autorizó esas políticas para esta entrega; no se modificó el texto de
la constitución ni se inventaron firmas o ratificación formal del equipo.
