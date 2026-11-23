# Rutas y contratos — v2

Todas las colecciones aceptan `?limite=1000`; límite no positivo: 400.
Colección activa vacía: 204. Con filas: `{tabla, limite, total, datos}`.
POST: 200. PUT/PATCH/DELETE: 200 con `filasAfectadas`. Validación: 422.

| Tabla | Colección GET/POST | Registro GET/PUT/PATCH/DELETE |
|---|---|---|
| `docente` | `/api/docente` | `/api/docente/{cedula}` |
| `grupo_investigacion` | `/api/grupo_investigacion` | `/api/grupo_investigacion/{id}` |
| `semillero` | `/api/semillero` | `/api/semillero/{id}` |
| `participa_semillero` | `/api/participa_semillero` | `/api/participa_semillero/{docente}/{semillero}` |
| `participa_grupo` | `/api/participa_grupo` | `/api/participa_grupo/{docente_cedula}/{grupo_investigacion_id}` |
| `semillero_linea` | `/api/semillero_linea` | `/api/semillero_linea/{semillero}/{linea_investigacion}` |
| `grupo_linea` | `/api/grupo_linea` | `/api/grupo_linea/{grupo_investigacion}/{linea_investigacion}` |
| `ac_linea` | `/api/ac_linea` | `/api/ac_linea/{linea_investigacion}/{area_conocimiento}` |
| `ods_linea` | `/api/ods_linea` | `/api/ods_linea/{linea_investigacion}/{ods}` |
| `aa_linea` | `/api/aa_linea` | `/api/aa_linea/{area_aplicacion}/{linea_investigacion}` |

Los cuatro catálogos de soporte tienen únicamente GET de colección y de registro.
Consulte `/docs` para los campos y tipos exactos de cada cuerpo.
