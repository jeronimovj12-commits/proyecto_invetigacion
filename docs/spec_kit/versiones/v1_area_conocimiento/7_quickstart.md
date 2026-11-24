# Quickstart — Versión 1: Arranque y Smoke Test

## 1. Configuración y Arranque
1. Copiar `.env.example` a `.env` en la raíz del proyecto.
2. Levantar los 3 servicios en un solo comando:
```powershell
docker compose up -d --build
```

## 2. Verificación rápida

Desde PowerShell, en la raíz del repositorio:

```powershell
docker compose ps
$api = "http://localhost:8025"
(Invoke-RestMethod "$api/").version
(Invoke-RestMethod "$api/api/area_conocimiento").total
(Invoke-RestMethod "$api/api/area_conocimiento?limite=3").datos.Count
(Invoke-RestMethod "$api/api/objetivo_desarrollo_sostenible").total
(Invoke-RestMethod "$api/api/area_aplicacion").total
curl.exe -i "$api/api/universidad"
curl.exe -sS -o NUL -w "%{http_code}`n" "http://localhost:8078/"
docker compose exec -T api-investigacion python pruebas/prueba_capas.py
```

Los valores iniciales esperados son `v1`, `218`, `3`, `17` y `21`;
`/api/universidad` debe responder `204 No Content` sin filas activas. La
prueba de capas también debe pasar con PostgreSQL apagado:

```powershell
docker compose stop postgres
docker compose exec -T api-investigacion python pruebas/prueba_capas.py
docker compose start postgres
```

Con la API apagada, el frontend debe seguir disponible y no mostrar fichas:

```powershell
docker compose stop api-investigacion
curl.exe -sS -o NUL -w "%{http_code}`n" "http://localhost:8078/areas-de-conocimiento"
docker compose start api-investigacion
```