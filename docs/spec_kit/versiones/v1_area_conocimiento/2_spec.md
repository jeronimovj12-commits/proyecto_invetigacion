# Especificación — Versión 1: Tablas Base (sin FK) + PostgreSQL + Frontend

> **Versión 1** ([mapa](../0_mapa_versiones.md)) · Ante conflicto con este documento, manda la [constitución](../../1_constitution.md).

## 1. Propósito de la v1
Construir la API REST (FastAPI + SQLAlchemy Core `text()`) y el Frontend independiente (Flask + Jinja2 + CSS manual UMV) para las **6 tablas sin clave foránea** del módulo Investigación: `area_conocimiento`, `objetivo_desarrollo_sostenible`, `area_aplicacion`, `termino_clave`, `universidad` y `linea_investigacion`.

## 2. Alcance

**Incluye**
- CRUD completo (`GET` listado con `?limite`, `GET/{id}`, `POST`, `PUT`, `PATCH`, `DELETE` lógico) para las **6 tablas sin FK**.
- **Borrado lógico**: `DELETE` marca `activo = FALSE` y todas las lecturas filtran `activo = TRUE` (Artículo 6).
- **Frontend Flask separado** en puerto `8078` con una pantalla propia por cada uno de los 6 recursos, sin conexión a BD y respetando `marca.css` (Artículos 1.1 y 12).
- Manejo de variables de entorno mediante `.env` y `.env.example` (Artículo 7).
- Prueba de capas desacopladas (`pruebas/prueba_capas.py`) corriendo con PostgreSQL apagado.

**NO incluye**
- Ninguna de las 10 tablas con FK ni las 3 de seguridad (v2 y v3).
- Autenticación, JWT ni roles (v3).
- Reactivación de registros inactivos (`activo = TRUE`).

## 3. Requisitos funcionales

- **RF1 — Listar recursos (`GET /api/{recurso}[?limite=N]`):** Devuelve `200` con `{tabla, limite, total, datos}` solo con registros `activo = TRUE`. Si no hay filas activas devuelve `204` sin cuerpo. Si `limite <= 0` devuelve `400`.
- **RF2 — Obtener por llave primaria (`GET /api/{recurso}/{id}`):** Devuelve `200` con el registro activo. Si no existe o tiene `activo = FALSE`, devuelve `404`.
- **RF3 — Crear (`POST /api/{recurso}`):** Valida campos obligatorios con Pydantic (`422` si faltan o exceden longitud). Inserta con `activo = TRUE` y devuelve `200`. Si la PK ya existe, la base rechaza y devuelve `500`.
- **RF4 — Reemplazar (`PUT /api/{recurso}/{id}`):** Exige **todos** los campos editables (`422` si falta uno). Actualiza y devuelve `200` con `filasAfectadas: 1` (`404` si no existe o está inactivo).
- **RF5 — Actualizar parcialmente (`PATCH /api/{recurso}/{id}`):** Actualiza solo los campos enviados (`200`). Si el cuerpo llega vacío `{}` devuelve `400`. Si no existe o está inactivo devuelve `404`.
- **RF6 — Eliminar lógicamente (`DELETE /api/{recurso}/{id}`):** Ejecuta `UPDATE ... SET activo = FALSE WHERE pk = :id AND activo = TRUE`. Devuelve `200` si afectó 1 fila, o `404` si no existía o ya estaba inactivo.
- **RF7 — Diagnóstico (`GET /`):** Devuelve `200` con `{"mensaje": "...", "version": "v1", "contratos": "/docs"}`.
- **RF8 — Interfaz Web Flask (`http://localhost:8078`):** 6 pantallas independientes (`/areas-de-conocimiento`, `/ods`, `/areas-aplicacion`, `/terminos-clave`, `/universidades`, `/lineas-investigacion`), con botones «Guardar la ficha completa» (`PUT`) y «Guardar solo lo que cambié» (`PATCH`), traducción de errores 422 al español y tolerancia a `204` (tabla vacía) y caída de la API.

## 4. Criterios de aceptación
1. **Arranque único:** `docker compose up -d --build` levanta PostgreSQL (con las 19 tablas y semillas: 218 áreas, 17 ODS, 21 áreas de aplicación), la API (`8025`) y el Frontend (`8078`). `GET /` responde `"version": "v1"`.
2. **Lecturas y límites:** `GET /api/area_conocimiento` devuelve `total: 218`; `?limite=3` devuelve `3`; `GET /api/objetivo_desarrollo_sostenible` devuelve `total: 17`; `GET /api/area_aplicacion` devuelve `total: 21`; `GET /api/universidad` (vacía inicialmente) devuelve `204`.
3. **Obtener individual y 404:** `GET /api/area_conocimiento/1A01` y `GET /api/objetivo_desarrollo_sostenible/1` devuelven `200`; códigos inexistentes (`9Z99`, `999`) devuelven `404`.
4. **Ciclo completo y contraste PUT vs PATCH:** En cada recurso, `POST` → `PUT` → `PATCH` → `GET` → `DELETE` → segundo `DELETE` (`404`). Enviar un cuerpo incompleto a `PUT` devuelve `422` y el mismo cuerpo a `PATCH` devuelve `200`.
5. **Borrado lógico verificable:** Tras `DELETE` en `area_conocimiento/9Z01`, el `total` vuelve a `218` pero `SELECT activo FROM area_conocimiento WHERE id='9Z01'` muestra `f` (`FALSE`).
6. **Validación y frontera:** `POST` con campos faltantes o longitudes excedidas → `422` con `errores[]`; PK duplicada → `500`.
7. **Prueba de capas y separación de procesos:** `pruebas/prueba_capas.py` pasa con PostgreSQL apagado (`docker compose stop postgres`). Con la API apagada (`docker compose stop api-investigacion`), Flask sigue respondiendo sin mostrar datos ni caer.

## 5. Clarificaciones
- **C1 a C5 (del script `db/init.sql`):** `area_conocimiento.id` es `VARCHAR(6)`, `disciplina` es `VARCHAR(150)`, `area_aplicacion.nombre` es `VARCHAR(150)`, todas las tablas tienen `activo BOOLEAN NOT NULL DEFAULT TRUE`, y se corrigió `Ciencias Naturales`.
- **C6 (Tipos de llaves primarias por tabla):**
  - `area_conocimiento`: `id` (`VARCHAR(6)`), provisto por el usuario en `POST`.
  - `termino_clave`: `termino` (`VARCHAR(30)`), clave natural de texto provista por el usuario en `POST`.
  - `objetivo_desarrollo_sostenible`, `area_aplicacion`, `universidad`: `id` (`INT`), provisto por el usuario en `POST`.
  - `linea_investigacion`: `id` (`SERIAL`), autogenerado por PostgreSQL en `POST` (no se envía en el cuerpo de creación).
- **C7 (Secretos):** Se cumple el Artículo 7 estricto: `.env` está en `.gitignore` y el repositorio incluye `.env.example`.