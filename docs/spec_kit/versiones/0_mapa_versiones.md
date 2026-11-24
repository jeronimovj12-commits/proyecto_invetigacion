# Mapa de versiones — Módulo Investigación

> La ruta completa del proyecto. Cada versión se especifica **solo cuando
> la anterior está cerrada** (commit + tag). Este mapa da la dirección; el
> spec kit de cada versión da el detalle.

## La ruta

| Versión | Qué agrega (acumulativo) | Estado |
|---|---|---|
| **v1** | CRUD completo de las **6 tablas sin clave foránea**, API REST + Frontend Flask con marca UMV | **En curso** ([spec](v1_tablas_base/2_spec.md)) |
| v2 | CRUD de las **10 tablas con clave foránea**: listas desplegables desde la API e integridad referencial | Sin especificar |
| v3 | **JWT**, sesiones y control de acceso por roles; CRUD de `usuario`, `rol` y `rol_usuario` solo para administradores | Sin especificar |
| v4 | **10 consultas multitabla** (4+ tablas c/u), dashboard con gráficos, páginas corporativas, responsive/PWA y **publicación** | Sin especificar |

## Qué tabla entra en qué versión

| Versión | Tablas |
|---|---|
| **v1** | `area_conocimiento` · `objetivo_desarrollo_sostenible` · `area_aplicacion` · `termino_clave` · `universidad` · `linea_investigacion` |
| v2 | `docente` · `grupo_investigacion` · `semillero` · `participa_grupo` · `participa_semillero` · `grupo_linea` · `semillero_linea` · `ac_linea` · `ods_linea` · `aa_linea` |
| v3 | `rol` · `usuario` · `rol_usuario` |

## Reglas del mapa
1. **No se anticipa nada de una versión futura** (Artículo 1): en la v1 no aparece `usuario`, ni FK, ni JWT.
2. **Una versión cerrada no se reabre**: los ajustes van en la siguiente.
3. **Regresión obligatoria**: al cerrar la vN, los criterios de todas las versiones anteriores deben seguir pasando.