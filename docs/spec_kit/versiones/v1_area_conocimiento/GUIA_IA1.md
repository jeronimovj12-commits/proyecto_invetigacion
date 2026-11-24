# Guía de Construcción con IA — Versión 1 (`GUIA_IA1.md`)

> **Versión 1** ([mapa](../0_mapa_versiones.md)) · Rige la [constitución](../../1_constitution.md)[cite: 8, 9, 13].
> Este documento registra el procedimiento real seguido con asistencia de IA (arquitectura y generación de código) para pasar de la especificación (`2_spec.md` a `8_tasks.md`) al sistema funcional[cite: 6, 9].

## 1. Flujo de Trabajo y Herramientas

* **Herramienta utilizada:** IDE Agéntico / Asistente de programación (ChatGPT Pro / Workspace) supervisado fase por fase contra `8_tasks.md`[cite: 9, 11].
* **Insumos entregados a la IA:** `1_constitution.md` y los documentos de `docs/spec_kit/versiones/v1_tablas_base/` (`2_spec.md` hasta `8_tasks.md`), dejando `db/init.sql` como artefacto de solo lectura[cite: 11, 17, 18].
* **Regla de supervisión:** Ningún código se da por terminado sin verificar la separación estricta API/Frontend, el borrado lógico (`activo = FALSE`), el contraste `PUT` (`422`) vs `PATCH` (`200`) y la ejecución del smoke test de `7_quickstart.md`.

---

## 2. Prompt Principal Utilizado (Generación de la Versión 1)

```text
@workspace Actúa como ingeniero de software senior. Vamos a construir desde cero y de forma limpia la VERSIÓN 1 completa del proyecto de aula (Módulo Investigación) cumpliendo al pie de la letra `docs/spec_kit/1_constitution.md` y los documentos de `docs/spec_kit/versiones/v1_tablas_base/`.

ALCANCE EXACTO DE LA VERSIÓN 1:
1. **Base de datos (`db/init.sql`):** Ya existe y crea las 19 tablas. NO lo modifiques. El código de la v1 SOLO puede interactuar con las **6 tablas sin llaves foráneas**:
   - `area_conocimiento` (PK: `id VARCHAR(6)`, `gran_area VARCHAR(60)`, `area VARCHAR(60)`, `disciplina VARCHAR(150)`)
   - `objetivo_desarrollo_sostenible` (PK: `id INT`, `nombre VARCHAR(60)`, `categoria VARCHAR(45)`)
   - `area_aplicacion` (PK: `id INT`, `nombre VARCHAR(150)`)
   - `termino_clave` (PK: `termino VARCHAR(30)`, `termino_ingles VARCHAR(30)` opcional)
   - `universidad` (PK: `id INT`, `nombre VARCHAR(60)`, `tipo VARCHAR(45)`, `ciudad VARCHAR(45)`)
   - `linea_investigacion` (PK: `id SERIAL` autoincremental en BD, `nombre VARCHAR(45)`, `descripcion VARCHAR(256)`)

2. **Infraestructura y Secretos (Art. 4 y 7):**
   - Crea `.env.example` y `.env` (y asegúrate de que `.env` esté en `.gitignore`) con `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB=investigacion_local`, `DATABASE_URL=postgresql+asyncpg://...` y `URL_API_INVESTIGACION=http://api-investigacion:8025`.
   - Crea `docker-compose.yml` con 3 servicios:
     * `postgres` (puerto `15440:5432`, montando `./db/init.sql:/docker-entrypoint-initdb.d/init.sql`, con `healthcheck`).
     * `api-investigacion` (puerto `8025:8025`, `depends_on: postgres: condition: service_healthy`).
     * `front-flask` (puerto `8078:8078`, SIN `depends_on` hacia `postgres`).

3. **Backend FastAPI (`api_investigacion/` - Art. 2, 3, 6, 8, 9, 10):**
   - **Prohibido usar ORM** para consultas y prohibido crear rutas genéricas `/api/{tabla}`.
   - Usa SQLAlchemy Core (`text()` con `:parametro`) y `asyncpg`.
   - Implementa arquitectura en **3 capas con interfaces `Protocol`** (`controllers/`, `models/`, `servicios/` + `servicios/abstracciones/` + `ensamblador.py`, `repositorios/` + `repositorios/abstracciones/`) para cada una de las 6 tablas.
   - Tres modelos Pydantic por tabla (`Crear`, `Reemplazo` para PUT, `Actualizar` para PATCH) usando `Field(alias=...)` para exponer camelCase en JSON (`granArea`, `terminoIngles`, `filasAfectadas`) mientras Python y SQL usan snake_case.
   - Endpoints específicos por tabla (`GET` listado con `?limite=1000`, `GET/{id}`, `POST`, `PUT`, `PATCH`, `DELETE`):
     * Listado vacío → `204 No Content` sin cuerpo.
     * `limite <= 0` o `PATCH {}` vacío → `400`.
     * Validación Pydantic fallida → `422` con formato `{"estado": 422, "mensaje": "Datos inválidos.", "detalle": "...", "errores": [...]}`.
     * Registro inexistente o inactivo → `404`.
     * `DELETE` ejecuta borrado lógico (`UPDATE tabla SET activo = FALSE WHERE pk = :id AND activo = TRUE`) y todos los `SELECT` filtran `WHERE activo = TRUE`.
   - Incluye `GET /` devolviendo `{"mensaje": "API Investigación — v1", "version": "v1", "contratos": "/docs"}`.
   - Crea `api_investigacion/pruebas/prueba_capas.py` probando los servicios con repositorios falsos en memoria (sin BD).
   - **Comentarios obligatorios:** Todos los archivos deben tener comentarios en español explicando **POR QUÉ** se tomó cada decisión técnica (para sustentación oral), no qué hace la sintaxis.

4. **Frontend Flask (`front_flask/` - Art. 1.1 y 12):**
   - `requirements.txt` SOLO con `flask` y `requests` (sin drivers de BD ni imports de `api_investigacion`).
   - `cliente_api.py` con funciones explícitas por cada recurso y operación (nada de funciones genéricas) y traductor centralizado al español de los errores `422` de Pydantic.
   - Rutas propias en `app.py`: `/`, `/areas-de-conocimiento`, `/ods`, `/areas-aplicacion`, `/terminos-clave`, `/universidades`, `/lineas-investigacion`.
   - En cada formulario de edición, incluye los dos botones exigidos: **«Guardar la ficha completa»** (`PUT`) y **«Guardar solo lo que cambié»** (`PATCH`), manteniendo los datos del formulario si hay error, mostrando aviso amigable en `204` (sin filas) y manteniendo la app en pie si la API está apagada.
   - Estilos escritos 100% a mano en `static/marca.css` (paleta institucional Universidad Monte Verde `#1F5E4C`, `#D99B26`, etc.) y `static/estilos.css`. Prohibido usar Bootstrap o CDN externos.

Genera todos los archivos necesarios en orden limpio. Al terminar, indícame el comando para levantar Docker y verificar los endpoints.