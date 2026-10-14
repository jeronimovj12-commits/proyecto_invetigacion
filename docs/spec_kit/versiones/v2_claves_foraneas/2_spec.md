# Propuesta de implementación — Versión 2

Estado: código preparado para revisión; no versión cerrada ni etiquetada.

## Alcance

CRUD y pantalla propia de docente, grupo_investigacion, semillero,
participa_semillero, participa_grupo, semillero_linea, grupo_linea, ac_linea,
ods_linea y aa_linea. Los formularios cargan sus relaciones desde la API.
Se agregan consultas GET de universidad, linea_investigacion,
objetivo_desarrollo_sostenible y area_aplicacion como soporte de los selectores.
Se conserva la API y pantalla de area_conocimiento.

## Decisiones propuestas para revisar con el equipo

- Referencia inexistente o inactiva: 400; no se confirma la escritura.
- Registro inexistente o inactivo: 404, también en el segundo DELETE.
- DELETE desactiva. Un padre con relaciones activas no se desactiva: 400.
- Sin reactivación. `activo` no es un campo editable del cuerpo.
- Las siete claves compuestas van completas en la ruta. PUT/PATCH pueden
  cambiar los componentes de esas relaciones; se consulta después con la nueva ruta.
- POST/PUT exigen los campos declarados, incluidos los anulables, que admiten null.
  PATCH distingue omisión de null: omitir conserva el dato y null solo se admite
  para columnas anulables. Un PATCH vacío responde 400.
- Llave duplicada: se conserva el tratamiento de v1 (500 con detalle).
- El JSON nuevo usa los nombres de columna del SQL, incluso `universidsad`
  y `nacionalidaad`; las pantallas muestran etiquetas corregidas.
- Los catálogos de universidades y líneas no tienen semillas en el init.sql
  actual. Las opciones permanecerán vacías hasta cargar datos reales. No se
  inventan registros oficiales. La prueba integrada carga sus propias fichas.

## Integridad y capas

Servicio y repositorio siguen comunicándose por interfaces. Las referencias
se revisan en la misma transacción que la escritura, con aislamiento
SERIALIZABLE de PostgreSQL. Una carrera concurrente puede abortar y devolver
un error; la operación no queda confirmada a medias.

## Pendiente para declarar terminada

Ejecutar la prueba integrada con PostgreSQL y el front reales, comprobar los
formularios manualmente, revisar estas decisiones de negocio y firmar el
checklist del equipo. No hacer tag v2 antes de completar esos pasos.
