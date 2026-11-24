# Quickstart — Versión 3: Seguridad, Roles y Regresión

## 1. Variables de Entorno y Arranque
Asegurar que `.env` (y `.env.example`) contengan `JWT_SECRET`, `JWT_ALGORITHM=HS256`, `JWT_EXPIRE_MINUTES=120` y `FLASK_SECRET_KEY`.
```powershell
docker compose up -d --build