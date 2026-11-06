# Contratos implementados — backend parcial v3

Estos tres contratos son políticas autorizadas por el usuario. El profesor
confirma POST /api/login con JWT y logout, pero no estos cuerpos, tiempos o claims.
El resto del CRUD y la protección global siguen pendientes.

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
El vencimiento no renueva sesión; el futuro front deberá solicitar nuevo login.
La revocación no cancela operaciones que ya habían sido autorizadas y estaban
cursando antes del COMMIT del logout.

## Errores

Sobre común `{estado,mensaje,detalle}`; 422 añade `errores` traducidos, sin
copiar el cuerpo ni los valores sensibles. 401 incorpora WWW-Authenticate: Bearer.

- 401: Credenciales inválidas / Autenticación requerida; identidad no vigente.
- 403: Acceso denegado; identidad válida sin permisos suficientes.
- 422: JSON inválido, campos faltantes/adicionales o longitudes inválidas.
- 500: fallo interno, texto genérico sin SQL, hashes, tokens ni excepciones completas.

Los contratos existentes de v2 no se modifican. No están implementados todavía
/api/usuario, /api/rol ni /api/rol_usuario; no hay middleware que proteja todas
las rutas de dominio. La función de política interna permite administrador
para lectura/escritura/seguridad y consulta solo para lectura de investigación.
