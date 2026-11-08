# Verificación manual: Áreas de las líneas (`ac_linea`)

## Alcance

Recorrido manual de creación, edición parcial del área y retiro lógico de una
relación línea–área de conocimiento en la pantalla **Áreas de las líneas**.

## Entorno y datos

- Rama: `prueba-areas-lineas`, creada desde `origin/v2-desarrollo` actualizado.
- Pantalla: `http://localhost:8078/ac-linea`.
- PostgreSQL del proyecto: servicio Compose `postgres`, base
  `investigacion_local` (puerto local `15440`).
- El checkout no tenía un volumen previo de este proyecto. Se usó el volumen
  nuevo e independiente de Compose y la carga opcional ficticia `demo_v2.sql`;
  no se modificó el PostgreSQL que escucha en el puerto `5432`.
- Antes del recorrido había 0 relaciones `ac_linea` activas y 218 áreas de
  conocimiento activas. Se verificaron las opciones usadas:
  - Línea `1902000001`: **DEMO V2 1 Línea ficticia**.
  - Área `1A01`: **Matemáticas puras**.
  - Área `1A02`: **Matemáticas aplicadas**.

## Resultado observado

1. **Crear:** el usuario confirmó que guardó la relación
   `(1902000001, '1A01')` desde la pantalla.
2. **Editar solo el área:** el usuario cambió el área a `1A02` y confirmó que
   el listado conserva la línea `1902000001` y muestra `1A02`. La consulta de
   solo lectura encontró la fila activa `(1902000001, '1A02')`; no encontró
   `(1902000001, '1A01')` activa.
3. **Retirar:** el usuario confirmó que la fila desapareció y la pantalla
   mostró **No hay fichas disponibles**. La consulta de solo lectura confirmó
   que la fila `(1902000001, '1A02')` permanece en PostgreSQL con
   `activo = FALSE`; quedan 0 relaciones `ac_linea` activas.

Consultas finales ejecutadas con `default_transaction_read_only = on`:

```sql
SELECT linea_investigacion, area_conocimiento, activo
FROM ac_linea
WHERE linea_investigacion = 1902000001
  AND area_conocimiento = '1A02';

SELECT count(*) AS relaciones_activas_restantes
FROM ac_linea
WHERE activo IS TRUE;
```

Resultado: `(1902000001, '1A02', FALSE)` y `relaciones_activas_restantes = 0`.

## Prueba automatizada

Se adaptó la prueba existente `test_clave_compuesta_y_cambio_de_relacion` en
`api_investigacion/pruebas/prueba_v2.py` para probar el cambio exclusivo del
área, conservar la misma línea y dejar la combinación anterior inaccesible
como activa. Se ejecutó `python pruebas/prueba_v2.py`: **12 pruebas pasaron**.

## Pendiente

- Este recorrido cubre la pantalla `ac_linea`; no completa la revisión manual
  de las otras nueve pantallas de v2.
- No se adjuntó captura del estado posterior a la creación, edición o retiro;
  esos resultados se registran a partir de las confirmaciones del usuario y
  las consultas indicadas.
