# Plan de Arquitectura e Implementación — Versión 2 (`PLAN_V2.md`)

> **Proyecto:** Módulo de Investigación — Universidad Monte Verde  
> **Alcance:** Entidades Relacionales y Tablas Puente (10 tablas con llaves foráneas + regresión v1)

## 1. Objetivo de la Versión 2
Ampliar el dominio del sistema incorporando las **10 tablas relacionales** de `db/init.sql` (alcanzando 16 recursos operativos), garantizando integridad referencial en la API y sustituyendo cualquier captura manual de IDs foráneos por listas desplegables (`<select>`) en el frontend.

## 2. Entidades Incorporadas (10 Tablas Relacionales)

### A. Entidades Principales con Llave Foránea Simple (3)
1. **`docente`** (`PK: cedula INT`) — FK opcional `linea_investigacion_principal` $\rightarrow$ `linea_investigacion(id)`. Mapeo exacto en SQL de columnas `nacionalidaad` y `cat_minciencia` con alias JSON limpio (`nacionalidad`, `catMinciencia`).
2. **`grupo_investigacion`** (`PK: id INT`) — FK opcional `universidsad` $\rightarrow$ `universidad(id)`, expuesto como `universidad` en la frontera JSON.
3. **`semillero`** (`PK: id INT`) — FK obligatoria `grupo_investigacion` $\rightarrow$ `grupo_investigacion(id)`.

### B. Tablas Puente con Llave Primaria Compuesta (7)
4. **`participa_grupo`** (`PK: docente_cedula, grupo_investigacion_id` + `rol`, `fecha_inicio`, `fecha_fin`)
5. **`participa_semillero`** (`PK: docente, semillero` + `rol`, `fecha_inicio`, `fecha_fin`)
6. **`grupo_linea`** (`PK: grupo_investigacion, linea_investigacion`)
7. **`semillero_linea`** (`PK: semillero, linea_investigacion`)
8. **`ac_linea`** (`PK: linea_investigacion, area_conocimiento`)
9. **`ods_linea`** (`PK: linea_investigacion, ods`)
10. **`aa_linea`** (`PK: area_aplicacion, linea_investigacion`)

## 3. Decisiones Técnicas y Contratos
* **Rutas explícitas para claves compuestas:** Los endpoints individuales de las 7 tablas puente reciben ambas llaves en la ruta (`/api/{tabla}/{fk1}/{fk2}`) para operaciones `GET`, `PUT`, `PATCH` y `DELETE`.
* **Control de integridad referencial:** Las violaciones de llave foránea (`IntegrityError`) capturadas desde PostgreSQL son interceptadas y traducidas a respuestas HTTP controladas con detalle legible.
* **Listas desplegables dinámicas en Flask:** Antes de renderizar cualquier formulario de creación o edición en `app.py`, el controlador frontend consulta los endpoints `GET` de las tablas padre mediante `cliente_api.py` y alimenta etiquetas `<select>` con nombres descriptivos.
* **Regresión garantizada:** Los 6 catálogos base de la v1 permanecen intactos y operativos.