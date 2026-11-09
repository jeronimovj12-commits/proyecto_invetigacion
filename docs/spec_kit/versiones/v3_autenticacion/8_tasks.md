# Tareas y evidencia — v3

Actualizado: 9 de noviembre de 2026. V2 abierta; entrega sin merge/tag ni firmas.

## Implementación

- [x] Auditar estado, commits, constitución y documentos; conservar los tres commits previos y la rama v3-desarrollo.
- [x] Conservar login JWT, Argon2id, bootstrap y logout persistente existentes.
- [x] Proteger todas las rutas de investigación/seguridad en API, también peticiones directas, y declarar Bearer en OpenAPI.
- [x] Implementar administración con interfaces, SQL parametrizado y borrado lógico.
- [x] Proteger último administrador mediante transacción y bloqueo de las tres tablas; nombres iniciales inmutables.
- [x] Revocar sesiones al cambiar contraseña y retirar cuenta; filtrar roles/asignaciones inactivos.
- [x] Front separado por HTTP: login/logout, sesión de servidor, menús, acciones y URL según permisos.
- [x] Cookies sin JWT, CSRF en todo POST, rotación al login, no-store y manejo de 401/403/vencimiento/caída.
- [x] Docker aislado de v2, migración obligatoria antes de API y dependencias v3 fijadas.
- [x] Guía nueva/existente y scripts de configuración/verificación; sin secretos reales versionados.

## Verificación automática

Evidencia detallada y resultados en VERIFICACION_V3.md; comandos en scripts/verificar_v3.ps1.

- [x] Migración con datos anteriores, repetición y rechazo incompatible.
- [x] 14 pruebas HTTP/política de autenticación, revocación y reinicio.
- [x] Matriz de las 90 operaciones, CRUD administrativo, bajas concurrentes y regresión CRUD de dominio con administrador.
- [x] Prueba de capas v1 y 12 pruebas en memoria v2.
- [x] 5 casos Flask de cookies/CSRF/roles/URL/errores, con transporte simulado.
- [x] Recorrido Flask→HTTP→API→PostgreSQL real, sin mocks; formularios reales de alta y administración.

## Pendientes humanos / fuera de alcance

- [ ] Recorrido humano del prompt oculto del bootstrap y revisión visual del navegador, vencimiento y botón atrás.
- [ ] Aportes/revisión del equipo, firmas, ratificación formal de enmiendas y aceptación de v3.
- [ ] Pendientes manuales de v2 y su cierre independiente.

No se edita prueba_permisos_v3_equipo.py ni VERIFICACION_API_V3_EQUIPO.md ni
VERIFICACION_FRONT_V3_EQUIPO.md. No se ejecuta migración sobre investigacion_local.
Fuera de alcance: recuperación por correo, registro público, restitución de
asignaciones retiradas y funcionalidades v4. No hay limitación de intentos de
login; la configuración entregada es local. No se atribuye aceptación al profesor.
