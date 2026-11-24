# Modelo de Datos — Versión 1 (6 Tablas Independientes)

La base `investigacion_local` se crea con sus 19 tablas desde `db/init.sql`, pero la v1 opera exclusivamente sobre estas **6 tablas sin llaves foráneas**:

## 1. `area_conocimiento` (218 filas semilla)
| Columna | Tipo | Restricción | JSON camelCase |
|---|---|---|---|
| `id` | `VARCHAR(6)` | PK (manual en POST) | `id` |
| `gran_area` | `VARCHAR(60)` | NOT NULL | `granArea` |
| `area` | `VARCHAR(60)` | NOT NULL | `area` |
| `disciplina` | `VARCHAR(150)` | NOT NULL | `disciplina` |
| `activo` | `BOOLEAN` | DEFAULT TRUE (solo DELETE) | *(interno)* |

## 2. `objetivo_desarrollo_sostenible` (17 filas semilla)
| Columna | Tipo | Restricción | JSON camelCase |
|---|---|---|---|
| `id` | `INT` | PK (manual en POST) | `id` |
| `nombre` | `VARCHAR(60)` | NOT NULL | `nombre` |
| `categoria` | `VARCHAR(45)` | NOT NULL | `categoria` |
| `activo` | `BOOLEAN` | DEFAULT TRUE (solo DELETE) | *(interno)* |

## 3. `area_aplicacion` (21 filas semilla)
| Columna | Tipo | Restricción | JSON camelCase |
|---|---|---|---|
| `id` | `INT` | PK (manual en POST) | `id` |
| `nombre` | `VARCHAR(150)` | NOT NULL | `nombre` |
| `activo` | `BOOLEAN` | DEFAULT TRUE (solo DELETE) | *(interno)* |

## 4. `termino_clave` (0 filas semilla)
| Columna | Tipo | Restricción | JSON camelCase |
|---|---|---|---|
| `termino` | `VARCHAR(30)` | PK texto (manual en POST) | `termino` |
| `termino_ingles` | `VARCHAR(30)` | NULL permitido | `terminoIngles` |
| `activo` | `BOOLEAN` | DEFAULT TRUE (solo DELETE) | *(interno)* |

## 5. `universidad` (0 filas semilla)
| Columna | Tipo | Restricción | JSON camelCase |
|---|---|---|---|
| `id` | `INT` | PK (manual en POST) | `id` |
| `nombre` | `VARCHAR(60)` | NOT NULL | `nombre` |
| `tipo` | `VARCHAR(45)` | NOT NULL | `tipo` |
| `ciudad` | `VARCHAR(45)` | NOT NULL | `ciudad` |
| `activo` | `BOOLEAN` | DEFAULT TRUE (solo DELETE) | *(interno)* |

## 6. `linea_investigacion` (0 filas semilla)
| Columna | Tipo | Restricción | JSON camelCase |
|---|---|---|---|
| `id` | `SERIAL` | PK autoincremental (generada por BD) | `id` |
| `nombre` | `VARCHAR(45)` | NOT NULL | `nombre` |
| `descripcion` | `VARCHAR(256)` | NOT NULL | `descripcion` |
| `activo` | `BOOLEAN` | DEFAULT TRUE (solo DELETE) | *(interno)* |