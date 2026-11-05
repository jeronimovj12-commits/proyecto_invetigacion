# Checklist de aceptación — v2: claves foráneas

## Alcance y API

- [x] La API gestiona `docente` mediante GET, POST, PUT, PATCH y DELETE
  lógico. Evidencia: `6_contracts.md`, `8_tasks.md` y
  `VERIFICACION_V2.md`.
- [x] La API gestiona `grupo_investigacion` mediante GET, POST, PUT, PATCH y
  DELETE lógico. Evidencia: `6_contracts.md`, `8_tasks.md` y
  `VERIFICACION_V2.md`.
- [x] La API gestiona `semillero` mediante GET, POST, PUT, PATCH y DELETE
  lógico. Evidencia: `6_contracts.md`, `8_tasks.md` y
  `VERIFICACION_V2.md`.
- [x] La API gestiona `participa_semillero` mediante GET, POST, PUT, PATCH y
  DELETE lógico. Evidencia: `6_contracts.md`, `8_tasks.md` y
  `VERIFICACION_V2.md`.
- [x] La API gestiona `participa_grupo` mediante GET, POST, PUT, PATCH y
  DELETE lógico. Evidencia: `6_contracts.md`, `8_tasks.md` y
  `VERIFICACION_V2.md`.
- [x] La API gestiona `semillero_linea` mediante GET, POST, PUT, PATCH y
  DELETE lógico. Evidencia: `6_contracts.md`, `8_tasks.md` y
  `VERIFICACION_V2.md`.
- [x] La API gestiona `grupo_linea` mediante GET, POST, PUT, PATCH y DELETE
  lógico. Evidencia: `6_contracts.md`, `8_tasks.md` y
  `VERIFICACION_V2.md`.
- [x] La API gestiona `ac_linea` mediante GET, POST, PUT, PATCH y DELETE
  lógico. Evidencia: `6_contracts.md`, `8_tasks.md` y
  `VERIFICACION_V2.md`.
- [x] La API gestiona `ods_linea` mediante GET, POST, PUT, PATCH y DELETE
  lógico. Evidencia: `6_contracts.md`, `8_tasks.md` y
  `VERIFICACION_V2.md`.
- [x] La API gestiona `aa_linea` mediante GET, POST, PUT, PATCH y DELETE
  lógico. Evidencia: `6_contracts.md`, `8_tasks.md` y
  `VERIFICACION_V2.md`.

## Integridad y claves

- [x] Las claves compuestas de `participa_semillero` se reciben completas y
  en orden (`docente`, `semillero`). Evidencia: `6_contracts.md` y
  `8_tasks.md`.
- [x] Las claves compuestas de `participa_grupo` se reciben completas y en
  orden (`docente_cedula`, `grupo_investigacion_id`). Evidencia:
  `6_contracts.md` y `8_tasks.md`.
- [x] Las claves compuestas de `semillero_linea` se reciben completas y en
  orden (`semillero`, `linea_investigacion`). Evidencia: `6_contracts.md` y
  `8_tasks.md`.
- [x] Las claves compuestas de `grupo_linea` se reciben completas y en orden
  (`grupo_investigacion`, `linea_investigacion`). Evidencia:
  `6_contracts.md` y `8_tasks.md`.
- [x] Las claves compuestas de `ac_linea` se reciben completas y en orden
  (`linea_investigacion`, `area_conocimiento`). Evidencia: `6_contracts.md` y
  `8_tasks.md`.
- [x] Las claves compuestas de `ods_linea` se reciben completas y en orden
  (`linea_investigacion`, `ods`). Evidencia: `6_contracts.md` y
  `8_tasks.md`.
- [x] Las claves compuestas de `aa_linea` se reciben completas y en orden
  (`area_aplicacion`, `linea_investigacion`). Evidencia: `6_contracts.md` y
  `8_tasks.md`.
- [x] La API rechaza referencias inexistentes antes de confirmar la
  escritura. Evidencia: las 12 pruebas en memoria de
  `api_investigacion/pruebas/prueba_v2.py`, registradas en
  `VERIFICACION_V2.md`.
- [x] La API rechaza referencias existentes pero inactivas antes de confirmar
  la escritura. Evidencia: `api_investigacion/pruebas/prueba_v2.py` y
  `VERIFICACION_V2.md`.
- [x] La API impide desactivar un registro padre con relaciones activas.
  Evidencia: `api_investigacion/pruebas/prueba_v2.py` y
  `VERIFICACION_V2.md`.
- [x] DELETE aplica borrado lógico, conserva la fila y la excluye de los
  listados activos. Evidencia: `api_investigacion/pruebas/prueba_v2.py` y
  smoke test con PostgreSQL descrito en `VERIFICACION_V2.md`.
- [x] La API no permite reactivar registros mediante `activo = TRUE`.
  Evidencia: `api_investigacion/pruebas/prueba_v2.py` y
  `8_tasks.md`.

## Formularios y desplegables

- [x] Los desplegables de relaciones cargan sus opciones desde la API.
  Evidencia: `8_tasks.md` y `VERIFICACION_V2.md`.
- [x] Las consultas GET de `universidad`, `linea_investigacion`,
  `objetivo_desarrollo_sostenible` y `area_aplicacion` están disponibles como
  soporte de los selectores. Evidencia: `2_spec.md`, `6_contracts.md` y
  `8_tasks.md`.
- [x] El selector de `area_conocimiento` usa la API y conserva el código
  textual del catálogo. Evidencia: `2_spec.md`, `8_tasks.md` y
  `VERIFICACION_V2.md`.
- [x] Las plantillas, formularios y selectores de las diez pantallas fueron
  comprobados mediante HTTP simulado. Evidencia: `VERIFICACION_V2.md`.
- [ ] Revisar manualmente las diez pantallas en el navegador, incluidos
  desplegables, mensajes de error, botones de guardar, edición y borrado
  lógico. La prueba automática no sustituye este recorrido. Pendiente
  registrado en `VERIFICACION_V2.md` y `8_tasks.md`.

## Pruebas ejecutadas

- [x] Pasaron las 12 pruebas en memoria de integridad y contratos. Evidencia:
  `api_investigacion/pruebas/prueba_v2.py` y `VERIFICACION_V2.md`.
- [x] Pasaron las pruebas de capas de la v1. Evidencia:
  `VERIFICACION_V2.md`.
- [x] Pasaron las pruebas de las rutas HTTP de las diez tablas con servicios
  en memoria. Evidencia: `VERIFICACION_V2.md`.
- [x] Pasó la prueba integrada con Docker y PostgreSQL el 4 de noviembre de
  2026. Evidencia: `VERIFICACION_V2.md`.
- [x] El smoke test con PostgreSQL comprobó las operaciones de las diez
  tablas, referencias, desplegables y borrado lógico. Identificador de las
  fichas: `1701599219`. Evidencia: `VERIFICACION_V2.md`.
- [x] Se comprobó el comportamiento del front cuando la API no está
  disponible: aviso y lista vacía. Evidencia: `VERIFICACION_V2.md`.
- [ ] Ejecutar y registrar la revisión manual posterior en el navegador.
  Pendiente: la automatización no certifica el recorrido visual.

## Entrega

- [ ] Revisar con el equipo las decisiones de negocio de `2_spec.md`,
  incluidos códigos de error, llaves duplicadas, campos anulables y
  comportamiento de reactivación.
- [ ] Firmar el checklist por parte del equipo.
- [ ] Cerrar formalmente el checklist de la v2 después de completar la
  revisión manual de las diez pantallas.
- [ ] Crear el tag de la v2. No se crea mientras existan requisitos
  pendientes.
