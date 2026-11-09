# Instalar y verificar el borrador v2

1. Trabajar en `v2-desarrollo`, conservando los cambios existentes. Si ya
   existe la rama: `git switch v2-desarrollo`. No fusionar con main ni crear tag.
2. Usar los archivos de esta rama en la raíz del clon, donde están
   docker-compose.yml, api_investigacion, front_flask y db.
3. Ejecutar `docker compose up -d --build`. No borrar el volumen PostgreSQL.
4. Abrir http://localhost:8025/ (version v2), http://localhost:8025/docs
   y http://localhost:8078/ (las diez pantallas nuevas).
5. Pruebas sin base:
   `docker compose exec api-investigacion python pruebas/prueba_capas.py`
   `docker compose exec api-investigacion python pruebas/prueba_v2.py`
6. Prueba real de las diez tablas:
   `docker compose exec api-investigacion python pruebas/humo_v2.py`
   Utiliza fichas marcadas como pruebas y las deja inactivas. En caso de
   fallo, imprime el caso y se detiene; no modifica registros oficiales.
7. Revisar manualmente las opciones, errores y los dos botones de guardar.

No se debe declarar terminada la v2 solo porque estas pruebas de capas pasan.
También se deben ejecutar la prueba integrada y la revisión visual en Docker.

## Cargas opcionales: instalación existente y nueva

Desde la raíz, después de `docker compose up -d --build`, ejecutar estos
comandos (iguales en PowerShell y terminal POSIX):

```sh
docker compose exec -T postgres pg_isready -U investigacion -d investigacion_local
docker compose cp db/opcionales postgres:/tmp/v2-opcionales
```

Esperar la disponibilidad de PostgreSQL. En una instalación nueva, el volumen
vacío recibe automáticamente las semillas oficiales de `db/init.sql`.
En una existente se conserva la base: **no ejecutar init.sql de nuevo** porque
contiene DROP TABLE; no borrar la base ni los volúmenes.

Para incorporar las seis universidades oficiales del Excel del módulo:

```sh
docker compose exec -T postgres psql -X -U investigacion -d investigacion_local -f /tmp/v2-opcionales/universidades_oficiales_v2.sql
```

Para cargar voluntariamente datos ficticios de demostración:

```sh
docker compose exec -T postgres psql -X -U investigacion -d investigacion_local -f /tmp/v2-opcionales/demo_v2.sql
```

Los comandos sirven tanto para una instalación existente como para una nueva.
Copiar la carpeta completa permite resolver `carga_segura.sql` mediante `\ir`;
no ejecutar el auxiliar por separado. `psql -X` evita configuraciones personales.
La demo no depende de cargar antes las universidades oficiales.

La demo crea dos universidades, dos líneas, dos docentes, dos grupos y dos
semilleros, en orden de dependencia. Sus nombres empiezan por `DEMO V2`, con
IDs/cédulas `1902000001` y `1902000002`, fechas ficticias y URLs/correos
`example.invalid`. No modifica la secuencia SERIAL ni carga las siete relaciones:
estas se crean desde las pantallas. Respeta longitudes, nulabilidad y las FK
reales, incluidos los nombres `universidsad` y `nacionalidaad`.

Cada carga es una transacción independiente: conserva filas idénticas activas;
ante claves ocupadas con valores diferentes o inactivos, informa tabla y clave,
sale con error y revierte toda esa carga. Nunca sobrescribe ni reactiva.
La demo exige al menos un área de conocimiento, ODS y área de aplicación activos;
si faltan, se detiene y se deben obtener datos oficiales aprobados. Consultar
los conflictos con el responsable de datos, sin borrar ni forzar registros.
Después de editar o retirar fichas DEMO, repetir la carga puede informar un
conflicto: es la protección esperada, no un mecanismo de restauración.

## Orden recomendado de las diez pantallas

Comprobar primero los GET `/api/universidad`, `/api/linea_investigacion`,
`/api/area_conocimiento`, `/api/objetivo_desarrollo_sostenible` y
`/api/area_aplicacion`, con `?limite=1000`: 200 con opciones activas; 204
significa que no hay opciones activas.

| Orden | Pantalla | Dependencias para los desplegables |
|---|---|---|
| 1 | Docente | Línea principal (anulable) |
| 2 | Grupo de investigación | Universidad (anulable) |
| 3 | Semillero | Grupo activo obligatorio |
| 4 | Participación en grupo | Docente y grupo |
| 5 | Participación en semillero | Docente y semillero |
| 6 | Grupo–línea | Grupo y línea |
| 7 | Semillero–línea | Semillero y línea |
| 8 | Área de conocimiento–línea | Línea y área de conocimiento |
| 9 | ODS–línea | Línea y ODS |
| 10 | Área de aplicación–línea | Área de aplicación y línea |

En cada pantalla comprobar listado, creación, ambos botones de guardar,
edición, errores y retiro lógico. Las dos opciones DEMO permiten cambiar FK.
Para crear docentes, grupos y semilleros usar claves nuevas y nombres de prueba
explícitos. Una clave compuesta retirada no se puede reutilizar ni reactivar.
Retirar primero las relaciones de los pasos 4–10, luego semilleros, docentes y
grupos: no se puede retirar un padre con dependientes activos.

Registrar lo observado en `VERIFICACION_V2.md`. La evidencia manual parcial de
`aa_linea` y `ods_linea` no completa las diez pantallas. Siguen pendientes el
recorrido restante, revisión e integración de aportes de compañeros, firmas y
cierre. Las pruebas automáticas no sustituyen estos pasos.
