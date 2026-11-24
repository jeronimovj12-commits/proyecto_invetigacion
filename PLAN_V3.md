# Plan de Arquitectura e Implementación — Versión 3 (`PLAN_V3.md`)

> **Proyecto:** Módulo de Investigación — Universidad Monte Verde  
> **Alcance:** Autenticación JWT, Control de Acceso por Roles (RBAC), CRUD de Seguridad y UI Corporativa Final

## 1. Objetivo de la Versión 3
Cerrar el ciclo completo del proyecto (19 tablas de `db/init.sql`) incorporando autenticación basada en tokens **JWT**, cifrado de contraseñas con **bcrypt**, autorización granular por roles (**RBAC**) en backend y frontend, administración de usuarios/roles y una interfaz web moderna inspirada en *Modern Business* con identidad institucional de Universidad Monte Verde.

## 2. Seguridad Backend (`api_investigacion/seguridad/`)
* **Cifrado de contraseñas (`bcrypt`):** Uso directo de `bcrypt.hashpw` y `bcrypt.checkpw` al crear o actualizar usuarios. Ningún endpoint `GET` expone la columna `password`.
* **Tokens JWT (`PyJWT`):** Endpoint público `POST /api/login` que valida credenciales y emite un token firmado con `HS256` (`JWT_SECRET` y `JWT_EXPIRE_MINUTES` desde `.env`), además de integrar `HTTPBearer` en OpenAPI/Swagger (`/docs`).
* **Siembra idempotente al arranque (`lifespan`):** Al iniciar FastAPI, se crean automáticamente los roles `ADMIN`, `INVESTIGADOR` y `CONSULTOR` junto con sus usuarios iniciales (`admin`, `juanjoherrera`, `consultor`) mediante `ON CONFLICT DO NOTHING`.
* **Matriz de Permisos (RBAC):**
  * **Público:** `GET /`, `GET /docs`, `GET /openapi.json`, `POST /api/login`.
  * **Solo `ADMIN` (`403 Forbidden` a otros roles):** CRUD completo de `/api/usuario`, `/api/rol` y `/api/rol_usuario`.
  * **Dominio de Investigación (16 tablas de v1 y v2):**
    * `ADMIN` e `INVESTIGADOR`: Lectura y escritura completa (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`).
    * `CONSULTOR`: Solo lectura (`GET`); cualquier intento de escritura retorna `403 Forbidden`.

## 3. Frontend Flask y Experiencia de Usuario (`front_flask/`)
* **Gestión de sesión resiliente:** Uso de `FLASK_SECRET_KEY` desde entorno y middleware `ProxyFix(app.wsgi_app, x_proto=1, x_host=1)` para evitar errores de sesión o validación detrás de proxies HTTPS en despliegue en la nube.
* **Propagación de identidad:** `cliente_api.py` adjunta `Authorization: Bearer <token>` en todas las peticiones hacia FastAPI e intercepta respuestas `401` redirigiendo limpiamente a `/login`.
* **Interfaz *Modern Business* local sin CDN:**
  * Estilos compilados locales (`bootstrap-modern.css` + `bootstrap.bundle.min.js`) personalizados con la paleta institucional de Universidad Monte Verde en `marca.css` (`#1F5E4C` y `#D99B26`).
  * Barra superior oscura con menús desplegables agrupados por dominio (**Catálogos**, **Investigación**, **Vínculos y Participación** y **Administración**).
  * Renderizado condicional por rol: el menú de **Administración** (`/usuarios`, `/roles`, `/rol-usuario`) solo se muestra a `ADMIN`, y los botones de crear, editar y retirar se ocultan automáticamente para `CONSULTOR`.
  * Pantalla de inicio limpia con *Hero Section* institucional y acceso directo a todos los módulos del sistema.