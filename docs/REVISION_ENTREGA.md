# Revisión de entrega — v1, v2 y v3

Fecha: **9 de noviembre de 2026**. Código revisado: **`90aaad8fcfd572fc4ec4d6353420e6295b1e63e1`**, rama `v3-desarrollo`. Git estaba limpio y sincronizado con la referencia local `origin/v3-desarrollo` al iniciar. Este documento no cierra versiones, no firma checklists y no integra aportes.

**No hay evidencia suficiente para declarar aceptada la entrega integral v1–v3.** Hay automatización satisfactoria registrada para los casos cubiertos y pendientes de alcance, integración, datos, documentación y aceptación humana que deben resolverse antes del cierre.


## Registro de incorporación documental

Esta matriz ya existía sin commit y conserva sus hallazgos y evidencias. Se revisa
para incorporarla a Git después de `33bf497` (guía de exposición) y `d763b72`
(instrucciones de instalación). Ambos commits modifican solo documentación; el
código funcional auditado sigue siendo el de `90aaad8`.

La actualización de instalación separa los caminos nuevo/existente, sitúa respaldo
antes de migración y documenta cargas opcionales para v3. Esas mejoras de instrucciones
no acreditan que se hayan ejecutado el respaldo/restauración, el clon limpio ni la
carga en el volumen principal v3. Los conteos, referencias Git y resultados de pruebas
que se citan más abajo pertenecen a la auditoría registrada, no a nuevas consultas o
nuevos recorridos. En este aporte se revisaron archivos y enlaces; no se repitieron
las suites ni se hicieron escrituras en API/BD. V2 y v3 continúan con sus pendientes.

## 1. Bloqueos de entrega

| Bloqueo | Hallazgo comprobado y alcance | Qué falta para levantarlo |
|---|---|---|
| **B1. Alcance integral de v1/v2 sin cumplir frente al módulo original** | El [módulo original](../ProyectosDeAula/docs/modulo_investigacion.md), §3, exige seis CRUD API + front en v1 y dieciséis en v2. La [spec local v1](spec_kit/versiones/v1_area_conocimiento/2_spec.md) recorta explícitamente el ejemplo a `area_conocimiento`; v2 añade diez CRUD y cuatro consultas auxiliares. El OpenAPI observado ofrece solo GET de `universidad`, `linea_investigacion`, `objetivo_desarrollo_sostenible` y `area_aplicacion`, y ninguna colección de `termino_clave`. No existen los otros cinco CRUD completos en esta versión. | Acordar y registrar si se entrega el ejemplo de alcance reducido o el módulo completo del curso. No afirmar cumplimiento de los 16 CRUD ni añadirlos por esta auditoría. Si rige el módulo completo, esos cinco CRUD siguen faltando. |
| **B2. Aporte funcional de v2 pendiente de integrar en v3** | Las referencias Git locales muestran `origin/v2-desarrollo=6391d3f` con PR #2 y seis commits de `ac_linea` ausentes de `90aaad8`. Incluyen pruebas, bloqueo de guardado sin catálogos y nombres visibles. El aporte de documentación sí es ancestro de HEAD. | Revisar e integrar el aporte funcional, conservando autenticación/CSRF de v3, resolver diferencias y volver a verificar. La mera existencia de la rama o del PR no prueba integración ni aceptación. |
| **B3. Demostración v3 con dependencias sin datos** | Consulta SQL de solo lectura de esta auditoría: `universidad=0`, `linea_investigacion=0`. El compose v3 no carga los SQL opcionales de v2. Los formularios dependientes necesitan esos padres; las cantidades históricas de v2 no describen el volumen v3. | El quickstart v3 ya ofrece el procedimiento opcional adaptado; decidir y ejecutar la carga para la demostración, registrar el resultado y verificar opciones/recorridos. Su documentación no acredita ejecución. Distinguir seis universidades oficiales de padres ficticios demo. No inventar líneas oficiales ni ejecutar cargas sobre v2 desde esta revisión. |
| **B4. Aceptación manual y firmas pendientes** | Checklist v1 sin firma; v2 sigue abierta; v3 deja explícitamente pendientes navegador y prompt oculto. Solo hay confirmaciones manuales históricas parciales de `aa_linea` y `ods_linea`. No aparecen tags locales. | Completar revisión humana y decisiones del equipo, registrar responsables/resultados y obtener firmas reales. La ausencia de tags es coherente con versiones sin aceptar; no crear tags para sustituir esa aceptación. |
| **B5. Guías y contratos no conciliados con la entrega acumulativa** | El quickstart v1 conserva instrucciones incompatibles con el compose actual (`sa`, `postgres-init`, `uvicorn --project pruebas`) y una indicación destructiva `down -v`. V1/v2 documentan detalle del motor en errores 500; `main_v3.py` lo sustituye por texto genérico, mientras v3 afirma conservar los contratos anteriores. La constitución continúa sin enmienda formal para las excepciones de v3. | README y quickstart v3 se actualizaron en d763b72; siguen pendientes los comandos históricos aplicables de v1 y documentar la excepción de errores de v3. Resolver las enmiendas sin volver a exponer detalles internos. No declarar compatibilidad contractual exacta de todos los errores. |
| **B6. Evidencia de instalación y aceptación incompleta** | Hay build/arranque registrado, pruebas de migración aisladas y guía de actualización. No se acredita clon limpio completo de un compañero, respaldo/restauración integral de una copia representativa ni medición específica del listado v1 en menos de un segundo. | Ejecutar y registrar esos criterios si forman parte de la aceptación exigida. Diferenciar un ensayo aislado con filas sintéticas de actualizar/restaurar una instalación existente completa. |
| **B7. Confirmación de retiro incompatible con CSP (inspección estática)** | El contrato v1 exige «Retirar, tras confirmar». La plantilla de áreas usa un `onsubmit` inline con `confirm()`, mientras `app_v3.py` establece `default-src 'self'` sin autorizar scripts inline. La combinación apunta a una regresión de la confirmación; no fue reproducida en navegador. | Verificar el comportamiento en navegador y restablecer la confirmación cumpliendo la CSP vigente antes de dar por aceptado ese criterio visual. No retirar la CSP como conclusión de esta auditoría. |

Estos bloqueos tienen distinta naturaleza: B1 es de alcance, B2 de integración, B3 de preparación de datos, B4/B6 de aceptación y evidencia, B5 de coherencia documental y B7 una regresión inferida de configuración/código, pendiente de confirmación en navegador. No se presentan como fallos funcionales reproducidos todos ellos. Esta revisión no cambia código ni amplía el alcance.

## 2. Cómo se interpreta el estado

- **VA — Verificado automáticamente:** existe una ejecución registrada o una comprobación automática efectuada en esta auditoría. Se indica el entorno y el alcance; no significa aceptación integral del requisito.
- **VM-H — Verificado manualmente, histórico:** una confirmación humana está expresamente registrada en una fuente previa. No se repitió ni se atribuye una verificación nueva al usuario o al equipo.
- **E — Inspección estática:** se encontró implementación, configuración o contrato. No acredita su funcionamiento por sí sola.
- **P — Pendiente:** falta implementación dentro del alcance aplicable, evidencia suficiente, integración o aceptación. **VA parcial / P** conserva el resultado probado y deja visible lo que falta.

### Fuentes y ejecuciones

- **R1:** [constitución](spec_kit/1_constitution.md), [mapa](spec_kit/versiones/0_mapa_versiones.md), [módulo original](../ProyectosDeAula/docs/modulo_investigacion.md) y [metodología](../ProyectosDeAula/docs/0_METODOLOGIA.md).
- **R2:** specs, contratos, tareas y checklists locales de [v1](spec_kit/versiones/v1_area_conocimiento/2_spec.md), [v2](spec_kit/versiones/v2_claves_foraneas/2_spec.md) y [v3](spec_kit/versiones/v3_autenticacion/2_spec.md). Los checklists no sustituyen sus pruebas ni una firma.
- **A2:** [VERIFICACION_V2.md](../VERIFICACION_V2.md), registros del 4–5 de noviembre: pruebas de capas, API/front, humo PostgreSQL y carga de datos. Se usa la actualización cronológicamente más reciente, conservando el carácter histórico.
- **A3:** [VERIFICACION_V3.md](spec_kit/versiones/v3_autenticacion/VERIFICACION_V3.md), ejecución final del 9 de noviembre: **14 autenticación + 5 administración/regresión + 12 v2 en memoria + 5 Flask + 1 integración = 37 casos**, además de migración y recorrido de capas v1. La matriz recorre **92 operaciones HTTP**. Los cinco casos Flask simulan el transporte; el caso integrado usa HTTP y PostgreSQL reales. Ninguno es un recorrido humano en navegador.
- **N:** comprobaciones nuevas de esta auditoría: Git, lectura de archivos, OpenAPI local, GET del login y consultas SQL de conteos/metadatos. **No se volvió a ejecutar la suite completa**, no se enviaron escrituras a la API ni a la base, no se probaron credenciales y no se realizó un recorrido manual. La ejecución A3 previa corresponde al código revisado; sus límites se conservan.

## 3. Matriz de requisitos y evidencia

| Requisito | Archivo que lo implementa o debería implementarlo | Evidencia | Estado | Pendiente |
|---|---|---|---|---|
| **Alcance: seis CRUD sin FK de v1 y dieciséis de v2 según módulo original** | [main.py](../api_investigacion/main.py), controladores y [v1 spec](spec_kit/versiones/v1_area_conocimiento/2_spec.md) | R1/R2 y N: área con GET/POST y rutas de detalle; cuatro catálogos solo GET; `termino_clave` sin colección | **E / P — B1** | Definir alcance evaluable. No confundir el patrón de una tabla con todo el módulo. |
| **V1: listar y obtener área por código textual** | [area_conocimiento_controller.py](../api_investigacion/controllers/area_conocimiento_controller.py), [repositorio](../api_investigacion/repositorios/repositorio_area_conocimiento_postgresql.py) | A2 registra catálogo de 218 activas; A3 consulta catálogo real y GET de ficha creada | **VA parcial / P** | Revalidar expresamente todos los criterios v1: límite exacto 3, código inexistente, respuesta vacía y sobres. No inferirlos de la consulta feliz. |
| **V1: POST, PUT completo y PATCH parcial** | [modelo](../api_investigacion/models/area_conocimiento.py), [servicio](../api_investigacion/servicios/servicio_area_conocimiento.py), controlador de áreas | A3: capas en memoria y `test_regresion_crud_dominio_con_administrador` comprueban POST/PATCH/GET/DELETE de área | **VA parcial / P** | El ciclo HTTP final de área no recorre de nuevo todos los casos PUT/PATCH y validaciones de la aceptación original. |
| **V1: borrado lógico, exclusión de inactivos y segundo retiro** | Servicio/repositorio de áreas; [prueba_capas.py](../api_investigacion/pruebas/prueba_capas.py) | A3: repositorio falso verifica fila conservada e inactiva y segundo retiro; regresión HTTP retira el área creada | **VA con alcance limitado** | Registrar recorrido HTTP/SQL completo de área y aceptación humana si se exige el cierre original v1. |
| **V1: errores exactos y llave duplicada** | Controlador de áreas; [main.py](../api_investigacion/main.py); [main_v3.py](../api_investigacion/main_v3.py) | E: v1 exige 500 con detalle del motor; middleware v3 oculta todo detalle interno 500. A3 no acredita ese cuerpo de error de duplicado | **E / P — B5** | Conciliar contrato acumulativo y probar respuesta pública aprobada, conservando la protección de secretos. |
| **V1: listado de 218 áreas en menos de un segundo** | Ruta y repositorio de áreas | No se encontró medición específica. La duración de una suite no mide esta respuesta | **P — B6** | Medir con conjunto y entorno declarados; registrar resultado real. |
| **V1: servicio con repositorio falso y capas desacopladas** | [interfaces](../api_investigacion/repositorios/abstracciones/i_repositorio_area_conocimiento.py), servicio y `prueba_capas.py` | A2/A3 registran prueba sin dependencia de BD | **VA** | No equivale a haber apagado PostgreSQL en esta auditoría ni a revisar exhaustivamente cada clase del proyecto. |
| **V1: pantalla, botones completo/parcial, errores en español, vacío y caída** | [app.py](../front_flask/app.py), [cliente_api.py](../front_flask/cliente_api.py), [plantillas](../front_flask/templates/areas_conocimiento/lista.html) | A2: front y caída registrados; A3: renderizado y consulta de catálogo real. [humo_front.py](../pruebas_humo/humo_front.py) existe, sin ejecución nueva aquí | **VA parcial / P** | Smoke humano v1, ambos botones y revisión visual completa no acreditados para la entrega actual. |
| **V1: confirmar antes de retirar una ficha desde el navegador** | [lista de áreas](../front_flask/templates/areas_conocimiento/lista.html), CSP de [app_v3.py](../front_flask/app_v3.py) | E: contrato v1 «tras confirmar»; handler `onsubmit` inline y CSP `default-src 'self'` incompatibles para esa ejecución. No se ejecutó navegador | **E / P — B7** | Confirmar la regresión visual y corregir preservando CSP; el cliente de pruebas Flask no ejecuta JavaScript. |
| **V1/v2: base completa de 19 tablas y semillas** | [db/init.sql](../db/init.sql) | N: 19 tablas públicas; 218 áreas, 17 ODS, 21 áreas de aplicación en v3. A2 también registra inventario/carga | **VA de conteos / P de cotejo** | Conteos no prueban igualdad campo por campo con el Excel; registrar cotejo si se exige fidelidad completa. |
| **V2: CRUD de docente, grupo y semillero** | [docente_controller.py](../api_investigacion/controllers/docente_controller.py), [grupo](../api_investigacion/controllers/grupo_investigacion_controller.py), [semillero](../api_investigacion/controllers/semillero_controller.py), modelos/servicios/repositorios homónimos | A2: humo integrado; A3: regresión HTTP con administrador y los CASOS de humo_v2 | **VA de API / P de aceptación visual** | Completar POST/edición/retiro en navegador con las opciones de la versión final y revisión del equipo. |
| **V2: CRUD de las siete relaciones** | Controladores `participa_grupo`, `participa_semillero`, `grupo_linea`, `semillero_linea`, `ac_linea`, `ods_linea`, `aa_linea` en [controllers](../api_investigacion/controllers) | A2: humo de diez tablas; A3: ciclos HTTP autorizados, PUT/PATCH, referencias inválidas y retiro lógico | **VA de casos cubiertos / P** | No equivale a los ciclos visuales completos ni a los aportes de `ac_linea` todavía ausentes. |
| **V2: FK inexistentes/inactivas, nulabilidad, padres con dependientes y no reactivación** | [prueba_v2.py](../api_investigacion/pruebas/prueba_v2.py), modelos/servicios/repositorios v2 | A3 registra 12 casos en memoria y regresión HTTP de referencias inválidas y dependientes | **VA** | Mantener distinción entre cobertura en memoria y PostgreSQL; revisar decisiones de negocio pendientes en spec v2. |
| **V2: cambiar componentes de claves compuestas y consultar nueva ruta** | Servicios/repositorios de relaciones; `prueba_v2.py` | A3: prueba en memoria de cambio de relación. La regresión HTTP final reenvía componentes existentes, sin acreditar todos los cambios efectivos de clave | **VA parcial / P** | Integrar/verificar pruebas de `ac_linea`; repetir los casos aprobados con PostgreSQL y front autenticado. |
| **V2: desplegables desde API, sin acceso directo del front a PostgreSQL** | `cliente_api.py`, [formularios](../front_flask/templates), controladores GET de catálogos | A2: selectores con PostgreSQL; A3: render de GET sin argumentos; N confirma catálogos vacíos de universidades/líneas en v3 | **VA parcial / P — B3** | Preparar datos del entorno final y probar selección/guardado, no solo que el HTML responda. |
| **V2: bloqueo de guardado sin opciones activas** | [formulario aa_linea](../front_flask/templates/aa_linea/formulario.html), vistas; aporte pendiente de `ac_linea` | VM-H de aa_linea en A2; E: ese formulario deshabilita guardado. El aporte de bloqueo ac_linea no está en HEAD | **VM-H parcial / P — B2** | No generalizar a las diez pantallas. Integrar aporte y revisar todos los formularios con catálogos vacíos. |
| **V2: recorrido manual de aa_linea** | [vistas](../front_flask/app.py), [controlador](../api_investigacion/controllers/aa_linea_controller.py) | A2, 5-nov: usuario confirmó crear, cambiar área 2→3 y retirar; lectura SQL posterior inactiva | **VM-H**, limitado al recorrido registrado | No repetir como verificación de v3 ni como aceptación de todas las pantallas. |
| **V2: recorrido manual de ods_linea** | Vistas y [controlador](../api_investigacion/controllers/ods_linea_controller.py) | A2, 5-nov: usuario reportó crear 5→editar 6→retirar; comprobación posterior DELETE 200, fila false, GET 404 y lista 204 | **VM-H parcial + VA histórico** | La causa de la lectura inicial contradictoria no quedó determinada; no presentarla como fallo actual reproducido. Revisión global sigue pendiente. |
| **V2: revisión humana de las diez pantallas** | [checklist v2](spec_kit/versiones/v2_claves_foraneas/9_checklist.md) | A2/R2 dejan la casilla abierta; solo hay evidencia manual parcial anterior | **P — B4** | Completar y registrar navegador, desplegables, errores, ambos botones, edición y retiro, con responsables reales. |
| **Datos: seis universidades oficiales** | [universidades_oficiales_v2.sql](../db/opcionales/universidades_oficiales_v2.sql), [Excel fuente](<../ProyectosDeAula/Mapa_conocimiento/04_Modelo_y_Base_de_datos/Base de Datos v6.xlsx>) | A2, 5-nov: carga/repetición/conflicto ensayados y carga local v2 corroborada por SQL/HTTP. N: v3 tiene cero universidades | **VA histórico v2 / P v3 — B3** | No transferir evidencia entre volúmenes. El quickstart v3 documenta la carga; su ejecución y comprobación siguen pendientes. |
| **Datos: demo voluntaria, marcada y separada de oficiales** | [demo_v2.sql](../db/opcionales/demo_v2.sql), [carga_segura.sql](../db/opcionales/carga_segura.sql) | A2: diez filas ficticias, dos por universidad/línea/docente/grupo/semillero; idempotencia, conflictos, inactivos y catálogo vacío probados | **VA histórico v2 / P v3** | El procedimiento opcional v3 está documentado y aún debe ejecutarse/verificarse. No llamarlas oficiales ni asumir que vienen en init.sql; no generan todas las relaciones. |
| **Datos: fidelidad de fuente y ausencia de fichas inventadas como oficiales** | `db/init.sql`, SQL opcionales y Excel | A2 distingue seis universidades completas, hojas sin datos y docente incompleto; no acredita comparación exhaustiva de todos los campos de las 256 semillas iniciales | **E + VA histórico parcial / P** | Registrar cotejo de fuente si se exige; no completar artificialmente líneas/docentes como datos oficiales. |
| **Instalación v1/v2 por Docker** | [docker-compose.yml](../docker-compose.yml), Dockerfiles API/front | A2: arranque y humo del 4-nov. La guía histórica v1 conserva desajustes; README ya orienta a v3. `docker compose up` predeterminado arranca v2, no v3 | **VA histórico / P — B5** | Identificar comandos vigentes y revalidar si se entrega también el arranque v2 de esta revisión. No aplicar down -v a datos existentes. |
| **Instalación v3 reproducible y aislada** | [docker-compose.v3.yml](../docker-compose.v3.yml), [configurar_v3.ps1](../scripts/configurar_v3.ps1), locks v3 | A3: build/arranque código 0 y servicios separados. N: API dice v3 y login responde 200 | **VA parcial / P — B6** | Ensayo completo desde clon limpio con configuración nueva y datos definidos. El arranque no certifica flujos dependientes ni bootstrap humano. |
| **Migraciones conservadoras, idempotentes y rechazo incompatible** | [v3_001_sesiones_asignaciones.sql](../db/migraciones/v3_001_sesiones_asignaciones.sql), [prueba_migracion_v3.py](../api_investigacion/pruebas/prueba_migracion_v3.py) | A3: filas previas e inactivos conservados, versión 7 mantenida, repetición y rechazo al retirar NOT NULL | **VA en base aislada** | No se migró investigacion_local compartida; no certificar una conversión de sus datos reales. |
| **Actualizar instalación existente con respaldo recuperable** | [quickstart v3](spec_kit/versiones/v3_autenticacion/7_quickstart.md), servicio migrar-v3 | E: en d763b72 se documentan parada de escrituras, dump/copia, migración y arranque; A3 prueba migración aislada con datos previos | **E + VA parcial / P — B6** | Ejecutar y verificar restauración de respaldo y actualización en copia representativa antes de afirmar recuperación demostrada. |
| **Primer administrador seguro** | [crear_administrador.py](../api_investigacion/comandos/crear_administrador.py), servicio/repositorio de autenticación | A3: primer alta transaccional del servicio, rechazo ante cuentas existentes y comando sin terminal rechazado. N: hay una cuenta en v3, sin inspeccionar credenciales | **VA parcial / P** | La presencia de una cuenta no prueba cómo fue creada. Recorrido humano de entrada oculta y confirmación de contraseña sigue pendiente. |
| **V3: login JWT, Argon2id, firma/claims y vencimiento** | [servicio_autenticacion.py](../api_investigacion/servicios/servicio_autenticacion.py), [adaptadores.py](../api_investigacion/seguridad/adaptadores.py), controlador | A3: 14 casos HTTP/política, credenciales erróneas, actividad, firma, algoritmo, claims y expiración | **VA** | Aceptación visual y vencimiento real del navegador no acreditados por esa suite. |
| **V3: logout global persistente, cambio de clave e inactividad** | Repositorio de autenticación y [repositorio_seguridad_postgresql.py](../api_investigacion/repositorios/repositorio_seguridad_postgresql.py) | A3: dos tokens, logouts concurrentes, reinicio real de uvicorn y cambio de clave que invalida token. La inactividad se prueba también mediante SQL directo | **VA** | Navegador/botón atrás pendiente; no afirmar cancelación de operaciones ya autorizadas antes de revocar. |
| **V3: revocación tras DELETE administrativo de cuenta** | `retirar()` del repositorio de seguridad y servicio de autenticación | E: DELETE incrementa versión y desactiva. En la prueba administrativa el token ya fue invalidado por cambiar la clave antes de retirar la cuenta | **E / P de caso específico** | Probar token vigente → DELETE de usuario → reutilización rechazada con 401. No acreditar ese caso específico por un token que ya era inválido. |
| **V3: CRUD administrativo completo y lógico** | [seguridad_controller.py](../api_investigacion/controllers/seguridad_controller.py), modelos/servicio/interfaces/repositorio de seguridad | A3: usuarios/roles/asignaciones; PUT/PATCH, null/duplicado/FK, no-op, retiro y rollback de edición de asignaciones. E: solo campos permitidos | **VA de casos cubiertos** | Revisión humana de los formularios administrativos y decisiones de contrato. No reactivar pares retirados. |
| **V3: conservar último administrador activo** | Repositorio de seguridad, transacción y bloqueo de usuario/rol/rol_usuario | A3: bajas de cuenta, rol y asignación rechazadas; bajas simultáneas conservan un admin; cambio de par que lo pierde se revierte | **VA** | Validación humana de mensajes y revisión del equipo; no inferir prueba de toda combinación concurrente posible. |
| **V3: administrador, consulta y usuario sin roles; API directa** | [main_v3.py](../api_investigacion/main_v3.py), política de autenticación | A3: matriz OpenAPI de 92 operaciones; anónimo 401, consulta sin escritura/seguridad, sin rol 403, roles/asignaciones inactivos excluidos; CRUD de dominio con admin | **VA** | Repetir después de integrar B2 y de cualquier ruta nueva; el conteo de rutas por sí solo no acredita permisos. |
| **V3: menú, acciones y URL del front según permisos** | [app_v3.py](../front_flask/app_v3.py), [base.html](../front_flask/templates/base.html), listas protegidas | A3: cinco casos Flask con mocks y un recorrido real; consulta sin acciones y URL de alta/seguridad denegada | **VA parcial / P** | No todas las rutas con argumentos y todos los POST de las diez pantallas fueron recorridos visualmente. |
| **V3: 401, 403, vencimiento y API caída** | `app_v3.py`, [cliente_api.py](../front_flask/cliente_api.py) | A3: 401 limpia sesión, 403 deniega, expiración local, desconexión y 500 de sesión simulados; logout integrado real | **VA parcial / P** | Recorrido real en navegador: expiración, botón atrás y caída efectiva del proceso API en v3, sin datos protegidos. |
| **V3: JWT solo en servidor, cookie y CSRF** | [sesiones_servidor.py](../front_flask/sesiones_servidor.py), `app_v3.py`, formularios | A3: cookie sin JWT, rotación y flags HttpOnly/SameSite; token en servidor; CSRF en login/logout y formularios probados, POST sin token 400 | **VA parcial / P** | No acredita Secure sobre HTTPS (local COOKIE_SECURE=0), comportamiento de navegador ni una auditoría exhaustiva de XSS/CSRF. HTTPS/despliegue público no se añaden aquí. |
| **Arquitectura: front por HTTP, sin driver PostgreSQL/API** | [requirements front](../front_flask/requirements.txt), compose y cliente_api; SQLite solo para sesiones locales | A3: inspección importlib sin asyncpg/sqlalchemy/fastapi; prueba real entre servicios. E: front no depende de postgres en compose | **VA + E** | La sesión SQLite no es acceso a los datos PostgreSQL del módulo. No atribuir prueba de caída física nueva en esta auditoría. |
| **Arquitectura: SQL parametrizado, interfaces y separación** | [repositorios](../api_investigacion/repositorios), [servicios](../api_investigacion/servicios), ensambladores | E: valores parametrizados y nombres internos en seguridad; A3: capas e integración. No se revisó exhaustivamente cada sentencia de todas las ramas | **E + VA parcial** | Revisión de código del equipo y de los aportes al integrarlos; no equiparar pasar tests con cumplimiento arquitectónico exhaustivo. |
| **Secretos v3 externos y sin exposición en respuestas** | [.env.example](../.env.example), [.gitignore](../.gitignore), configurar_v3, adaptadores y compose v3 | A3: rechazo sin secreto; revisión registrada de ausencia de tres valores locales en archivos publicables; pruebas de respuestas sin password/hash/JWT en HTML/cookie | **VA con alcance explícito** | No acredita auditoría completa de historia Git, ramas y todos los logs. No imprimir ni incorporar configuración real al informe. |
| **Secretos heredados v1/v2** | Compose predeterminado y fallback de sesión de [app.py](../front_flask/app.py) | E: valores didácticos versionados; excepción expresa en constitución. V3 sobrescribe su clave y exige externos | **E — excepción documentada** | No afirmar «repositorio sin secretos» ni usar el arranque v2 como prueba de seguridad v3 o despliegue público. |
| **Regresión acumulativa v1/v2 bajo v3** | [verificar_v3.ps1](../scripts/verificar_v3.ps1), pruebas de capas/v2/administración y front | A3: 37 casos, migración y capas; HTTP real con admin en las diez entidades v2 y área v1 | **VA parcial / P** | No cubre todos los criterios originales: rendimiento, cada cuerpo de error, cambio real de toda clave compuesta, formularios con argumentos y aceptación visual. |
| **Aporte documental del equipo** | Referencia local `origin/aporte-documentacion=959e4bc` | N: `git merge-base --is-ancestor origin/aporte-documentacion HEAD` devuelve 0 | **VA de ascendencia Git** | Integración histórica no equivale a lectura, aceptación o firma por compañeros. |
| **Aporte funcional de ac_linea** | Rama `origin/prueba-areas-lineas`; `verificacion_ac_linea.md`, `test_ac_linea.py` y cambios API/front en origin/v2 | N: `git log HEAD..origin/v2-desarrollo` y diff muestran aportes ausentes en HEAD | **P — B2** | Revisar/integrar y adaptar pruebas a v3; no ejecutar ni atribuir aquí las verificaciones de otra rama. |
| **Archivos reservados del equipo** | `prueba_permisos_v3_equipo.py`, `VERIFICACION_API_V3_EQUIPO.md`, `VERIFICACION_FRONT_V3_EQUIPO.md` | N: no aparecen entre archivos versionados de HEAD; no se tocaron | **P de evidencia del equipo** | Solicitar/incorporar aportes cuando existan y hayan sido revisados. Sus nombres reservados no son evidencia de pruebas realizadas. |
| **Documentación, enmiendas y cierre** | Constitución, mapas, quickstarts y [checklist v1](spec_kit/versiones/v1_area_conocimiento/9_checklist.md), [v2](spec_kit/versiones/v2_claves_foraneas/9_checklist.md) y [v3](spec_kit/versiones/v3_autenticacion/9_checklist.md) | E/N: mapa conserva estados antiguos; v3 usa dependencias/columnas/401–403/409, puertos aislados y comando explícito; sin tags locales ni firmas de cierre | **P — B4/B5** | Resolver coherencia formal. V3 omite --reload y usa nombres/puertos distintos por aislamiento; registrar la decisión frente a artículos 4/10. No marcar cerradas v1/v2/v3 por existir código. |
| **Identidad visual y lenguaje institucional** | [marca.css](../front_flask/static/marca.css), [base.html](../front_flask/templates/base.html), [manual](../MANUAL_DE_MARCA.md) | E: identidad Monte Verde existe; el pie aún dice «Universidad de Ejemplo». No hay QA visual final acreditada | **E / P** | Corregir inconsistencia dentro de la revisión autorizada y completar inspección visual; el render HTTP no valida marca/legibilidad. |
| **Límites de v3 y exclusiones** | Spec/contratos v3 | E: registro público, correo automático, refresh, restitución de pares retirados y funcionalidades v4 están fuera del alcance autorizado | **Fuera de alcance** | No tratarlos como faltantes de esta entrega ni implementarlos para cerrar esta revisión. |

## 4. Comprobaciones nuevas y sus resultados exactos

Se hicieron solo comprobaciones de lectura. Las referencias `origin/*` son las que estaban disponibles localmente; **no se ejecutó fetch en esta auditoría** y no se afirma que describan cambios remotos posteriores.

### Git

```powershell
git status --short --branch
git log -10 --oneline
git log --oneline HEAD..origin/v2-desarrollo
git diff --name-only HEAD...origin/v2-desarrollo
git merge-base --is-ancestor origin/aporte-documentacion HEAD
git tag
```

Al inicio: `v3-desarrollo...origin/v3-desarrollo`, sin cambios. HEAD `90aaad8`.
`origin/v2-desarrollo` tiene PR #2 (`6391d3f`) y los seis commits `ded4238`,
`1099f60`, `6470a1d`, `8e83056`, `d739910`, `62e11f7`, ausentes de HEAD.
El diff incluye pruebas API, `front_flask/app.py`, plantillas ac_linea,
`front_flask/pruebas/test_ac_linea.py` y su documento de verificación.
El aporte documental es ancestro de HEAD (salida 0). `git tag` no mostró tags
locales; no se consultó aquí el listado de tags del servidor.

### Servicios y datos v3

GET `http://localhost:8026/openapi.json` identificó la API como v3. Colecciones:
`area_conocimiento`: GET/POST; ODS, áreas de aplicación, universidad y líneas:
solo GET; `termino_clave`: sin ruta de colección. El CRUD de área incluye sus
operaciones de detalle documentadas. GET `http://localhost:8079/login`: **200**.
Estas lecturas no verifican login con credenciales ni autorización autenticada.

La consulta SQL usó `psql -X` contra `postgres-v3`, base `investigacion_v3`,
solo con SELECT de conteos e `information_schema.tables`:

| Medición | Resultado observado |
|---|---:|
| Tablas públicas base | 19 |
| area_conocimiento | 218 |
| objetivo_desarrollo_sostenible | 17 |
| area_aplicacion | 21 |
| universidad | 0 |
| linea_investigacion | 0 |
| usuario | 1 |

El conteo de usuarios no acredita su origen ni un recorrido humano del bootstrap;
no se consultaron passwords, hashes, tokens ni datos personales. No se inspeccionó
ni alteró la base compartida v2 en esta revisión. No se cargaron datos ni se crearon
cuentas. No se apagaron servicios ni se modificó configuración.

## 5. Siguiente revisión necesaria para aceptar

1. Resolver el alcance de B1 y revisar/integrar B2 sin perder autenticación ni CSRF.
2. Preparar y verificar datos de soporte v3, respetando fuente oficial frente a demo.
3. Conciliar guías/contratos/enmiendas y verificar clon limpio y restauración de una copia representativa.
4. Repetir la automatización en la versión que resulte de esa integración; conservar resultados con commit y entorno, sin secretos.
5. Completar recorrido humano de pantallas, confirmación de retiro, bootstrap y vencimiento/botón atrás; registrar solo lo que cada persona realmente confirme.
6. Revisar decisiones y obtener firmas reales antes de cualquier declaración de cierre. V2 continúa abierta; este informe no autoriza merge a main ni tag v3.
