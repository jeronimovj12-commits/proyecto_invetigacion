# Investigación y decisiones por revisar — v3

Fecha de inspección: 5 de noviembre de 2026. Este documento contiene hallazgos
y propuestas, no decisiones ya aprobadas por el profesor o el equipo.
Los apartados iniciales conservan la inspección anterior a implementar;
la actualización al final registra la autorización y el trabajo posterior.

## Estado de Git y verificaciones documentales

Al inicio, `git status --short --branch` mostró v2-desarrollo limpia; la
evidencia de carga local ya estaba en el commit 851e3ac, titulado
"Registra la carga de catálogos y verifica opciones activas en la API".
No había cambios pendientes que justificaran crear otro commit para esa
evidencia ni se renombró el commit existente. La rama v3-desarrollo no existía
y se creó desde ese avance de v2-desarrollo mediante `git switch -c v3-desarrollo`.
Se conservó intacta la historia previa.

En esta preparación se leyeron constitución, mapa, módulo Investigación,
metodología, SQL y código; se consultaron solo metadatos y conteos de PostgreSQL
y el OpenAPI real. No se implementó ni probó autenticación; no se insertaron
usuarios o roles, no se aplicaron migraciones y no se ejecutaron pruebas de v3.

## Estado real comprobado

- db/init.sql y el SQL original de ProyectosDeAula definen las tres tablas;
  no incluyen semillas de usuarios o roles. La consulta local de information_schema
  y pg_constraint confirmó el modelo de 5_data_model.md. Conteos: usuario=0,
  rol=0, rol_usuario=0. No se consultaron contraseñas ni se alteraron tablas.
- Búsqueda en api_investigacion/ y front_flask/: sin implementación de login,
  logout, JWT, Bearer, verificación de password o control por roles.
- GET real a http://localhost:8025/openapi.json: cero rutas que coincidan con
  login/logout/usuario/rol y ningún components.securitySchemes. Es diagnóstico
  de lo existente, no una prueba de autenticación implementada.
- api_investigacion/main.py identifica la versión v2; registra routers y un
  manejador común de errores. servicios/ensamblador.py construye servicios y
  repositorios; es el lugar real de composición de dependencias.
- front_flask/app.py usa sesión de Flask para flash y permite CLAVE_SESION por
  entorno con un valor alternativo versionado. Eso no es una sesión autenticada.
  cliente_api.py envía solicitudes con requests sin Bearer.
- requirements.txt de API no contiene librería JWT ni de hash de contraseñas;
  el front depende solo de Flask y requests. .gitignore incluye *.env, pero no
  hay .env.example versionado. Compose conserva credenciales didácticas; no se
  modificaron ni se consideran adecuadas para los secretos nuevos de v3.

## Integración propuesta con las capas actuales

El controlador de login valida con Pydantic y llama a IServicioAutenticacion.
El servicio busca al usuario mediante IRepositorioUsuario, verifica activo y
hash con un adaptador por interfaz y solicita la emisión de JWT a otro adaptador.
Servicios de usuarios, roles y asignaciones reciben repositorios por interfaz;
el SQL vive únicamente en repositorios PostgreSQL con text() y parámetros.
No se propone ORM ni acceso de controladores al motor.

Un middleware obtiene la identidad del Bearer mediante el servicio de seguridad;
la autorización por recurso/verbo comprueba permisos antes de la operación. Las
dependencias del controlador pueden complementar ese middleware; no sustituyen
el requisito del profesor por una comprobación del menú. El servicio no recibe
Request ni lanza HTTPException: usa excepciones de negocio que la frontera
HTTP traduce. El ensamblador existente construye los adaptadores concretos.

## Propuestas técnicas, sin elección cerrada

| Tema | Propuesta y consecuencia | Aprobación pendiente |
|---|---|---|
| Hash | Usar bcrypt o equivalente mediante librería mantenida, con salt y comparación propia de la librería; password de SQL guarda solo hash | Elegir algoritmo, parámetros, librería y límites de entrada |
| JWT | Firma con algoritmo permitido fijo; validar firma, exp, emisor y destinatario acordados; sub identifica usuario, no contraseña | Algoritmo, librería, claims y rotación |
| Roles | Consultar usuario y roles activos en servidor para evitar que un JWT antiguo mantenga permisos retirados; denegar por defecto | Matriz completa y costo/consistencia de consulta |
| Bootstrap | Comando explícito sin endpoint público; no reemplazar cuenta existente ni reactivar; secreto por entorno | Quién ejecuta y cómo se entrega la primera credencial |
| Almacenamiento del front | Mantener independencia HTTP; preferir token en almacenamiento del servidor y cookie de sesión opaca | Comparar infraestructura adicional con sesión Flask firmada; no usar variable global compartida |
| CSRF y cookies | Proteger formularios de cambio y logout, cookies HttpOnly/SameSite y Secure cuando se use HTTPS | Mecanismo concreto y configuración local |
| Secretos | JWT_SECRET y CLAVE_SESION obligatorios por entorno, sin valores alternativos reales; .env.example solo con marcadores | Configuración de arranque y transición del compose didáctico |

No seleccionar versiones de librerías a partir de este borrador: reevaluar
compatibilidad y mantenimiento al implementar. El art. 2 limita las dependencias;
antes de añadir bibliotecas de seguridad se debe proponer y aceptar la enmienda
según el art. 11. Ampliar 401/403 también exige conciliar el art. 10.

## Sesión Flask y logout

La sesión predeterminada de Flask se almacena en cookie firmada; no debe
confundirse firma con cifrado. Su almacenamiento se debe evaluar antes de poner
un Bearer dentro. La alternativa del servidor requiere elegir almacenamiento,
caducidad y comportamiento al reiniciar; no existe hoy en el proyecto.
[Referencia oficial de Flask](https://flask.palletsprojects.com/en/stable/api/#sessions).

Eliminar el token del front no invalida por sí solo una copia de un JWT que
sigue vigente. Propuestas para discutir: logout local con esa limitación
documentada y tokens cortos, o revocación del lado servidor con estado adicional.
No se elige una ni se promete revocación inmediata sin diseñarla. El modelo
actual no tiene sesión, lista de revocados, refresh token ni versión de token.
Especificar si el logout afecta una sesión o todas y cómo se prueba reutilización.

Las validaciones de algoritmo y destinatario se apoyan en
[RFC 8725, buenas prácticas JWT](https://www.rfc-editor.org/rfc/rfc8725).
Es referencia técnica, no especificación del profesor.

## Conflictos que bloquean decisiones de implementación

1. Art. 1 y metodología: se adelanta el borrador por decisión del usuario sin
   cerrar v2; registrar la resolución formal antes de implementar.
2. Art. 6: rol_usuario no tiene activo. No se puede prometer DELETE lógico
   individual con este esquema ni reemplazarlo por DELETE físico. Desactivar
   todo un usuario tampoco equivale a quitar solo un rol. Evaluar con el equipo
   una migración mínima o enmienda de la regla; ninguna está aprobada o aplicada.
3. Art. 2: bibliotecas de JWT/hash y posible almacenamiento del front requieren
   justificar dependencias. No implementar criptografía propia para evitarlas.
4. Art. 10: 401/403 no están enumerados. Proponer incorporarlos al contrato y
   tramitar la enmienda, sin convertir esta propuesta en constitución vigente.

Recuperación de acceso, registro público, duración y política del último admin
no están detallados en los originales; deben resolverse antes de cerrar contratos.

## Actualización: primera implementación autorizada

El usuario autorizó dos roles, permisos del administrador y consulta, alta por
administrador, TTL de 30 minutos configurable sin refresh token, logout global
con version_sesion, asignaciones con borrado lógico y Argon2. Recuperación por
correo, restitución de asignaciones, front, CRUD administrativo y protección
de todas las rutas quedaron fuera de esta entrega. No son requisitos nuevos
atribuidos al profesor. El cierre de v2 permanece pendiente.

Antes de migrar se consultaron nuevamente information_schema y pg_constraint
locales: coincidieron con el esquema original, con cero cuentas/roles/asignaciones.
Después de las pruebas, la base compartida conserva cero columnas nuevas y
cero filas en esas tablas. No se aplicó allí la migración.

Se eligieron PyJWT 2.15.1 y pwdlib[argon2] 0.3.0, instalados y probados en la
imagen aislada. La [guía oficial de FastAPI](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
usa estas bibliotecas para JWT y Argon2; la [API oficial de PyJWT](https://pyjwt.readthedocs.io/en/stable/api.html)
documenta algorithms fijo y require para exigir claims. Se consultaron estas
fuentes en esta sesión. PasswordHash.recommended produce Argon2id; no se
implementó hashing ni firma propios. Las versiones anteriores del stack siguen
con el esquema de dependencias del proyecto; no se convirtieron todas a un lockfile.

La razón para ampliar las dependencias (art. 2) es usar bibliotecas mantenidas
en lugar de criptografía propia. La razón para ampliar las tablas (art. 5) es
persistir revocación tras reinicio y permitir borrado lógico sin borrar vínculos.
La razón para ampliar errores (art. 10) es distinguir autenticación fallida
(401) de autorización insuficiente (403). Estas propuestas de enmienda se
ejecutan en el alcance autorizado por el usuario, sin afirmar ratificación
formal del texto constitucional ni firmas del equipo.

Se usa main_v3:app y un compose separado para no romper el entorno de v2 con
columnas/dependencias aún no instaladas. El controlador solo conoce la interfaz
de servicio; el servicio recibe repositorio y adaptadores por interfaces; el
ensamblador_autenticacion construye implementaciones concretas. El repositorio
oculta parámetros en errores SQLAlchemy; la frontera HTTP y el comando no
imprimen excepciones internas. No se agregó middleware global todavía.

La política de logout quedó concretada: incremento atómico condicional de la
versión en PostgreSQL. Se verificó con HTTP, dos logouts concurrentes y reinicio
real del proceso uvicorn de prueba; no depende de memoria de la API. Las
operaciones ya autorizadas antes del logout no se cancelan retroactivamente.

## Implementación completa del alcance autorizado — 9 de noviembre de 2026

El nuevo pedido autoriza completar API, CRUD y Flask, proteger el último administrador
y publicar en origin/v3-desarrollo. Sustituye las restricciones de la primera entrega
que dejaban estas partes pendientes y prohibían push. Se conserva v2 abierta.

Se consultaron [seguridad de Flask](https://flask.palletsprojects.com/en/stable/web-security/)
y [transacciones SQLAlchemy](https://docs.sqlalchemy.org/en/20/core/connections.html).
La cookie firmada no cifra datos: solo contiene identificador opaco, CSRF y avisos.
Los JWT residen en SQLite del servidor, archivo 0600, directorio de creación 0700,
volumen separado y expiración limitada al TTL devuelto por API. No se renueva.
SQLite usa transacciones, conexión por operación y cierre explícito; no agrega
paquetes ni acceso al motor del módulo desde Flask. La cookie es HttpOnly y SameSite=Lax;
Secure se habilita con COOKIE_SECURE=1 al usar HTTPS. Los formularios comparan un
CSRF aleatorio con compare_digest; login y logout también lo requieren.

El middleware cierra por defecto `/api/` salvo login y las dos rutas que verifican
su propio Bearer. La política se aplica antes de validar el body o ejecutar la
operación, y se probó desde solicitudes HTTP directas sobre las 92 operaciones
actuales de investigación y administración. Diagnóstico y OpenAPI siguen públicos.

La protección del último administrador requiere atomicidad entre tres tablas.
Las mutaciones administrativas toman LOCK TABLE usuario, rol, rol_usuario IN
EXCLUSIVE MODE antes de leer, con aislamiento READ COMMITTED; después de esperar
ven el último commit. Comprueban administradores efectivos antes y después, y
hacen rollback si la operación deja cero. Incluye retirar cuenta, rol o asignación.
Las cuentas/roles no se reactivan; los nombres de roles iniciales son inmutables.
Cambiar password o desactivar cuenta incrementa version_sesion. No se almacenan
ni retornan hashes en contratos de consulta administrativa.

La migración sigue sin cambiar la base compartida. El servicio migrar-v3 corre
antes de API tanto con volumen nuevo como existente; falla cerrado si detecta
incompatibilidad. requirements-v3.lock fija las dependencias realmente instaladas;
los arranques v2 conservan su opción original de requisitos. No se declara v4,
protección frente a fuerza bruta ni producción pública. Evidencia y pendientes
en VERIFICACION_V3.md; no se inventan pruebas manuales ni firmas.


La revisión final completó PUT/PATCH de rol_usuario: conserva la fila original
inactiva y crea el nuevo par en una transacción. Destino duplicado (activo o
retirado), FK inválida o pérdida del último administrador provoca rollback y
conserva origen activo. No-op conserva el par sin cambios. No agrega columnas.
