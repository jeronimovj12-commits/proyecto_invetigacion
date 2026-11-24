# Plan de Arquitectura e Implementación — Versión 1 (`PLAN_V1.md`)

> **Proyecto:** Módulo de Investigación — Universidad Monte Verde  
> **Alcance:** Catálogos Base Independientes (6 tablas sin llaves foráneas)

## 1. Objetivo de la Versión 1
Construir la base estructural del sistema bajo una arquitectura limpia en tres capas desacopladas, estableciendo los contratos HTTP, el acceso a datos sin ORM en PostgreSQL 16, el borrado lógico y las vistas iniciales en Flask con identidad institucional.

## 2. Arquitectura y Stack Tecnológico
* **Base de Datos (`db/init.sql`):** PostgreSQL 16 ejecutado en contenedor Docker con `healthcheck` activo y semillas iniciales cargadas en `area_conocimiento` (218 registros), `objetivo_desarrollo_sostenible` (17 registros) y `area_aplicacion` (20 registros).
* **Backend (`api_investigacion/`):** FastAPI en Python organizado estrictamente en 3 capas independientes mediante contratos `typing.Protocol`:
  1. **Capa de Controladores (`controllers/`):** Enrutadores específicos por recurso, validación de esquemas Pydantic (`Field(alias=...)` exponiendo `camelCase` en JSON), manejo estandarizado de errores y códigos HTTP (`200`, `201`, `204`, `400`, `404`, `409`, `500`).
  2. **Capa de Servicios (`servicios/`):** Lógica de negocio pura desacoplada de SQL y de HTTP, instanciada mediante funciones fábrica en `ensamblador.py`.
  3. **Capa de Repositorios (`repositorios/`):** Consultas SQL escritas manualmente con `sqlalchemy.text()` y parámetros enlazados (`:parametro`), prohibiendo el uso de ORM.
* **Frontend (`front_flask/`):** Aplicación web Flask con plantillas Jinja2, cliente HTTP explícito en `cliente_api.py` (sin llamadas genéricas) y hoja de estilos institucional `marca.css`.

## 3. Entidades Cubiertas (6 Tablas Base)
1. `area_conocimiento` (PK: `codigo` `VARCHAR(6)`)
2. `objetivo_desarrollo_sostenible` (PK: `id` `INT`)
3. `area_aplicacion` (PK: `id` `INT`)
4. `termino_clave` (PK: `termino` `VARCHAR(30)`)
5. `universidad` (PK: `id` `INT`)
6. `linea_investigacion` (PK: `id` `INT`)

## 4. Reglas Transversales Establecidas
* **Borrado lógico obligatorio:** Ningún endpoint `DELETE` ejecuta `DELETE FROM`; actualiza `activo = FALSE` y todas las consultas `GET` filtran `WHERE activo = TRUE`.
* **Listados vacíos:** Si una colección activa no tiene registros, la API responde `204 No Content`.
* **Actualización dual:** Cada entidad expone `PUT /api/{recurso}/{id}` (reemplazo completo) y `PATCH /api/{recurso}/{id}` (actualización parcial), reflejados en el frontend mediante los botones *«Guardar la ficha completa»* y *«Guardar solo lo que cambié»*.
* **Aislamiento de credenciales:** Parámetros de conexión gestionados vía `.env` con plantilla `.env.example` versionada.