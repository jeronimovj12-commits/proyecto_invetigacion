# Tareas pendientes — v3

Borrador del 5 de noviembre de 2026. Todas las tareas de aprobación,
implementación y aceptación permanecen pendientes; inspeccionar y documentar
no acredita que la autenticación funcione. Hallazgos reales en 4_research.md.

## Acuerdos y especificación

- [ ] Resolver con el equipo la preparación anticipada frente a art. 1 y metodología, manteniendo v2 abierta.
- [ ] Completar pruebas manuales, integración de aportes y firmas de v2 en su propio seguimiento.
- [ ] Revisar este alcance contra los originales del profesor y aprobar el spec kit.
- [ ] Acordar matriz por recurso/verbo, roles múltiples, usuario sin roles y rutas públicas.
- [ ] Definir bootstrap del primer administrador y responsable de credenciales.
- [ ] Definir alta administrada, invitaciones o registro público, sin asumir este último.
- [ ] Definir duración, inactividad, renovación, concurrencia y alcance del logout.
- [ ] Definir recuperación de acceso y protección del último administrador.
- [ ] Resolver borrado lógico de rol_usuario sin borrar físicamente por omisión.
- [ ] Tramitar enmiendas necesarias: secuencia, dependencias, 401/403 y cualquier excepción de esquema.
- [ ] Cerrar DTO, normalización/unicidad, errores, contraseña y reasignaciones de 6_contracts.md.

## Implementación futura (fuera de este pedido)

- [ ] Seleccionar bibliotecas de hash y JWT tras revisar mantenimiento y compatibilidad.
- [ ] Configurar secretos obligatorios por entorno y .env.example sin valores reales.
- [ ] Implementar interfaces, servicios, adaptadores y repositorios SQL parametrizados.
- [ ] Integrar middleware de autenticación/autorización y composición de dependencias.
- [ ] Implementar login, sesión, logout y CRUD administrativo con contratos aprobados.
- [ ] Implementar login/logout, menú y pantallas administrativas en Flask por HTTP.
- [ ] Resolver almacenamiento del token, aislamiento de sesiones, CSRF y cookies.

## Verificación y aceptación futura

- [ ] Probar servicios con repositorios falsos y reloj controlado.
- [ ] Verificar hash seguro y ausencia de password/hash/token en respuestas y logs improcedentes.
- [ ] Verificar login válido e inválido y usuario/rol inactivos o nulos.
- [ ] Verificar 401 sin token, vencido, alterado y algoritmo no permitido.
- [ ] Verificar 403 de consulta al escribir y de no-admin al gestionar seguridad, sin cambios en BD.
- [ ] Verificar permisos de cada recurso y cambios de rol con token ya emitido.
- [ ] Verificar logout y reutilización del token conforme a la política acordada.
- [ ] Verificar dos sesiones aisladas y comportamiento después de reiniciar.
- [ ] Ejecutar regresión v1–v2 con identidades autorizadas y catálogos existentes.
- [ ] Revisar manualmente login, errores, expiración, menú, URL directa, CRUD y logout.
- [ ] Registrar comandos, resultados y evidencia manual real; no sustituirla por automatización.
- [ ] Revisar e integrar aportes de compañeros, obtener firmas y evaluar aceptación final.

No crear tags ni fusionar con main mediante esta preparación. No hay tareas
de implementación marcadas como realizadas ni pruebas de v3 ejecutadas.
