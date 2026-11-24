# Tareas — Versión 3: Orden de Construcción

- **Fase 1 — Secretos y Dependencias:** Actualizar `.env.example`, `.env` y `api_investigacion/requirements.txt` (`PyJWT`, `bcrypt`).
- **Fase 2 — Núcleo JWT, RBAC y Lifespan:** Implementar `jwt_handler.py`, dependencias `obtener_usuario_actual` / `requerir_roles` y el sembrado idempotente de roles y usuarios en `lifespan`.
- **Fase 3 — CRUD Seguridad (`rol`, `usuario`, `rol_usuario`):** Implementar las 3 capas con `Protocol` y SQL `text()`, hasheando contraseñas en `usuario` y ocultando `password` en lecturas.
- **Fase 4 — Protección de los 16 Endpoints de Dominio:** Aplicar dependencias JWT/RBAC en los routers de v1 y v2 (`ADMIN` e `INVESTIGADOR` escriben; `CONSULTOR` solo lee) y actualizar `GET /` a `"v3"`.
- **Fase 5 — Frontend Flask con Login y Menú por Rol:** Implementar `/login`, `/logout`, `ProxyFix`, envío de `Bearer` en `cliente_api.py`, ocultamiento de botones según rol y pantallas `/usuarios`, `/roles`, `/rol-usuario`.
- **Fase 6 — Verificación Total:** Ejecutar smoke test v3 y regresión completa de v1 y v2.