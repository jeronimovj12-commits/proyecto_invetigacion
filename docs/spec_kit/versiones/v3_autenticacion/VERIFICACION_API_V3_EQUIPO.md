# Verificación de seguridad de la API v3 — equipo

Fecha: 11 de noviembre de 2026. Versión probada: `origin/v3-desarrollo` en
`367f8b3` (`docs(v3): registrar verificacion API del equipo`). La identidad
local de Git se verificó antes del trabajo. La rama solicitada
`pruebas-seguridad-v3` y el PR #4 ya existían; el head del PR estaba basado en
una revisión anterior y GitHub lo reportaba no mergeable. Se volvió a basar la
rama de trabajo en `origin/v3-desarrollo`; el PR existente se actualizará.

## Alcance

Se amplió `api_investigacion/pruebas/prueba_permisos_v3_equipo.py` sin modificar
código de producción, controladores ni servicios. La suite usa la clase HTTP de
autenticación existente, una base PostgreSQL aleatoria para casos de integración
y un repositorio falso para comprobar reglas de sesión del servicio.

La cobertura añadida comprueba:

- Sesión y recursos protegidos sin token; token alterado, vencido y revocado.
- Matriz de OpenAPI: consulta puede leer las rutas de dominio y recibe 403 al
  escribir o administrar usuarios, roles y asignaciones; el administrador no
  recibe 401/403 en las operaciones declaradas.
- CRUD permitido de usuario, rol y asignación con administrador.
- Usuario inactivo (401), y rol o asignación inactivos (403).
- Conteos y valores antes/después de intentos denegados, para demostrar que no
  se modifican usuario, rol, asignación ni área de conocimiento.
- Login, lectura de sesión y revocación de versión con repositorio falso.

## Aislamiento y comandos

Se revisaron `docker-compose.v3.yml`, `docker-compose.v3.pruebas.yml`,
`scripts/verificar_v3.ps1` y `7_quickstart.md`. `prueba_autenticacion_v3.py`
requiere `PRUEBAS_V3=1`, host `postgres-v3` y base inicial `investigacion_v3`,
y crea después una base con nombre aleatorio. Las pruebas no apuntaron a
`investigacion_local` ni al volumen v2.

Se usó el proyecto Docker exclusivo
`investigacion-v3-seguridad-final-20261111`, con volumen
`investigacion-v3-seguridad-final-20261111_pgdata-v3`. La composición de prueba
no publica puertos. `V3_DB_PASSWORD` se tomó de `v3-local.env`; `JWT_SECRET` y
`CLAVE_SESION` se generaron efímeros en el proceso. No se registraron secretos.
Los contenedores se detuvieron al terminar; los volúmenes y bases aleatorias se
conservaron.

Comandos ejecutados desde la raíz en PowerShell (las variables secretas se
prepararon en el proceso y no se imprimieron):

```powershell
$bytes = New-Object byte[] 48
$rng = [Security.Cryptography.RandomNumberGenerator]::Create()
try { $rng.GetBytes($bytes) } finally { $rng.Dispose() }
$valor = -join ($bytes | ForEach-Object { $_.ToString('x2') })
$env:JWT_SECRET = $valor
$env:CLAVE_SESION = $valor
$compose = @('-p','investigacion-v3-seguridad-final-20261111','--env-file','./v3-local.env','-f','docker-compose.v3.yml','-f','docker-compose.v3.pruebas.yml')
docker compose @compose build --quiet api-v3
docker compose @compose run --rm -T migrar-v3
docker compose @compose run --rm -T -e PRUEBAS_V3=1 api-v3 python pruebas/prueba_autenticacion_v3.py
docker compose @compose run --rm -T -e PRUEBAS_V3=1 api-v3 python pruebas/prueba_administracion_v3.py
docker compose @compose run --rm -T -e PRUEBAS_V3=1 api-v3 python pruebas/prueba_permisos_v3_equipo.py
```

## Resultados reales

Las tres suites terminaron con código 0:

| Suite | Resultado | Base aislada |
|---|---|---|
| `prueba_autenticacion_v3.py` | 14 pruebas OK, 7.686 s. Migración repetida y bootstrap/conflicto OK. | `pruebas_v3_c446543e91e54aeda82e064063fde137` |
| `prueba_administracion_v3.py` | 5 pruebas OK, 3.491 s; matriz de 92 operaciones. | `pruebas_v3_e237d76c078f4363b1b909d9fc19d954` |
| `prueba_permisos_v3_equipo.py` | 7 pruebas OK, 2.968 s; matriz de 92 operaciones. | `pruebas_v3_76911f788be442ddbdb08c23d6854f43` |

En el primer intento sobre el volumen nuevo, Compose inició `migrar-v3` mientras
PostgreSQL reiniciaba el servidor temporal de `initdb`; `psql` recibió
`Connection refused` y esa ejecución no llegó a las pruebas. Se reintentó la
migración una vez PostgreSQL estuvo listo; terminó con `COMMIT`. Las tres suites
se ejecutaron después y pasaron. Esto se registra como una intermitencia de
arranque del entorno Docker; no se cambió Compose ni producción.

No se encontraron fallos de permisos en estas ejecuciones. La matriz usa las
92 operaciones de OpenAPI presentes en la versión `367f8b3`. Esto no acredita
pruebas manuales ni aceptación de otros integrantes.

## Preparación de la entrega

Los cambios reales se dividirán en commits de prueba y documentación. El archivo
local ajeno `er.name` se conserva intacto y fuera de Git. No se hará merge ni se
crearán etiquetas.
