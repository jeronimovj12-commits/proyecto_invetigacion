# Verificación de permisos API v3 del equipo

Fecha: 11 de noviembre de 2026. Rama `pruebas-seguridad-v3`; destino previsto
del PR: `v3-desarrollo`. No se hizo commit, push, merge ni se creó una etiqueta.

## Estado inicial y cambios

Al inicio, la rama estaba sincronizada con `origin/v3-desarrollo`. El árbol
contenía dos archivos sin seguimiento: `api_investigacion/pruebas/prueba_permisos_v3_equipo.py`,
vacío, y `er.name`, ajeno al proyecto. Se dejó `er.name` intacto y fuera de las
operaciones de Git. No se modificaron controladores, servicios ni código de
producción.

La prueba del equipo ahora importa el fixture y el ciclo HTTP de
`prueba_autenticacion_v3.py`. Recorre las operaciones de OpenAPI para verificar
que `consulta` pueda leer las rutas de dominio, reciba 403 al escribir o acceder
a rutas de seguridad, y que `administrador` no reciba 401/403. Todo se probó
contra una base temporal nueva; no se usaron cuentas de una instalación real.

## Aislamiento y ejecución

Se revisaron `docker-compose.v3.yml`, `docker-compose.v3.pruebas.yml`,
`scripts/verificar_v3.ps1` y la guía `7_quickstart.md`. La suite de autenticación
rechaza la ejecución salvo que `PRUEBAS_V3=1`, el host sea `postgres-v3` y la
base configurada sea `investigacion_v3`; luego crea y usa una base con nombre
aleatorio. El compose de pruebas no publica puertos. La ejecución se hizo con
el proyecto Docker exclusivo `investigacion-v3-equipo-20261111`, por lo que
PostgreSQL usó su propio servicio y volumen `pgdata-v3`, separados del proyecto
habitual `investigacion-v3` y de v2. Los valores efímeros de JWT y sesión se
inyectaron solo al proceso y no se registraron en este informe.

Comando de cada suite, desde la raíz (con las variables locales requeridas):

```powershell
$v3 = @('-p','investigacion-v3-equipo-20261111','--env-file','./v3-local.env','-f','docker-compose.v3.yml','-f','docker-compose.v3.pruebas.yml')
docker compose @v3 run --rm -T -e PRUEBAS_V3=1 api-v3 python pruebas/prueba_autenticacion_v3.py
docker compose @v3 run --rm -T -e PRUEBAS_V3=1 api-v3 python pruebas/prueba_administracion_v3.py
docker compose @v3 run --rm -T -e PRUEBAS_V3=1 api-v3 python pruebas/prueba_permisos_v3_equipo.py
```

## Resultados ejecutados

Las tres ejecuciones terminaron con código 0:

| Suite | Resultado |
|---|---|
| `prueba_autenticacion_v3.py` | 14 pruebas, OK, 12.348 s. Migración repetida y conflicto de bootstrap también OK. Base `pruebas_v3_44d42e7b88f9471283c60031e9bbc005`. |
| `prueba_administracion_v3.py` | 5 pruebas, OK, 5.595 s. Matriz de 92 operaciones protegidas. Base `pruebas_v3_7da5480e960e44b3a6421e045bc207c3`. |
| `prueba_permisos_v3_equipo.py` | 1 prueba, OK, 2.269 s. Verificó permisos para 92 operaciones. Base `pruebas_v3_a7bf54674daf4b8e91ab3d7182424290`. |

Las tres bases pertenecen al PostgreSQL del proyecto Docker exclusivo; ninguna
suite apuntó a `investigacion_local` ni al volumen del proyecto compartido. No se
borraron bases o volúmenes. La prueba confirma la matriz HTTP del contrato
OpenAPI disponible durante esta ejecución; no sustituye la revisión humana ni
declara aceptación del equipo.

## Preparación de commits

Cambios previstos en dos commits separados: primero la prueba del equipo y luego
este informe. `er.name` debe permanecer fuera de ambos. El diff y `git diff
--check` se revisan antes de solicitar confirmación. No se hará commit ni push
hasta recibirla.
