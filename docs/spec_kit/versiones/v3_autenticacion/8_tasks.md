# Tareas y evidencia — primera entrega v3

Fecha: 5 de noviembre de 2026. Las casillas completadas acreditan únicamente
esta parte de backend. Detalles de ejecución en VERIFICACION_V3.md.

## Políticas y preparación

- [x] Registrar las políticas explícitas del usuario y distinguirlas de los requisitos del profesor. Evidencia: 2_spec.md y GUIA_IA3.md.
- [x] Inspeccionar esquema local antes de migrar, sin consultar credenciales. Evidencia: 4_research.md y db/migraciones/README_V3.md.
- [x] Preparar y probar migración inicial/repetida y rechazo incompatible en PostgreSQL aislado; conservar inactivos y versiones. Evidencia: README_V3.md de migraciones.
- [x] Preparar entorno Docker y secretos externos independientes de v2. Evidencia: docker-compose.v3.yml, .env.example y 7_quickstart.md.

## Backend parcial

- [x] Implementar interfaces, servicio, repositorio parametrizado y adaptadores PyJWT/Argon2id. Evidencia: api_investigacion/seguridad/, servicio_autenticacion.py y repositorio_autenticacion_postgresql.py.
- [x] Implementar los tres contratos login/sesion/logout sin exponer hash o password. Evidencia: autenticacion_controller.py y 6_contracts.md.
- [x] Consultar actividad y versión persistidas, roles y asignaciones activos por solicitud. Evidencia: consulta SQL y pruebas HTTP.
- [x] Incrementar versión atómicamente y comprobar revocación después de reinicio. Evidencia: prueba_autenticacion_v3.py.
- [x] Preparar bootstrap transaccional con getpass, sin predeterminados, rechazo de cuentas/conflictos y terminal obligatoria. Evidencia: comandos/crear_administrador.py y pruebas del servicio/comando no interactivo.

## Verificaciones realmente ejecutadas

- [x] Login válido/inválido, usuario inexistente/inactivo/nulo, ausencia/alteración/firma/algoritmo/vencimiento/claims inválidos y roles insuficientes: 14 pruebas HTTP y de política pasaron. Evidencia: VERIFICACION_V3.md.
- [x] Exclusión de rol y asignación inactivos, logout concurrente, revocación de múltiples tokens y persistencia al reiniciar. Evidencia: misma suite.
- [x] Bootstrap real del servicio en base nueva y rechazo posterior conservando cuentas; comando sin terminal rechazado. Evidencia: misma suite. No acredita recorrido manual del prompt oculto.
- [x] Regresión en memoria: prueba_capas.py y las 12 pruebas de prueba_v2.py. Evidencia: VERIFICACION_V3.md.
- [x] Comprobar por lectura que investigacion_local sigue sin columnas v3 y sin cuentas/roles/asignaciones. Evidencia: VERIFICACION_V3.md.

## Pendientes que esta entrega no certifica

- [ ] Aplicar migración a la base local compartida: expresamente fuera del pedido actual.
- [ ] Proteger todas las rutas de investigación y seguridad por recurso/verbo, con middleware/autorización.
- [ ] Implementar CRUD administrativo y endpoints de retiro lógico de asignaciones.
- [ ] Implementar pantallas Flask, Bearer, expiración, logout, menú y CSRF.
- [ ] Validar manualmente el bootstrap con entrada oculta y todas las pantallas futuras.
- [ ] Resolver y verificar protección del último administrador, límites de login y recuperación operativa.
- [ ] Implementar restitución de asignaciones retiradas o recuperación automática por correo: fuera de esta primera entrega.
- [ ] Completar regresión integrada de dominio y revisión manual; las pruebas en memoria no la sustituyen.
- [ ] Ratificar formalmente las enmiendas y revisar/integrar aportes del equipo.
- [ ] Completar pendientes manuales de v2 y obtener firmas; v2 sigue abierta.
- [ ] Completar aceptación de v3; no declarar esta entrega completamente protegida.
