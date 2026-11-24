# Guía de Construcción con IA — Versión 3 (`GUIA_IA3.md`)

> **Versión 3** ([mapa](../0_mapa_versiones.md)) · Rige la [constitución](../../1_constitution.md).

## 1. Criterios de Seguridad Auditados
| Punto Auditado | Riesgo Prevenido | Implementación Aplicada |
| :--- | :--- | :--- |
| **Exposición del hash de contraseña** | Que `GET /api/usuario` devuelva el campo `password`. | El modelo de salida y el `SELECT` explícito excluyen la columna `password`. |
| **Incompatibilidad `passlib` + `bcrypt`** | Fallo de arranque en Python 3.12 al hashear contraseñas. | Uso directo de `bcrypt.hashpw` y `bcrypt.checkpw` encapsulado en `seguridad/jwt_handler.py`. |
| **Error `400 Bad Request` en Flask/Render** | Pérdida de sesión o validación CSRF detrás de reverse proxy HTTPS. | Configuración de `ProxyFix` y `FLASK_SECRET_KEY` fija en variables de entorno, sin tokens CSRF frágiles acoplados a memoria volátil. |
| **Acceso sin autenticación en Swagger/API** | Que las 16 tablas de v1/v2 queden abiertas tras implementar login. | Inyección de `Depends(obtener_usuario_actual)` y `requerir_roles(...)` en todos los routers del dominio. |