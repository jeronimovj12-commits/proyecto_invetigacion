# Borrador de contratos — v3

**No implementado ni aprobado.** Solo POST /api/login, JWT, Bearer, control por
roles, CRUD administrativo y logout proceden del alcance original. Los cuerpos,
códigos nuevos, rutas restantes y políticas siguientes son propuestas revisables.
No sustituye los contratos actuales de v1–v2.

## Autenticación y sesión propuestas

| Método y ruta | Cuerpo / resultado propuesto | Acceso |
|---|---|---|
| POST /api/login | JSON {username, password}; 200 con access_token, token_type="bearer", expires_in y usuario público con roles | Público |
| GET /api/sesion | 200 con identidad y roles efectivos, sin token ni password | Autenticado |
| POST /api/logout | 200 {estado:200, mensaje:"Sesión cerrada."}; semántica de revocación pendiente | Autenticado; acordar repetición/vencimiento |

expires_in se expresa en segundos; su valor no está decidido. Claims propuestos:
sub como ID de usuario en texto, iat y exp, iss/aud acordados; jti solo si la
política de revocación lo necesita. No incluir contraseña, hash ni secretos.
Cabecera de llamadas protegidas: Authorization: Bearer <token>.

Login fallido propone 401 con mensaje genérico "Credenciales inválidas." tanto
para cuenta inexistente como contraseña incorrecta/inactividad. No devolver
detalles internos. Falta acordar límites de intentos y política de bloqueo.

## Administración propuesta

Todas estas operaciones requieren administrador efectivo en la API, además
de menú restringido en el front. Respuestas de usuario nunca contienen password.

| Recurso | Rutas propuestas | Campos de creación / edición |
|---|---|---|
| usuario | GET/POST /api/usuario; GET/PUT/PATCH/DELETE /api/usuario/{id} | username, email, nombre_completo; password solo de entrada al crear; proponer cambio de contraseña por operación separada aún por definir |
| rol | GET/POST /api/rol; GET/PUT/PATCH/DELETE /api/rol/{id} | nombre, descripcion |
| rol_usuario | GET/POST /api/rol_usuario; GET/PUT/PATCH/DELETE /api/rol_usuario/{usuario_id}/{rol_id} | usuario_id, rol_id |

IDs SERIAL de usuario/rol asignados por servidor. No admitir id, activo o fechas
como campos editables en los cuerpos de usuario/rol. No se aprueban aún reglas
para cambiar componentes de rol_usuario: evaluar cambio de clave frente a
operación de reasignación transaccional, sin borrar físicamente como atajo.
DELETE de rol_usuario está **bloqueado para especificación final** por falta
de activo; enumerarlo conserva el requisito CRUD, no afirma soporte existente.

Proponer mantener convenciones del proyecto: listas con limite y sobre
{tabla, limite, total, datos}, vacías 204; creaciones 200, modificaciones/retiros
200 con filasAfectadas; PUT exige los campos editables acordados, PATCH distingue
omisión y null. Antes de implementar, concretar DTO de cada operación y respuesta,
política de duplicados, cambios de contraseña y retiro del último administrador.

## Errores propuestos y compatibilidad

| Estado | Uso |
|---|---|
| 401 | Falta de Bearer, token inválido/vencido o login inválido; proponer WWW-Authenticate: Bearer |
| 403 | Identidad válida sin permiso; ninguna escritura |
| 400 | Regla de negocio o referencia inactiva; PATCH vacío |
| 404 | Registro inexistente o inactivo, después de autorizar al solicitante |
| 422 | Cuerpo inválido según modelos Pydantic |
| 500 | Fallo interno con respuesta pública sin secretos |

Conservar sobre {estado, mensaje, detalle}; 422 añade errores. Proponer detalle
genérico en errores de autenticación, sin credenciales, hash, token o SQL.
401/403 requieren revisar el art. 10 antes de cerrar el contrato. No cambiar
automáticamente la política v2 de claves duplicadas por otro código.

La matriz de permisos por recurso/verbo está pendiente. No se asume que admin
pueda escribir todos los recursos de dominio solo por administrar usuarios.
El requisito confirmado es que consulta no escribe y seguridad es solo admin.

## Contrato de front por acordar

Proponer GET/POST /login y POST /logout en Flask, gestión de usuarios/roles y
asignaciones con rutas propias. API sigue decidiendo permisos; front solo adapta
mensajes y navegación. No devolver tokens en URLs ni guardar sesión autenticada
en una variable global. Ante 401 pedir login; ante 403 mostrar acceso denegado;
ante API caída mostrar aviso sin datos. Validar destino de redirección de vuelta
para impedir redirecciones externas. Formulario de logout con protección CSRF.
El almacenamiento definitivo del token y revocación siguen pendientes.
