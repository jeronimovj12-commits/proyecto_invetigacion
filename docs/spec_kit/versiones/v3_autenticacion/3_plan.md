# Plan por etapas — v3

Estado: planificación documental anticipada, no implementación autorizada.
Alcance y fuentes en [2_spec.md](2_spec.md). No cierra v2.

## Etapas propuestas y sus entregables

1. **Revisión del equipo.** Confirmar alcance y matriz de permisos por recurso
   y verbo. Resolver bootstrap, registro, expiración, logout y recuperación.
   Resolver la secuencia v2/v3, el retiro de rol_usuario y las enmiendas del
   art. 11 antes de programar decisiones incompatibles con la constitución.
2. **Contratos.** Acordar los cuerpos, errores y rutas de 6_contracts.md;
   identificar qué endpoints de v1–v2 serán protegidos. Enumerar excepciones
   públicas (login, diagnóstico, documentación si se aprueba), sin protegerlas
   o exponerlas accidentalmente mediante una regla genérica.
3. **Servicios e interfaces.** Diseñar autenticación, usuarios, roles y
   asignaciones; interfaces para verificar hashes y firmar/verificar JWT.
   Probar reglas con repositorios falsos, reloj controlado y sin PostgreSQL.
4. **Persistencia y adaptadores.** Repositorios PostgreSQL con SQL manual
   parametrizado y transacciones para asignaciones y protección del último
   administrador, si se aprueba. Elegir librerías auditadas y declararlas solo
   tras resolver el límite de dependencias del art. 2. No ejecutar init.sql
   sobre una instalación existente. Cualquier migración requeriría diseño y
   aprobación propios; no forma parte de esta preparación.
5. **API.** Controladores tipados y middleware de autenticación/autorización;
   verificar permisos antes de llamar a escrituras. Ensamblar implementaciones
   en el punto existente de composición. Mantener repositorios y servicios
   libres de HTTP. Ampliar el manejador común para 401/403 sin filtrar secretos.
6. **Front Flask.** Login, logout, menú por roles y gestión de las tres tablas.
   cliente_api agrega Bearer por solicitud y traduce 401/403. Manejar expiración
   con mensaje en español y nueva autenticación; una API caída deja aviso sin
   datos. Acordar almacenamiento y CSRF antes de conectar formularios.
7. **Verificación e integración futura.** Ejecutar la matriz siguiente, regresión
   v1–v2 adaptada a autenticación, revisión del equipo, revisión manual y firmas.
   Ninguna prueba está completada por haberla descrito aquí.

## Matriz de verificación pendiente

| Caso | Servicio / API futura | Front y revisión manual futura |
|---|---|---|
| Login válido | Verificar hash; JWT firmado y expiración; sin hash en JSON ni logs | Entrar con cada rol y observar menú autorizado |
| Login inválido/inactivo | Mismo error público; no emitir JWT | Aviso claro, sin revelar existencia de usuario |
| Sin autenticar | 401 propuesto en lectura/escritura protegida; no tocar filas | Acceso por URL lleva al login; sin datos protegidos |
| Token alterado/vencido | Rechazar firma, algoritmo o vigencia inválidos | Expiración limpia estado; pedir nuevo login |
| Permiso insuficiente | 403 propuesto para consulta intentando POST/PUT/PATCH/DELETE y no-admin gestionando seguridad | Sin menú de administración; URL directa también bloqueada |
| Admin | CRUD de las tres tablas, validación de FK y unicidad | Crear, editar y retirar según reglas aprobadas |
| Logout | Comprobar token reutilizado según política acordada; no asumir revocación | Limpiar sesión, volver a URL protegida y probar botón atrás |
| Cambio de rol/inactividad | Repetir solicitud con token previo y comprobar la política | Menú y mensajes coherentes; no conservar permiso obsoleto |
| Regresión | Repositorios/servicios de dominio siguen cumpliendo v1–v2 con identidades autorizadas | Desplegables y formularios existentes siguen funcionando |
| Sesiones simultáneas | Dos usuarios no comparten tokens ni roles | Dos navegadores/sesiones permanecen aislados |

Preparar datos de prueba aislados, comprobar ausencia de escrituras tras rechazos
y registrar comandos, resultados y evidencia visual real en futuros documentos
de verificación. No reutilizar evidencia de v2 para acreditar seguridad de v3.
