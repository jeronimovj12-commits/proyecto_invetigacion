# Especificación — autenticación y administración v3

Estado: implementación API y front en `v3-desarrollo`, 9 de noviembre de 2026.
V2 sigue abierta. No hay merge a main, tag v3 ni aceptación manual atribuida al equipo.

## Fuentes y políticas autorizadas

- [Módulo Investigación §3](../../../../ProyectosDeAula/docs/modulo_investigacion.md): login JWT, autorización, menú por roles, administración de usuario/rol/rol_usuario y logout.
- [Metodología](../../../../ProyectosDeAula/docs/0_METODOLOGIA.md) y [constitución](../../1_constitution.md): capas con interfaces, front independiente por HTTP, SQL parametrizado y borrado lógico.
- El usuario autorizó continuar v3 conservando v2 abierta. Los dos roles, TTL, Argon2id, HS256 y version_sesion son políticas de esta implementación, sin inventar aprobación del profesor.

| Tema | Comportamiento |
|---|---|
| Administrador | Lee y escribe investigación y administra seguridad |
| Consulta | Solo lectura de investigación; seguridad denegada |
| Sin roles efectivos | 403; roles arbitrarios no otorgan permisos |
| Autenticación | Usuario activo, firma/claims/vencimiento válidos y versión persistida coincidente; fallo: 401 |
| Roles | Se consultan roles y asignaciones activos por solicitud; no se confía en roles del JWT |
| Contraseña | Argon2id; altas y cambios: 12–1024 caracteres; nunca se devuelve hash |
| Sesión | 30 minutos configurables, sin refresh ni renovación automática |
| Logout | Invalida todas las sesiones anteriores mediante incremento atómico persistente |
| Primer administrador | Comando local con entrada oculta, transacción y rechazo de cuentas/conflictos existentes |
| Administración | CRUD de cuentas/roles; asignación por alta, lectura, edición transaccional y retiro lógico, sin reactivar pares retirados |
| Último administrador | Rechazo 409 y rollback de bajas que eliminen el último administrador efectivo; nombres de roles iniciales inmutables |
| Cambios de clave | Incrementan version_sesion; baja de cuenta también revoca |
| Navegador | Cookie firmada con identificador opaco y CSRF; JWT solo en almacenamiento del servidor; no localStorage ni campos HTML con JWT |

## Entrega

`main_v3:app` protege todas las rutas `/api/` de investigación y seguridad.
Públicos: login, diagnóstico y documentación OpenAPI. Sesión y logout verifican
su propia credencial. Las solicitudes directas reciben los mismos controles.

`app_v3.py` integra login/logout, menú, gestión administrativa, lectura y acciones
según permisos, comprobación de sesión por solicitud y manejo de 401/403/caída.
Los formularios POST, incluido login y logout, exigen CSRF. No hay acceso a PostgreSQL
desde Flask; SQLite local guarda únicamente sesiones del front, en volumen separado.

Compose v3 usa puertos 8026/8079 en loopback, PostgreSQL y volúmenes independientes.
La migración idempotente es un servicio previo obligatorio de la API; init.sql solo
inicializa volúmenes nuevos. Guía para bases existentes y nuevas en 7_quickstart.md.

## Límites y aceptación

Fuera de alcance: registro público, recuperación por correo, refresh, restitución
de asignaciones retiradas y funciones de v4. No se añadió limitación de intentos
de login; el compose es local y no constituye un despliegue público de producción.
No se migró la base compartida de v2. Pendientes: revisión humana de pantallas y
prompt oculto, aportes y firmas del equipo, aceptación y enmiendas formales.

Las ampliaciones de los artículos 2, 5 y 10 se justifican en 4_research.md. Esta
implementación sigue la autorización del usuario; no cambia la constitución ni
certifica ratificación formal. Evidencia automatizada en VERIFICACION_V3.md.
