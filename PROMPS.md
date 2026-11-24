# V1

@workspace Actúa como arquitecto e ingeniero de software senior. Tu tarea es construir desde cero y por completo la VERSIÓN 1 del proyecto de aula (Módulo Investigación) siguiendo estrictamente `docs/spec_kit/1_constitution.md` y todos los documentos dentro de `docs/spec_kit/versiones/v1_tablas_base/`.

Antes de crear o editar cualquier archivo, lee `docs/spec_kit/1_constitution.md`, los archivos de `docs/spec_kit/versiones/v1_tablas_base/` y `db/init.sql` (el cual es SOLO LECTURA y NO debes modificar).

### ALCANCE Y REGLAS INQUEBRANTABLES DE LA VERSIÓN 1:

1. **Alcance Estricto (6 Tablas Independientes sin FK):**
   El código de la v1 SOLO puede nombrar e interactuar con estas 6 tablas exactas definidas en `db/init.sql`:
   - `area_conocimiento`: `id VARCHAR(6)` (PK manual), `gran_area VARCHAR(60)`, `area VARCHAR(60)`, `disciplina VARCHAR(150)`.
   - `objetivo_desarrollo_sostenible`: `id INT` (PK manual), `nombre VARCHAR(60)`, `categoria VARCHAR(45)`.
   - `area_aplicacion`: `id INT` (PK manual), `nombre VARCHAR(150)`.
   - `termino_clave`: `termino VARCHAR(30)` (PK texto manual), `termino_ingles VARCHAR(30)` (opcional/nullable).
   - `universidad`: `id INT` (PK manual), `nombre VARCHAR(60)`, `tipo VARCHAR(45)`, `ciudad VARCHAR(45)`.
   - `linea_investigacion`: `id SERIAL` (PK autoincremental generada por BD, NO se envía en POST), `nombre VARCHAR(45)`, `descripcion VARCHAR(256)`.
   *(Prohibido mencionar tablas de v2 o v3, JWT, usuarios o roles en esta versión).*

2. **Infraestructura, Docker y Secretos (Art. 4, 7 y 10):**
   - Crea `.env.example` y `.env` (y agrega `.env` a `.gitignore`) con: `POSTGRES_USER=investigacion`, `POSTGRES_PASSWORD=investigacion_pass`, `POSTGRES_DB=investigacion_local`, `DATABASE_URL=postgresql+asyncpg://investigacion:investigacion_pass@postgres:5432/investigacion_local` y `URL_API_INVESTIGACION=http://api-investigacion:8025`.
   - Crea `docker-compose.yml` con prefijo de contenedores `paradigmas-investigacion-` y 3 servicios:
     * `postgres`: imagen `postgres:16`, puerto `15440:5432`, montando `./db/init.sql:/docker-entrypoint-initdb.d/init.sql` y con `healthcheck` (`pg_isready`).
     * `api-investigacion`: puerto `8025:8025`, `depends_on: postgres: condition: service_healthy`, corriendo `uvicorn main:app --host 0.0.0.0 --port 8025 --reload`.
     * `front-flask`: puerto `8078:8078`, SIN `depends_on` hacia `postgres`.

3. **Backend FastAPI (`api_investigacion/` - Art. 2, 3, 6, 8, 9, 10):**
   - **Prohibido usar ORM** para consultas y prohibido crear rutas genéricas `/api/{tabla}`. Usa `sqlalchemy[asyncio]` + `asyncpg` ejecutando SQL escrito a mano con `text()` y parámetros `:parametro`.
   - Implementa arquitectura en **3 capas con interfaces `typing.Protocol`** para cada una de las 6 tablas:
     * `models/`: 3 esquemas Pydantic por tabla (`Crear`, `Reemplazo` para PUT, `Actualizar` para PATCH) exponiendo **camelCase** en JSON (`granArea`, `terminoIngles`, `filasAfectadas`) mediante `Field(alias=...)` y `populate_by_name=True`, mientras Python y SQL usan `snake_case`.
     * `repositorios/abstracciones/` y `repositorios/`: Interfaces `IRepositorio...` e implementaciones PostgreSQL con `text()`. Todos los `SELECT` filtran `WHERE activo = TRUE`. El `DELETE` ejecuta borrado lógico en una sola consulta: `UPDATE tabla SET activo = FALSE WHERE pk = :id AND activo = TRUE`.
     * `servicios/abstracciones/`, `servicios/` y `servicios/ensamblador.py`: Interfaces `IServicio...` y lógica de negocio que lanza `ValueError` (para reglas como `limite <= 0` o `PATCH {}` vacío) y `LookupError` (si no existe o afectó 0 filas), sin importar nada de FastAPI.
     * `controllers/` y `main.py`: 6 controladores específicos (`APIRouter`) con `GET /api/{tabla}`, `GET /api/{tabla}/{id}`, `POST /api/{tabla}`, `PUT /api/{tabla}/{id}`, `PATCH /api/{tabla}/{id}`, `DELETE /api/{tabla}/{id}`:
       - Listado sin filas activas → `Response(status_code=204)` sin cuerpo.
       - `ValueError` → `400`, `LookupError` → `404`, errores de integridad/BD → `500` con detalle.
       - Manejador global de `RequestValidationError` devolviendo `422` con formato exacto: `{"estado": 422, "mensaje": "Datos inválidos.", "detalle": "Error de validación en los campos enviados.", "errores": [...]}`.
       - Endpoint raíz `GET /` → `{"mensaje": "API Investigación — v1", "version": "v1", "contratos": "/docs"}`.
   - Crea `api_investigacion/pruebas/prueba_capas.py`: script ejecutable con `python pruebas/prueba_capas.py` que prueba los servicios inyectando repositorios falsos en memoria (sin conexión a PostgreSQL).
   - **Comentarios obligatorios (Art. 8):** En cada archivo Python, escribe comentarios en español explicando **POR QUÉ** se tomó cada decisión arquitectónica (separación de capas, SQL parametrizado, borrado lógico, diferencia PUT vs PATCH), no qué hace la sintaxis.

4. **Frontend Flask (`front_flask/` - Art. 1.1 y 12):**
   - `requirements.txt` debe tener ÚNICAMENTE `flask` y `requests` (prohibido `asyncpg`, `sqlalchemy` o importar archivos de `api_investigacion`).
   - `cliente_api.py`: funciones explícitas por cada recurso y operación (ej. `listar_areas_conocimiento`, `crear_area_conocimiento`, etc. — prohibido cliente genérico), manejando `204` como lista vacía sin error, capturando `requests.exceptions.RequestException` si la API está apagada, y traduciendo al español los mensajes de error `422` de Pydantic.
   - `app.py` y `templates/`: rutas propias (`/`, `/areas-de-conocimiento`, `/ods`, `/areas-aplicacion`, `/terminos-clave`, `/universidades`, `/lineas-investigacion`), listado y formulario de creación/edición para cada una. En edición, incluye ambos botones: **«Guardar la ficha completa»** (`PUT`) y **«Guardar solo lo que cambié»** (`PATCH`), manteniendo los valores ingresados si ocurre un error.
   - **Identidad Visual Universidad Monte Verde (Art. 12):** Prohibido usar Bootstrap o cualquier CDN externo. Crea `front_flask/static/marca.css` con las variables CSS oficiales (`--umv-verde: #1F5E4C`, `--umv-ocre: #D99B26`, etc.) y `front_flask/static/estilos.css` consumiendo exclusivamente esas variables (`var(--umv-...)`).

Construye todos los archivos de forma ordenada y completa. Al finalizar, ejecuta o indícame los comandos exactos en PowerShell para levantar `docker compose up -d --build` y correr las verificaciones de `7_quickstart.md`.



# V2

@workspace Actúa como arquitecto e ingeniero de software senior. Vamos a implementar la PRIMERA MITAD de la VERSIÓN 2 del proyecto de aula (Módulo Investigación).

Antes de crear o editar cualquier archivo, lee ÚNICAMENTE `docs/spec_kit/1_constitution.md`, los documentos dentro de `docs/spec_kit/versiones/v2_tablasfk/` y `db/init.sql`.
REGLA CRÍTICA DE SOLO LECTURA: Tienes ESTRICTAMENTE PROHIBIDO crear, editar o eliminar cualquier archivo dentro de la carpeta `docs/` (donde viven los spec_kits) o dentro de `db/`.

Mantén intactas las 6 tablas de la v1 (regresión obligatoria) y agrega exactamente estas **5 tablas relacionales** respetando la misma arquitectura de 3 capas con interfaces `typing.Protocol`, SQL escrito a mano con `text()` y `:parametro` (prohibido usar ORM), camelCase en JSON mediante `Field(alias=...)`, borrado lógico (`activo = FALSE`), manejo de `204` en listas vacías y comentarios en español explicando el **POR QUÉ** de cada decisión técnica:

1. `docente` (PK: `cedula INT` — FK opcional: `linea_investigacion_principal INT` -> `linea_investigacion(id)`). Respeta los nombres exactos de columnas en `db/init.sql` incluyendo `nacionalidaad` y `cat_minciencia` nullable (exponiendo `nacionalidad` y `catMinciencia` en JSON).
2. `grupo_investigacion` (PK: `id INT` — FK opcional: `universidsad INT` -> `universidad(id)`). Respeta el nombre exacto de columna `universidsad` en SQL y expón `universidad` en JSON.
3. `semillero` (PK: `id INT` — FK obligatoria: `grupo_investigacion INT` -> `grupo_investigacion(id)`).
4. `participa_grupo` (PK compuesta: `docente_cedula INT` + `grupo_investigacion_id INT`, campos: `rol VARCHAR(15)`, `fecha_inicio DATE`, `fecha_fin DATE` opcional). Rutas: `GET /api/participa_grupo`, `POST /api/participa_grupo`, `GET/PUT/PATCH/DELETE /api/participa_grupo/{docente_cedula}/{grupo_investigacion_id}`.
5. `participa_semillero` (PK compuesta: `docente INT` + `semillero INT`, campos: `rol VARCHAR(15)`, `fecha_inicio DATE`, `fecha_fin DATE` opcional). Rutas: `GET /api/participa_semillero`, `POST /api/participa_semillero`, `GET/PUT/PATCH/DELETE /api/participa_semillero/{docente}/{semillero}`.

REQUISITOS DE FRONTEND FLASK (`front_flask/`):
- Agrega funciones explícitas en `cliente_api.py` (sin cliente genérico) y sus rutas/plantillas en `app.py` (`/docentes`, `/grupos-investigacion`, `/semilleros`, `/participa-grupo`, `/participa-semillero`).
- **Regla obligatoria de v2:** En todos los formularios de creación y edición, las llaves foráneas DEBEN ser etiquetas `<select>` desplegables cargadas consumiendo los endpoints `GET` de la API (nunca inputs numéricos manuales para FKs).
- Conserva los dos botones en edición: «Guardar la ficha completa» (`PUT`) y «Guardar solo lo que cambié» (`PATCH`), usando únicamente `marca.css` y `estilos.css` sin Bootstrap ni CDN.

Genera todos los archivos de `api_investigacion/` y `front_flask/` para estas 5 tablas de forma ordenada.

===============================================================

@workspace Ahora completa la SEGUNDA MITAD de la VERSIÓN 2 leyendo `docs/spec_kit/1_constitution.md`, `docs/spec_kit/versiones/v2_tablasfk/` y `db/init.sql`.
REGLA CRÍTICA DE SOLO LECTURA: Tienes ESTRICTAMENTE PROHIBIDO modificar o eliminar cualquier archivo dentro de `docs/` o `db/`.

Implementa las **5 tablas puente** restantes de `db/init.sql`, manteniendo intactas las 6 tablas de v1 y las 5 tablas del Bloque A:

1. `grupo_linea` (PK compuesta: `grupo_investigacion INT` + `linea_investigacion INT`).
2. `semillero_linea` (PK compuesta: `semillero INT` + `linea_investigacion INT`).
3. `ac_linea` (PK compuesta: `linea_investigacion INT` + `area_conocimiento VARCHAR(6)`).
4. `ods_linea` (PK compuesta: `linea_investigacion INT` + `ods INT`).
5. `aa_linea` (PK compuesta: `area_aplicacion INT` + `linea_investigacion INT`).

REGLAS TÉCNICAS PARA ESTAS 5 TABLAS PUENTE:
- Backend (`api_investigacion/`): 3 capas con interfaces `Protocol`, SQL `text()` sin ORM, camelCase en JSON, borrado lógico (`UPDATE tabla SET activo = FALSE WHERE fk1 = :fk1 AND fk2 = :fk2 AND activo = TRUE`), `GET /api/{tabla}` (`204` si está vacía), `GET /api/{tabla}/{fk1}/{fk2}`, `POST /api/{tabla}` y `DELETE /api/{tabla}/{fk1}/{fk2}`. Registra todos los routers de la v2 en `main.py` y actualiza la versión del endpoint raíz `GET /` a `"v2"`.
- Frontend (`front_flask/`): Funciones explícitas en `cliente_api.py` y pantallas propias en `app.py` (`/grupo-linea`, `/semillero-linea`, `/ac-linea`, `/ods-linea`, `/aa-linea`) con listas desplegables `<select>` cargadas desde la API para seleccionar ambas entidades a vincular.
- Actualiza `templates/base.html` e `inicio.html` organizando claramente en el menú los módulos de Catálogos Base (v1) y los módulos Relacionales (v2), respetando `marca.css` sin CDN externos.

Al finalizar, dame el comando para reconstruir los contenedores con Docker Compose y verificar que los 16 recursos de dominio aparecen en Swagger.


# V3


@workspace Actúa como arquitecto e ingeniero de software senior. Vamos a implementar la VERSIÓN 3 completa del proyecto de aula (Módulo Investigación: Autenticación JWT, Contraseñas Hasheadas con bcrypt, Control de Acceso por Roles RBAC y CRUD de Seguridad).

Antes de crear o editar cualquier archivo, lee ÚNICAMENTE `docs/spec_kit/1_constitution.md`, los documentos dentro de `docs/spec_kit/versiones/v3_log/` y `db/init.sql`.
REGLA CRÍTICA DE SOLO LECTURA: Tienes ESTRICTAMENTE PROHIBIDO crear, editar o eliminar cualquier archivo dentro de `docs/` o `db/`.

### REQUERIMIENTOS EXACTOS DE LA VERSIÓN 3:

1. **Variables de Entorno y Dependencias (Art. 7):**
   - Agrega a `.env.example` y `.env`: `JWT_SECRET=clave_secreta_investigacion_2026_segura`, `JWT_ALGORITHM=HS256`, `JWT_EXPIRE_MINUTES=120` y `FLASK_SECRET_KEY=clave_sesion_flask_investigacion_2026`.
   - En `api_investigacion/requirements.txt`, agrega `PyJWT` y `bcrypt` (usa `bcrypt` directamente, NO `passlib`). En `front_flask/requirements.txt` mantén ÚNICAMENTE `flask` y `requests`.

2. **Seguridad JWT, RBAC y Bootstrapping en `lifespan` (`api_investigacion/`):**
   - Crea el módulo `api_investigacion/seguridad/` con:
     * Hasheo y verificación de contraseñas con `bcrypt.hashpw` / `bcrypt.checkpw`.
     * Creación y validación de tokens JWT HS256 leyendo `JWT_SECRET` desde variables de entorno.
     * Dependencias FastAPI `obtener_usuario_actual` (valida `Authorization: Bearer <token>` y responde `401` si falta, es inválido o el usuario está inactivo) y `requerir_roles(*roles_permitidos)` (responde `403` si el usuario no tiene ninguno de los roles exigidos).
   - Configura un evento `lifespan` en `api_investigacion/main.py` que, al arrancar la API, siembre de forma idempotente (`ON CONFLICT DO NOTHING`):
     * Roles: `ADMIN`, `INVESTIGADOR`, `CONSULTOR`.
     * Usuarios iniciales con contraseña hasheada:
       - `admin` / `Admin123*` (`admin@umv.edu.co`, rol `ADMIN`)
       - `juanjoherrera` / `Invest123*` (`juanjo@umv.edu.co`, rol `INVESTIGADOR`)
       - `consultor` / `Consult123*` (`consultor@umv.edu.co`, rol `CONSULTOR`)
   - Crea el endpoint público `POST /api/login` que valida `username` y `password`, consulta los roles activos del usuario y retorna `{"accessToken": "...", "tokenType": "bearer", "usuario": {"id": ..., "username": ..., "email": ..., "nombreCompleto": ..., "roles": [...]}}` (o `401` si falla).
   - Configura `HTTPBearer` en FastAPI para que Swagger (`/docs`) muestre el botón **Authorize** y permita probar endpoints con el token.

3. **CRUD de Seguridad (3 Capas con `Protocol` + SQL `text()` sin ORM) — SOLO ROL `ADMIN`:**
   - Implementa `rol` (`id SERIAL`, `nombre`, `descripcion`, borrado lógico `activo = FALSE`), `usuario` (`id SERIAL`, `username`, `password` hasheada al crear/actualizar, `email`, `nombre_completo`, borrado lógico `activo = FALSE`, **NUNCA devolver `password` en los `GET`**) y `rol_usuario` (`usuario_id`, `rol_id`, PK compuesta, rutas `GET /api/rol_usuario`, `GET /api/rol_usuario/{usuario_id}/{rol_id}`, `POST /api/rol_usuario`, `DELETE /api/rol_usuario/{usuario_id}/{rol_id}`).
   - Protege todos los endpoints de `/api/rol`, `/api/usuario` y `/api/rol_usuario` exigiendo rol `ADMIN` (`403` si no lo tiene).

4. **Protección de los 16 Recursos de Dominio (Regresión v1 + v2) y `GET /`:**
   - Protege TODOS los routers de las 16 tablas de v1 y v2:
     * Todos los `GET` requieren usuario autenticado (`ADMIN`, `INVESTIGADOR` o `CONSULTOR`).
     * Todos los `POST`, `PUT`, `PATCH` y `DELETE` requieren rol `ADMIN` o `INVESTIGADOR` (`CONSULTOR` recibe `403`).
   - Actualiza `GET /` para que responda `"version": "v3"`.
   - Mantén comentarios en español explicando el **POR QUÉ** de cada decisión técnica.

5. **Frontend Flask con Sesión, Menú por Rol y Protección Proxy (`front_flask/`):**
   - Configura `ProxyFix(app.wsgi_app, x_proto=1, x_host=1)` y `app.secret_key = os.getenv("FLASK_SECRET_KEY", ...)` en `app.py` para evitar errores `400 Bad Request` detrás de proxies HTTPS como Render.
   - Implementa `/login` (formulario limpio con `marca.css` mostrando credenciales de prueba como ayuda) y `/logout`.
   - Protege todas las vistas del frontend: si no hay token en `session`, redirige a `/login`. Si la API responde `401`, limpia la sesión y redirige a `/login`.
   - Envía la cabecera `Authorization: Bearer <token>` en todas las peticiones de `cliente_api.py`.
   - Agrega las pantallas de administración `/usuarios`, `/roles` y `/rol-usuario` (con `<select>` de usuarios y roles), protegidas para que solo las vea y acceda un usuario con rol `ADMIN`.
   - En `templates/base.html` y las plantillas de listas/formularios, muestra el usuario logueado y su rol, oculta el menú de Administración a quienes no sean `ADMIN`, y oculta botones de crear/editar/retirar a usuarios que solo tengan rol `CONSULTOR`.

Construye todos los archivos de forma ordenada y completa. Al finalizar, indícame el comando para reconstruir en Docker y probar el flujo completo de v3.

===============================================================

@workspace Actúa como diseñador UI/UX senior y desarrollador frontend especialista en Flask + Jinja2. Tu única tarea en este paso es rediseñar y pulir por completo la capa visual y las plantillas de `front_flask/` usando la plantilla **Modern Business** (Start Bootstrap), manteniendo intacta toda la lógica funcional, rutas de `app.py`, `cliente_api.py` y el backend `api_investigacion/`.

### REGLAS ESTRICTAS DE ARCHIVOS Y DEPENDENCIAS:
- NO modifiques `api_investigacion/`, `db/` ni `docs/`.
- **Plantilla Modern Business (Local, sin CDN):** Descarga y guarda localmente dentro de `front_flask/static/` los recursos de la plantilla oficial:
  1. CSS compilado (`front_flask/static/bootstrap-modern.css`): `https://raw.githubusercontent.com/StartBootstrap/startbootstrap-modern-business/master/dist/css/styles.css`
  2. JS interactivo (`front_flask/static/bootstrap.bundle.min.js`): `https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js` (descárgalo como archivo local para que funcionen los menús desplegables `dropdown` sin depender de internet ni CDN en tiempo de ejecución).
  3. Toma como referencia estructural: `https://raw.githubusercontent.com/StartBootstrap/startbootstrap-modern-business/master/dist/index.html`
- **Identidad Institucional (`front_flask/static/marca.css`):** Carga `/static/bootstrap-modern.css` primero y luego `/static/marca.css` para sobrescribir los colores primarios y oscuros de Bootstrap (`--bs-primary`, `--bs-dark`, `.bg-dark`, `.btn-primary`) con los colores institucionales de **Universidad Monte Verde** (`--umv-verde: #1F5E4C`, `--umv-verde-oscuro: #143D32`, `--umv-ocre: #D99B26`, `--umv-crema: #F6F5F0`), manteniendo el logo oficial de la universidad en la barra superior y el login.

---

### CAMBIOS VISUALES Y DE EXPERIENCIA OBLIGATORIOS:

1. **Pantalla de Login (`templates/login.html`):**
   - Diseño centrado tipo tarjeta moderna de Bootstrap (`card shadow-sm border-0`) con cabecera institucional de Universidad Monte Verde y el logo.
   - **ELIMINA POR COMPLETO** cualquier texto, recuadro o ayuda que muestre credenciales de prueba (`admin`, `juanjoherrera`, `consultor` o contraseñas). Solo debe mostrar el título "Iniciar sesión", campos de Usuario y Contraseña, alertas de error si fallan credenciales y el botón de ingresar.

2. **Barra de Navegación Limpia estilo *Modern Business* (`templates/base.html`):**
   - Navbar oscura arriba (`navbar navbar-expand-lg navbar-dark bg-dark`) con el logo de Universidad Monte Verde + título **"Módulo de Investigación"**.
   - Agrupa los enlaces de navegación en **menús desplegables (`nav-item dropdown`)** limpios de Bootstrap 5:
     * **Inicio** (`/`)
     * **Catálogos** (Áreas de conocimiento, ODS, Áreas de aplicación, Términos clave, Universidades, Líneas de investigación)
     * **Investigación** (Docentes, Grupos de investigación, Semilleros)
     * **Vínculos y Participación** (Participación en grupos, Participación en semilleros, Grupo – Línea, Semillero – Línea, Área conocimiento – Línea, ODS – Línea, Área aplicación – Línea)
     * **Administración** *(Visible ÚNICAMENTE si el usuario autenticado tiene rol `ADMIN`)*: Usuarios, Roles, Asignación de Roles.
   - A la derecha de la navbar: nombre del usuario logueado con una insignia (`badge`) de su rol y botón estilizado **Cerrar sesión**.

3. **Página de Inicio (`templates/inicio.html`) limpia y sin etiquetas de versiones:**
   - **ELIMINA POR COMPLETO** los textos `(v1)`, `(v2)`, `(v3)` o cualquier mención a versiones de desarrollo en títulos, encabezados, subtítulos y menús.
   - Incluye la **Hero Section oscura** característica de *Modern Business* (`bg-dark py-5` con colores Monte Verde), título de bienvenida al Módulo de Investigación, breve descripción del sistema y botones de acceso rápido (`btn-primary` y `btn-outline-light`) hacia **Docentes** y **Grupos de Investigación**.
   - Debajo, muestra la cuadrícula de tarjetas (`row g-4` + `card h-100 shadow-sm`) con todas las tablas disponibles organizadas por dominio funcional (**Catálogos Institucionales**, **Actores y Grupos de Investigación**, **Relaciones y Líneas** y, solo visible para `ADMIN`, **Seguridad y Administración**).

4. **Consistencia en Tablas y Formularios (`templates/`):**
   - Estiliza todas las vistas de listado (`lista.html`) y formularios (`formulario.html`) de las 19 entidades usando las clases de Bootstrap 5 (`table table-hover align-middle`, `table-dark` en cabecera, `card shadow-sm`, `form-control`, `form-select`, `btn`).
   - Respeta el control por rol: si el usuario tiene rol `CONSULTOR`, oculta los botones de crear nuevo registro, editar y retirar en todas las vistas.
   - Conserva intactos los dos botones en todos los formularios de edición: **«Guardar la ficha completa»** (`PUT`) y **«Guardar solo lo que cambié»** (`PATCH`).

Actualiza los archivos estáticos en `front_flask/static/` y todas las plantillas HTML en `front_flask/templates/`. Al finalizar, dame el comando para reconstruir `front-flask` en Docker Compose.