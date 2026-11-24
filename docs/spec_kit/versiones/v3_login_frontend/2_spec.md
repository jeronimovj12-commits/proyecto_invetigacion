# Especificación — Versión 3: Autenticación JWT y Control de Acceso por Roles (RBAC)

> **Versión 3** ([mapa](../0_mapa_versiones.md)) · Crece acumulativamente sobre `v1` y `v2` sin romperlas. Rige la [constitución](../../1_constitution.md).

## 1. Propósito de la v3
Incorporar seguridad basada en tokens **JWT**, contraseñas cifradas con **bcrypt**, control de acceso basado en roles (**RBAC**) en la API y el Frontend Flask, y el CRUD completo para las **3 tablas de seguridad** (`rol`, `usuario`, `rol_usuario`) accesible exclusivamente por administradores.

## 2. Alcance

**Incluye**
- **Bootstrapping automático al iniciar la API (`lifespan`):** Crea idempotente los roles base (`ADMIN`, `INVESTIGADOR`, `CONSULTOR`) y usuarios iniciales con contraseñas hasheadas (`bcrypt`) si la tabla `usuario` está vacía (incluyendo `admin` / `Admin123*` y `juanjoherrera` / `Invest123*`).
- **Autenticación (`POST /api/login`):** Valida `username` y `password` contra el hash almacenado; devuelve `access_token` (JWT firmado con `JWT_SECRET` de `.env`), `token_type: "bearer"` y datos básicos del usuario con sus roles.
- **Protección de Endpoints y Autorización por Roles:**
  - Rutas públicas: `GET /`, `GET /docs`, `GET /openapi.json`, `POST /api/login`.
  - CRUD de `/api/usuario`, `/api/rol` y `/api/rol_usuario`: **Exclusivo rol `ADMIN`** (`403 Forbidden` si otro rol intenta acceder).
  - Endpoints del dominio (16 tablas de v1 y v2): Requieren token JWT válido (`401 Unauthorized` si falta o expiró); operaciones de escritura (`POST`, `PUT`, `PATCH`, `DELETE`) permitidas para `ADMIN` e `INVESTIGADOR`, mientras `CONSULTOR` tiene solo lectura (`GET`, respondiendo `403` ante escritura).
- **Frontend Flask con Sesión y Menú Dinámico:**
  - Pantalla `/login` y ruta `/logout` usando sesión firmada de Flask (`FLASK_SECRET_KEY`).
  - Envío automático de cabecera `Authorization: Bearer <token>` hacia la API.
  - Renderizado condicional del menú y botones: solo `ADMIN` ve el módulo de Administración (Usuarios, Roles y Asignación de Roles); `CONSULTOR` no ve botones de crear/editar/retirar.

## 3. Criterios de Aceptación
1. **Login y Token:** `POST /api/login` con credenciales válidas devuelve `200` y un JWT válido; con credenciales incorrectas devuelve `401`.
2. **Contraseñas Hasheadas:** En PostgreSQL, la columna `usuario.password` almacena hashes `$2b$...` (nunca texto plano).
3. **Protección de Rutas (401 / 403):** Consultar `/api/area_conocimiento` sin token devuelve `401`. Consultar `/api/usuario` con token de `INVESTIGADOR` devuelve `403`.
4. **CRUD de Seguridad (Solo ADMIN):** Un usuario con rol `ADMIN` puede crear, listar, actualizar y eliminar lógicamente en `/api/rol`, `/api/usuario` y `/api/rol_usuario`.
5. **Regresión Total:** Con un token válido de `ADMIN`, las 16 tablas de v1 y v2 siguen pasando todas sus operaciones sin fallos.