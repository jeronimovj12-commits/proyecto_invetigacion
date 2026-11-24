# Modelo de Datos — Versión 2 (10 Tablas con FK)

1. **`docente`**: `cedula` (`INT` PK), `nombres` (`VARCHAR(60)`), `apellidos` (`VARCHAR(60)`), `genero` (`VARCHAR(12)`), `cargo` (`VARCHAR(30)`), `fecha_nacimiento` (`DATE`), `correo` (`VARCHAR(70)`), `telefono` (`VARCHAR(20)`), `url_cvlac` (`VARCHAR(128)`), `fecha_actualizacion` (`DATE`), `escalafon` (`VARCHAR(45)`), `perfil` (`TEXT`), `cat_minciencia` (`VARCHAR(45)` NULL), `conv_minciencia` (`VARCHAR(45)`), `nacionalidaad` (`VARCHAR(45)`), `linea_investigacion_principal` (`INT` FK NULL $\rightarrow$ `linea_investigacion.id`), `activo` (`BOOLEAN`).
2. **`grupo_investigacion`**: `id` (`INT` PK), `nombre` (`VARCHAR(60)`), `url_gruplac` (`VARCHAR(128)` NULL), `categoria` (`VARCHAR(10)` NULL), `convocatoria` (`VARCHAR(10)` NULL), `fecha_fundacion` (`DATE`), `universidsad` (`INT` FK NULL $\rightarrow$ `universidad.id`), `interno` (`SMALLINT`), `ambito` (`VARCHAR(45)`), `activo` (`BOOLEAN`).
3. **`semillero`**: `id` (`INT` PK), `nombre` (`VARCHAR(60)`), `fecha_fundacion` (`DATE`), `grupo_investigacion` (`INT` FK NOT NULL $\rightarrow$ `grupo_investigacion.id`), `activo` (`BOOLEAN`).
4. **`participa_grupo`**: `docente_cedula` (`INT` PK/FK), `grupo_investigacion_id` (`INT` PK/FK), `rol` (`VARCHAR(15)`), `fecha_inicio` (`DATE`), `fecha_fin` (`DATE` NULL), `activo` (`BOOLEAN`).
5. **`participa_semillero`**: `docente` (`INT` PK/FK), `semillero` (`INT` PK/FK), `rol` (`VARCHAR(15)`), `fecha_inicio` (`DATE`), `fecha_fin` (`DATE` NULL), `activo` (`BOOLEAN`).
6. **`grupo_linea`**: `grupo_investigacion` (`INT` PK/FK), `linea_investigacion` (`INT` PK/FK), `activo` (`BOOLEAN`).
7. **`semillero_linea`**: `semillero` (`INT` PK/FK), `linea_investigacion` (`INT` PK/FK), `activo` (`BOOLEAN`).
8. **`ac_linea`**: `linea_investigacion` (`INT` PK/FK), `area_conocimiento` (`VARCHAR(6)` PK/FK), `activo` (`BOOLEAN`).
9. **`ods_linea`**: `linea_investigacion` (`INT` PK/FK), `ods` (`INT` PK/FK), `activo` (`BOOLEAN`).
10. **`aa_linea`**: `area_aplicacion` (`INT` PK/FK), `linea_investigacion` (`INT` PK/FK), `activo` (`BOOLEAN`).