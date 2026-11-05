# Modelo de datos de la v2

## Alcance

La v2 gestiona diez tablas del módulo de investigación. El alcance se
contrastó con las rutas registradas en
[`api_investigacion/main.py`](../api_investigacion/main.py), los repositorios
PostgreSQL y las pruebas de [`api_investigacion/pruebas/prueba_v2.py`](../api_investigacion/pruebas/prueba_v2.py).
Una fila de cualquiera de estas tablas representa un registro de negocio
visible para la aplicación o una relación explícita entre dos registros.

Las tablas de referencia son `area_conocimiento`, `objetivo_desarrollo_sostenible`,
`area_aplicacion` y `universidad`. Sus endpoints se consultan para llenar
desplegables; no forman parte de las diez pantallas de gestión. El SQL también
incluye `termino_clave`, `rol`, `usuario` y `rol_usuario`, pero la v2 no los
gestiona ni los usa como catálogos de sus formularios.

En las tablas de gestión, `activo` implementa el borrado lógico. La API no lo
devuelve en sus listados y consultas, y las consultas PostgreSQL solo consideran
filas con `activo = TRUE`.

## Tablas gestionadas por la v2

### `linea_investigacion`

Una fila representa una línea temática de investigación. Su identificador lo
asigna PostgreSQL mediante la secuencia de `SERIAL`. La API actualmente la
consulta mediante [`linea_investigacion_controller.py`](../api_investigacion/controllers/linea_investigacion_controller.py);
su repositorio solo expone listado y consulta.

**Clave primaria:** `id`.

| Columna | Tipo SQL | ¿Admite NULL? | Función |
|---|---|---:|---|
| `id` | `SERIAL` | No | Identificador de la línea; la clave primaria lo hace no nulo. |
| `nombre` | `VARCHAR(45)` | No | Nombre de la línea. |
| `descripcion` | `VARCHAR(256)` | No | Descripción de la línea. |
| `activo` | `BOOLEAN` | No | Marca de vigencia para el borrado lógico; valor predeterminado `TRUE`. |

### `docente`

Una fila representa un docente que puede pertenecer a grupos y semilleros y
tener una línea de investigación principal.

**Clave primaria:** `cedula`.

| Columna | Tipo SQL | ¿Admite NULL? | Función |
|---|---|---:|---|
| `cedula` | `INT` | No | Identificador del docente. |
| `nombres` | `VARCHAR(60)` | No | Nombres. |
| `apellidos` | `VARCHAR(60)` | No | Apellidos. |
| `genero` | `VARCHAR(12)` | No | Género registrado. |
| `cargo` | `VARCHAR(30)` | No | Cargo institucional. |
| `fecha_nacimiento` | `DATE` | No | Fecha de nacimiento. |
| `correo` | `VARCHAR(70)` | No | Correo electrónico. |
| `telefono` | `VARCHAR(20)` | No | Teléfono de contacto. |
| `url_cvlac` | `VARCHAR(128)` | No | URL del perfil CvLAC. |
| `fecha_actualizacion` | `DATE` | No | Fecha de actualización de la ficha. |
| `escalafon` | `VARCHAR(45)` | No | Escalafón docente. |
| `perfil` | `TEXT` | No | Perfil o reseña del docente. |
| `cat_minciencia` | `VARCHAR(45)` | Sí | Categoría en MinCiencias, si existe. |
| `conv_minciencia` | `VARCHAR(45)` | No | Convocatoria de MinCiencias. |
| `nacionalidaad` | `VARCHAR(45)` | No | Nacionalidad; se conserva el nombre exacto del SQL. |
| `linea_investigacion_principal` | `INT` | Sí | Línea principal; referencia a `linea_investigacion.id`. |
| `activo` | `BOOLEAN` | No | Vigencia lógica; valor predeterminado `TRUE`. |

**Claves foráneas:** `linea_investigacion_principal` ->
`linea_investigacion(id)`.

La definición Pydantic correspondiente está en
[`models/docente.py`](../api_investigacion/models/docente.py).

### `grupo_investigacion`

Una fila representa un grupo de investigación. Puede estar asociado a una
universidad de referencia y relacionarse con docentes, líneas y semilleros.

**Clave primaria:** `id`.

| Columna | Tipo SQL | ¿Admite NULL? | Función |
|---|---|---:|---|
| `id` | `INT` | No | Identificador del grupo. |
| `nombre` | `VARCHAR(60)` | No | Nombre del grupo. |
| `url_gruplac` | `VARCHAR(128)` | Sí | URL de GrupLAC. |
| `categoria` | `VARCHAR(10)` | Sí | Categoría del grupo. |
| `convocatoria` | `VARCHAR(10)` | Sí | Convocatoria asociada. |
| `fecha_fundacion` | `DATE` | No | Fecha de fundación. |
| `universidsad` | `INT` | Sí | Universidad de referencia; el nombre conserva el typo del SQL. |
| `interno` | `SMALLINT` | No | Indicador numérico de grupo interno. |
| `ambito` | `VARCHAR(45)` | No | Ámbito del grupo. |
| `activo` | `BOOLEAN` | No | Vigencia lógica; valor predeterminado `TRUE`. |

**Claves foráneas:** `universidsad` -> `universidad(id)`.

La API conserva el nombre `universidsad`, como se ve en
[`models/grupo_investigacion.py`](../api_investigacion/models/grupo_investigacion.py).

### `semillero`

Una fila representa un semillero de investigación perteneciente a un grupo.

**Clave primaria:** `id`.

| Columna | Tipo SQL | ¿Admite NULL? | Función |
|---|---|---:|---|
| `id` | `INT` | No | Identificador del semillero. |
| `nombre` | `VARCHAR(60)` | No | Nombre del semillero. |
| `fecha_fundacion` | `DATE` | No | Fecha de fundación. |
| `grupo_investigacion` | `INT` | No | Grupo propietario; referencia a `grupo_investigacion.id`. |
| `activo` | `BOOLEAN` | No | Vigencia lógica; valor predeterminado `TRUE`. |

**Claves foráneas:** `grupo_investigacion` ->
`grupo_investigacion(id)`.

La API comprueba que el grupo exista y esté activo antes de crear o actualizar
una fila, mediante [`servicio_semillero.py`](../api_investigacion/servicios/servicio_semillero.py).

### `participa_grupo`

Una fila representa la participación de un docente en un grupo, con su rol y
periodo de participación.

**Clave primaria compuesta, en orden:** (`docente_cedula`,
`grupo_investigacion_id`).

| Columna | Tipo SQL | ¿Admite NULL? | Función |
|---|---|---:|---|
| `docente_cedula` | `INT` | No | Docente participante; referencia a `docente.cedula`. |
| `grupo_investigacion_id` | `INT` | No | Grupo participante; referencia a `grupo_investigacion.id`. |
| `rol` | `VARCHAR(15)` | No | Rol del docente en el grupo. |
| `fecha_inicio` | `DATE` | No | Inicio de la participación. |
| `fecha_fin` | `DATE` | Sí | Fin de la participación, si terminó. |
| `activo` | `BOOLEAN` | No | Vigencia lógica; valor predeterminado `TRUE`. |

**Claves foráneas:** `docente_cedula` -> `docente(cedula)`;
`grupo_investigacion_id` -> `grupo_investigacion(id)`.

### `participa_semillero`

Una fila representa la participación de un docente en un semillero, con su rol
y periodo.

**Clave primaria compuesta, en orden:** (`docente`, `semillero`).

| Columna | Tipo SQL | ¿Admite NULL? | Función |
|---|---|---:|---|
| `docente` | `INT` | No | Docente participante; referencia a `docente.cedula`. |
| `semillero` | `INT` | No | Semillero participante; referencia a `semillero.id`. |
| `rol` | `VARCHAR(15)` | No | Rol del docente en el semillero. |
| `fecha_inicio` | `DATE` | No | Inicio de la participación. |
| `fecha_fin` | `DATE` | Sí | Fin de la participación, si terminó. |
| `activo` | `BOOLEAN` | No | Vigencia lógica; valor predeterminado `TRUE`. |

**Claves foráneas:** `docente` -> `docente(cedula)`; `semillero` ->
`semillero(id)`.

### `semillero_linea`

Una fila representa la asociación entre un semillero y una línea de
investigación.

**Clave primaria compuesta, en orden:** (`semillero`, `linea_investigacion`).

| Columna | Tipo SQL | ¿Admite NULL? | Función |
|---|---|---:|---|
| `semillero` | `INT` | No | Semillero asociado; referencia a `semillero.id`. |
| `linea_investigacion` | `INT` | No | Línea asociada; referencia a `linea_investigacion.id`. |
| `activo` | `BOOLEAN` | No | Vigencia lógica; valor predeterminado `TRUE`. |

**Claves foráneas:** `semillero` -> `semillero(id)`;
`linea_investigacion` -> `linea_investigacion(id)`.

### `grupo_linea`

Una fila representa la asociación entre un grupo de investigación y una línea.

**Clave primaria compuesta, en orden:** (`grupo_investigacion`,
`linea_investigacion`).

| Columna | Tipo SQL | ¿Admite NULL? | Función |
|---|---|---:|---|
| `grupo_investigacion` | `INT` | No | Grupo asociado; referencia a `grupo_investigacion.id`. |
| `linea_investigacion` | `INT` | No | Línea asociada; referencia a `linea_investigacion.id`. |
| `activo` | `BOOLEAN` | No | Vigencia lógica; valor predeterminado `TRUE`. |

**Claves foráneas:** `grupo_investigacion` -> `grupo_investigacion(id)`;
`linea_investigacion` -> `linea_investigacion(id)`.

### `ac_linea`

Una fila representa la asociación entre una línea y un área de conocimiento
del catálogo.

**Clave primaria compuesta, en orden:** (`linea_investigacion`,
`area_conocimiento`).

| Columna | Tipo SQL | ¿Admite NULL? | Función |
|---|---|---:|---|
| `linea_investigacion` | `INT` | No | Línea asociada; referencia a `linea_investigacion.id`. |
| `area_conocimiento` | `VARCHAR(6)` | No | Código del área; referencia a `area_conocimiento.id`. |
| `activo` | `BOOLEAN` | No | Vigencia lógica; valor predeterminado `TRUE`. |

**Claves foráneas:** `linea_investigacion` -> `linea_investigacion(id)`;
`area_conocimiento` -> `area_conocimiento(id)`.

El tipo textual de `area_conocimiento` es intencional: el cambio de `INT` a
`VARCHAR(6)` aparece documentado en [`db/init.sql`](../db/init.sql) y también
está reflejado en [`models/ac_linea.py`](../api_investigacion/models/ac_linea.py).

### `ods_linea`

Una fila representa la asociación entre una línea y un Objetivo de Desarrollo
Sostenible del catálogo.

**Clave primaria compuesta, en orden:** (`linea_investigacion`, `ods`).

| Columna | Tipo SQL | ¿Admite NULL? | Función |
|---|---|---:|---|
| `linea_investigacion` | `INT` | No | Línea asociada; referencia a `linea_investigacion.id`. |
| `ods` | `INT` | No | ODS asociado; referencia a `objetivo_desarrollo_sostenible.id`. |
| `activo` | `BOOLEAN` | No | Vigencia lógica; valor predeterminado `TRUE`. |

**Claves foráneas:** `linea_investigacion` -> `linea_investigacion(id)`;
`ods` -> `objetivo_desarrollo_sostenible(id)`.

### `aa_linea`

Una fila representa la asociación entre una línea y un área de aplicación del
catálogo.

**Clave primaria compuesta, en orden:** (`area_aplicacion`,
`linea_investigacion`).

| Columna | Tipo SQL | ¿Admite NULL? | Función |
|---|---|---:|---|
| `area_aplicacion` | `INT` | No | Área asociada; referencia a `area_aplicacion.id`. |
| `linea_investigacion` | `INT` | No | Línea asociada; referencia a `linea_investigacion.id`. |
| `activo` | `BOOLEAN` | No | Vigencia lógica; valor predeterminado `TRUE`. |

**Claves foráneas:** `area_aplicacion` -> `area_aplicacion(id)`;
`linea_investigacion` -> `linea_investigacion(id)`.

## PostgreSQL frente a la API

### Restricciones de PostgreSQL

[`db/init.sql`](../db/init.sql) impone los tipos, longitudes declaradas,
`NOT NULL`, claves primarias y claves foráneas. Por tanto, no permite una fila
duplicada según su clave primaria ni una referencia a una clave inexistente.
También asigna `TRUE` por defecto a `activo` y conserva físicamente las filas
desactivadas. Las claves foráneas no tienen `ON DELETE CASCADE` en las diez
tablas de gestión: el borrado físico de un padre con dependientes sería
rechazado por PostgreSQL.

### Validaciones de la API

Los modelos Pydantic de `api_investigacion/models/` rechazan campos
desconocidos, comprueban tipos, longitudes y cadenas vacías, y diferencian
`PUT` (todos los campos del reemplazo) de `PATCH` (solo los campos enviados).
Los servicios consultan que cada referencia exista y esté activa antes de
guardar. También comprueban que un registro padre no tenga relaciones activas
antes de marcarlo como inactivo. El borrado lógico se ejecuta como
`UPDATE ... SET activo = FALSE`; no se hace `DELETE`, y la API no permite
reactivar enviando `activo = TRUE`.

La API además filtra las filas inactivas en los `SELECT` y convierte una
actualización inválida en un error sin escribir los datos anteriores. Estas
reglas de negocio no son restricciones declaradas en el SQL.

### Diferencias comprobadas

* `activo` existe y es obligatorio en el SQL, pero no forma parte de los
  modelos públicos ni de las respuestas de la API; el repositorio lo fija en
  `TRUE` al crear.
* El SQL declara `cat_minciencia` y
  `linea_investigacion_principal` como opcionales, pero
  [`models/docente.py`](../api_investigacion/models/docente.py) los incluye en
  el contrato de entrada y solo permite `None` para esos dos campos. En
  cambio, los otros campos `NOT NULL` se rechazan explícitamente como nulos
  durante un `PATCH`.
* El SQL permite `NULL` en los campos opcionales de
  `grupo_investigacion` y `fecha_fin`; la API conserva esa posibilidad, pero
  rechaza `None` para los campos que el SQL declara `NOT NULL`, mediante los
  validadores de los modelos.
* El SQL solo garantiza que una FK apunte a una fila existente. La API añade
  la condición de que esa fila esté activa y bloquea la desactivación de un
  padre con dependientes activos.
* `linea_investigacion` se crea con `SERIAL` en PostgreSQL, mientras que la
  API solo la consulta actualmente: su controlador no ofrece `POST`, `PUT`,
  `PATCH` ni `DELETE`. Esto se ve en
  [`linea_investigacion_controller.py`](../api_investigacion/controllers/linea_investigacion_controller.py)
  y [`repositorio_linea_investigacion_postgresql.py`](../api_investigacion/repositorios/repositorio_linea_investigacion_postgresql.py).

## Ejemplo de relación

Supóngase la línea `id = 7` y el área de conocimiento de código `1A01`.
Una fila de `ac_linea` con
`(linea_investigacion, area_conocimiento) = (7, '1A01')` significa que la
línea 7 está clasificada en esa área. PostgreSQL verifica mediante sus dos
claves foráneas que exista `linea_investigacion.id = 7` y que exista
`area_conocimiento.id = '1A01'`; la clave primaria compuesta impide repetir la
misma asociación.

Antes de insertar, el servicio de `ac_linea` vuelve a comprobar que ambas
referencias estén activas. Si el área existe pero está desactivada, la API
rechaza la operación aunque PostgreSQL consideraría válida la FK. Si después
se desactiva la asociación, la fila permanece con `activo = FALSE`, deja de
aparecer en los listados y no se reutiliza como una asociación activa.
