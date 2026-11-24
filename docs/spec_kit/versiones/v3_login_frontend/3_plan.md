# Plan — Versión 3: Seguridad JWT, RBAC y Despliegue Resiliente

## 1. Piezas Técnicas Incorporadas
- **Dependencias API (`api_investigacion/requirements.txt`):** `PyJWT` y `bcrypt` (evitando incompatibilidades de versiones antiguas de `passlib` con `bcrypt >= 4.1`).
- **Seguridad Centralizada (`api_investigacion/seguridad/`):**
  - `jwt_handler.py`: Generación y decodificación de tokens HS256 usando `JWT_SECRET` y `JWT_EXPIRE_MINUTES` desde variables de entorno.
  - `dependencias.py`: Dependencias FastAPI (`obtener_usuario_actual`, `requerir_roles(...)`) para inyectar identidad y validar permisos sin acoplar SQL en los controladores.
  - `arranque.py`: Función idempotente ejecutada en el `lifespan` de FastAPI que siembra roles y usuarios iniciales hasheados.
- **Nuevos Módulos en 3 Capas (`rol`, `usuario`, `rol_usuario`):** Misma arquitectura `Protocol` + SQL `text()` + borrado lógico (`activo = FALSE` en `rol` y `usuario`; en `rol_usuario` asignación/desasignación limpia).
- **Frontend Flask (`front_flask/`):**
  - `ProxyFix` de `werkzeug.middleware.proxy_fix` configurado en `app.py` para evitar errores de cookies/CSRF detrás de proxies HTTPS (como Render).
  - Decorador `@login_requerido` y `@admin_requerido` en `app.py`.
  - Context processor en Jinja2 exponiendo `usuario_actual`, `es_admin` y `puede_escribir` a `base.html` y todas las vistas.

## 2. Chequeo de Constitución (12 Artículos)
- **Art. 1 y 1.1:** Cierra el alcance v3 con JWT, RBAC y pantallas de login y administración en Flask. ✅
- **Art. 2 y 3:** SQL `text()` parametrizado, contraseñas hasheadas con `bcrypt`, arquitectura en 3 capas intacta. ✅
- **Art. 7:** `JWT_SECRET` y `FLASK_SECRET_KEY` leídos desde `.env` con `.env.example` actualizado; cero secretos quemados. ✅
- **Art. 8, 9, 10 y 12:** Comentarios explicando el *por qué*, contratos exactos y diseño fiel a `marca.css`. ✅