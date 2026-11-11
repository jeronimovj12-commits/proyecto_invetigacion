# Verificación de seguridad de la API v3 — equipo

Fecha: 11 de noviembre de 2026. Versión de implementación probada:
`origin/v3-desarrollo` en `367f8b3`; no se modificó producción. Se verificaron
la identidad local de Git y el estado del repositorio antes del trabajo. Los
siete commits de esta entrega se incorporan directamente en `v3-desarrollo`.
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
  consulta ya emitido.
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

Las tres suites terminaron con código 0 contra el PostgreSQL aislado:

| Suite | Resultado | Base aislada |
|---|---|---|
| `prueba_autenticacion_v3.py` | 14 pruebas OK, 8.269 s. Migración repetida y bootstrap/conflicto OK. | `pruebas_v3_e69e1e5ade9b439698e073dcaf6604ca` |
| `prueba_administracion_v3.py` | 5 pruebas OK, 3.873 s; matriz de 92 operaciones. | `pruebas_v3_cc5013e85ab7487fb9d430b14dec14d2` |
| `prueba_permisos_v3_equipo.py` | 12 pruebas OK, 4.433 s; matriz de 92 operaciones. | `pruebas_v3_7441a34361af4fd98c59eaf51a01bd62` |

En esta ejecución la migración repetida terminó con `COMMIT`. En una ejecución
anterior sobre un volumen recién creado, PostgreSQL reinició el servidor
temporal de `initdb` después de que Compose lo reportó saludable; `psql` recibió
`Connection refused`. Esa invocación no llegó a ejecutar pruebas. Reintentar la
migración cuando PostgreSQL terminó de inicializar funcionó y las suites
pasaron. La incidencia fue de arranque del entorno aislado; no se cambió Compose
ni producción.

No se encontraron fallos de permisos. La evidencia cubre la implementación v3
publicada en `367f8b3` y la suite ampliada en esta rama. No acredita pruebas
manuales ni aceptación de otros integrantes.

## Cambios directos en v3

Los commits separan cobertura ya verificada de cinco pruebas HTTP adicionales;
el último commit añade además este informe actualizado. `er.name` se conserva
intacto y fuera de Git. No se hizo merge ni se crearon etiquetas.
