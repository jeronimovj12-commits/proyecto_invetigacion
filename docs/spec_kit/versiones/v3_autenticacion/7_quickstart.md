# Arrancar y verificar v3 sin cerrar v2

Desde la raíz del repositorio, con Git, Docker Desktop iniciado en modo contenedores
Linux y PowerShell. La primera construcción necesita acceso a las imágenes y paquetes.
No hace falta instalar Python ni PostgreSQL en el equipo para seguir este recorrido.

| Elemento | Nombre/dirección real |
|---|---|
| Proyecto Compose | investigacion-v3 |
| Servicios | postgres-v3, migrar-v3, api-v3, front-v3 |
| Front | http://localhost:8079/login |
| API/documentación | http://localhost:8026/ y http://localhost:8026/docs |
| Base v3 | investigacion_v3, usuario de conexión investigacion_v3; sin puerto publicado al equipo |
| Volúmenes | pgdata-v3 y sesiones-v3, separados de v2 por el proyecto Compose |

`main_v3:app` y `app_v3.py` son las entradas de v3. El compose predeterminado sigue
arrancando v2 en 8025/8078 y conserva sus datos. No cambiar sus volúmenes para probar v3.

## Qué está verificado y qué son instrucciones por ejecutar

| Procedimiento | Evidencia/estado |
|---|---|
| Configuración externa, build/arranque v3, diagnóstico, migración previa y dependencias fijadas | Ejecución registrada del 9 de noviembre en [VERIFICACION_V3.md](VERIFICACION_V3.md) |
| Migración aislada nueva/con filas anteriores, repetición e incompatibilidad; 37 casos y recorrido de capas | Ejecuciones registradas; no se repitieron durante esta actualización documental |
| Bootstrap del servicio y rechazo del comando sin terminal | Verificados automáticamente; recorrido humano de entrada oculta pendiente |
| Clon limpio completo de un compañero | Instrucción preparada; sin ejecución completa acreditada |
| Respaldo, restauración integral y secuencia de actualización de una instalación existente | Pasos revisados contra Compose y herramientas; no ejecutados como ensayo integral |
| Cargas opcionales oficiales/demo en el volumen principal v3 | Comandos adaptados abajo; no ejecutados aquí. Sus SQL tienen pruebas históricas en v2, que no prueban una carga en v3 |

Esta actualización modifica documentación. No crea cuentas, carga datos ni certifica
pruebas manuales. Mantener las instrucciones pendientes diferenciadas de los resultados.

## 1. Obtener el código y preparar configuración

Si todavía no hay clon:

```powershell
git clone --branch v3-desarrollo https://github.com/jeronimovj12-commits/proyecto_invetigacion.git
cd proyecto_invetigacion
```

En un clon existente, revisar primero `git status --short --branch`. Conservar trabajo
local; no usar reset/clean. Solo si el estado permite actualizar sin mezclar cambios:

```powershell
git fetch origin
git switch v3-desarrollo
git pull --ff-only origin v3-desarrollo
git log -1 --oneline
```

`fetch` actualiza referencias; `switch` selecciona la rama; `pull --ff-only` se detiene
si existe divergencia. `git log` identifica la versión que se va a mostrar. Anotar
ese commit junto con cualquier verificación posterior.

Preparar argumentos y secretos externos, tanto para una instalación nueva como existente:

```powershell
docker version
if ($LASTEXITCODE -ne 0) { throw 'Iniciar Docker Desktop antes de continuar' }
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/configurar_v3.ps1
if ($LASTEXITCODE -ne 0) { throw 'Falló la configuración local' }
git check-ignore v3-local.env
$v3 = @('-p','investigacion-v3','--env-file','v3-local.env','-f','docker-compose.v3.yml')
```

El script genera solo V3_DB_PASSWORD, JWT_SECRET y CLAVE_SESION faltantes mediante el
generador aleatorio del sistema y conserva valores existentes. `v3-local.env` queda
ignorado; [.env.example](../../../../.env.example) solo tiene marcadores. No mostrar
ese archivo ni ejecutar comandos que vuelquen secretos en informes. ExecutionPolicy
se limita a ese proceso, sin modificar la política permanente del equipo.

Si el archivo existente está incompleto o tiene valores inválidos, revisar su
configuración sin publicarla; el script no reemplaza valores por estar vacíos o ser
incorrectos. No regenerar la contraseña PostgreSQL de un volumen ya inicializado.
Los identificadores JWT_ISSUER/AUDIENCE vienen del compose. JWT_MINUTOS=30 admite
1–1440; sin refresh ni renovación. COOKIE_SECURE=0 corresponde a HTTP local;
con HTTPS debe usarse 1, fuera de este recorrido local.

**Elegir ahora una de las dos secciones siguientes.** No ejecutar el arranque de una
instalación nueva antes del respaldo de una existente: `up` puede aplicar migraciones.

## 2. Instalación nueva: base vacía y primer administrador

```powershell
docker compose @v3 up -d --build
if ($LASTEXITCODE -ne 0) { throw 'Falló el arranque: revisar servicios y migración' }
docker compose @v3 ps -a
```

`-p` separa el proyecto, `--env-file` carga configuración y `-f` elige v3.
`--build` construye con los `requirements-v3.lock`; `-d` deja los servicios en segundo
plano. El volumen PostgreSQL vacío recibe [init.sql](../../../../db/init.sql) una vez.
`migrar-v3` ejecuta SQL idempotente y debe terminar con código 0 antes de iniciar API;
no es un servidor que deba permanecer ejecutándose. `ps -a` permite ver ese servicio
terminado junto con los tres servicios en ejecución. El front no depende de PostgreSQL
ni API y puede mostrar un aviso mientras el servicio no esté listo.

No se crean cuentas predeterminadas. En terminal interactiva, sin `-T` ni contraseña
en argumentos o tuberías:

```powershell
docker compose @v3 exec api-v3 python -m comandos.crear_administrador
if ($LASTEXITCODE -ne 0) { throw 'No se creó el primer administrador; revisar el mensaje' }
```

Pide nombre, correo y contraseña dos veces con entrada oculta (12–1024 caracteres).
Crea los roles administrador/consulta y primera cuenta/asignación en una transacción.
Si hay cuentas o roles iniciales ocupados, rechaza sin sobrescribir/reactivar. No es
herramienta de recuperación. El prompt humano aún debe verificarse; la prueba automática
acredita el servicio y el rechazo de ejecución sin terminal.

Abrir http://localhost:8079/login y entrar con la cuenta creada. El administrador
crea usuarios, roles y asignaciones desde el menú. Consulta solo lee investigación;
una cuenta sin rol efectivo no puede entrar. Para demostrar relaciones con opciones,
preparar también los datos de la sección 4. No compartir respuestas de login ni capturas
de credenciales.

## 3. Instalación v3 existente: respaldo antes de migrar

Conservar archivo de entorno y volúmenes. Si ya hay administrador, utilizar esa cuenta;
no repetir bootstrap como recuperación. Asegurar PostgreSQL, detener API/front para
impedir escrituras de la aplicación y tomar respaldo antes de ejecutar `migrar-v3`.
Coordinar también cualquier otro cliente que pueda escribir directamente en la base.

**Esta secuencia de respaldo/actualización es una instrucción revisada, aún sin ensayo
integral registrado. La restauración del respaldo debe probarse en una copia separada.**

```powershell
docker compose @v3 up -d postgres-v3
if ($LASTEXITCODE -ne 0) { throw 'No arrancó PostgreSQL' }
docker compose @v3 stop api-v3 front-v3
if ($LASTEXITCODE -ne 0) { throw 'No se detuvieron los servicios; no continuar' }
docker compose @v3 exec -T postgres-v3 pg_isready -U investigacion_v3 -d investigacion_v3
if ($LASTEXITCODE -ne 0) { throw 'PostgreSQL todavía no está listo' }

New-Item -ItemType Directory -Force respaldos | Out-Null
$marcaV3 = Get-Date -Format 'yyyyMMdd-HHmmss'
$dumpV3 = "/tmp/respaldo-v3-$marcaV3.dump"
docker compose @v3 exec -T postgres-v3 pg_dump -U investigacion_v3 -d investigacion_v3 -Fc -f $dumpV3
if ($LASTEXITCODE -ne 0) { throw 'Falló respaldo; no migrar' }
docker compose @v3 cp "postgres-v3:$dumpV3" "./respaldos/respaldo-v3-$marcaV3.dump"
if ($LASTEXITCODE -ne 0) { throw 'Falló copia del respaldo; no migrar' }

docker compose @v3 run --rm -T migrar-v3
if ($LASTEXITCODE -ne 0) { throw 'Migración rechazada; conservar respaldo y revisar incompatibilidad' }
docker compose @v3 up -d --build
if ($LASTEXITCODE -ne 0) { throw 'Falló el arranque posterior; revisar estado' }
docker compose @v3 ps -a
```

`pg_dump -Fc` produce respaldo en formato de archivo; `cp` lo conserva también fuera
del contenedor. Su nombre incluye fecha/hora para no reutilizar siempre el mismo nombre.
El dump contiene hashes y datos del sistema: `respaldos/` está ignorado, no adjuntarlo.
La migración repetida conserva filas, versiones e inactivos; rechaza incompatibilidades.
No ejecutar init.sql ni `down -v` para actualizar. No existe rollback destructivo automático.
Una instalación antigua con contraseñas sin Argon2id requiere resolución del responsable;
no se sobrescriben cuentas ni se importan claves en texto automáticamente.

Las sesiones del front están en otro volumen. Conservarlas permite reiniciar Flask;
cambiar su clave invalida las cookies. Su JWT sigue sujeto al vencimiento original.

### Si la instalación que existe es v2

No aplicar esta migración a `investigacion_local` compartida: v2 sigue abierta. V3 usa
otra base/volumen. Una copia compatible podría migrarse sin ejecutar init.sql, pero el
equipo debe preparar y probar respaldo/restauración en otra base antes de hacerlo.
No se ejecutó esa conversión sobre los datos compartidos. No confundir los datos cargados
en v2 con datos ya disponibles en v3.

## 4. Preparar datos oficiales y demo para la sustentación

Esta sección es **voluntaria**: no crea usuarios ni cambia permisos. `init.sql` ya
incluye 218 áreas, 17 ODS y 21 áreas de aplicación, pero no universidades/líneas.
No basta arrancar v3 para tener todos los padres de los desplegables.

| Archivo existente | Qué contiene |
|---|---|
| [universidades_oficiales_v2.sql](../../../../db/opcionales/universidades_oficiales_v2.sql) | Seis universidades completas de la fuente Excel, con claves 1–6 |
| [demo_v2.sql](../../../../db/opcionales/demo_v2.sql) | Diez filas ficticias: dos por universidad, línea, docente, grupo y semillero, marcadas DEMO V2; no precarga todas las relaciones |
| [carga_segura.sql](../../../../db/opcionales/carga_segura.sql) | Auxiliar temporal que los dos archivos incluyen mediante `\ir`; debe estar en la misma carpeta |

Las cargas fueron ensayadas en PostgreSQL v2 según [VERIFICACION_V2.md](../../../../VERIFICACION_V2.md).
Los comandos adaptados siguientes **no se ejecutaron en esta actualización ni prueban
que el volumen principal v3 ya tenga esos datos**. En una instalación existente, respaldar
antes según la sección 3. Mantener API/front detenidos durante la carga y coordinar otros
clientes; ante un conflicto, detenerse sin borrar, sobreescribir ni reactivar registros.

Preparar los archivos en PostgreSQL y cargar solo las universidades oficiales:

```powershell
docker compose @v3 stop api-v3 front-v3
if ($LASTEXITCODE -ne 0) { throw 'No se detuvieron los servicios' }
docker compose @v3 exec -T postgres-v3 mkdir -p /tmp/v3-opcionales
if ($LASTEXITCODE -ne 0) { throw 'No se preparó la carpeta temporal' }
docker compose @v3 cp ./db/opcionales/. postgres-v3:/tmp/v3-opcionales/
if ($LASTEXITCODE -ne 0) { throw 'Falló la copia de los SQL opcionales' }
docker compose @v3 exec -T postgres-v3 psql -X -v ON_ERROR_STOP=1 -U investigacion_v3 -d investigacion_v3 -f /tmp/v3-opcionales/universidades_oficiales_v2.sql
if ($LASTEXITCODE -ne 0) { throw 'Carga oficial rechazada; revisar conflicto sin forzar datos' }
```

Si además se decide utilizar datos ficticios para practicar las relaciones:

```powershell
docker compose @v3 exec -T postgres-v3 psql -X -v ON_ERROR_STOP=1 -U investigacion_v3 -d investigacion_v3 -f /tmp/v3-opcionales/demo_v2.sql
if ($LASTEXITCODE -ne 0) { throw 'Carga demo rechazada; revisar catálogos/conflictos sin forzar' }
```

`psql -X` evita configuración personal; ON_ERROR_STOP detiene el script ante error.
Cada carga se ejecuta en transacción: acepta una fila ya idéntica y activa, o inserta
la faltante. Datos distintos, filas retiradas o catálogos base sin opciones provocan
rechazo. Repetir después de editar/retirar DEMO puede producir conflicto: no restaura
ni reactiva esas fichas. Las claves explícitas no reinician secuencias.

Para comprobar y reanudar tras la carga elegida:

```powershell
docker compose @v3 exec -T postgres-v3 psql -X -v ON_ERROR_STOP=1 -U investigacion_v3 -d investigacion_v3 -c "SELECT 'universidad' AS tabla, count(*) AS activas FROM universidad WHERE activo IS TRUE UNION ALL SELECT 'linea_investigacion', count(*) FROM linea_investigacion WHERE activo IS TRUE;"
if ($LASTEXITCODE -ne 0) { throw 'Falló la comprobación de datos' }
docker compose @v3 up -d api-v3 front-v3
if ($LASTEXITCODE -ne 0) { throw 'No se reanudaron los servicios' }
```

En una base nueva, solo oficiales aportan seis universidades y ninguna línea; añadir
demo aporta dos universidades y dos líneas ficticias, además de sus otros padres.
En una base existente puede haber más filas; comprobar identidad/estado sin asumir
un total fijo. Después iniciar sesión y recorrer dependencias: docente/grupo → semillero
→ participaciones y relaciones con líneas/catálogos. El orden detallado está en el
[quickstart v2](../v2_claves_foraneas/7_quickstart.md); usar aquí puertos y permisos v3.
Un SELECT de conteos no demuestra por sí solo todos los formularios ni su edición.

## 5. Comprobar servicios y ejecutar las pruebas disponibles

Estas comprobaciones públicas no muestran credenciales:

```powershell
docker compose @v3 ps -a
(Invoke-RestMethod http://localhost:8026/).version
(Invoke-WebRequest -UseBasicParsing http://localhost:8079/login).StatusCode
```

Se espera diagnóstico `v3` y login 200. Si el proceso aún está arrancando, esperar
brevemente y repetir la lectura; si falla, revisar `docker compose @v3 logs --tail 50 api-v3`
y el estado de migrar-v3 sin divulgar configuración sensible. Esto verifica disponibilidad,
no un login correcto ni aceptación de pantalla.

Para ejecutar la suite registrada en la versión que se tenga actualmente:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verificar_v3.ps1
if ($LASTEXITCODE -ne 0) { throw 'Verificación fallida: revisar salida y no declarar éxito' }
```

[El verificador](../../../../scripts/verificar_v3.ps1) construye con versiones fijadas,
comprueba migración, 14 casos de credenciales/sesiones, 5 de administración/regresión
(matriz de 92 operaciones HTTP), capas v1, 12 casos v2 en memoria, 5 Flask y un recorrido
Flask→HTTP→API→PostgreSQL. Usa bases aleatorias y credenciales efímeras, sin utilizar
ni modificar el primer administrador de la base principal. No imprime claves ni JWT.
Los cinco casos Flask simulan HTTP; el recorrido integrado usa API/BD reales.

La integración añade docker-compose.v3.pruebas.yml y volumen fixture-v3 con cuentas
efímeras en archivo 0600; recrea su API interna sin puerto público y la detiene al
terminar. Conserva bases/volúmenes. No usar unittest discover sin patrón: mocks e
integración requieren entornos distintos. Los comandos individuales están en el script.
No ejecutar humo_v2.py sin adaptar como si ya tuviera Bearer y CSRF de v3.

Anotar commit, entorno, comando y resultado al repetir pruebas. La ejecución previa
se conserva en [VERIFICACION_V3.md](VERIFICACION_V3.md); esta guía no la convierte
en una ejecución nueva ni certifica restauración, carga v3 o navegador.

## 6. Verificación humana pendiente

Recorrer entrada oculta del bootstrap, login con ambos roles, edición/retiro, rechazo
del último administrador, vencimiento, logout y botón atrás. Verificar confirmación
de retiro de áreas frente a la CSP y los datos de todos los desplegables. No se declara
que el usuario o compañeros hayan realizado aquí esas pruebas. V2 sigue abierta;
faltan revisión/aportes, enmiendas y firmas. No hay registro público, recuperación
por correo ni funciones v4.
