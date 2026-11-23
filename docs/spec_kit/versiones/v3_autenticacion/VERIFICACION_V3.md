# Verificación ejecutada — implementación v3

Fecha: 9 de noviembre de 2026. Rama v3-desarrollo; v2 abierta. No acredita pruebas
manuales, firmas, aceptación del equipo ni cierre de versión. El registro anterior
se conserva al final como evidencia histórica del backend parcial.

## Estado auditado y alcance

Al inicio: Git limpio, v3-desarrollo tres commits por delante de origin (ee05b39,
9c34ba9 y 7ed5594). Se conservaron. Se revisaron constitución y todos los documentos
v3, capas, migración y front. Faltaban protección global, administración, último
administrador, Flask autenticado y arranque completo. Estas partes se implementaron.
No se editaron prueba_permisos_v3_equipo.py, VERIFICACION_API_V3_EQUIPO.md ni
VERIFICACION_FRONT_V3_EQUIPO.md. No se migró investigacion_local ni se cerró v2.

## Comando final ejecutado y resultado

Desde la raíz:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verificar_v3.ps1
```

Terminó con código 0 y «Verificaciones automáticas v3 completadas». Construyó las
imágenes con requirements-v3.lock y ejecutó secuencialmente estas comprobaciones:

| Comprobación | Resultado de la ejecución final |
|---|---|
| prueba_migracion_v3.py | Datos anteriores inactivos conservados, repetición, versión=7 y asignación retirada conservadas; esquema incompatible rechazado |
| prueba_autenticacion_v3.py | 14 pruebas, OK, 6.592 s |
| prueba_administracion_v3.py | 5 pruebas, OK, 2.843 s; matriz de 92 operaciones HTTP |
| prueba_capas.py | Recorrido de capas v1 en memoria, todos los pasos OK |
| prueba_v2.py | 12 pruebas en memoria, OK, 0.072 s |
| prueba_front_seguro_v3.py | 5 pruebas Flask, OK, 0.472 s; transporte simulado |
| prueba_integracion_v3.py | 1 recorrido real Flask→HTTP→API→PostgreSQL, OK, 1.377 s |

Bases aleatorias creadas en esa ejecución (servidor postgres-v3 aislado):
pruebas_migracion_v3_83a65586c7aa4d50be34de476333842a,
pruebas_v3_373e27c5e8f340bdb51738d55ccda743 y
pruebas_v3_6869e2d13ee645028341b7d6b05efc51. La integración usa otra base nueva
creada por servidor_integracion_v3.py. Las bases y volúmenes se conservan; el script
detuvo el servidor API de pruebas al terminar, sin borrar datos ni usar cuentas reales.
Credenciales efímeras en memoria o fixture-v3 con archivo 0600, nunca en Git ni informe.

## Cobertura y límites de la evidencia

- Login, claims/firma/algoritmo/expiración, inactividad, ausencia de rol, exclusión de roles/asignaciones inactivos, no exposición de password/hash y configuración externa.
- Logout concurrente con incremento único; dos tokens invalidados y rechazo después de reiniciar el proceso uvicorn. Bootstrap del servicio crea la primera cuenta y rechaza otra inicialización; CLI sin terminal rechazada. No se recorrió manualmente getpass.
- Matriz generada desde OpenAPI: 92 operaciones de dominio/seguridad rechazan acceso anónimo; consulta rechaza toda escritura y toda seguridad; lecturas de investigación autorizadas. OpenAPI declara Bearer en todas esas operaciones para Swagger Authorize.
- CRUD administrativo, unicidad, FK activas, no reactivación, PUT obligatorio/PATCH parcial, password revoca tokens y DELETE conserva filas inactivas. Bajas de cuenta, rol o asignación del último administrador: 409; dos retiros concurrentes dejan un administrador efectivo. Nombres de roles iniciales inmutables.
- PUT/PATCH de asignaciones: baja/alta atómica, par idéntico sin mutación, origen retirado 404, null/PUT incompleto 422, PATCH vacío 409, destino activo/retirado 409 y rollback conservando origen; cambio que pierde último administrador rechazado. Edición desde Flask incluida en recorrido real.
- Regresión HTTP con administrador de las diez entidades/relaciones de humo_v2, comprobando PUT/PATCH, FK inválidas sin cambios, dependientes y borrado lógico; también creación/cambio/retiro de área de conocimiento v1. No se ejecutó humo_v2.py sin adaptar contra la base compartida.
- Cliente Flask: login con CSRF, rotación, HttpOnly/SameSite, cookie sin JWT, token solo en servidor, menús/URL directas, todos los formularios GET sin argumentos renderizados, 400 sin CSRF, 401/403, vencimiento local, caída y 500 de sesión. Estas cinco pruebas simulan HTTP.
- Integración sin mocks: login consulta y admin, catálogo real, ausencia de acciones de consulta, URL denegada, renderizado de listados y formularios de alta sin parámetros, creación de usuario/rol/asignación desde Flask, usuario creado puede autenticarse, aviso de último administrador y logout que invalida el token en API.

Se corrigieron fallos encontrados durante las ejecuciones: lector de pruebas que
intentaba parsear JSON de un 204, semillas de regresión sin campos obligatorios o
con código demasiado largo, manejo de 500/JSON inesperado de sesión y ausencia de
Bearer en OpenAPI. Las suites finales anteriores se ejecutaron después de corregirlos.
Una auditoría adicional de solo lectura no detectó otros fallos críticos.

## Pendientes reales

Recorrido humano del prompt oculto y navegador (incluido vencimiento/botón atrás),
revisión/aportes del equipo, enmiendas formales, firmas y aceptación. V2 sigue abierta.
No hay registro público, recuperación por correo, refresh, restitución de asignaciones
ni funciones v4. No se incorporó limitación de intentos; compose solo publica en loopback.
Las pruebas automáticas no certifican un despliegue público ni aceptación humana.
Comandos de arranque y actualización: [7_quickstart.md](7_quickstart.md).

## Comprobaciones finales del entorno

El arranque final `docker compose -p investigacion-v3 --env-file v3-local.env -f
docker-compose.v3.yml up -d --build` volvió a terminar con código 0: migración
previa completada, API en 127.0.0.1:8026, Flask en 127.0.0.1:8079 y PostgreSQL
sin puerto publicado. Se comprobó la ausencia de valores de JWT_SECRET,
V3_DB_PASSWORD y CLAVE_SESION locales en los archivos publicables, sin mostrarlos.

Tras el arranque se consultó GET / de la API: version=v3; GET /login de Flask:
200; GET /api/usuario sin credencial: 401. Inspección por importlib.util en la
imagen del front confirmó ausencia de asyncpg, sqlalchemy y fastapi. No se usó
navegador ni se declara aceptación humana. git diff --check pasó; se corrigió
un espacio final en una prueba antes de crear los commits.

---

# Registro histórico — 5 de noviembre de 2026

Lo siguiente describe exclusivamente el estado previo, superado por la implementación
y evidencia del 9 de noviembre documentadas arriba.

# Verificación ejecutada — backend parcial v3

Fecha: 5 de noviembre de 2026. No es cierre de v2/v3 ni revisión manual.

## Aislamiento y migración

Se inspeccionaron information_schema.columns y pg_constraint en la base local
compartida investigacion_local, antes de cambiar archivos: esquema original,
cero filas en usuario, rol y rol_usuario. No se consultaron passwords.

Se creó docker-compose.v3.yml: proyecto investigacion-v3, servicio postgres-v3,
volumen investigacion-v3_pgdata-v3 y red separados. API parcial vinculada solo
a 127.0.0.1:8026. Configuración real en v3-local.env ignorado; sin imprimirla.

En prueba_migraciones_v3_20261105 (servidor aislado) se cargó init.sql y una
cuenta/rol ficticios inactivos, con una asignación. Se ejecutó la migración,
se puso version_sesion=7 y asignación inactiva, y se repitió. Un DO verificó
preservación de valores previos, versión y asignación retirada. Finalmente se
quitó NOT NULL de rol_usuario.activo solo allí: la migración rechazó ese esquema
con salida no cero. Se conserva la incompatibilidad de prueba.

La migración también se aplicó con éxito a investigacion_v3 del servidor
separado, lista para que el usuario ejecute su bootstrap interactivo. No se creó
allí ninguna cuenta real mediante contraseña predeterminada.

Comandos reproducibles de carga y bootstrap: 7_quickstart.md. Su aplicación a
la base compartida está expresamente fuera de esta entrega.

## Pruebas automáticas ejecutadas

Después de construir la imagen api-v3 con requirements.txt, se ejecutó:

```powershell
$v3 = @('-p','investigacion-v3','--env-file','v3-local.env','-f','docker-compose.v3.yml')
docker compose @v3 run --rm -T -e PRUEBAS_V3=1 api-v3 python pruebas/prueba_autenticacion_v3.py
```

La versión final de la suite pasó **14 pruebas**, en 6.586 segundos. Base nueva:
pruebas_v3_9fbaa2fcdb96462ca911a1f8bc852864. Una ejecución anterior con 11
casos también pasó; se amplió para incluir concurrencia y configuración externa.
Los JWT, hashes y contraseñas se mantuvieron solo en memoria y no se imprimieron.

Cobertura real:

- Bootstrap del servicio contra base nueva: primera cuenta/roles/asignación
  confirmados y segundo intento rechazado sin alterar el número de cuentas.
- Login correcto, contraseña incorrecta y cuenta inexistente (incluido texto de
  inyección SQL): los dos fallos respondieron 401 con el mismo sobre público.
- Usuario activo frente a inactivo/NULL, sin Bearer, token alterado/malformado,
  firma con otra clave, algoritmo no permitido, vencimiento y claims ausentes o
  inválidos: rechazados con 401. SecretStr/errores 422 no copiaron valores sensibles.
- Sesión pública sin password/hash/versión interna; TTL y no-store comprobados.
- Login real con administrador y consulta activos: devolvió ambos roles. GET
  /api/usuario devolvió 404 (CRUD aún inexistente) y la colección de áreas devolvió
  200 sin Bearer: se verifica y explicita que no hay protección global todavía.
- Sin rol efectivo y con credenciales vigentes: 403; roles/asignaciones inactivos
  excluidos. Se comprobó el caso de rol retirado después de emitir un JWT.
- Función interna de permisos: consulta solo lectura, administrador escritura y
  seguridad. Esto NO prueba protección HTTP de recursos aún sin middleware.
- Logout global: dos tokens previos rechazados, incluso después de terminar y
  arrancar de nuevo uvicorn. Nuevo login sí funciona con la versión actual.
- Dos logouts simultáneos: estados 200/401 y solo un incremento de versión.
- Arranque sin JWT_SECRET rechazado; comando sin terminal interactiva rechazado.

Se ejecutaron además:

```powershell
docker compose @v3 run --rm -T api-v3 python pruebas/prueba_capas.py
docker compose @v3 run --rm -T api-v3 python pruebas/prueba_v2.py
```

Pasó el recorrido de capas en memoria v1 y pasaron las 12 pruebas en memoria
v2. No se ejecutó humo_v2.py sobre la base compartida ni se repitió la revisión
manual del navegador. No se afirma regresión integrada completa.

## Comprobación de la base compartida

Consulta posterior de solo lectura en investigacion_local: cero coincidencias
para usuario.version_sesion y rol_usuario.activo en information_schema.columns;
usuario=0, rol=0 y rol_usuario=0. La migración y cuentas de pruebas permanecen
exclusivamente en PostgreSQL v3 aislado. No se borraron bases o volúmenes.

## Limitaciones y pendientes

Falta probar manualmente la entrada oculta del bootstrap. El test usa el
servicio y verifica que el comando rechaza entrada sin terminal; no certifica
un recorrido humano del prompt. No se implementaron ni probaron pantallas Flask,
CRUD administrativo ni middleware global de autorización. Las rutas de dominio
existentes siguen públicas. No hay límites de intentos de login ni recuperación
automática. Restituir asignaciones retiradas está fuera de esta primera entrega.

Siguen pendientes los aportes/revisión del equipo, enmiendas formales, firmas,
pruebas manuales restantes de v2 y aceptación integral de v3. No hubo push, merge
ni tags. La evidencia automática no sustituye estas actividades.

Comprobación final del servicio aislado, tras reiniciarlo con el código final:
GET http://localhost:8026/openapi.json respondió 200 y version=v3-parcial.
El diagnóstico existente http://localhost:8025/ siguió respondiendo version=v2.
Se revisaron enlaces locales de Markdown y git diff --check sin errores. Se
comprobó que los valores secretos del archivo local no estaban en los archivos
preparados para commit, sin imprimirlos. Git tenía identidad configurada.