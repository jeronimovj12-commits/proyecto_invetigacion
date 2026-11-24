# Módulo de Investigación — versión 1

Implementación de API REST y frontend web para administrar seis catálogos
independientes. La API usa FastAPI y SQL parametrizado con SQLAlchemy Core;
la interfaz es un proceso Flask separado que se comunica exclusivamente por
HTTP.

## Arranque

Requiere Docker Desktop. Las variables locales están en `.env`; `.env.example`
documenta los valores de desarrollo.

```powershell
docker compose up -d --build
```

| Servicio | Dirección |
|---|---|
| Frontend | http://localhost:8078 |
| Documentación de la API | http://localhost:8025/docs |
| Diagnóstico de la API | http://localhost:8025/ |
| PostgreSQL | `localhost:15440` |

El esquema de la base se inicializa desde `db/init.sql`. Para reiniciar los
datos semilla desde cero:

```powershell
docker compose down -v
docker compose up -d --build
```

## Recursos de la versión 1

- `area_conocimiento`
- `objetivo_desarrollo_sostenible`
- `area_aplicacion`
- `termino_clave`
- `universidad`
- `linea_investigacion`

Cada recurso ofrece listado, consulta individual, creación, reemplazo completo
(`PUT`), actualización parcial (`PATCH`) y retiro lógico (`DELETE`). La
pantalla presenta los botones **«Guardar la ficha completa»** y **«Guardar
solo lo que cambié»**; si la API no está disponible, Flask permanece
accesible sin mostrar registros.

## Verificaciones

```powershell
docker compose ps
Invoke-RestMethod http://localhost:8025/
curl.exe -sS -o NUL -w "%{http_code}`n" http://localhost:8078/
docker compose exec api-investigacion python pruebas/prueba_capas.py
```

Para comprobar respuestas de un catálogo:

```powershell
curl.exe -i http://localhost:8025/api/area_conocimiento
curl.exe -i "http://localhost:8025/api/area_conocimiento?limite=3"
curl.exe -i http://localhost:8025/api/universidad
```

`GET /api/universidad` responde `204 No Content` mientras no haya fichas
activas.

## Estructura

- `api_investigacion/`: controladores, modelos, servicios y repositorios.
- `front_flask/`: rutas y plantillas Flask, cliente HTTP y estilos UMV.
- `db/init.sql`: esquema y datos iniciales, de solo lectura para esta versión.
- `docs/spec_kit/`: constitución y especificaciones del proyecto.

Los contratos interactivos de la API se publican en `/docs`.
