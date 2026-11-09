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

## Inventario y cargas opcionales — 5 de noviembre de 2026

Trabajo en `v2-desarrollo`, con árbol inicialmente limpio. Se leyeron la
constitución y los documentos v2. No se fusionó con main ni se creó tag.

Consulta de solo lectura de `investigacion_local`, antes de cualquier carga:

| Catálogo o padre de desplegable | Total | Activos | Procedencia observada |
|---|---:|---:|---|
| area_conocimiento | 218 | 218 | Catálogo de referencia de init.sql |
| objetivo_desarrollo_sostenible | 17 | 17 | Catálogo de referencia de init.sql |
| area_aplicacion | 21 | 21 | Catálogo de referencia de init.sql |
| universidad | 2 | 0 | PRUEBA V2, ambas inactivas |
| linea_investigacion | 2 | 1 | PRUEBA V2; activa la 1701599220 de revisión manual |
| docente | 1 | 0 | Prueba v2, inactivo |
| grupo_investigacion | 1 | 0 | Prueba v2, inactivo |
| semillero | 1 | 0 | Prueba v2, inactivo |

Los tres catálogos de init.sql son las semillas de referencia del módulo;
las cantidades coinciden con las semillas, pero no se hizo una comparación
campo por campo de las 256 filas locales. Una tabla con filas inactivas no
está físicamente vacía, aunque su desplegable no tenga opciones.

Fuentes revisadas: `db/init.sql`, los SQL de
`ProyectosDeAula/db_scripts/postgresql/` (no se hallaron INSERT/COPY de estos
padres) y las hojas pertinentes de
`ProyectosDeAula/Mapa_conocimiento/04_Modelo_y_Base_de_datos/Base de Datos v6.xlsx`.
La hoja universidad sí contiene seis filas completas, incorporadas literalmente
en `db/opcionales/universidades_oficiales_v2.sql`. Las hojas grupo_investigacion,
semillero y linea_ivestigacion solo tienen encabezados. La fila de docente está
incompleta y no permite cumplir los NOT NULL del esquema: no se inventaron sus
campos faltantes ni se trató como ficha oficial cargable.

`db/opcionales/demo_v2.sql` prepara diez filas ficticias: dos por cada padre
universidad, línea, docente, grupo y semillero. Los nombres comienzan por
DEMO V2 y las claves son 1902000001 y 1902000002. No se precargan relaciones:
los padres permiten probar los siete formularios de asociación y los cambios
de sus FK. El auxiliar `carga_segura.sql` compara la fila completa con parámetros,
usa bloqueos de tabla y solo existe en pg_temp. Las cargas no alteran semillas,
no sobrescriben, no reactivan y abortan íntegramente ante conflictos.
Los comandos exactos de instalación nueva y existente están en `7_quickstart.md`.

### Verificaciones ejecutadas en esta sesión

Docker requirió acceso fuera del sandbox y luego estuvo disponible. Se creó
únicamente la base aislada `verificacion_datos_v2_20261105` en el servicio
postgres, inicializada con `init.sql` usando `psql -X -v ON_ERROR_STOP=1`.
El script de inicialización se ejecutó **solo en esa base nueva**.

Se copiaron los opcionales con `docker compose cp db/opcionales postgres:/tmp/v2-opcionales`
y se ejecutaron ambos archivos con el mismo comando del quickstart, sustituyendo
`-d investigacion_local` por `-d verificacion_datos_v2_20261105`.

Resultados reales:

- Primera carga: seis universidades oficiales y diez filas DEMO insertadas,
  con FK y NOT NULL reales de PostgreSQL 16.
- Segunda ejecución de cada carga: éxito y avisos de fila idéntica, sin duplicar.
  Totales: ocho universidades, dos líneas, dos docentes, dos grupos y dos semilleros.
- Inactivación controlada de semillero 1902000002 en la base de prueba:
  demo abortó con conflicto, salida no cero; la fila siguió inactiva.
- Cambio controlado del nombre de universidad 1 a `Ajeno: conflicto controlado`:
  carga oficial abortó con conflicto, salida no cero; el valor se conservó.
- Inactivación de las 21 áreas de aplicación exclusivamente en la base de prueba:
  demo abortó por falta de catálogo activo antes de insertar.
- La secuencia linea_investigacion_id_seq conservó last_value=1 e is_called=false.

La base de prueba se conserva con esos conflictos intencionales para inspección;
no es una demostración lista para usar. No se borró ninguna base ni volumen.
Las cargas opcionales **no se ejecutaron sobre investigacion_local**; allí solo
se consultaron datos. No se repitieron las pruebas de API ni el smoke test en
esta sesión, ni se realizó un nuevo recorrido manual del navegador.

Se conserva la evidencia previa de aa_linea (creación, edición y retiro manual)
y ods_linea (recorrido del usuario y comprobación final de inactividad), sin
atribuirles cobertura de todos los casos. Continúan pendientes la revisión
manual restante de las diez pantallas, revisión e integración de aportes de
compañeros, decisiones de negocio, firmas y cierre. La v2 sigue abierta.

## Carga ejecutada en PostgreSQL local — 5 de noviembre de 2026

Por solicitud explícita del usuario se ejecutaron ahora las cargas opcionales
sobre `investigacion_local`. Este apartado actualiza el estado posterior al
ensayo aislado anterior; no modifica su evidencia histórica.

Comandos ejecutados desde la raíz del repositorio:

```sh
docker compose exec -T postgres pg_isready -U investigacion -d investigacion_local
docker compose cp db/opcionales postgres:/tmp/v2-opcionales
docker compose exec -T postgres psql -X -U investigacion -d investigacion_local -f /tmp/v2-opcionales/universidades_oficiales_v2.sql
docker compose exec -T postgres psql -X -U investigacion -d investigacion_local -f /tmp/v2-opcionales/demo_v2.sql
```

PostgreSQL confirmó disponibilidad. Ambas cargas terminaron con COMMIT y código
de salida 0, sin conflictos: se insertaron las seis universidades oficiales
(IDs 1–6) y las diez fichas DEMO V2 (dos universidades, líneas, docentes,
grupos y semilleros; claves 1902000001 y 1902000002).

Se consultaron realmente por HTTP los ocho endpoints de la API local con
`GET http://localhost:8025/api/{tabla}?limite=1000`. Todos respondieron 200;
`total` coincidió con la cantidad de elementos de `datos`:

| Tabla | HTTP | Opciones activas devueltas |
|---|---:|---:|
| universidad | 200 | 8 |
| linea_investigacion | 200 | 3 |
| docente | 200 | 2 |
| grupo_investigacion | 200 | 2 |
| semillero | 200 | 2 |
| area_conocimiento | 200 | 218 |
| objetivo_desarrollo_sostenible | 200 | 17 |
| area_aplicacion | 200 | 21 |

La consulta directa posterior de solo lectura confirmó que las universidades
1701599218 y 1701599219 siguen inactivas; la línea 1701599219 y las fichas de
docente, grupo y semillero 1701599219 también siguen inactivas. La línea previa
1701599220 continúa activa. Las nuevas fichas DEMO están activas. Los scripts
solo insertaron las filas nuevas; no sobrescribieron ni reactivaron las previas.
No se ejecutó init.sql ni se borraron datos, bases o volúmenes.

Esta comprobación acredita carga y disponibilidad de opciones desde la API.
No se realizó un nuevo recorrido manual del navegador ni se ejecutó el smoke
test en esta sesión. Continúan pendientes las pruebas manuales restantes de
las diez pantallas, la revisión e integración de aportes de compañeros, las
decisiones pendientes del equipo y las firmas. La v2 no se declara terminada.
No se creó tag v2 ni se fusionó con main. No se hizo commit ni push en esta sesión.
