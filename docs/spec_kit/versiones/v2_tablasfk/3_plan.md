# Plan — Versión 2: Arquitectura Relacional y Listas Desplegables

> **Versión 2** ([mapa](../0_mapa_versiones.md)) · Rige la [constitución](../../1_constitution.md).

## 1. Estrategia de Crecimiento Acumulativo
La v2 conserva intactos los 6 módulos de la v1 y añade **10 nuevos módulos independientes** (3 entidades con FK simple y 7 tablas puente con PK compuesta), manteniendo la misma arquitectura de 3 capas con interfaces `typing.Protocol`, SQL escrito a mano con `text()` y cero ORM.

## 2. Estructura de Carpetas Agregada

```text
api_investigacion/
├── controllers/                 # +10 controladores específicos (uno por tabla v2)
├── models/                      # +10 archivos Pydantic (Crear, Reemplazo, Actualizar)
├── servicios/
│   ├── abstracciones/           # +10 interfaces IServicio...
│   ├── ensamblador.py           # +10 funciones fábrica
│   └── ...                      # +10 servicios de negocio
└── repositorios/
    ├── abstracciones/           # +10 interfaces IRepositorio...
    └── ...                      # +10 repositorios PostgreSQL con text()

front_flask/
├── app.py                       # +10 rutas HTML cargando catálogos para <select>
├── cliente_api.py               # +60 funciones explícitas (6 operaciones × 10 tablas)
└── templates/
    ├── docentes/                # lista.html, formulario.html (<select> línea)
    ├── grupos_investigacion/    # lista.html, formulario.html (<select> universidad)
    ├── semilleros/              # lista.html, formulario.html (<select> grupo)
    ├── participa_grupo/         # lista.html, formulario.html (<select> docente y grupo)
    ├── participa_semillero/     # lista.html, formulario.html (<select> docente y semillero)
    ├── grupo_linea/             # lista.html, formulario.html (<select> grupo y línea)
    ├── semillero_linea/         # lista.html, formulario.html (<select> semillero y línea)
    ├── ac_linea/                # lista.html, formulario.html (<select> línea y área con.)
    ├── ods_linea/               # lista.html, formulario.html (<select> línea y ODS)
    └── aa_linea/                # lista.html, formulario.html (<select> área apl. y línea)