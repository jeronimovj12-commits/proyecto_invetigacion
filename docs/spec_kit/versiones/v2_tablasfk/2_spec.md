# Especificación — Versión 2: Tablas Relacionales y Tablas Puente

> **Versión 2** ([mapa](../0_mapa_versiones.md)) · Crece acumulativamente sobre la `v1` sin romperla. Rige la [constitución](../../1_constitution.md).

## 1. Propósito de la v2
Incorporar el CRUD completo (API REST + Frontend Flask) para las **10 tablas con llaves foráneas** del módulo Investigación definidas en `db/init.sql`, manteniendo intactas las 6 tablas de la `v1` (regresión obligatoria).

## 2. Alcance

**Incluye**
- **3 entidades principales con llave foránea simple:**
  1. `docente` (PK: `cedula INT` — FK: `linea_investigacion_principal` $\rightarrow$ `linea_investigacion(id)`)
  2. `grupo_investigacion` (PK: `id INT` — FK: `universidsad` $\rightarrow$ `universidad(id)`)
  3. `semillero` (PK: `id INT` — FK: `grupo_investigacion` $\rightarrow$ `grupo_investigacion(id)`)
- **7 tablas puente con llave primaria compuesta:**
  4. `participa_grupo` (`docente_cedula` + `grupo_investigacion_id`, `rol`, `fecha_inicio`, `fecha_fin`)
  5. `participa_semillero` (`docente` + `semillero`, `rol`, `fecha_inicio`, `fecha_fin`)
  6. `grupo_linea` (`grupo_investigacion` + `linea_investigacion`)
  7. `semillero_linea` (`semillero` + `linea_investigacion`)
  8. `ac_linea` (`linea_investigacion` + `area_conocimiento`)
  9. `ods_linea` (`linea_investigacion` + `ods`)
  10. `aa_linea` (`area_aplicacion` + `linea_investigacion`)
- **Frontend Flask:** 10 nuevas pantallas independientes donde **toda llave foránea se selecciona mediante listas desplegables (`<select>`)** cargadas desde los endpoints `GET` de la API.
- **Borrado lógico:** `activo = FALSE` en todas las tablas nuevas y filtrado `WHERE activo = TRUE`.

**NO incluye**
- Autenticación, JWT ni roles (`rol`, `usuario`, `rol_usuario` pertenecen a la v3).
- Consultas multitabla del dashboard (v4).

## 3. Criterios de Aceptación
1. **Regresión v1:** Todos los endpoints y pantallas de las 6 tablas de la v1 siguen funcionando sin cambios.
2. **Integridad referencial:** Intentar crear un registro con una llave foránea inexistente en `POST` o `PUT` devuelve error controlado (`400` o `500` con detalle de llave foránea) sin corromper datos.
3. **Tablas puente:** Permiten consultar por llave compuesta `GET /api/{tabla}/{fk1}/{fk2}`, crear, actualizar (donde aplique) y eliminar lógicamente (`DELETE /api/{tabla}/{fk1}/{fk2}`).
4. **Listas desplegables en Frontend:** Ningún formulario pide digitar manualmente el ID de una FK; todos cargan opciones legibles desde la API.