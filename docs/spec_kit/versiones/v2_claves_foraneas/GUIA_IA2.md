# Guía de uso de IA — v2: claves foráneas

## 1. Propósito y estado

Este documento registra el uso real de herramientas de inteligencia artificial
durante la preparación de la v2. Sigue la organización del Spec Kit:
especificación, plan, investigación, modelo de datos, contratos, quickstart,
tareas, checklist y esta guía.

La constitución del proyecto exige trabajar por versiones, entregar API y
frontend juntos, y no declarar una versión terminada hasta cumplir sus
criterios de aceptación. La metodología también establece que la
interpretabilidad no se delega a una IA: el equipo debe poder explicar el
resultado. Por eso esta guía registra qué se apoyó con IA, qué verificó el
usuario y qué continúa pendiente.

**Estado:** la v2 no está cerrada. La revisión manual de las diez pantallas,
la firma del equipo y el cierre formal siguen pendientes. No se creó el tag de
la v2.

## 2. Herramientas utilizadas y responsabilidades

| Herramienta o participante | Uso real y responsabilidad |
|---|---|
| ChatGPT | Orientó el trabajo y propuso instrucciones. No se dispone en este repositorio ni en esta sesión del historial de ChatGPT. |
| Codex en VS Code | Revisó los archivos del proyecto y elaboró el modelo de datos, la lista de tareas, el checklist y esta guía a partir de evidencia disponible. |
| Usuario/equipo | Aportó el contexto del trabajo, ejecutó el smoke test con Docker y PostgreSQL el 4 de noviembre de 2026 y debe realizar la revisión manual, firmar y explicar las decisiones. |
| Repositorio y pruebas | Constituyen la fuente de comprobación: código de `api_investigacion/`, `front_flask/`, SQL, documentos v2 y resultados registrados en `VERIFICACION_V2.md`. |

La IA no sustituye la responsabilidad del equipo sobre decisiones de negocio,
revisión visual, firma ni sustentación oral.

## 3. Prompts de Codex disponibles en esta conversación

Los siguientes son los prompts de usuario que sí están disponibles en esta
conversación de Codex. Se copian literalmente. Las respuestas y archivos
indicados como resultado se limitan a lo que se puede comprobar en el
repositorio.

### Prompt 1 — modelo de datos

> Crea 5_data_model.md en la misma carpeta que 4_research.md. Escribe el documento en español.
>
> Revisa los archivos SQL de la carpeta db y las definiciones de la API para identificar las diez tablas que gestiona la v2. Distingue esas tablas de los catálogos que solo sirven de referencia.
>
> Para cada una de las diez tablas, explica qué representa una fila. Incluye una tabla Markdown con el nombre exacto de cada columna, su tipo SQL, si admite NULL y su función. Identifica la clave primaria y, si es compuesta, enumera sus columnas en orden. Para cada clave foránea, indica la tabla y la columna de destino.
>
> Cierra con un ejemplo real de cómo se relacionan dos tablas del proyecto. Distingue las restricciones que impone PostgreSQL de las validaciones que realiza la API, incluido el borrado lógico. Si el SQL y la API difieren, señala la diferencia y los archivos donde aparece.
>
> Comprueba los nombres contra el código y guarda únicamente 5_data_model.md.

**Objetivo:** documentar el modelo de datos de la v2 y separar tablas
gestionadas de catálogos.

**Archivos consultados:** `db/init.sql`, `docs/4_research.md`,
`api_investigacion/main.py`, modelos, controladores, servicios, repositorios y
pruebas de `api_investigacion/`.

**Resultado verificable:** se creó un modelo de datos en español con las diez
tablas gestionadas, claves, columnas, referencias, catálogos y diferencias
entre SQL y API. Durante la primera ubicación quedó en
`docs/5_data_model.md`; después se trasladó a
`docs/spec_kit/versiones/v2_claves_foraneas/5_data_model.md`.

### Prompt 2 — tareas

> Crea únicamente docs/spec_kit/versiones/v2_claves_foraneas/8_tasks.md.
>
> Revisa 2_spec.md, 3_plan.md y 7_quickstart.md de esa carpeta, el código de la v2 y el archivo VERIFICACION_V2.md de la raíz.
>
> Escribe en español una lista de tareas agrupadas en API, formularios, pruebas y entrega. Usa [x] para tareas completadas con evidencia y [ ] para las pendientes. Junto a cada tarea completada, indica el archivo o la prueba que la respalda.
>
> Registra que pasaron las 12 pruebas en memoria y que la prueba integrada terminó con el identificador 1701599219. Mantén pendiente la revisión manual de las diez pantallas: la prueba automática no sustituye ese recorrido en el navegador.
>
> Guarda solo 8_tasks.md, sin modificar otros archivos ni hacer commit.

**Objetivo:** convertir el plan y la evidencia disponible en tareas verificables
agrupadas por API, formularios, pruebas y entrega.

**Archivos consultados:** `2_spec.md`, `3_plan.md`, `7_quickstart.md`,
`VERIFICACION_V2.md`, `api_investigacion/` y el frontend.

**Resultado verificable:** se creó
`docs/spec_kit/versiones/v2_claves_foraneas/8_tasks.md`, con casillas
completadas respaldadas por archivos o pruebas y con la revisión manual
pendiente.

### Prompt 3 — checklist

> Crea docs/spec_kit/versiones/v2_claves_foraneas/9_checklist.md en español.
>
> Lee 2_spec.md, 6_contracts.md, 8_tasks.md y VERIFICACION_V2.md. Arma una lista de verificación con una casilla por requisito. Incluye el CRUD de las diez tablas, las claves compuestas, los desplegables cargados desde la API, el rechazo de referencias inexistentes o inactivas y el borrado lógico.
>
> Marca [x] únicamente cuando haya evidencia de que el requisito se comprobó. Junto a cada casilla marcada, indica la prueba o el documento que lo respalda. Registra las 12 pruebas en memoria y el smoke test con PostgreSQL del 4 de noviembre de 2026, con identificador 1701599219.
>
> Deja [ ] para la revisión manual de las diez pantallas, la firma del equipo y cualquier otro punto sin verificar. Guarda solo 9_checklist.md, sin hacer commit ni crear el tag.

**Objetivo:** crear un checklist de aceptación con evidencia por requisito y
pendientes explícitos.

**Archivos consultados:** `2_spec.md`, `6_contracts.md`, `8_tasks.md` y
`VERIFICACION_V2.md`.

**Resultado verificable:** se creó
`docs/spec_kit/versiones/v2_claves_foraneas/9_checklist.md`. Incluye el CRUD
de las diez tablas, las siete claves compuestas, los desplegables, la
validación de referencias, el borrado lógico, las pruebas automáticas
registradas y los pendientes de revisión manual, firma y tag.

### Prompt 4 — esta guía

> Crea únicamente docs/spec_kit/versiones/v2_claves_foraneas/GUIA_IA2.md, en español.
>
> El documento debe registrar el uso real de IA durante la v2. Lee la constitución, la metodología del proyecto y los documentos existentes de la v2 para respetar su estructura.
>
> Usa como contexto confirmado:
> - Se utilizó ChatGPT para orientar el trabajo y proponer instrucciones.
> - Se utilizó Codex en VS Code para elaborar el modelo de datos, las tareas y el checklist a partir de los archivos del proyecto.
> - Inicialmente 3_plan.md, 4_research.md y 5_data_model.md quedaron directamente en docs. Después se trasladaron a docs/spec_kit/versiones/v2_claves_foraneas/.
> - Las 12 pruebas en memoria pasaron.
> - El usuario ejecutó el smoke test con Docker y PostgreSQL el 4 de noviembre de 2026. Terminó con el identificador 1701599219.
> - La revisión manual de las diez pantallas sigue pendiente.
>
> Incluye:
> 1. Herramientas utilizadas y responsabilidades del equipo.
> 2. Los prompts reales disponibles en esta conversación de Codex, copiados literalmente. Para cada uno, indica su objetivo, los archivos consultados y el resultado que puedas verificar.
> 3. Correcciones realizadas, incluida la ubicación de los documentos.
> 4. Cómo se verificaron los resultados, diferenciando pruebas automáticas y revisión manual.
> 5. Evidencias o mensajes que aún falte incorporar.
>
> No tienes acceso automático al historial de ChatGPT. Si no puedes recuperar el texto exacto de un prompt anterior, describe su propósito como resumen y señala que falta adjuntar el original. No inventes mensajes, respuestas, firmas ni pruebas.
>
> Guarda solo GUIA_IA2.md. No hagas commit ni marques la v2 como terminada.

**Objetivo:** dejar una trazabilidad honesta del uso de IA, sus límites y la
evidencia de verificación.

**Archivos consultados:** `docs/spec_kit/1_constitution.md`,
`ProyectosDeAula/docs/0_METODOLOGIA.md`, todos los documentos existentes de
`docs/spec_kit/versiones/v2_claves_foraneas/` y `VERIFICACION_V2.md`.

**Resultado verificable:** este archivo, sin commit ni tag.

### Prompts de ChatGPT

No se tiene acceso automático al historial de ChatGPT desde este repositorio ni
desde esta sesión de Codex. Por tanto, no se puede copiar literalmente ningún
prompt anterior de ChatGPT. Falta adjuntar los originales si el equipo desea
que formen parte de la trazabilidad.

## 4. Correcciones y ubicación de documentos

Durante la elaboración inicial, `3_plan.md`, `4_research.md` y
`5_data_model.md` quedaron directamente en `docs/`. La estructura prevista por
el Spec Kit requiere que los documentos de la versión estén juntos en:

`docs/spec_kit/versiones/v2_claves_foraneas/`

La ubicación de trabajo de la v2 quedó así:

- `2_spec.md`
- `3_plan.md`
- `4_research.md`
- `5_data_model.md`
- `6_contracts.md`
- `7_quickstart.md`
- `8_tasks.md`
- `9_checklist.md`
- `GUIA_IA2.md`

La corrección consistió en trasladar los tres documentos iniciales a la
carpeta de la versión y continuar allí la documentación. No se modificó el
código para resolver una discrepancia documental. Se conservaron los nombres
exactos del SQL y de la API, incluidos `universidsad` y `nacionalidaad`, cuando
correspondía.

## 5. Verificación de resultados

### Pruebas automáticas

La evidencia registrada en `VERIFICACION_V2.md` indica:

- Pasaron las 12 pruebas de integridad y contratos en memoria.
- Pasaron las pruebas de capas de v1.
- Pasaron las rutas HTTP de las diez tablas con servicios en memoria.
- Pasaron las comprobaciones con HTTP simulado de plantillas, formularios y
  selectores de las diez pantallas.
- El front mostró aviso y lista vacía cuando la API no estaba disponible.
- El usuario ejecutó el smoke test integrado con Docker y PostgreSQL el 4 de
  noviembre de 2026.
- El smoke test comprobó las operaciones de las diez tablas, referencias,
  desplegables y borrado lógico.
- El identificador de las fichas de prueba fue `1701599219`.

El quickstart documenta los comandos de las pruebas en
`api_investigacion/pruebas/prueba_v2.py`, `prueba_capas.py` y `humo_v2.py`.

### Revisión manual

La revisión manual de las diez pantallas sigue pendiente. En particular, aún
deben recorrerse en el navegador las opciones de los desplegables, mensajes de
error, botones de guardar, edición y borrado lógico. Las pruebas automáticas y
el HTTP simulado no sustituyen ese recorrido visual, conforme a
`2_spec.md`, `7_quickstart.md`, `8_tasks.md`, `9_checklist.md` y
`VERIFICACION_V2.md`.

## 6. Evidencias o mensajes pendientes de incorporar

- El texto original de los prompts usados en ChatGPT, porque no está
  disponible en esta conversación de Codex.
- Capturas, observaciones y resultados de la revisión manual de las diez
  pantallas.
- Confirmación documentada de que el equipo revisó las decisiones de negocio
  de `2_spec.md`.
- Firma o nombres de quienes aprueban el checklist.
- Cierre del checklist después de la revisión visual.
- El commit y el tag `v2`, que no deben realizarse mientras existan requisitos
  pendientes.

Este archivo no constituye una declaración de terminación de la v2. La
constitución y la metodología exigen completar la compuerta del frontend,
aceptación y sustentación antes del cierre.
