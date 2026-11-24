### 4. `4_research.md`

```markdown
# Decisiones Técnicas — Versión 1

- **D-v1-1 (SQLAlchemy Core `text()` sin ORM):** Se usa `sqlalchemy[asyncio]` + `asyncpg` ejecutando SQL explícito parametrizado (`:param`) para cumplir el Art. 2 y permitir auditar cada consulta.
- **D-v1-2 (Separación en 6 módulos explícitos):** Cada una de las 6 tablas tiene su propio modelo Pydantic, interfaz de servicio, interfaz de repositorio, repositorio PostgreSQL y controlador. Se descarta cualquier endpoint genérico `/api/{tabla}` (Metodología §6.1).
- **D-v1-3 (Tres esquemas Pydantic por tabla):** `Crear`, `Reemplazo` (`PUT`) y `Actualizar` (`PATCH`) permiten que Pydantic diferencie automáticamente 422 vs 200 sin `if` en el servicio.
- **D-v1-4 (Manejo de PK heterogéneas):** `area_conocimiento` (`VARCHAR(6)`) y `termino_clave` (`VARCHAR(30)`) usan PK de texto; `ods`, `area_aplicacion` y `universidad` usan `INT` manual; `linea_investigacion` usa `SERIAL` autogenerado por PostgreSQL.
- **D-v1-5 (Secretos en `.env`):** A diferencia de la plantilla didáctica, se aplica el Art. 7 completo usando `.env` en `.gitignore` y `.env.example` en el repo, preparando el terreno para Render/Neon en v4.
- **D-v1-6 (Identidad visual desacoplada en `marca.css`):** Se separan los tokens de color de la Universidad Monte Verde en `marca.css` (Art. 12) y se prohíbe Bootstrap por CDN para garantizar operación offline.
