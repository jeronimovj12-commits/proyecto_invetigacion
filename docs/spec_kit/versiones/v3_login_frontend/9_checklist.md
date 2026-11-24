# Lista de Chequeo — Versión 3 (Compuerta 3)

- [x] **JWT y Contraseñas Hasheadas:** `POST /api/login` emite JWT HS256; contraseñas cifradas con `bcrypt` y nunca expuestas en respuestas.
- [x] **RBAC Completo:** `rol`, `usuario` y `rol_usuario` protegidos exclusivamente para `ADMIN`; 16 recursos de dominio protegidos con JWT y permisos por rol.
- [x] **Cero Secretos Quemados:** `JWT_SECRET` y `FLASK_SECRET_KEY` en `.env` y documentados en `.env.example`.
- [x] **Frontend con Sesión y Menú Condicional:** Solo `ADMIN` ve la sección de seguridad; tolerante a proxies (`ProxyFix`) sin errores `400 Bad Request`.
- [x] **Regresión v1 + v2:** Las 16 tablas anteriores operan normalmente con token válido.

**Veredicto:** 🟢 En verde — Autorizado para generar código de Versión 3.