# Verificación de seguridad de la API v3 — equipo

Fecha: 11 de noviembre de 2026. Versión de implementación probada:
`v3-desarrollo` en `ec7dcf5`; no se modificó producción. Se verificaron
la identidad local de Git y el estado del repositorio antes del trabajo. Los
siete commits anteriores y cinco commits nuevos de esta ampliación se incorporan
directamente en `v3-desarrollo`. El commit base de implementación comprobado fue
`ec7dcf5`; los commits nuevos amplían únicamente pruebas y este informe.
El PR #4 preexistente permanece abierto y no se fusionó.

## Alcance

Se amplió `api_investigacion/pruebas/prueba_permisos_v3_equipo.py` con la base
HTTP compartida de las pruebas existentes, una base PostgreSQL aleatoria para
integración y un repositorio falso para reglas del servicio.

La suite verifica:

- Token ausente, alterado, vencido o revocado; los tokens en URL o cookie no
  autentican. Los esquemas Authorization inválidos se rechazan y el esquema
  Bearer acepta diferencias de mayúsculas.
- La consulta lee rutas de dominio y recibe 403 al escribir o administrar
  usuarios, roles y asignaciones. El administrador ejecuta CRUD permitido.
- HEAD y OPTIONS no evaden los permisos de seguridad.
- Usuario inactivo devuelve 401; rol o asignación inactivos devuelven 403.
  Retirar una asignación con administrador deniega de inmediato el token de
  consulta ya emitido. También se rechaza una asignación de administrador
  inactiva, un rol administrador inactivo y cambios de permisos reflejados en
  tokens ya emitidos.
- La ruta `/api/usuario/` con barra final no omite la autorización.
- Los rechazos conservan los datos y la versión de sesión; las respuestas 401
  y 403 usan `Cache-Control: no-store`.
- Matriz de las 92 operaciones de OpenAPI y reglas de login, sesión y logout
  con repositorio falso.

## Aislamiento y comandos

Se revisaron `docker-compose.v3.yml`, `docker-compose.v3.pruebas.yml`,
`scripts/verificar_v3.ps1` y `7_quickstart.md`. La suite de autenticación exige
`PRUEBAS_V3=1`, el host `postgres-v3` y la base inicial `investigacion_v3`; crea
una base aleatoria por ejecución. Las pruebas no utilizaron `investigacion_local`
ni volúmenes compartidos de v2.

Se usó el proyecto Docker exclusivo
`investigacion-v3-seguridad-final-20261111`, con volumen
`investigacion-v3-seguridad-final-20261111_pgdata-v3`. El compose de pruebas no
publica puertos. `V3_DB_PASSWORD` provino de `v3-local.env`; `JWT_SECRET` y
`CLAVE_SESION` se generaron efímeros en el proceso, sin imprimirlos ni guardarlos
en el repositorio. Los contenedores quedaron detenidos y el volumen aislado se
conservó.

Comandos ejecutados desde la raíz en PowerShell:

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

Las suites terminaron con código 0 contra el PostgreSQL aislado:

| Suite | Resultado | Base aislada |
|---|---|---|
| `prueba_autenticacion_v3.py` | 14 pruebas OK, 22.322 s. Migración repetida y bootstrap/conflicto OK. | `pruebas_v3_6532b264e3e64ff982f232cf0d5d40c2` |
| `prueba_administracion_v3.py` | 5 pruebas OK, 10.243 s; matriz de 92 operaciones. | `pruebas_v3_b786e58c43fc44138fd4248edd226f57` |
| `prueba_permisos_v3_equipo.py` | 16 pruebas OK, 15.856 s; matriz de 92 operaciones. | `pruebas_v3_490f050afe7c48ee80dd1975fea51253` |

En la primera ejecución de la suite de permisos ampliada, 15 pruebas pasaron y
una terminó con `NameError` porque el bloque de una prueba había quedado bajo el
método de ruta con barra final. Se corrigió la ubicación del bloque y se repitió
la suite completa; las 16 pruebas pasaron. No se oculta el primer resultado.

En esta ejecución la migración repetida terminó con `COMMIT`. En una ejecución
anterior sobre un volumen recién creado, PostgreSQL reinició el servidor
temporal de `initdb` después de que Compose lo reportó saludable; `psql` recibió
`Connection refused`. Esa invocación no llegó a ejecutar pruebas. Reintentar la
migración cuando PostgreSQL terminó de inicializar funcionó y las suites
pasaron. La incidencia fue de arranque del entorno aislado; no se cambió Compose
ni producción.

No se encontraron fallos de permisos en la ejecución corregida. La evidencia
cubre la implementación v3 publicada en `ec7dcf5` y la suite ampliada en esta
rama. No acredita pruebas manuales ni aceptación de otros integrantes.

## Cambios directos en v3

Los cinco commits nuevos son:

1. `test(v3): rechazar asignacion admin inactiva`
2. `test(v3): denegar admin con rol inactivo`
3. `test(v3): aplicar cambios de rol a sesiones activas`
4. `test(v3): proteger rutas con barra final`
5. `docs(v3): registrar pruebas de permisos ampliadas`

`er.name` se conserva intacto y fuera de Git. No se hizo merge ni se crearon
etiquetas.
