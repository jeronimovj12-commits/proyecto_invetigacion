# Tareas de implementación — v2: claves foráneas

## API

- [x] Implementar las operaciones de las diez tablas gestionadas: `docente`,
  `grupo_investigacion`, `semillero`, `participa_semillero`,
  `participa_grupo`, `semillero_linea`, `grupo_linea`, `ac_linea`,
  `ods_linea` y `aa_linea`. Evidencia: controladores, servicios y
  repositorios de `api_investigacion/`; `VERIFICACION_V2.md`.
- [x] Implementar consultas de los catálogos y tablas de soporte para los
  selectores: `area_conocimiento`, `universidad`, `linea_investigacion`,
  `objetivo_desarrollo_sostenible` y `area_aplicacion`. Evidencia:
  `api_investigacion/main.py` y los controladores correspondientes.
- [x] Validar referencias inexistentes o inactivas antes de confirmar una
  escritura. Evidencia: servicios y repositorios de
  `api_investigacion/`; 12 pruebas en memoria de
  `api_investigacion/pruebas/prueba_v2.py`.
- [x] Implementar `PUT` como reemplazo completo y `PATCH` como actualización
  parcial, incluidos los cambios de componentes de claves compuestas.
  Evidencia: modelos Pydantic, controladores y
  `api_investigacion/pruebas/prueba_v2.py`.
- [x] Implementar el borrado lógico, impedir la reactivación y bloquear la
  desactivación de padres con relaciones activas. Evidencia: servicios y
  repositorios de `api_investigacion/`; `VERIFICACION_V2.md`.
- [x] Comprobar la API con la prueba integrada de las diez tablas, sus
  referencias, desplegables y borrado lógico. Evidencia:
  `VERIFICACION_V2.md`; smoke test completado con el identificador
  `1701599219`.

## Formularios

- [x] Conectar las diez pantallas con la API para listar, crear, editar y
  desactivar los registros correspondientes. Evidencia: `front_flask/` y
  `VERIFICACION_V2.md`.
- [x] Cargar las opciones de las relaciones desde la API en los selectores,
  sin inventar registros de catálogo. Evidencia: `front_flask/`,
  `7_quickstart.md` y `VERIFICACION_V2.md`.
- [x] Mostrar etiquetas corregidas en pantalla y conservar en el JSON los
  nombres exactos del SQL, incluidos `universidsad` y `nacionalidaad`.
  Evidencia: formularios de `front_flask/` y modelos de
  `api_investigacion/models/`.
- [x] Cubrir mediante HTTP simulado los formularios y selectores de las diez
  pantallas. Evidencia: `VERIFICACION_V2.md`.
- [ ] Revisar manualmente en el navegador las diez pantallas: opciones de los
  selectores, mensajes de error, botones de guardar y comportamiento de
  edición y borrado lógico. La prueba automática no sustituye este recorrido
  visual. Evidencia de pendiente: `VERIFICACION_V2.md` y `7_quickstart.md`.

## Pruebas

- [x] Ejecutar las pruebas de capas de la v1 para comprobar que la ampliación
  no rompe el comportamiento anterior. Evidencia: `VERIFICACION_V2.md`.
- [x] Ejecutar las 12 pruebas en memoria de integridad y contratos. Evidencia:
  `api_investigacion/pruebas/prueba_v2.py` y
  `VERIFICACION_V2.md`; resultado: las 12 pruebas pasaron.
- [x] Ejecutar las rutas HTTP de las diez tablas con servicios en memoria.
  Evidencia: `VERIFICACION_V2.md`.
- [x] Ejecutar el smoke test con Docker y PostgreSQL para las operaciones
  reales de las diez tablas. Evidencia: `api_investigacion/pruebas/humo_v2.py`
  y `VERIFICACION_V2.md`; identificador de las fichas de prueba:
  `1701599219`.
- [x] Comprobar que los listados del front muestran un aviso y una lista
  vacía cuando la API no está disponible. Evidencia: `VERIFICACION_V2.md`.
- [ ] Completar el recorrido manual en navegador después de ejecutar Docker,
  y registrar cualquier hallazgo visual o funcional. La automatización no
  certifica esta tarea. Evidencia de pendiente: `VERIFICACION_V2.md`.

## Entrega

- [x] Documentar el alcance, las claves, las relaciones y las diferencias
  entre PostgreSQL y la API. Evidencia:
  `5_data_model.md`, `2_spec.md` y `3_plan.md`.
- [x] Documentar el procedimiento para levantar Docker, ejecutar las pruebas
  y revisar las pantallas. Evidencia: `7_quickstart.md`.
- [x] Registrar los resultados de la verificación automática y de la prueba
  integrada. Evidencia: `VERIFICACION_V2.md`.
- [ ] Realizar y documentar la revisión manual de las diez pantallas; no
  declarar cerrada la v2 hasta completar este recorrido. Evidencia de
  pendiente: `VERIFICACION_V2.md`.
- [ ] Cerrar el checklist de la v2 después de la revisión manual. Evidencia de
  pendiente: `3_plan.md` y `VERIFICACION_V2.md`.
