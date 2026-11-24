# Plan — Versión 1: Arquitectura y Estructura

## 1. Stack Tecnológico
- **Backend:** Python 3.12, FastAPI, Pydantic v2, SQLAlchemy Core (`text()` con `asyncpg`), Uvicorn (puerto `8025`). Sin ORM.
- **Base de datos:** PostgreSQL 16 (puerto `15440`), inicializada vía `db/init.sql`.
- **Frontend:** Python 3.12, Flask 3, Jinja2, `requests` (puerto `8078`). CSS escrito a mano (`marca.css` + `estilos.css`), cero CDN externos.
- **Orquestación:** Docker Compose con variables cargadas desde `.env`.

## 2. Estructura de Carpetas

```text
proyecto_investigacion/
├── .env.example
├── .gitignore
├── docker-compose.yml
├── db/
│   └── init.sql
├── api_investigacion/
│   ├── main.py
│   ├── database.py                  # Engine asíncrono SQLAlchemy leyendo DATABASE_URL
│   ├── controllers/                 # Capa 1: 6 controladores específicos (uno por tabla)
│   ├── models/                      # Frontera Pydantic: Crear, Reemplazo, Actualizar x 6 tablas
│   ├── servicios/
│   │   ├── abstracciones/           # 6 Interfaces Protocol (IServicio...)
│   │   ├── ensamblador.py           # Inyección de dependencias
│   │   └── ...                      # 6 Servicios de negocio (ValueError / LookupError)
│   ├── repositorios/
│   │   ├── abstracciones/           # 6 Interfaces Protocol (IRepositorio...)
│   │   └── ...                      # 6 Repositorios PostgreSQL con SQL text()
│   ├── pruebas/
│   │   └── prueba_capas.py          # Prueba unitaria con repositorio falso en memoria
│   ├── requirements.txt
│   └── Dockerfile
└── front_flask/
    ├── app.py                       # Vistas HTML para las 6 entidades
    ├── cliente_api.py               # Funciones HTTP explícitas por operación y traducción 422
    ├── templates/
    │   ├── base.html
    │   ├── inicio.html
    │   ├── areas_conocimiento/      # lista.html, formulario.html
    │   ├── ods/                     # lista.html, formulario.html
    │   ├── areas_aplicacion/        # lista.html, formulario.html
    │   ├── terminos_clave/          # lista.html, formulario.html
    │   ├── universidades/           # lista.html, formulario.html
    │   └── lineas_investigacion/    # lista.html, formulario.html
    ├── static/
    │   ├── marca.css                # Variables hexadecimales del Manual de Marca UMV
    │   └── estilos.css              # Reglas de interfaz usando var(--umv-*)
    ├── requirements.txt             # Solo flask y requests
    └── Dockerfile