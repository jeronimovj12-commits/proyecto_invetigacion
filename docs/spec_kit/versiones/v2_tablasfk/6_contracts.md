# Contratos HTTP — Versión 2 (10 Recursos Relacionales)

> Base API: `http://localhost:8025` · Swagger: `/docs` · Base Front: `http://localhost:8078`

## 1. Entidades Principales con FK Simple
1. **Docentes (`/api/docente` y `/api/docente/{cedula}`):**
   - Campos JSON: `cedula`, `nombres`, `apellidos`, `genero`, `cargo`, `fechaNacimiento`, `correo`, `telefono`, `urlCvlac`, `fechaActualizacion`, `escalafon`, `perfil`, `catMinciencia` (opcional), `convMinciencia`, `nacionalidad`, `lineaInvestigacionPrincipal` (opcional).
2. **Grupos de Investigación (`/api/grupo_investigacion` y `/api/grupo_investigacion/{id}`):**
   - Campos JSON: `id`, `nombre`, `urlGruplac` (opcional), `categoria` (opcional), `convocatoria` (opcional), `fechaFundacion`, `universidad` (opcional), `interno`, `ambito`.
3. **Semilleros (`/api/semillero` y `/api/semillero/{id}`):**
   - Campos JSON: `id`, `nombre`, `fechaFundacion`, `grupoInvestigacion`.

## 2. Tablas Puente con Llave Primaria Compuesta
4. **Participación en Grupo (`/api/participa_grupo` y `/api/participa_grupo/{docente_cedula}/{grupo_investigacion_id}`):**
   - Campos JSON: `docenteCedula`, `grupoInvestigacionId`, `rol`, `fechaInicio`, `fechaFin` (opcional).
5. **Participación en Semillero (`/api/participa_semillero` y `/api/participa_semillero/{docente}/{semillero}`):**
   - Campos JSON: `docente`, `semillero`, `rol`, `fechaInicio`, `fechaFin` (opcional).
6. **Grupo – Línea (`/api/grupo_linea` y `/api/grupo_linea/{grupo_investigacion}/{linea_investigacion}`):**
   - Campos JSON: `grupoInvestigacion`, `lineaInvestigacion`.
7. **Semillero – Línea (`/api/semillero_linea` y `/api/semillero_linea/{semillero}/{linea_investigacion}`):**
   - Campos JSON: `semillero`, `lineaInvestigacion`.
8. **Área Conocimiento – Línea (`/api/ac_linea` y `/api/ac_linea/{linea_investigacion}/{area_conocimiento}`):**
   - Campos JSON: `lineaInvestigacion`, `areaConocimiento`.
9. **ODS – Línea (`/api/ods_linea` y `/api/ods_linea/{linea_investigacion}/{ods}`):**
   - Campos JSON: `lineaInvestigacion`, `ods`.
10. **Área Aplicación – Línea (`/api/aa_linea` y `/api/aa_linea/{area_aplicacion}/{linea_investigacion}`):**
   - Campos JSON: `areaAplicacion`, `lineaInvestigacion`.

## 3. Pantallas del Frontend Flask (`http://localhost:8078`)
- `/docentes`, `/grupos-investigacion`, `/semilleros`
- `/participa-grupo`, `/participa-semillero`, `/grupo-linea`, `/semillero-linea`, `/ac-linea`, `/ods-linea`, `/aa-linea`
- Todos los formularios renderizan `<select>` dinámicos poblados desde la API.