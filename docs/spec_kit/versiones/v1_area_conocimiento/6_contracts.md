# Contratos HTTP — Versión 1 (API + Frontend)

> Base API: `http://localhost:8025` · Swagger: `/docs` · Base Front: `http://localhost:8078`

## 1. Convenciones Globales API
- **Listado (`GET /api/{tabla}[?limite=N]`):** `200` con `{"tabla": "<nombre>", "limite": 1000, "total": N, "datos": [...]}` si hay filas activas; **`204`** (sin cuerpo) si no hay filas activas; **`400`** si `limite <= 0`.
- **Obtener (`GET /api/{tabla}/{id}`):** `200` con el objeto JSON en camelCase; **`404`** si no existe o `activo = FALSE`.
- **Crear (`POST /api/{tabla}`):** `200` con `{"estado": 200, "mensaje": "..."}` (en `linea_investigacion` devuelve también el `id` creado). **`422`** si falla validación Pydantic (`{"estado": 422, "mensaje": "Datos inválidos.", "errores": [...]}`); **`500`** si la PK ya existe.
- **Reemplazar (`PUT /api/{tabla}/{id}`):** Exige **todos** los campos editables (`422` si falta alguno). Devuelve `200` con `{"estado": 200, "mensaje": "...", "filasAfectadas": 1}` o `404`.
- **Actualizar parcial (`PATCH /api/{tabla}/{id}`):** Acepta subconjunto de campos (`200`). Devuelve `400` si el cuerpo está vacío `{}` y `404` si no existe o está inactivo.
- **Eliminar (`DELETE /api/{tabla}/{id}`):** Borrado lógico (`activo = FALSE`). Devuelve `200` con `filasAfectadas: 1`, o `404` si no existe o ya estaba inactivo.

## 2. Endpoints Específicos por Recurso
1. `GET /` → `{"mensaje": "API Investigación — v1", "version": "v1", "contratos": "/docs"}`
2. **Áreas de Conocimiento:** `/api/area_conocimiento` y `/api/area_conocimiento/{id}` (`id`, `granArea`, `area`, `disciplina`)
3. **ODS:** `/api/objetivo_desarrollo_sostenible` y `/api/objetivo_desarrollo_sostenible/{id}` (`id`, `nombre`, `categoria`)
4. **Áreas de Aplicación:** `/api/area_aplicacion` y `/api/area_aplicacion/{id}` (`id`, `nombre`)
5. **Términos Clave:** `/api/termino_clave` y `/api/termino_clave/{termino}` (`termino`, `terminoIngles`)
6. **Universidades:** `/api/universidad` y `/api/universidad/{id}` (`id`, `nombre`, `tipo`, `ciudad`)
7. **Líneas de Investigación:** `/api/linea_investigacion` y `/api/linea_investigacion/{id}` (`id` solo salida, `nombre`, `descripcion`)

## 3. Rutas del Frontend Flask (`http://localhost:8078`)
- `/` → Inicio con tarjetas hacia los 6 catálogos.
- `/areas-de-conocimiento` → Gestión de `area_conocimiento`.
- `/ods` → Gestión de `objetivo_desarrollo_sostenible`.
- `/areas-aplicacion` → Gestión de `area_aplicacion`.
- `/terminos-clave` → Gestión de `termino_clave`.
- `/universidades` → Gestión de `universidad`.
- `/lineas-investigacion` → Gestión de `linea_investigacion`.

Cada formulario de edición incluye ambos botones exigidos por la Constitución: **«Guardar la ficha completa»** (`PUT`) y **«Guardar solo lo que cambié»** (`PATCH`), conservando los datos escritos ante error y traduciendo los `422` al español.