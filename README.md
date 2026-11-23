# Módulo Investigación — ejemplo de referencia (Python)
Jeronimo velasquez
samuel jimenez
juen jose herrera

Este repositorio contiene **dos cosas distintas**, y conviene no confundirlas:

| | Qué es |
|---|---|
| [`ProyectosDeAula/`](ProyectosDeAula/) | **El material del curso**: la metodología, los documentos de módulo y los scripts de base de datos. Es lo que ya conocen |
| Todo lo demás | **El ejemplo de referencia** del módulo Investigación, ampliado con relaciones v2 y autenticación v3; las versiones siguen pendientes de aceptación formal |

El ejemplo no es un sistema para descargar: es un **molde de método**. Se
ejecuta, se estudia, y se reconstruye.

**El stack es el de paradigmas**: Python, FastAPI y PostgreSQL. El mismo
módulo existe en otro repositorio con otro lenguaje — y esa es justamente la
demostración de que **la metodología y los contratos no dependen del stack**.

---

## 1. Instalación actual: v3 en entorno separado

La rama de trabajo es `v3-desarrollo`. La guía completa y única del procedimiento es
[Arrancar y verificar v3](docs/spec_kit/versiones/v3_autenticacion/7_quickstart.md):
prerrequisitos, configuración externa, base, migración, primer administrador y datos.
Este README sirve como entrada; no repite la secuencia de actualización.

Para publicar una demostración temporal en Render y compartir un enlace web,
consulta la [Guía Render](docs/GUIA_RENDER_DEMO.md). Esta configuración aún requiere
publicar sus archivos en la rama de GitHub y no significa que ya exista una URL pública.

| Qué | Nombre o dirección real |
|---|---|
| Front v3 | http://localhost:8079/login |
| API v3 y contratos | http://localhost:8026/ y http://localhost:8026/docs |
| Proyecto Compose | `investigacion-v3`, archivo `docker-compose.v3.yml` |
| Servicios | `postgres-v3`, `migrar-v3`, `api-v3`, `front-v3` |
| Base | `investigacion_v3`; PostgreSQL v3 no publica puerto al equipo |

1. Revisar `git status --short --branch` y `git log -1 --oneline` para conservar
   cambios e identificar el código que se va a ejecutar.
2. Si es una instalación **nueva**, seguir configuración y sección 2 del quickstart:
   Docker inicializa el volumen vacío, ejecuta migración y permite crear el primer
   administrador con entrada oculta. No hay cuenta ni contraseña predeterminadas.
3. Si es una instalación **existente**, seguir la sección 3: detener escrituras,
   respaldar y copiar el respaldo **antes** de ejecutar la migración o el arranque.
   Conservar secretos/volúmenes; no volver a ejecutar init.sql ni borrar volúmenes.
4. Para mostrar relaciones con datos, elegir en sección 4 las cargas oficiales y/o
   demo. No vienen automáticamente en v3 y no son datos intercambiables con v2.
5. Seguir sección 5 para disponibilidad y pruebas. Allí se distingue lo ejecutado
   según [la evidencia](docs/spec_kit/versiones/v3_autenticacion/VERIFICACION_V3.md)
   de las instrucciones aún pendientes de ensayo integral.

Se necesita Git, PowerShell y Docker Desktop iniciado con contenedores Linux. Las
imágenes instalan sus dependencias; no se necesita Python/PostgreSQL local. El script
`scripts/configurar_v3.ps1` crea solo secretos faltantes en un archivo ignorado y
preserva los existentes; no mostrar ni versionar ese archivo.

El comando predeterminado `docker compose up -d --build` **sigue arrancando v2** en
8025/8078, no v3. Sus volúmenes y base `investigacion_local` se conservan. En v3 las
entradas son `main_v3:app` y `app_v3.py`; no se usa `--reload`, por lo que cambiar
código requiere reiniciar/recrear según el quickstart. V2 continúa abierta.

## 2. Qué construye la versión 1

El CRUD completo de **`area_conocimiento`** de punta a punta: controlador,
servicio, repositorio, interfaces, modelos por verbo y una prueba que corre
**sin base de datos**.

La tabla arranca con **218 filas** de catálogo, cargadas del Excel del
módulo — incluidas las **48** donde la fuente decía *"Cienias Naturales"* y
que este script corrige.

**La v1 del módulo original pide seis tablas sin clave foránea.** Este repositorio
construye **una sola, completa**: es el molde. Las otras cinco son el mismo
patrón con otros nombres. El equipo que tome este ejemplo lo revisa y, **si
está de acuerdo, lo retoma y lo completa; si no, lo rehace a su manera**. Lo
que no puede es cambiar la especificación sin pasar por sus compuertas.

## 3. Estructura

```
proyecto_invetigacion/
├── db/init.sql                         la base COMPLETA (artefacto DADO)
├── api_investigacion/
│   ├── main.py                         arma la app y registra el router
│   ├── controllers/                    CAPA 1: HTTP — códigos de estado y JSON
│   ├── models/                         la frontera: Pydantic valida → 422
│   ├── servicios/                      CAPA 2: negocio — no conoce HTTP ni el motor
│   │   ├── abstracciones/                la interfaz que la capa 1 conoce
│   │   └── ensamblador.py                el ÚNICO sitio que decide el motor
│   ├── repositorios/                   CAPA 3: datos — el SQL a mano
│   │   └── abstracciones/                la interfaz que la capa 2 conoce
│   └── pruebas/                        el servicio con un repositorio de mentiras
├── front_flask/                        LA PANTALLA: Flask + Jinja2
│   ├── app.py                          las vistas: ruta → pantalla
│   ├── cliente_api.py                  lo ÚNICO que habla HTTP con la API
│   ├── templates/                      el marco y las pantallas
│   └── static/estilos.css              escritos a mano, sin CDN
│
├── docs/spec_kit/                      LA FUENTE DE VERDAD (ver abajo)
├── postman/                            los endpoints listos para probar con clics
├── docker-compose.yml                  TODO el sistema declarado en un archivo
└── ProyectosDeAula/                    el material del curso
```

**La regla de lectura:** el sistema vive en `docker-compose.yml`, la API en
`api_investigacion/` (una carpeta por capa), y **todo lo que explica** vive
en `docs/`.

## 4. Las especificaciones

Empiece por **[SDD_SPECKIT.md](docs/SDD_SPECKIT.md)**: qué es SDD, qué es
GitHub Spec Kit, y cómo se arman estos documentos.

| Documento | Contenido |
|---|---|
| [PLAN_V1.md](PLAN_V1.md) | **El plan con el que se construyó esta versión**: los hallazgos, las decisiones, los ocho pasos y el prompt |
| [SDD_SPECKIT.md](docs/SDD_SPECKIT.md) | **Empiece por aquí**: el método |
| [1_constitution.md](docs/spec_kit/1_constitution.md) | Las reglas permanentes del proyecto |
| [0_mapa_versiones.md](docs/spec_kit/versiones/0_mapa_versiones.md) | La ruta v1 → v4 y qué tabla entra en cada versión |
| [2_spec.md](docs/spec_kit/versiones/v1_area_conocimiento/2_spec.md) | QUÉ construir, los criterios y las **Clarificaciones** |
| [3_plan.md](docs/spec_kit/versiones/v1_area_conocimiento/3_plan.md) | CÓMO: el stack, las capas y el **chequeo de constitución** |
| [4_research.md](docs/spec_kit/versiones/v1_area_conocimiento/4_research.md) | Las decisiones con la alternativa que se descartó |
| [5_data_model.md](docs/spec_kit/versiones/v1_area_conocimiento/5_data_model.md) | La tabla, sus semillas y quién no puede escribir qué |
| [6_contracts.md](docs/spec_kit/versiones/v1_area_conocimiento/6_contracts.md) | Los 7 endpoints con TODOS sus códigos |
| [7_quickstart.md](docs/spec_kit/versiones/v1_area_conocimiento/7_quickstart.md) | El smoke test, comando por comando |
| [8_tasks.md](docs/spec_kit/versiones/v1_area_conocimiento/8_tasks.md) | Las fases, cada una con su verificación |
| [9_checklist.md](docs/spec_kit/versiones/v1_area_conocimiento/9_checklist.md) | **La compuerta 3**: se firma ANTES de programar |
| [GUIA_IA1.md](docs/spec_kit/versiones/v1_area_conocimiento/GUIA_IA1.md) | Reconstruir la versión con IA, con el prompt listo |

## 5. Lo que hay que mirar del código

| Si quiere entender… | Abra |
|---|---|
| Por qué el 422 sale solo | `api_investigacion/models/area_conocimiento.py` |
| Por qué PUT y PATCH se comportan distinto | los **tres** modelos: la diferencia es el tipo, no un `if` |
| Dónde está el SQL | `api_investigacion/repositorios/` — a la vista y parametrizado |
| Por qué el servicio no sabe qué es un 404 | `api_investigacion/servicios/servicio_area_conocimiento.py` |
| Que las capas son de verdad | `api_investigacion/pruebas/prueba_capas.py`, que corre **con la base apagada** |

## Material conceptual del curso

Los conceptos del curso, **con el código de este repositorio como material**: los ejemplos hablan de `area_conocimiento`, no de un proyecto de otro módulo.

| Documento | Qué cubre |
|---|---|
| [Flujo de una peticion](docs/FLUJO_DE_UNA_PETICION.md) | El viaje completo de una petición por las capas, de la ruta al SQL y de vuelta |
| [Paradigma poo](docs/PARADIGMA_POO.md) | Qué es un paradigma, los cuatro pilares de la P.O.O., y dónde vive cada paradigma en este proyecto |
| [Solid capas patrones](docs/SOLID_CAPAS_PATRONES.md) | Los cinco principios SOLID y las tres capas — con el archivo de este repositorio donde se ve cada uno |
| [Principios acid](docs/PRINCIPIOS_ACID.md) | Las cuatro garantías transaccionales, cada una señalada en el código y en la base de ESTE módulo |
| [Programacion asincronica](docs/PROGRAMACION_ASINCRONICA.md) | Qué resuelve el asincronismo en la web, qué se daña sin él, y cómo se ve en este código |
| [Conceptos docker](docs/CONCEPTOS_DOCKER.md) | Imagen, contenedor, volumen y compose, con el `docker-compose.yml` de aquí explicado línea por línea |
| [Calidad de pruebas](docs/PRUEBAS_Y_CALIDAD_DE_PRUEBAS.md) | Cobertura, la métrica CRAP y las pruebas de mutación: cómo saber si sus pruebas de verdad protegen |
| [Sdd speckit](docs/SDD_SPECKIT.md) | La metodología con la que se trabaja este curso: la especificación manda sobre el código |

> Los tutoriales de administración de la base de datos (pgAdmin, SSMS, phpMyAdmin, SQLTools) **no están todavía**: llevan capturas de pantalla que hay que tomar contra la base de este módulo.

---

## La identidad visual

Este proyecto se construye para la **Universidad Monte Verde**, una
institución **inventada para el curso**, que tiene su manual de marca como lo
tendría cualquier organización real.

| Archivo | Qué es |
|---|---|
| [`MANUAL_DE_MARCA.md`](MANUAL_DE_MARCA.md) | El Manual de Identidad Visual Corporativa: logosímbolo, paleta, tipografía, tamaño mínimo, área de reserva y usos incorrectos |
| [`docs/CONCEPTOS_IDENTIDAD_VISUAL.md`](docs/CONCEPTOS_IDENTIDAD_VISUAL.md) | Qué es una identidad visual, por qué obliga al software y cómo se calcula el contraste — con referencias verificables |
| [`front_flask/static/marca.css`](front_flask/static/marca.css) | Los valores del manual, en un archivo aparte de los estilos de la aplicación |
| [`marca/`](marca/) | El logosímbolo en sus cuatro versiones |

**Los colores no se cambian.** El artículo tercero de la resolución que
adopta el manual es explícito, y la **versión 4** del proyecto evalúa que la
pantalla lo cumpla.

## Guía para la sustentación (v1–v3)

Para comprender los archivos reales, explicar las capas y seguir una petición desde Flask hasta PostgreSQL, consultar la [guía de exposición del proyecto](docs/GUIA_EXPOSICION_PROYECTO.md). Incluye autenticación, pruebas, comandos y preguntas posibles, distinguiendo lo implementado de lo verificado y lo pendiente.

El [índice explicativo de Spec Kit](docs/spec_kit/README.md) orienta la lectura de requisitos, planes, contratos y evidencia. Para arrancar v3, seguir su [quickstart](docs/spec_kit/versiones/v3_autenticacion/7_quickstart.md); las instrucciones anteriores conservan contenido histórico del ejemplo.
