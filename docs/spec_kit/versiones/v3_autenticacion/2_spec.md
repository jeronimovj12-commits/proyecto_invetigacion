# Especificación inicial — v3: autenticación, JWT, usuarios y roles

Fecha: 5 de noviembre de 2026. **Borrador para revisión del equipo**.
Solo preparación documental; no hay implementación de v3 ni cambio de esquema.

## Procedencia y adelanto autorizado

Requisitos originales localizados en documentos del profesor del repositorio:

| Fuente (rutas relativas a esta carpeta) | Requisito confirmado |
|---|---|
| [Módulo Investigación §2–3](../../../../ProyectosDeAula/docs/modulo_investigacion.md) | POST /api/login con JWT, middleware de autenticación/autorización, menú por roles, CRUD de usuario/rol/rol_usuario solo para administradores y logout; consulta no escribe |
| [Metodología §2 y §6](../../../../ProyectosDeAula/docs/0_METODOLOGIA.md) | JWT, sesiones, Authorization: Bearer desde el front, contraseñas hasheadas (bcrypt o equivalente), regresión v1–v2 |
| [Mapa de versiones](../0_mapa_versiones.md) | Las tres tablas entran en v3; dashboard y consultas multitabla pertenecen a v4 |
| [Constitución](../../1_constitution.md), artículos 1–11 | Capas con interfaces, SQL parametrizado sin ORM, front separado por HTTP, secretos por entorno, borrado lógico y contratos explícitos |

Sí existe el alcance original de v3; no se encontró un contrato detallado
original de sus cuerpos, permisos por recurso, expiración o recuperación.
Los detalles de este spec kit que no constan en las fuentes son propuestas.

La constitución (art. 1), el mapa y la metodología (§1.1) exigen cerrar una
versión antes de escribir la siguiente. El usuario decidió explícitamente
adelantar esta preparación mientras v2 sigue abierta. Se registra la desviación
de secuencia, sin simular cierre, aceptación del profesor ni enmienda aprobada.
La constitución no se modifica. Antes de implementar, el equipo debe resolver
esta secuencia conforme al art. 11 y a sus responsabilidades con el profesor.

V2 conserva pendientes las pruebas manuales restantes, revisión e integración
de aportes de compañeros, decisiones y firmas. Véase
[VERIFICACION_V2.md](../../../../VERIFICACION_V2.md). No fusionar con main ni crear tags.

## Alcance confirmado

- Inicio de sesión que entrega JWT y control de acceso por roles en la API.
- Sesiones y cierre de sesión, con pantallas y menú coherentes con los roles.
- CRUD de `usuario`, `rol` y `rol_usuario`, API y front, solo para administradores.
- Un usuario de consulta no puede escribir, incluso accediendo directamente a la API.
- Contraseñas hasheadas, nunca expuestas en respuestas ni almacenadas en claro.
- Front Flask independiente: conserva el token y lo envía como Bearer por HTTP;
  no importa código de la API ni consulta PostgreSQL.
- Preservar el comportamiento de dominio de v1–v2 para usuarios autorizados.

No se incluyen dashboard, consultas de v4 ni publicación. Registro público,
recuperación automática, refresh tokens y MFA no se asumen como requisitos.

## Decisiones pendientes del equipo

| Tema | Confirmado | Por decidir / propuesta |
|---|---|---|
| Permisos | Administración de seguridad solo admin; consulta no escribe | Matriz por recurso/verbo, roles adicionales, lecturas anónimas, combinación de roles y usuario sin rol; proponer denegar lo no concedido |
| Primer usuario | No hay usuarios ni roles locales | Proponer comando de bootstrap controlado, idempotente, con secreto por entorno y sin contraseña predeterminada; definir responsable |
| Registro | No se exige alta pública | Proponer alta solo por admin; definir si habrá invitaciones o registro público |
| Sesiones | JWT y logout obligatorios | Duración absoluta/inactividad, renovación, almacenamiento del front y revocación; no fijar tiempos sin acuerdo |
| Recuperación | Sin procedimiento especificado | Definir responsable, verificación de identidad y mecanismo; no prometer correo automático |
| Roles y cambios | Existen usuario y rol activos | Definir efecto inmediato al desactivar o quitar un rol, protección del último admin y autoedición |
| Retiro de asignaciones | CRUD exigido, borrado lógico constitucional | Resolver ausencia de activo en rol_usuario antes de contratar DELETE |

## Criterios de aceptación a verificar en el futuro

Login válido entrega token sin password/hash; credenciales incorrectas no revelan
si existe la cuenta. Token ausente, inválido o vencido impide acceso protegido.
Identidad válida sin permiso impide la operación sin cambiar datos. Admin puede
gestionar seguridad; consulta no escribe; ocultar el menú no sustituye la API.
Logout limpia el estado del front y cumple la política de revocación acordada.
Cada caso debe probarse en servicios, HTTP real y navegador; hoy están pendientes.
