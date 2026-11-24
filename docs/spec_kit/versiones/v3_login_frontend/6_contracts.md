# Contratos HTTP — Versión 3 (Autenticación y Administración)

## 1. Autenticación
- **`POST /api/login`** (Público):
  - Request: `{"username": "admin", "password": "..."}`
  - `200 OK`: `{"accessToken": "<jwt>", "tokenType": "bearer", "usuario": {"id": 1, "username": "admin", "email": "...", "nombreCompleto": "...", "roles": ["ADMIN"]}}`
  - `401 Unauthorized`: `{"estado": 401, "mensaje": "Credenciales inválidas.", "detalle": "Usuario o contraseña incorrectos, o cuenta inactiva."}`

## 2. Endpoints de Administración (Requieren `Authorization: Bearer <token>` con rol `ADMIN`)
- **Roles:** `GET /api/rol`, `GET /api/rol/{id}`, `POST /api/rol`, `PUT /api/rol/{id}`, `PATCH /api/rol/{id}`, `DELETE /api/rol/{id}`
- **Usuarios:** `GET /api/usuario`, `GET /api/usuario/{id}`, `POST /api/usuario` (hashea `password` antes de guardar), `PUT /api/usuario/{id}`, `PATCH /api/usuario/{id}` (si envía `password`, la re-hashea), `DELETE /api/usuario/{id}` (borrado lógico `activo = FALSE`). Ningún `GET` devuelve el campo `password`.
- **Asignación de Roles:** `GET /api/rol_usuario`, `GET /api/rol_usuario/{usuario_id}/{rol_id}`, `POST /api/rol_usuario`, `DELETE /api/rol_usuario/{usuario_id}/{rol_id}`.

## 3. Pantallas Flask (`http://localhost:8078`)
- `/login` y `/logout`
- `/usuarios`, `/roles`, `/rol-usuario` (visibles y accesibles solo si `"ADMIN"` está en `session["usuario"]["roles"]`).