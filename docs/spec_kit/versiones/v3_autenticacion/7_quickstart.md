# Probar el backend parcial v3 sin afectar v2

Solo Docker y PowerShell. Desde la raíz, en v3-desarrollo. Este compose usa
otra red, otro PostgreSQL, otro volumen y API en 127.0.0.1:8026. No ejecutar
la migración sobre investigacion_local. V2 conserva su compose, puertos y datos.

## Generar configuración externa una sola vez

El archivo v3-local.env está ignorado por *.env; .env.example solo documenta
nombres. El siguiente comando escribe secretos aleatorios directamente al
archivo, sin mostrarlos. No lo repita para una instalación ya inicializada:
rotar la contraseña de PostgreSQL requiere un procedimiento distinto.

```powershell
if (Test-Path v3-local.env) { throw 'Ya existe configuración; no sobrescribir' }
docker run --rm python:3.12-slim python -c "import secrets; print('V3_DB_PASSWORD='+secrets.token_hex(32)+'\nJWT_SECRET='+secrets.token_urlsafe(48)+'\nJWT_MINUTOS=30')" | Set-Content -Encoding ascii v3-local.env
if ($LASTEXITCODE -ne 0) { throw 'Falló la generación de configuración' }
git check-ignore v3-local.env
```

No adjuntar ni registrar el contenido. Mantener el archivo accesible solo al
responsable local; no ejecutar docker compose config ni imprimir variables en
informes. JWT_SECRET debe ser externo, aleatorio y de al menos 32 bytes; sin él
main_v3 no arranca. JWT_ISSUER=investigacion-v3 y JWT_AUDIENCE=investigacion-api
son identificadores no secretos definidos en el compose. JWT_MINUTOS=30 admite
1–1440; sin refresh ni renovación automática. Fuera de Docker, configurar también
DB_POSTGRES como URL SQLAlchemy asyncpg y los identificadores anteriores.

## Arranque y migración aislada

```powershell
$v3 = @('-p','investigacion-v3','--env-file','v3-local.env','-f','docker-compose.v3.yml')
docker compose @v3 up -d postgres-v3
docker compose @v3 exec -T postgres-v3 pg_isready -U investigacion_v3 -d investigacion_v3
```

Esperar disponibilidad y luego ejecutar:

```powershell
docker compose @v3 exec -T postgres-v3 psql -X -v ON_ERROR_STOP=1 -U investigacion_v3 -d investigacion_v3 -f /migraciones/v3_001_sesiones_asignaciones.sql
if ($LASTEXITCODE -ne 0) { throw 'Migración rechazada; conservar datos y revisar causa' }
docker compose @v3 up -d --build api-v3
```

init.sql solo se aplica automáticamente sobre el volumen NUEVO de postgres-v3.
No volver a ejecutarlo sobre una base existente. No usar down -v para reiniciar
pruebas. Las migraciones son explícitas; no corren al arrancar la API.

## Primer administrador

En terminal interactiva con TTY, sin -T ni redirección de contraseña:

```powershell
docker compose @v3 exec api-v3 python -m comandos.crear_administrador
```

Solicita nombre, correo y contraseña dos veces con entrada oculta (12–1024
caracteres). Rechaza ejecución sin terminal; no admite clave por argumento ni
credenciales predeterminadas. Crea los dos roles y solo la cuenta administrativa
en una transacción. Cualquier cuenta existente o rol inicial ya ocupado causa
rechazo, sin sobrescribir/reactivar. No es herramienta de recuperación.
Si falla, informa un mensaje sin exponer SQL, hash ni contraseña.

## Pruebas automáticas reproducibles

```powershell
docker compose @v3 run --rm -T -e PRUEBAS_V3=1 api-v3 python pruebas/prueba_autenticacion_v3.py
docker compose @v3 run --rm -T api-v3 python pruebas/prueba_capas.py
docker compose @v3 run --rm -T api-v3 python pruebas/prueba_v2.py
```

La suite v3 exige host postgres-v3, base de entrada investigacion_v3 y bandera
PRUEBAS_V3=1. Crea una base nueva con sufijo aleatorio, aplica init y la migración
repetida, genera credenciales efímeras y levanta su propio uvicorn interno en
8031. Reinicia ese proceso para comprobar revocación persistente. No necesita
usar ni modificar el primer administrador de la base principal aislada. Conserva
la base de pruebas para inspección y no imprime claves, hashes o tokens completos.
No es una prueba de las pantallas Flask.

## Probar los contratos sin imprimir credenciales

Abrir http://localhost:8026/docs para consultar los esquemas. No compartir
capturas de la respuesta de login. Para usar PowerShell conservando el JWT solo
en memoria (el prompt de contraseña está oculto):

```powershell
$cuenta = Get-Credential -Message 'Cuenta creada en PostgreSQL v3 aislado'
$cuerpo = @{ username=$cuenta.UserName; password=$cuenta.GetNetworkCredential().Password } | ConvertTo-Json
$sesion = Invoke-RestMethod -Method Post -Uri http://localhost:8026/api/login -ContentType application/json -Body $cuerpo
Remove-Variable cuerpo
$cabecera = @{ Authorization='Bearer '+$sesion.access_token }
Invoke-RestMethod -Uri http://localhost:8026/api/sesion -Headers $cabecera | Select-Object username,roles
Invoke-RestMethod -Method Post -Uri http://localhost:8026/api/logout -Headers $cabecera | Select-Object estado,mensaje
# La siguiente llamada debe responder 401: el JWT anterior ya no es válido.
Invoke-RestMethod -Uri http://localhost:8026/api/sesion -Headers $cabecera
Remove-Variable sesion,cabecera,cuenta
```

No copiar el objeto $sesion ni las cabeceras a logs/informes. Los ejemplos
interactivos están documentados para el usuario; no se afirma haberlos ejecutado
manualmente. Véase VERIFICACION_V3.md para los comandos realmente ejecutados.

**Límite:** solo login/sesion/logout incorporan seguridad en esta entrega.
Las rutas existentes siguen públicas; faltan middleware global, CRUD
administrativo, pantallas, aceptación del equipo y pruebas manuales. V2 sigue abierta.
