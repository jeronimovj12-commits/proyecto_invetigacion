### 8. `8_tasks.md`

```markdown
# Tareas — Versión 1: Orden de Construcción

- **Fase 0 — Infraestructura y Secretos:** Crear `.env.example`, `.env`, `.gitignore` y `docker-compose.yml` montando `db/init.sql`, `api-investigacion` (8025) y `front-flask` (8078).
- **Fase 1 — Base de Datos:** Verificar que PostgreSQL crea las 19 tablas y carga 218 áreas, 17 ODS y 21 áreas de aplicación.
- **Fase 2 — Frontera Pydantic (`models/`):** Crear las 3 clases (`Crear`, `Reemplazo`, `Actualizar`) para cada una de las 6 tablas respetando tipos y longitudes exactas.
- **Fase 3 — Interfaces y Servicios (`servicios/`):** Crear los 6 `Protocol` (`IServicio...`, `IRepositorio...`), las 6 implementaciones de servicio con `ValueError`/`LookupError` y `ensamblador.py`.
- **Fase 4 — Repositorios PostgreSQL (`repositorios/`):** Implementar las 6 clases con SQL parametrizado `text()`, filtrando siempre `activo = TRUE` y borrado lógico en una sola sentencia `UPDATE`.
- **Fase 5 — Controladores y `main.py` (`controllers/`):** Exponer los endpoints específicos de las 6 tablas, manejando `204` en listas vacías y mapeando excepciones a `400`/`404`/`500`.
- **Fase 6 — Prueba de Capas (`pruebas/prueba_capas.py`):** Verificar los servicios usando repositorios en memoria con PostgreSQL detenido.
- **Fase 7 — Frontend Flask (`front_flask/`):** Implementar `cliente_api.py` (funciones explícitas por operación y traductor de errores 422), `app.py`, `static/marca.css`, `static/estilos.css` y plantillas Jinja2 para los 6 recursos.
- **Fase 8 — Cierre v1:** Ejecutar smoke test completo, firmar `9_checklist.md`, redactar `GUIA_IA1.md` y crear tag `v1`.