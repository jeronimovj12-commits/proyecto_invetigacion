# Verificación del borrador v2

Verificado en este entorno:
- Prueba de capas de v1: pasa.
- 12 pruebas de integridad y contratos con repositorio en memoria: pasan.
- Rutas HTTP de las diez tablas con servicios en memoria: pasan.
- Plantillas, formularios y selectores de las diez pantallas con HTTP simulado: pasan.
- Listados del front ante API no disponible: muestran aviso y lista vacía.

El 4 de noviembre de 2026 se ejecutó el smoke test de la v2 con Docker y PostgreSQL.

Se comprobaron las operaciones de las diez tablas, las referencias, los desplegables y el borrado lógico.

Resultado de la terminal:
"Smoke test v2 completo. Identificador de las fichas de prueba: 1701599219."

Pendiente: revisión manual de las pantallas y cierre del checklist de la v2.

## Incidencia del formulario `aa-linea` — 4 de noviembre de 2026

Se consultó PostgreSQL y `linea_investigacion` no tiene líneas activas: solo
existe la ficha de prueba `id = 1701599219`, marcada `activo = FALSE`. Por
eso `GET /api/linea_investigacion?limite=1000` responde `204 No Content`.

El recorrido Flask interpretaba correctamente el `204` como una respuesta sin
filas, pero no lo trataba como una falta de opciones: habilitaba el formulario
y permitía enviar el valor vacío. La API recibía `""` y respondía que
`linea_investigacion` debía ser un entero.

Se corrigió `front_flask/app.py` y
`front_flask/templates/aa_linea/formulario.html`: si falta un catálogo activo,
se muestra un mensaje claro y se deshabilitan los botones; si hay opciones pero
no se selecciona una línea, el servidor muestra `Selecciona una línea de
investigación.` y no llama a la API. Los selectores también son obligatorios
en el navegador.

Verificación realizada: el estado de PostgreSQL y el `204` del endpoint fueron
confirmados. El usuario comprobó manualmente en
`http://localhost:8078/aa-linea/nuevo` el aviso de ausencia de líneas activas
y el bloqueo del botón de guardado. La revisión manual del resto de las diez
pantallas continúa pendiente.

Pruebas focalizadas realizadas después del cambio, dentro del contenedor
`front-flask`:

- `python -m py_compile /app/app.py /app/cliente_api.py`: pasó.
- GET real a `http://localhost:8025/api/linea_investigacion?limite=1000`:
  respondió `204`.
- GET real a `http://localhost:8078/aa-linea/nuevo`: respondió `200`, mostró
  `No hay líneas de investigación activas para seleccionar.` y dejó
  deshabilitado el botón de guardado.
- POST simulado sin líneas disponibles: mostró el mismo mensaje y no llamó a
  `crear_aa_linea`.
- POST simulado con opciones disponibles y sin seleccionar línea: mostró
  exactamente `Selecciona una línea de investigación` y no llamó a la API.
- La consulta posterior a PostgreSQL siguió mostrando una fila y cero filas
  activas; no se insertaron ni borraron datos.

Para cargar datos oficiales, primero deben incorporarse registros aprobados en
la tabla `linea_investigacion` mediante el procedimiento de carga definido por
el equipo. `db/init.sql` solo define la tabla y no contiene semillas para
`linea_investigacion`; no se deben inventar datos ni borrar la base. Tras la
carga, las filas deben quedar con `activo = TRUE` para que aparezcan en el
endpoint y en el desplegable. La carga, realizada por el responsable de la
base con datos oficiales aprobados, debe seguir esta forma parametrizada:

```sql
INSERT INTO linea_investigacion (id, nombre, descripcion, activo)
VALUES (<id_oficial>, '<nombre_oficial>', '<descripcion_oficial>', TRUE);
```

Después se debe repetir el GET del catálogo y comprobar que responde `200`
con la fila activa antes de probar el formulario.

## Preparación de la siguiente prueba manual — 4 de noviembre de 2026

Se creó en el PostgreSQL local una línea de prueba activa, sin modificar las
semillas oficiales ni reactivar la ficha del smoke test:

- `id`: `1701599220`
- `nombre`: `PRUEBA V2 - Revisión manual`
- `descripcion`: `Línea temporal para la revisión manual del formulario aa-linea`
- `activo`: `TRUE`

La fila `1701599219` permanece con `activo = FALSE`. La consulta
`GET /api/linea_investigacion?limite=1000` respondió `200` y devolvió la nueva
línea. También se comprobó que aparece como opción en
`http://localhost:8078/aa-linea/nuevo`.

El guardado de la relación `aa_linea` desde el navegador queda pendiente para
el usuario. La revisión manual no se considera cerrada hasta que el usuario
realice ese guardado y continúe el recorrido de las diez pantallas.

## Confirmación de la revisión manual — 5 de noviembre de 2026

El usuario confirmó que comprobó manualmente el aviso y el bloqueo del botón
de guardado cuando no hay líneas activas en `/aa-linea/nuevo`.

Se consultó nuevamente PostgreSQL local: ya existe la línea activa
`PRUEBA V2 - Revisión manual`, con ID `1701599220`, por lo que se reutiliza
sin insertar otra fila. La línea `1701599219` continúa con `activo = FALSE`.
No se modificaron datos de la base ni las semillas oficiales.

Se confirmó que `GET http://localhost:8025/api/linea_investigacion?limite=1000`
responde `200` y devuelve la línea `1701599220` con el nombre indicado.
La prueba de guardado en el navegador queda a cargo del usuario y continúa
pendiente; esta comprobación no cierra la revisión manual de la v2.

## Creación, edición y retiro manual de `aa_linea` — 5 de noviembre de 2026

El usuario confirmó el siguiente recorrido en el navegador para la línea
`1701599220` (`PRUEBA V2 - Revisión manual`): creó la ficha con
`area_aplicacion = 2`, la editó a `area_aplicacion = 3` y, al retirarla,
dejó de aparecer en el listado.

Después se ejecutó esta consulta de solo lectura en PostgreSQL local:

```sql
SELECT area_aplicacion, linea_investigacion, activo
FROM aa_linea
WHERE area_aplicacion = 3 AND linea_investigacion = 1701599220;
```

La consulta devolvió exactamente una fila: `area_aplicacion = 3`,
`linea_investigacion = 1701599220` y `activo = FALSE` (`f` en `psql`).
La fila sigue existiendo en la base y está inactiva, lo que confirma el
borrado lógico después del retiro observado en el navegador. Esta
comprobación no modificó los datos.

La prueba de guardado de `aa_linea`, que figuraba pendiente en los apartados
anteriores, queda confirmada por el usuario junto con la edición y el retiro.
La revisión manual del conjunto de las diez pantallas y el cierre de la v2
continúan pendientes.

## Creación, edición y retiro manual de `ods_linea` — 5 de noviembre de 2026

El usuario confirmó el siguiente recorrido en el navegador para la línea
`1701599220` (`PRUEBA V2 - Revisión manual`): creó la relación con `ods = 5`,
la cambió a `ods = 6` y, al retirarla, desapareció del listado.

Después se ejecutó esta consulta de solo lectura en PostgreSQL local:

```sql
SELECT linea_investigacion, ods, activo
FROM ods_linea
WHERE linea_investigacion = 1701599220 AND ods = 6;
```

La consulta devolvió exactamente una fila: `linea_investigacion = 1701599220`,
`ods = 6` y `activo = TRUE` (`t` en `psql`). Por tanto, la fila sigue
existiendo, pero está activa, no con `activo = FALSE`.

Existe una discrepancia entre la desaparición del listado observada por el
usuario y el estado activo consultado en PostgreSQL. El borrado lógico de
esta fila no queda confirmado y la causa de la discrepancia queda pendiente
de revisión. Esta comprobación no modificó los datos. La revisión manual
del conjunto de las diez pantallas y el cierre de la v2 continúan pendientes.

## Comprobación final de `ods_linea` — 5 de noviembre de 2026

Para la relación con `linea_investigacion = 1701599220` y `ods = 6`, la
revisión posterior confirmó:

- Los registros de la API muestran que
  `DELETE /api/ods_linea/1701599220/6` respondió `200`.
- La consulta directa a PostgreSQL devolvió la fila con `activo = FALSE`
  (`f` en `psql`): la relación sigue existiendo y quedó inactiva.
- `GET /api/ods_linea/1701599220/6` devolvió `404`, porque la fila está
  inactiva.
- `GET /api/ods_linea?limite=1000` devolvió `204`, sin filas activas en el
  listado.

Se comprobó también que la API y la consulta directa utilizan la misma base
`investigacion_local`, esquema `public`, y la misma tabla `ods_linea`.
El estado final observado en PostgreSQL coincide con las respuestas de la API
y con la ausencia de la relación en el listado del navegador.

Se conserva la observación anterior de `activo = TRUE` como parte del
historial. No se determinó la causa de la diferencia entre aquella lectura
y la comprobación final con `activo = FALSE`; la discrepancia ya no se
reprodujo durante esta revisión. El diagnóstico se realizó mediante consultas
de solo lectura y revisión de registros, sin modificar los datos.

Esta comprobación confirma el borrado lógico de la relación consultada; la
revisión manual del conjunto de las diez pantallas y el cierre de la v2
continúan pendientes.
