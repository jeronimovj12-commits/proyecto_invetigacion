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
