# Lista de Chequeo — Versión 2 (Compuerta 3)

- [x] **Regresión v1:** Las 6 tablas independientes de la v1 permanecen intactas y operativas.
- [x] **Completitud v2:** Están especificadas las 10 tablas con FK (3 entidades + 7 tablas puente).
- [x] **Coherencia con `db/init.sql`:** Se respetan tipos `DATE`, `SMALLINT` y nombres exactos de columnas (`universidsad`, `nacionalidaad`, `docente_cedula`, `grupo_investigacion_id`).
- [x] **Frontend con `<select>`:** Todas las FK se seleccionan desde listas desplegables alimentadas por la API.
- [x] **Alcance:** No se anticipa JWT, usuarios ni roles (v3).

**Veredicto:** 🟢 En verde — Autorizado para generar código de Versión 2.