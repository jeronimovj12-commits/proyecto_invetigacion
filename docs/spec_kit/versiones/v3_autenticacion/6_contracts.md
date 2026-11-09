# Contratos implementados — v3

Estos tres contratos son políticas autorizadas por el usuario. El profesor
confirma POST /api/login con JWT y logout, pero no estos cuerpos, tiempos o claims.
Actualizado el 9 de noviembre de 2026: CRUD y protección global implementados.

## POST /api/login

Público. Content-Type: application/json. Cuerpo exacto:
`{"username":"<cuenta>","password":"<contraseña>"}`.
username: texto de 1–100 caracteres; password: 1–1024; campos adicionales
rechazados. No hay normalización automática ni registro público.

200: `{access_token, token_type:"bearer", expires_in, usuario}`.
expires_in es JWT_MINUTOS*60 (30 minutos por defecto, configuración 1–1440).
usuario contiene únicamente `{id, username, email, nombre_completo, roles}`;
nombre_completo admite null y roles es lista de nombres activos efectivos.
Nunca se retorna password/hash. Cache-Control: no-store; Pragma: no-cache.

401 genérico para cuenta inexistente, contraseña incorrecta o usuario no activo
(incluido NULL); no se devuelve token. Credenciales válidas sin administrador
ni consulta efectivos: 403, sin token. La existencia de roles arbitrarios no
concede permisos de los dos roles iniciales.

## JWT emitido y validado

Algoritmo permitido fijo HS256, jamás obtenido del encabezado del solicitante.
JWT_SECRET externo, aleatorio y de al menos 32 bytes. Biblioteca PyJWT 2.15.1.

Claims obligatorios: sub (texto decimal positivo, ID integer PostgreSQL),
version_sesion (entero no negativo, sin booleanos), iat y exp (enteros UTC NumericDate),
iss y aud (coinciden exactamente con JWT_ISSUER y JWT_AUDIENCE; aud único).
Se exige exp>iat, vigencia no superior al TTL configurado, firma válida, token
no vencido e iat no futuro. No se admiten claims obligatorios omitidos.
No se confía en roles transportados por el token: se consultan en la base.

Después de verificar el JWT, cada operación consulta usuario activo y versión
vigente; roles: rol.activo IS TRUE y rol_usuario.activo IS TRUE. La API usa el
estado persistido, sin lista de revocaciones en memoria.

## GET /api/sesion

Cabecera Authorization: Bearer <token>. 200 con el usuario público descrito
arriba y cabeceras no-store. Credencial ausente/malformada, token inválido,
usuario inexistente/inactivo o versión antigua: 401. Identidad válida sin rol
inicial efectivo: 403.

## POST /api/logout

Bearer obligatorio. Sin cuerpo requerido. 200:
`{"estado":200,"mensaje":"Sesión cerrada en todos los dispositivos."}`.

UPDATE condicional atómico de version_sesion en PostgreSQL, con validación de
la versión presentada. Desde que confirma, tokens de la versión anterior reciben
401, incluso después de reiniciar la API. Logout repetido con el token anterior:
401. Dos logouts simultáneos sobre la misma versión: uno confirma y el otro
responde 401, sin perder el incremento. Token vigente de usuario que perdió sus
roles aún permite cerrar sus propias sesiones; no concede acceso de investigación.

Cambiar TTL, emisor, audiencia o secreto puede invalidar tokens existentes.
El vencimiento no renueva sesión; Flask solicita nuevo login.
La revocación no cancela operaciones que ya habían sido autorizadas y estaban
cursando antes del COMMIT del logout.

## Errores

Sobre común `{estado,mensaje,detalle}`; 422 añade `errores` traducidos, sin
copiar el cuerpo ni los valores sensibles. 401 incorpora WWW-Authenticate: Bearer.

- 401: Credenciales inválidas / Autenticación requerida; identidad no vigente.
- 403: Acceso denegado; identidad válida sin permisos suficientes.
- 422: JSON inválido, campos faltantes/adicionales o longitudes inválidas.
- 500: fallo interno, texto genérico sin SQL, hashes, tokens ni excepciones completas.

## Protección de investigación

Todas las rutas `/api/` de investigación existentes conservan sus contratos v2
para identidades autorizadas: administrador lee/escribe; consulta solo GET/HEAD/OPTIONS.
La autorización ocurre antes de ejecutar operaciones y también en solicitudes
directas. Seguridad requiere administrador para cualquier verbo. Usuario válido
sin rol efectivo: 403. Token ausente/inválido/inactivo/revocado: 401.
Públicos: POST /api/login, GET / y documentación /docs, /redoc, /openapi.json.
/api/sesion y /api/logout validan su propio Bearer.

## Administración

Bearer de administrador en todas estas rutas. Todas las lecturas filtran activo IS TRUE.
Listados y detalles: 200 con `{tabla,limite,total,datos:[...]}`. Listas vacías: 200,
datos `[]`; detalle inexistente/inactivo: 404. limite predeterminado 100, rango 1–1000;
detalles usan limite=1. Campos públicos:

- usuario: id, username, email, nombre_completo, activo.
- rol: id, nombre, descripcion, activo.
- rol_usuario: usuario_id, rol_id, activo.

| Recurso | Operaciones |
|---|---|
| /api/usuario | GET listado; POST crea, 201 con objeto público |
| /api/usuario/{id} | GET detalle; PUT reemplazo, PATCH parcial, 200 con objeto; DELETE lógico, 200 `{estado:200,mensaje:"Cuenta retirada."}` |
| /api/rol | GET listado; POST crea, 201 con objeto público |
| /api/rol/{id} | GET detalle; PUT reemplazo, PATCH parcial, 200 con objeto; DELETE lógico, 200 `{estado:200,mensaje:"Rol retirado."}` |
| /api/rol_usuario | GET listado; POST asigna, 201 con objeto público |
| /api/rol_usuario/{usuario_id}/{rol_id} | GET detalle; DELETE lógico, 200 `{estado:200,mensaje:"Asignación retirada."}` |

POST/PUT usuario: username (1–100), email (1–150), password (12–1024) obligatorios;
nombre_completo opcional/null (máximo 200). PUT exige también contraseña; cambiarla
revoca sesiones. PATCH admite los mismos campos presentes, sin password obligatorio;
null solo se admite en nombre_completo. No se expone version_sesion ni hash.

POST/PUT rol: nombre obligatorio (1–100), descripcion opcional/null (máximo 2000).
PATCH parcial con esos campos; nombre no admite null. Se recortan espacios en
los textos administrativos (las contraseñas no se recortan).

POST asignación: `{usuario_id: entero positivo, rol_id: entero positivo}`;
ambos padres activos. Clave compuesta inmutable: no existe PUT/PATCH para alterar
una asignación; cambiarla se expresa retirando y creando otra distinta. Pares
retirados no se reactivan. Roles arbitrarios no conceden permisos v3.

Campos extra, activo, valores nulos no permitidos o límites inválidos: 422.
PATCH vacío: 409. Duplicados (incluidos registros inactivos), FK inexistentes o
inactivas, renombrar administrador/consulta y perder el último administrador
efectivo: 409 `{estado:409,mensaje:"Operación rechazada.",detalle:<motivo público>}`.
Baja repetida/inexistente: 404. No hay reactivación ni borrado físico. La protección
del último administrador se evalúa transaccionalmente frente a mutaciones concurrentes.

## Contrato del navegador

GET/POST /login; POST /logout. Todas las rutas de investigación requieren sesión;
las de crear/editar/retirar y /seguridad/* requieren administrador. Administración:
/seguridad/usuarios, /seguridad/roles, /seguridad/asignaciones (GET/POST) y
/seguridad/{recurso}/{claves}/retirar (POST; par de asignación con guion).
La pantalla usa PATCH para edición, omite contraseña vacía y no la repinta.

Todo POST exige csrf_token del formulario vinculado a cookie firmada; omisión o
alteración: 400. Cookie HttpOnly, SameSite=Lax, Secure configurable para HTTPS;
JWT solo en servidor y Authorization agregado por cliente_api. Se rota identificador
y CSRF al entrar; se invalida sesión local tras confirmar logout global en API.
Si logout falla por caída de API se informa y permite reintentar, sin afirmar revocación.

401/vencimiento/invalidación: limpia sesión y redirige a login con aviso; 403:
pantalla de acceso denegado sin datos; API caída al comprobar sesión: 503 sin datos
de investigación. GET logout: 405. Respuestas front y API protegidas: no-store.
