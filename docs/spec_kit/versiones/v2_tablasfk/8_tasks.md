`8_tasks.md`

# Tareas — Versión 2: Orden de Construcción

- **Fase 1 — Entidades Principales con FK (`docente`, `grupo_investigacion`, `semillero`):** Implementar modelos Pydantic (con fechas `date` y mapeo de columnas `universidsad`/`nacionalidaad`), interfaces, repositorios SQL `text()`, servicios y controladores.
- **Fase 2 — Primeras Tablas Puente (`participa_grupo`, `participa_semillero`):** Implementar CRUD con llave primaria compuesta en rutas y borrado lógico.
- **Fase 3 — Tablas Puente de Líneas (`grupo_linea`, `semillero_linea`, `ac_linea`, `ods_linea`, `aa_linea`):** Implementar los 5 CRUD con PK compuesta y registrar los 10 routers en `api_investigacion/main.py`.
- **Fase 4 — Frontend Flask y Listas Desplegables (`front_flask/`):** Implementar las 60 funciones explícitas en `cliente_api.py`, las 10 rutas en `app.py` cargando catálogos padre para los `<select>`, y las 20 plantillas HTML respetando `marca.css`.
- **Fase 5 — Regresión y Cierre v2:** Verificar endpoints en Swagger, probar formularios con `<select>` en navegador y completar `9_checklist.md` y `GUIA_IA2.md`.