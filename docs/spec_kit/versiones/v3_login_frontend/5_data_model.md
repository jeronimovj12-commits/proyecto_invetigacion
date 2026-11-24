# Modelo de Datos — Versión 3 (Seguridad y RBAC)

## 1. `rol`
| Columna | Tipo | Restricción | JSON camelCase |
|---|---|---|---|
| `id` | `SERIAL` | PK autoincremental | `id` |
| `nombre` | `VARCHAR(100)` | NOT NULL UNIQUE | `nombre` |
| `descripcion` | `TEXT` | NULL | `descripcion` |
| `activo` | `BOOLEAN` | DEFAULT TRUE | *(interno)* |
| `fecha_creacion` | `TIMESTAMP` | DEFAULT CURRENT_TIMESTAMP | `fechaCreacion` |

## 2. `usuario`
| Columna | Tipo | Restricción | JSON camelCase |
|---|---|---|---|
| `id` | `SERIAL` | PK autoincremental | `id` |
| `username` | `VARCHAR(100)` | NOT NULL UNIQUE | `username` |
| `password` | `VARCHAR(255)` | NOT NULL (hash bcrypt; **nunca se expone en GET**) | `password` (solo entrada) |
| `email` | `VARCHAR(150)` | NOT NULL UNIQUE | `email` |
| `nombre_completo` | `VARCHAR(200)` | NULL | `nombreCompleto` |
| `activo` | `BOOLEAN` | DEFAULT TRUE | *(interno)* |
| `fecha_creacion` | `TIMESTAMP` | DEFAULT CURRENT_TIMESTAMP | `fechaCreacion` |
| `fecha_actualizacion` | `TIMESTAMP` | DEFAULT CURRENT_TIMESTAMP | `fechaActualizacion` |

## 3. `rol_usuario`
| Columna | Tipo | Restricción | JSON camelCase |
|---|---|---|---|
| `usuario_id` | `INT` | PK/FK $\rightarrow$ `usuario(id)` | `usuarioId` |
| `rol_id` | `INT` | PK/FK $\rightarrow$ `rol(id)` | `rolId` |