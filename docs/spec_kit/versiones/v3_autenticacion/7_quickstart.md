# Arrancar y verificar v3 sin cerrar v2

Desde la raíz del repositorio, con Docker Desktop y PowerShell. API en
http://localhost:8026/docs y front en http://localhost:8079. Puertos de v2
8025/8078 y su base/volúmenes se conservan. No usar main:app o app.py para v3:
el compose elige main_v3:app y app_v3.py.

## Misma versión y configuración

```powershell
git fetch origin
git switch v3-desarrollo
git pull --ff-only origin v3-desarrollo
git log -1 --oneline
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/configurar_v3.ps1
$v3 = @('-p','investigacion-v3','--env-file','v3-local.env','-f','docker-compose.v3.yml')
docker compose @v3 up -d --build
if ($LASTEXITCODE -ne 0) { throw 'Falló el arranque v3' }
```

Conservar cambios locales antes de cambiar de rama; no usar reset/clean.
El script genera solo V3_DB_PASSWORD, JWT_SECRET y CLAVE_SESION faltantes con el
generador aleatorio del sistema. Conserva valores existentes; v3-local.env está
ignorado. No imprimirlo ni adjuntarlo. El parámetro ExecutionPolicy se limita a
ese proceso, sin cambiar la política permanente. .env.example tiene solo marcadores.

Dependencias Python exactas verificadas: requirements-v3.lock de cada proyecto.
El front depende solo de Flask y requests más sus dependencias transitivas.
JWT_MINUTOS predeterminado 30, permitido 1–1440; sin renovación automática.
COOKIE_SECURE=0 solo para este HTTP local en loopback; con HTTPS usar 1.
JWT_ISSUER/AUDIENCE se definen en compose; sin secretos válidos no arranca v3.

## Instalación nueva

El volumen pgdata-v3 vacío recibe init.sql una sola vez. migrar-v3 aplica la
migración y debe terminar con éxito antes de arrancar la API. El front arranca
independientemente de PostgreSQL/API y muestra aviso si el servicio no está listo.
No se crean cuentas predeterminadas. Crear el primer administrador en terminal
interactiva (sin -T ni contraseña en argumentos):

```powershell
docker compose @v3 exec api-v3 python -m comandos.crear_administrador
```

Pide nombre, correo y contraseña dos veces con entrada oculta (12–1024 caracteres).
Crea administrador/consulta y primera cuenta/asignación en una transacción. Si ya
hay cuentas o roles iniciales ocupados, rechaza sin sobrescribir ni reactivar.
Después abrir http://localhost:8079/login. El administrador crea cuentas, roles
y asignaciones desde el menú. Consulta solo ve investigación. Cuenta sin rol no
puede entrar. No publicar capturas de credenciales ni respuestas de login.

## Instalación v3 existente

Conservar v3-local.env y los volúmenes. No regenerar la contraseña PostgreSQL de
un volumen inicializado. El script añade CLAVE_SESION si procede sin tocar lo demás.
Antes de actualizar, respaldar la base (el dump contiene hashes: no versionarlo):

```powershell
New-Item -ItemType Directory -Force respaldos | Out-Null
docker compose @v3 exec -T postgres-v3 pg_dump -U investigacion_v3 -d investigacion_v3 -Fc -f /tmp/respaldo-v3.dump
if ($LASTEXITCODE -ne 0) { throw 'Falló respaldo' }
docker compose @v3 cp postgres-v3:/tmp/respaldo-v3.dump ./respaldos/respaldo-v3.dump
if ($LASTEXITCODE -ne 0) { throw 'Falló copia del respaldo' }
docker compose @v3 stop api-v3
docker compose @v3 run --rm -T migrar-v3
if ($LASTEXITCODE -ne 0) { throw 'Esquema incompatible: conservar respaldo y corregir antes de continuar' }
docker compose @v3 up -d --build
```

La migración repetida conserva filas, versiones e inactivos; rechaza esquema
incompatible. No ejecutar init.sql ni down -v en instalaciones existentes.
Si ya hay cuentas, usar un administrador existente; el bootstrap no recupera acceso.
Un esquema antiguo con cuentas sin hashes Argon2id requiere resolución del responsable;
no se importan contraseñas en texto ni se sobrescriben cuentas automáticamente.
El volumen de sesiones permite reiniciar Flask; una clave de cookie nueva invalida
cookies. El JWT conserva su vencimiento original y cada solicitud valida en API.

## Instalación existente de v2

No ejecutar esta migración contra investigacion_local compartida. V2 sigue abierta.
La evaluación de v3 se hace en el volumen separado. Para copiar datos de investigación,
el equipo debe preparar y revisar un respaldo/restauración en otra base, manteniendo
intacta v2; no se ejecutó una conversión sobre sus datos. Una copia compatible puede
recibir v3_001 sin ejecutar init.sql. Planificar mantenimiento y respaldo antes de
cualquier migración fuera del entorno aislado.

## Verificación automática de la misma versión

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verificar_v3.ps1
if ($LASTEXITCODE -ne 0) { throw 'Verificación fallida' }
```

El script construye con versiones fijadas, verifica migración, 14 pruebas de
credenciales/sesiones, 5 casos de administración (matriz de 92 operaciones HTTP,
CRUD, concurrencia y regresión integrada de dominio), capas v1, 12 pruebas v2, 5 casos Flask y un recorrido real
Flask→HTTP→API→PostgreSQL. Crea bases aleatorias aisladas y credenciales efímeras;
no usa la cuenta real creada con bootstrap. No imprime tokens ni contraseñas.
El transporte de los 5 casos Flask es simulado; el recorrido integrado no usa mocks.

La integración usa docker-compose.v3.pruebas.yml, servidor API interno sin puerto
público y volumen fixture-v3 con credenciales efímeras 0600. El script recrea ese
servidor para obtener una base nueva y lo detiene al terminar; no borra volúmenes
ni bases. No usar unittest discover sin patrón: las suites unitarias e integradas
requieren configuraciones distintas. Los comandos individuales están en scripts/verificar_v3.ps1.

## Verificación humana pendiente

Recorrer bootstrap oculto, login con ambos roles, edición/retiro, rechazo del último
administrador, vencimiento, logout y botón atrás en navegador. No se declara que el
usuario o compañeros hayan realizado estas pruebas. Evidencia automatizada en
VERIFICACION_V3.md. No hay registro público, recuperación por correo ni funciones v4.
