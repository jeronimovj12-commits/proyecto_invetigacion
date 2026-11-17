-- ============================================================
-- Base de datos del módulo INVESTIGACIÓN — PostgreSQL
--
-- Este script SE DERIVA del que entrega el curso
-- (ProyectosDeAula/db_scripts/postgresql/investigacion.pg.sql). No es una
-- copia: le aplica CINCO cambios, y aquí están todos, para que quien lo
-- abra sepa exactamente qué se tocó y por qué.
--
--   1. area_conocimiento.id pasa de INT a VARCHAR(6). Los datos del Excel
--      son códigos alfanuméricos ('1A01'), no enteros: como estaba, el
--      script no podía cargar su propio catálogo. Arrastra a
--      ac_linea.area_conocimiento, que lo referencia.            [C1]
--   2. area_conocimiento.disciplina pasa a VARCHAR(150): el valor más
--      largo del catálogo tiene 124 caracteres y no cabía en 60.  [C2]
--   3. area_aplicacion.nombre pasa a VARCHAR(150): el suyo tiene 129. [C3]
--   4. Las 16 tablas del módulo ganan 'activo BOOLEAN NOT NULL DEFAULT
--      TRUE': el borrado es LÓGICO. Se usa BOOLEAN —el tipo de este
--      motor— y no BIT, que es de otro dialecto.                  [C4]
--   5. Se corrige 'Cienias Naturales' -> 'Ciencias Naturales' en 48
--      filas. Es un error de digitación de la fuente: cargarlo tal cual
--      lo dejaría a la vista en cada listado y en cada informe.    [C5]
--
-- Las 19 tablas se crean COMPLETAS aunque la v1 solo use una: la
-- base es infraestructura dada. Lo que crece por versiones es la API.
--
-- PostgreSQL ejecuta este archivo SOLO en el primer arranque, cuando el
-- volumen está vacío. Para volver a correrlo: docker compose down -v
-- ============================================================


-- ============================================================
-- LIMPIEZA (en orden inverso al de creación; CASCADE por las FK)
-- ============================================================
-- Elimina la tabla indicada si existe; CASCADE tambien retira dependencias.
DROP TABLE IF EXISTS rol_usuario CASCADE;
-- Elimina la tabla indicada si existe; CASCADE tambien retira dependencias.
DROP TABLE IF EXISTS usuario CASCADE;
-- Elimina la tabla indicada si existe; CASCADE tambien retira dependencias.
DROP TABLE IF EXISTS rol CASCADE;
-- Elimina la tabla indicada si existe; CASCADE tambien retira dependencias.
DROP TABLE IF EXISTS aa_linea CASCADE;
-- Elimina la tabla indicada si existe; CASCADE tambien retira dependencias.
DROP TABLE IF EXISTS ods_linea CASCADE;
-- Elimina la tabla indicada si existe; CASCADE tambien retira dependencias.
DROP TABLE IF EXISTS ac_linea CASCADE;
-- Elimina la tabla indicada si existe; CASCADE tambien retira dependencias.
DROP TABLE IF EXISTS grupo_linea CASCADE;
-- Elimina la tabla indicada si existe; CASCADE tambien retira dependencias.
DROP TABLE IF EXISTS semillero_linea CASCADE;
-- Elimina la tabla indicada si existe; CASCADE tambien retira dependencias.
DROP TABLE IF EXISTS participa_grupo CASCADE;
-- Elimina la tabla indicada si existe; CASCADE tambien retira dependencias.
DROP TABLE IF EXISTS participa_semillero CASCADE;
-- Elimina la tabla indicada si existe; CASCADE tambien retira dependencias.
DROP TABLE IF EXISTS semillero CASCADE;
-- Elimina la tabla indicada si existe; CASCADE tambien retira dependencias.
DROP TABLE IF EXISTS grupo_investigacion CASCADE;
-- Elimina la tabla indicada si existe; CASCADE tambien retira dependencias.
DROP TABLE IF EXISTS docente CASCADE;
-- Elimina la tabla indicada si existe; CASCADE tambien retira dependencias.
DROP TABLE IF EXISTS linea_investigacion CASCADE;
-- Elimina la tabla indicada si existe; CASCADE tambien retira dependencias.
DROP TABLE IF EXISTS universidad CASCADE;
-- Elimina la tabla indicada si existe; CASCADE tambien retira dependencias.
DROP TABLE IF EXISTS termino_clave CASCADE;
-- Elimina la tabla indicada si existe; CASCADE tambien retira dependencias.
DROP TABLE IF EXISTS area_aplicacion CASCADE;
-- Elimina la tabla indicada si existe; CASCADE tambien retira dependencias.
DROP TABLE IF EXISTS objetivo_desarrollo_sostenible CASCADE;
-- Elimina la tabla indicada si existe; CASCADE tambien retira dependencias.
DROP TABLE IF EXISTS area_conocimiento CASCADE;


-- ============================================================
-- TABLAS
-- ============================================================

-- Tabla: area_conocimiento
-- Crea la tabla indicada y define sus columnas y restricciones.
CREATE TABLE area_conocimiento (
    -- Declara una columna con su tipo y restricciones.
    id VARCHAR(6) NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    gran_area VARCHAR(60) NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    area VARCHAR(60) NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    disciplina VARCHAR(150) NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    -- Declara la clave primaria que identifica univocamente la fila.
    PRIMARY KEY (id)
-- Cierra la lista de columnas, valores o argumentos abierta.
);

-- Tabla: objetivo_desarrollo_sostenible
-- Crea la tabla indicada y define sus columnas y restricciones.
CREATE TABLE objetivo_desarrollo_sostenible (
    -- Declara una columna con su tipo y restricciones.
    id INT NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    nombre VARCHAR(60) NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    categoria VARCHAR(45) NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    -- Declara la clave primaria que identifica univocamente la fila.
    PRIMARY KEY (id)
-- Cierra la lista de columnas, valores o argumentos abierta.
);

-- Tabla: area_aplicacion
-- Crea la tabla indicada y define sus columnas y restricciones.
CREATE TABLE area_aplicacion (
    -- Declara una columna con su tipo y restricciones.
    id INT NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    nombre VARCHAR(150) NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    -- Declara la clave primaria que identifica univocamente la fila.
    PRIMARY KEY (id)
-- Cierra la lista de columnas, valores o argumentos abierta.
);

-- Tabla: termino_clave
-- Crea la tabla indicada y define sus columnas y restricciones.
CREATE TABLE termino_clave (
    -- Declara una columna con su tipo y restricciones.
    termino VARCHAR(30) NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    termino_ingles VARCHAR(30),
    -- Declara una columna con su tipo y restricciones.
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    -- Declara la clave primaria que identifica univocamente la fila.
    PRIMARY KEY (termino)
-- Cierra la lista de columnas, valores o argumentos abierta.
);

-- Tabla: universidad
-- Crea la tabla indicada y define sus columnas y restricciones.
CREATE TABLE universidad (
    -- Declara una columna con su tipo y restricciones.
    id INT NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    nombre VARCHAR(60) NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    tipo VARCHAR(45) NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    ciudad VARCHAR(45) NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    -- Declara la clave primaria que identifica univocamente la fila.
    PRIMARY KEY (id)
-- Cierra la lista de columnas, valores o argumentos abierta.
);

-- Tabla: linea_investigacion
-- Crea la tabla indicada y define sus columnas y restricciones.
CREATE TABLE linea_investigacion (
    -- Declara una columna con su tipo y restricciones.
    id SERIAL,
    -- Declara una columna con su tipo y restricciones.
    nombre VARCHAR(45) NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    descripcion VARCHAR(256) NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    -- Declara la clave primaria que identifica univocamente la fila.
    PRIMARY KEY (id)
-- Cierra la lista de columnas, valores o argumentos abierta.
);

-- Tabla: docente
-- Crea la tabla indicada y define sus columnas y restricciones.
CREATE TABLE docente (
    -- Declara una columna con su tipo y restricciones.
    cedula INT NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    nombres VARCHAR(60) NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    apellidos VARCHAR(60) NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    genero VARCHAR(12) NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    cargo VARCHAR(30) NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    fecha_nacimiento DATE NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    correo VARCHAR(70) NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    telefono VARCHAR(20) NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    url_cvlac VARCHAR(128) NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    fecha_actualizacion DATE NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    escalafon VARCHAR(45) NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    perfil TEXT NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    cat_minciencia VARCHAR(45),
    -- Declara una columna con su tipo y restricciones.
    conv_minciencia VARCHAR(45) NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    nacionalidaad VARCHAR(45) NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    linea_investigacion_principal INT,
    -- Declara una columna con su tipo y restricciones.
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    -- Declara la clave primaria que identifica univocamente la fila.
    PRIMARY KEY (cedula),
    -- Declara una clave foranea hacia la tabla referenciada.
    FOREIGN KEY (linea_investigacion_principal) REFERENCES linea_investigacion(id)
-- Cierra la lista de columnas, valores o argumentos abierta.
);

-- Tabla: grupo_investigacion
-- Crea la tabla indicada y define sus columnas y restricciones.
CREATE TABLE grupo_investigacion (
    -- Declara una columna con su tipo y restricciones.
    id INT NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    nombre VARCHAR(60) NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    url_gruplac VARCHAR(128),
    -- Declara una columna con su tipo y restricciones.
    categoria VARCHAR(10),
    -- Declara una columna con su tipo y restricciones.
    convocatoria VARCHAR(10),
    -- Declara una columna con su tipo y restricciones.
    fecha_fundacion DATE NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    universidsad INT,
    -- Declara una columna con su tipo y restricciones.
    interno SMALLINT NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    ambito VARCHAR(45) NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    -- Declara la clave primaria que identifica univocamente la fila.
    PRIMARY KEY (id),
    -- Declara una clave foranea hacia la tabla referenciada.
    FOREIGN KEY (universidsad) REFERENCES universidad(id)
-- Cierra la lista de columnas, valores o argumentos abierta.
);

-- Tabla: semillero
-- Crea la tabla indicada y define sus columnas y restricciones.
CREATE TABLE semillero (
    -- Declara una columna con su tipo y restricciones.
    id INT NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    nombre VARCHAR(60) NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    fecha_fundacion DATE NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    grupo_investigacion INT NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    -- Declara la clave primaria que identifica univocamente la fila.
    PRIMARY KEY (id),
    -- Declara una clave foranea hacia la tabla referenciada.
    FOREIGN KEY (grupo_investigacion) REFERENCES grupo_investigacion(id)
-- Cierra la lista de columnas, valores o argumentos abierta.
);

-- Tabla: participa_semillero
-- Crea la tabla indicada y define sus columnas y restricciones.
CREATE TABLE participa_semillero (
    -- Declara una columna con su tipo y restricciones.
    docente INT NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    semillero INT NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    rol VARCHAR(15) NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    fecha_inicio DATE NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    fecha_fin DATE,
    -- Declara una columna con su tipo y restricciones.
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    -- Declara la clave primaria que identifica univocamente la fila.
    PRIMARY KEY (docente, semillero),
    -- Declara una clave foranea hacia la tabla referenciada.
    FOREIGN KEY (docente) REFERENCES docente(cedula),
    -- Declara una clave foranea hacia la tabla referenciada.
    FOREIGN KEY (semillero) REFERENCES semillero(id)
-- Cierra la lista de columnas, valores o argumentos abierta.
);

-- Tabla: participa_grupo
-- Crea la tabla indicada y define sus columnas y restricciones.
CREATE TABLE participa_grupo (
    -- Declara una columna con su tipo y restricciones.
    docente_cedula INT NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    grupo_investigacion_id INT NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    rol VARCHAR(15) NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    fecha_inicio DATE NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    fecha_fin DATE,
    -- Declara una columna con su tipo y restricciones.
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    -- Declara la clave primaria que identifica univocamente la fila.
    PRIMARY KEY (docente_cedula, grupo_investigacion_id),
    -- Declara una clave foranea hacia la tabla referenciada.
    FOREIGN KEY (docente_cedula) REFERENCES docente(cedula),
    -- Declara una clave foranea hacia la tabla referenciada.
    FOREIGN KEY (grupo_investigacion_id) REFERENCES grupo_investigacion(id)
-- Cierra la lista de columnas, valores o argumentos abierta.
);

-- Tabla: semillero_linea
-- Crea la tabla indicada y define sus columnas y restricciones.
CREATE TABLE semillero_linea (
    -- Declara una columna con su tipo y restricciones.
    semillero INT NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    linea_investigacion INT NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    -- Declara la clave primaria que identifica univocamente la fila.
    PRIMARY KEY (semillero, linea_investigacion),
    -- Declara una clave foranea hacia la tabla referenciada.
    FOREIGN KEY (semillero) REFERENCES semillero(id),
    -- Declara una clave foranea hacia la tabla referenciada.
    FOREIGN KEY (linea_investigacion) REFERENCES linea_investigacion(id)
-- Cierra la lista de columnas, valores o argumentos abierta.
);

-- Tabla: grupo_linea
-- Crea la tabla indicada y define sus columnas y restricciones.
CREATE TABLE grupo_linea (
    -- Declara una columna con su tipo y restricciones.
    grupo_investigacion INT NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    linea_investigacion INT NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    -- Declara la clave primaria que identifica univocamente la fila.
    PRIMARY KEY (grupo_investigacion, linea_investigacion),
    -- Declara una clave foranea hacia la tabla referenciada.
    FOREIGN KEY (grupo_investigacion) REFERENCES grupo_investigacion(id),
    -- Declara una clave foranea hacia la tabla referenciada.
    FOREIGN KEY (linea_investigacion) REFERENCES linea_investigacion(id)
-- Cierra la lista de columnas, valores o argumentos abierta.
);

-- Tabla: ac_linea
-- Crea la tabla indicada y define sus columnas y restricciones.
CREATE TABLE ac_linea (
    -- Declara una columna con su tipo y restricciones.
    linea_investigacion INT NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    area_conocimiento VARCHAR(6) NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    -- Declara la clave primaria que identifica univocamente la fila.
    PRIMARY KEY (linea_investigacion, area_conocimiento),
    -- Declara una clave foranea hacia la tabla referenciada.
    FOREIGN KEY (linea_investigacion) REFERENCES linea_investigacion(id),
    -- Declara una clave foranea hacia la tabla referenciada.
    FOREIGN KEY (area_conocimiento) REFERENCES area_conocimiento(id)
-- Cierra la lista de columnas, valores o argumentos abierta.
);

-- Tabla: ods_linea
-- Crea la tabla indicada y define sus columnas y restricciones.
CREATE TABLE ods_linea (
    -- Declara una columna con su tipo y restricciones.
    linea_investigacion INT NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    ods INT NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    -- Declara la clave primaria que identifica univocamente la fila.
    PRIMARY KEY (linea_investigacion, ods),
    -- Declara una clave foranea hacia la tabla referenciada.
    FOREIGN KEY (linea_investigacion) REFERENCES linea_investigacion(id),
    -- Declara una clave foranea hacia la tabla referenciada.
    FOREIGN KEY (ods) REFERENCES objetivo_desarrollo_sostenible(id)
-- Cierra la lista de columnas, valores o argumentos abierta.
);

-- Tabla: aa_linea
-- Crea la tabla indicada y define sus columnas y restricciones.
CREATE TABLE aa_linea (
    -- Declara una columna con su tipo y restricciones.
    area_aplicacion INT NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    linea_investigacion INT NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    -- Declara la clave primaria que identifica univocamente la fila.
    PRIMARY KEY (area_aplicacion, linea_investigacion),
    -- Declara una clave foranea hacia la tabla referenciada.
    FOREIGN KEY (area_aplicacion) REFERENCES area_aplicacion(id),
    -- Declara una clave foranea hacia la tabla referenciada.
    FOREIGN KEY (linea_investigacion) REFERENCES linea_investigacion(id)
-- Cierra la lista de columnas, valores o argumentos abierta.
);

-- Tabla: rol
-- Crea la tabla indicada y define sus columnas y restricciones.
CREATE TABLE rol (
    -- Declara una columna con su tipo y restricciones.
    id SERIAL PRIMARY KEY,
    -- Declara una columna con su tipo y restricciones.
    nombre VARCHAR(100) NOT NULL UNIQUE,
    -- Declara una columna con su tipo y restricciones.
    descripcion TEXT,
    -- Declara una columna con su tipo y restricciones.
    activo BOOLEAN DEFAULT TRUE,
    -- Declara una columna con su tipo y restricciones.
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- Cierra la lista de columnas, valores o argumentos abierta.
);

-- Tabla: usuario
-- Crea la tabla indicada y define sus columnas y restricciones.
CREATE TABLE usuario (
    -- Declara una columna con su tipo y restricciones.
    id SERIAL PRIMARY KEY,
    -- Declara una columna con su tipo y restricciones.
    username VARCHAR(100) NOT NULL UNIQUE,
    -- Declara una columna con su tipo y restricciones.
    password VARCHAR(255) NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    email VARCHAR(150) NOT NULL UNIQUE,
    -- Declara una columna con su tipo y restricciones.
    nombre_completo VARCHAR(200),
    -- Declara una columna con su tipo y restricciones.
    activo BOOLEAN DEFAULT TRUE,
    -- Declara una columna con su tipo y restricciones.
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- Declara una columna con su tipo y restricciones.
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- Cierra la lista de columnas, valores o argumentos abierta.
);

-- Tabla: rol_usuario
-- Crea la tabla indicada y define sus columnas y restricciones.
CREATE TABLE rol_usuario (
    -- Declara una columna con su tipo y restricciones.
    usuario_id INT NOT NULL,
    -- Declara una columna con su tipo y restricciones.
    rol_id INT NOT NULL,
    -- Declara la clave primaria que identifica univocamente la fila.
    PRIMARY KEY (usuario_id, rol_id),
    -- Declara una clave foranea hacia la tabla referenciada.
    FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE CASCADE,
    -- Declara una clave foranea hacia la tabla referenciada.
    FOREIGN KEY (rol_id) REFERENCES rol(id) ON DELETE CASCADE
-- Cierra la lista de columnas, valores o argumentos abierta.
);


-- ============================================================
-- DATOS DE REFERENCIA (del Excel del módulo)
-- ============================================================

-- area_conocimiento: 218 filas
-- Inicia la insercion de filas en la tabla indicada.
INSERT INTO area_conocimiento (id, gran_area, area, disciplina) VALUES
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1A01', 'Ciencias Naturales', 'Matemáticas', 'Matemáticas puras'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1A02', 'Ciencias Naturales', 'Matemáticas', 'Matemáticas aplicadas'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1A03', 'Ciencias Naturales', 'Matemáticas', 'Estadística y probabilidades (investigación en metodologías)'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1B01', 'Ciencias Naturales', 'Coputación y ciencias de la información', 'Ciencias de la Computación'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1B02', 'Ciencias Naturales', 'Coputación y ciencias de la información', 'Ciencias de la Información y bioinformática (hardware en 2.B y aspectos sociales en 5.8)'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1C01', 'Ciencias Naturales', 'Ciencias físicas', 'Física Atómica, molecular y química'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1C02', 'Ciencias Naturales', 'Ciencias físicas', 'Física de la materia'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1C03', 'Ciencias Naturales', 'Ciencias físicas', 'Física de partículas y campos'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1C04', 'Ciencias Naturales', 'Ciencias físicas', 'Física nuclear'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1C05', 'Ciencias Naturales', 'Ciencias físicas', 'Física de plasmas y fluidos'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1C06', 'Ciencias Naturales', 'Ciencias físicas', 'Óptica'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1C07', 'Ciencias Naturales', 'Ciencias físicas', 'Acústica'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1C08', 'Ciencias Naturales', 'Ciencias físicas', 'Astronomía'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1D01', 'Ciencias Naturales', 'Ciencias químicas', 'Química orgánica'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1D02', 'Ciencias Naturales', 'Ciencias químicas', 'Química inorgánica y nuclear'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1D03', 'Ciencias Naturales', 'Ciencias químicas', 'Química física'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1D04', 'Ciencias Naturales', 'Ciencias químicas', 'Ciencia de los polímeros'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1D05', 'Ciencias Naturales', 'Ciencias químicas', 'Electroquímica'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1D06', 'Ciencias Naturales', 'Ciencias químicas', 'Química de los coloides'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1D07', 'Ciencias Naturales', 'Ciencias químicas', 'Química analítica'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1E01', 'Ciencias Naturales', 'Ciencias de la tierra y medioambientales', 'Geociencias (multidisciplinario)'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1E02', 'Ciencias Naturales', 'Ciencias de la tierra y medioambientales', 'Mineralogía'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1E03', 'Ciencias Naturales', 'Ciencias de la tierra y medioambientales', 'Paleontología'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1E04', 'Ciencias Naturales', 'Ciencias de la tierra y medioambientales', 'Geoquímica y geofísica'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1E05', 'Ciencias Naturales', 'Ciencias de la tierra y medioambientales', 'Geografía Física'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1E06', 'Ciencias Naturales', 'Ciencias de la tierra y medioambientales', 'Geología'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1E07', 'Ciencias Naturales', 'Ciencias de la tierra y medioambientales', 'Vulcanología'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1E08', 'Ciencias Naturales', 'Ciencias de la tierra y medioambientales', 'Ciencias del medio ambiente (aspectos sociales en 5.G)'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1E09', 'Ciencias Naturales', 'Ciencias de la tierra y medioambientales', 'Meteorología y ciencias atmosféricas'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1E10', 'Ciencias Naturales', 'Ciencias de la tierra y medioambientales', 'Investicación del clima.'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1E11', 'Ciencias Naturales', 'Ciencias de la tierra y medioambientales', 'Oceanografía, hidrología y recursos del agua'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1F01', 'Ciencias Naturales', 'Ciencias biológicas', 'Biología celular y microbiología'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1F02', 'Ciencias Naturales', 'Ciencias biológicas', 'Virología'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1F03', 'Ciencias Naturales', 'Ciencias biológicas', 'Bioquímica y biología molecular'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1F04', 'Ciencias Naturales', 'Ciencias biológicas', 'Métodos de investigación en bioquímica'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1F05', 'Ciencias Naturales', 'Ciencias biológicas', 'Micología'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1F06', 'Ciencias Naturales', 'Ciencias biológicas', 'Biofísica'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1F07', 'Ciencias Naturales', 'Ciencias biológicas', 'Genética y herencia (aspectos médicos en 3)'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1F08', 'Ciencias Naturales', 'Ciencias biológicas', 'Biología reproductiva (aspectos médicos en 3)'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1F09', 'Ciencias Naturales', 'Ciencias biológicas', 'Biología del desarrollo'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1F10', 'Ciencias Naturales', 'Ciencias biológicas', 'Botánica y ciencias de las plantas'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1F11', 'Ciencias Naturales', 'Ciencias biológicas', 'Zoología, Ornitología, Entomología, ciencias biológicas del comportamiento'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1F12', 'Ciencias Naturales', 'Ciencias biológicas', 'Biología marina del agua'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1F13', 'Ciencias Naturales', 'Ciencias biológicas', 'Ecología'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1F14', 'Ciencias Naturales', 'Ciencias biológicas', 'Conservación de la biodiversidad'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1F15', 'Ciencias Naturales', 'Ciencias biológicas', 'Biología (Teórica, matemática, criobiología, evolutiva…)'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1F16', 'Ciencias Naturales', 'Ciencias biológicas', 'Otras Biologías'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('1G01', 'Ciencias Naturales', 'Otras ciencias naturales', 'Otras ciencias naturales'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('2A01', 'Ingeniería y Tecnología', 'Ingeniería civil', 'Ingeniería civil'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('2A02', 'Ingeniería y Tecnología', 'Ingeniería civil', 'Ingeniería arquitectónica'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('2A03', 'Ingeniería y Tecnología', 'Ingeniería civil', 'Ingeniería de la construcción'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('2A04', 'Ingeniería y Tecnología', 'Ingeniería civil', 'Ingeniería estructural y municipal'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('2A05', 'Ingeniería y Tecnología', 'Ingeniería civil', 'Ingeniería del transporte'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('2B01', 'Ingeniería y Tecnología', 'Ingenierías Eléctrica, Electrónica e Informática', 'Ingeniería eléctrica y electrónica'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('2B02', 'Ingeniería y Tecnología', 'Ingenierías Eléctrica, Electrónica e Informática', 'Robótica y control automático'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('2B03', 'Ingeniería y Tecnología', 'Ingenierías Eléctrica, Electrónica e Informática', 'Automatización y sistemas de control'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('2B04', 'Ingeniería y Tecnología', 'Ingenierías Eléctrica, Electrónica e Informática', 'Ingeniería de sistemas y comunicaciones'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('2B05', 'Ingeniería y Tecnología', 'Ingenierías Eléctrica, Electrónica e Informática', 'Telecomunicaciones'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('2B06', 'Ingeniería y Tecnología', 'Ingenierías Eléctrica, Electrónica e Informática', 'Hardware y arquitectura de computadores'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('2C01', 'Ingeniería y Tecnología', 'Ingeniería Mecánica', 'Ingeniería mecánica'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('2C02', 'Ingeniería y Tecnología', 'Ingeniería Mecánica', 'Mecánica aplicada'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('2C03', 'Ingeniería y Tecnología', 'Ingeniería Mecánica', 'Termodinámica'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('2C04', 'Ingeniería y Tecnología', 'Ingeniería Mecánica', 'Ingeniería aeroespacial'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('2C05', 'Ingeniería y Tecnología', 'Ingeniería Mecánica', 'Ingeniería nuclear (física nuclear en 1.C)'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('2C06', 'Ingeniería y Tecnología', 'Ingeniería Mecánica', 'Ingeniería de audio'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('2D01', 'Ingeniería y Tecnología', 'Ingeniería Química', 'Ingeniería química (plantas y productos)'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('2D02', 'Ingeniería y Tecnología', 'Ingeniería Química', 'Ingeniería de procesos'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('2E01', 'Ingeniería y Tecnología', 'Ingeniería de los Materiales', 'Ingeniería mecánica'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('2E02', 'Ingeniería y Tecnología', 'Ingeniería de los Materiales', 'Cerámicos'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('2E03', 'Ingeniería y Tecnología', 'Ingeniería de los Materiales', 'Recubrimientos y películas'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('2E04', 'Ingeniería y Tecnología', 'Ingeniería de los Materiales', 'Compuestos (laminados, plásticos reforzados, fira sintéticas y naturales, e ECA.)'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('2E05', 'Ingeniería y Tecnología', 'Ingeniería de los Materiales', 'Papel y madera'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('2E06', 'Ingeniería y Tecnología', 'Ingeniería de los Materiales', 'Textiles (Nanomateriales en 2.J y biomateriales en 2.I)'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('2F01', 'Ingeniería y Tecnología', 'Ingeniería Médica', 'Ingeniería médica'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('2F02', 'Ingeniería y Tecnología', 'Ingeniería Médica', 'Tecnología médica de laboratorio (análisis de muestras, tecnologías para el diagnóstico)'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('2G01', 'Ingeniería y Tecnología', 'Ingeniería Ambiental', 'Ingeniería ambiental y geológica'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('2G02', 'Ingeniería y Tecnología', 'Ingeniería Ambiental', 'Geotécnicas'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('2G03', 'Ingeniería y Tecnología', 'Ingeniería Ambiental', 'Ingeniería del petróleo (combustibles, aceites), energía y combustibles'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('2G04', 'Ingeniería y Tecnología', 'Ingeniería Ambiental', 'Sensores remotos'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('2G05', 'Ingeniería y Tecnología', 'Ingeniería Ambiental', 'Mineria y procesamiento de minerales'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('2G06', 'Ingeniería y Tecnología', 'Ingeniería Ambiental', 'Ingeniería marina, naves'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('2G07', 'Ingeniería y Tecnología', 'Ingeniería Ambiental', 'Ingeniería oceanográfica'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('2H01', 'Ingeniería y Tecnología', 'Biotecnología Ambiental', 'Biotecnología industrial'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('2H02', 'Ingeniería y Tecnología', 'Biotecnología Ambiental', 'Bioremediación, biotecnología para el diagnóstico (Chips ADN y biosensores) en manejo ambiental'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('2H03', 'Ingeniería y Tecnología', 'Biotecnología Ambiental', 'Ética relacionada con biotecnología ambiental'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('2I01', 'Ingeniería y Tecnología', 'Biotecnología Industrial', 'Biotecnología industrial'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('2I02', 'Ingeniería y Tecnología', 'Biotecnología Industrial', 'Tecnologías de bioprocesamiento, biocatálisis, fermentación'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('2I03', 'Ingeniería y Tecnología', 'Biotecnología Industrial', 'Bioproductos (productos que se manufacturan usando biotecnología)'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('2J01', 'Ingeniería y Tecnología', 'Nanotecnología', 'Nanomateriales (producción y propiedades)'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('2J02', 'Ingeniería y Tecnología', 'Nanotecnología', 'Nanoprocesos (aplicaciones a nanoescala) (biomateriales en 2.I)'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('2K01', 'Ingeniería y Tecnología', 'Otras Ingenierías y tecnologías', 'Alimentos y bebidas'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('2K02', 'Ingeniería y Tecnología', 'Otras Ingenierías y tecnologías', 'Otras ingenierías y tecnologías'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('2K03', 'Ingeniería y Tecnología', 'Otras Ingenierías y tecnologías', 'Ingeniería de producción'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('2K04', 'Ingeniería y Tecnología', 'Otras Ingenierías y tecnologías', 'Ingeniería Industrial'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3A01', 'Ciencias Médicas y de la Salud', 'Medicina básica', 'Anatomía y morfología (ciencias vegetales en 1.F)'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3A02', 'Ciencias Médicas y de la Salud', 'Medicina básica', 'Genética humana'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3A03', 'Ciencias Médicas y de la Salud', 'Medicina básica', 'Inmunología'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3A04', 'Ciencias Médicas y de la Salud', 'Medicina básica', 'Neurociencias'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3A05', 'Ciencias Médicas y de la Salud', 'Medicina básica', 'Farmacología y farmacia'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3A06', 'Ciencias Médicas y de la Salud', 'Medicina básica', 'Medicina química'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3A07', 'Ciencias Médicas y de la Salud', 'Medicina básica', 'Toxicología'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3A08', 'Ciencias Médicas y de la Salud', 'Medicina básica', 'Fisiología (incluye citología)'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3A09', 'Ciencias Médicas y de la Salud', 'Medicina básica', 'Patología'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3B01', 'Ciencias Médicas y de la Salud', 'Medicina Clínica', 'Andrología'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3B02', 'Ciencias Médicas y de la Salud', 'Medicina Clínica', 'Obstetricia y ginecología'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3B03', 'Ciencias Médicas y de la Salud', 'Medicina Clínica', 'Pediatría'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3B04', 'Ciencias Médicas y de la Salud', 'Medicina Clínica', 'Cardiovascular'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3B05', 'Ciencias Médicas y de la Salud', 'Medicina Clínica', 'Vascular periférico'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3B06', 'Ciencias Médicas y de la Salud', 'Medicina Clínica', 'Hematología'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3B07', 'Ciencias Médicas y de la Salud', 'Medicina Clínica', 'Respiratoria'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3B08', 'Ciencias Médicas y de la Salud', 'Medicina Clínica', 'Cuidado crítico y de emergencia'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3B09', 'Ciencias Médicas y de la Salud', 'Medicina Clínica', 'Anestesiología'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3B10', 'Ciencias Médicas y de la Salud', 'Medicina Clínica', 'Ortopédica'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3B11', 'Ciencias Médicas y de la Salud', 'Medicina Clínica', 'Cirugía'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3B12', 'Ciencias Médicas y de la Salud', 'Medicina Clínica', 'Radiología, medicina nuclear y de imágenes'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3B13', 'Ciencias Médicas y de la Salud', 'Medicina Clínica', 'Trasplantes'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3B14', 'Ciencias Médicas y de la Salud', 'Medicina Clínica', 'Odontología, cirugía oral y medicina oral'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3B15', 'Ciencias Médicas y de la Salud', 'Medicina Clínica', 'Dermatología y enfermedades venéreas'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3B16', 'Ciencias Médicas y de la Salud', 'Medicina Clínica', 'Alergias'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3B17', 'Ciencias Médicas y de la Salud', 'Medicina Clínica', 'Reumatología'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3B18', 'Ciencias Médicas y de la Salud', 'Medicina Clínica', 'Endocrinología y metabolismo (incluye diabetes y trastornos hormonales)'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3B19', 'Ciencias Médicas y de la Salud', 'Medicina Clínica', 'Gastroenterología y hepatología'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3B20', 'Ciencias Médicas y de la Salud', 'Medicina Clínica', 'Urología y nefrología'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3B21', 'Ciencias Médicas y de la Salud', 'Medicina Clínica', 'Oncología'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3B22', 'Ciencias Médicas y de la Salud', 'Medicina Clínica', 'Oftalmología'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3B23', 'Ciencias Médicas y de la Salud', 'Medicina Clínica', 'Otorrinolaringología'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3B24', 'Ciencias Médicas y de la Salud', 'Medicina Clínica', 'Psiquiatría'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3B25', 'Ciencias Médicas y de la Salud', 'Medicina Clínica', 'Neurología clínica'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3B26', 'Ciencias Médicas y de la Salud', 'Medicina Clínica', 'Geriatría'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3B27', 'Ciencias Médicas y de la Salud', 'Medicina Clínica', 'Medicina general e interna'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3B28', 'Ciencias Médicas y de la Salud', 'Medicina Clínica', 'Otros temas de medicina clínica'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3B29', 'Ciencias Médicas y de la Salud', 'Medicina Clínica', 'Medicina complementaria (sistemas alternativos)'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3C01', 'Ciencias Médicas y de la Salud', 'Ciencias de la Salud', 'Ciencias del cuidado de la salud y servicios (administración de hospitales y financiamiento)'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3C02', 'Ciencias Médicas y de la Salud', 'Ciencias de la Salud', 'Políticas de salud y servicios'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3C03', 'Ciencias Médicas y de la Salud', 'Ciencias de la Salud', 'Enfermería'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3C04', 'Ciencias Médicas y de la Salud', 'Ciencias de la Salud', 'Nutrición y dietas'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3C05', 'Ciencias Médicas y de la Salud', 'Ciencias de la Salud', 'Salud pública'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3C06', 'Ciencias Médicas y de la Salud', 'Ciencias de la Salud', 'Medicina tropical'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3C07', 'Ciencias Médicas y de la Salud', 'Ciencias de la Salud', 'Parasitología'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3C08', 'Ciencias Médicas y de la Salud', 'Ciencias de la Salud', 'enfermedades infecciosas'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3C09', 'Ciencias Médicas y de la Salud', 'Ciencias de la Salud', 'Epidemiología'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3C10', 'Ciencias Médicas y de la Salud', 'Ciencias de la Salud', 'Salud ocupacional'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3C11', 'Ciencias Médicas y de la Salud', 'Ciencias de la Salud', 'Ciencias del deporte'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3C12', 'Ciencias Médicas y de la Salud', 'Ciencias de la Salud', 'Ciencias socio biomédicas (planificación familiar, salud sexual, efectos políticos y sociales de la investigación biomédica)'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3C13', 'Ciencias Médicas y de la Salud', 'Ciencias de la Salud', 'Ética'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3C14', 'Ciencias Médicas y de la Salud', 'Ciencias de la Salud', 'Abuso de sustancias'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3D01', 'Ciencias Médicas y de la Salud', 'Biotecnología en Salud', 'Biotecnología relacionada con la salud'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3D02', 'Ciencias Médicas y de la Salud', 'Biotecnología en Salud', 'Tecnologías para la manipulación de células, tejidos, órganos o el organismo (reporducción asistida)'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3D03', 'Ciencias Médicas y de la Salud', 'Biotecnología en Salud', 'Tecnología para la identificación y funcionamiento del ADN, proteinas y encimas y como influencian la enfermedad'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3D04', 'Ciencias Médicas y de la Salud', 'Biotecnología en Salud', 'Biomateriales (relacionados con implantes, dispositivos, sensores)'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3D05', 'Ciencias Médicas y de la Salud', 'Biotecnología en Salud', 'Ética relacionada con la biomedicina.'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3E01', 'Ciencias Médicas y de la Salud', 'Otras Ciencias Médicas', 'Forénsicas'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3E02', 'Ciencias Médicas y de la Salud', 'Otras Ciencias Médicas', 'Otras ciencias médicas'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('3E03', 'Ciencias Médicas y de la Salud', 'Otras Ciencias Médicas', 'Fonoaudiología'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('4A01', 'Ciencias Agrícolas', 'Agricultura, Silvicultura y Pesca', 'Agricultura'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('4A02', 'Ciencias Agrícolas', 'Agricultura, Silvicultura y Pesca', 'Forestal'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('4A03', 'Ciencias Agrícolas', 'Agricultura, Silvicultura y Pesca', 'Pesca'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('4A04', 'Ciencias Agrícolas', 'Agricultura, Silvicultura y Pesca', 'Ciencias del suelo'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('4A05', 'Ciencias Agrícolas', 'Agricultura, Silvicultura y Pesca', 'Horticultura y viticultura'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('4A06', 'Ciencias Agrícolas', 'Agricultura, Silvicultura y Pesca', 'Agronomía'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('4A07', 'Ciencias Agrícolas', 'Agricultura, Silvicultura y Pesca', 'Protección y nutrición de las plantas'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('4B01', 'Ciencias Agrícolas', 'Ciencias animales y lechería', 'Ciencias animales y lechería'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('4B02', 'Ciencias Agrícolas', 'Ciencias animales y lechería', 'Crías y mascotas'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('4C01', 'Ciencias Agrícolas', 'Ciencias Veterinarias', 'Ciencias Veterinarias'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('4D01', 'Ciencias Agrícolas', 'Biotecnología Agrícola', 'Biotecnología agrícola y de alimentos'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('4D02', 'Ciencias Agrícolas', 'Biotecnología Agrícola', 'Tecnología MG, clonamiento de ganado, selección asistida, diagnóstico'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('4D03', 'Ciencias Agrícolas', 'Biotecnología Agrícola', 'Ética relacionada a la biotecnología agrícola'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('4E01', 'Ciencias Agrícolas', 'Otras Ciencias Agrícolas', 'Otras ciencias Agrícolas'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('5A01', 'Ciencias Sociales', 'Psicología', 'Psicología (incluye relaciones hombre-máquina)'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('5A02', 'Ciencias Sociales', 'Psicología', 'Psicología (incluye terapias de aprendizaje, habla, visual y otras discapacidades físicas y mentales'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('5B01', 'Ciencias Sociales', 'Economía y Negocios', 'Economía'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('5B02', 'Ciencias Sociales', 'Economía y Negocios', 'Econometría'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('5B03', 'Ciencias Sociales', 'Economía y Negocios', 'Relaciones Industriales'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('5B04', 'Ciencias Sociales', 'Economía y Negocios', 'Negocios y Management'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('5C01', 'Ciencias Sociales', 'Ciencias de la Educación', 'Educación general (incluye capacitación, pedagogía)'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('5C02', 'Ciencias Sociales', 'Ciencias de la Educación', 'Educación especial (para estudios dotados y aquellos con dificultades del aprendizaje)'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('5D01', 'Ciencias Sociales', 'Sociología', 'Sociología'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('5D02', 'Ciencias Sociales', 'Sociología', 'Demografía'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('5D03', 'Ciencias Sociales', 'Sociología', 'Antropología'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('5D04', 'Ciencias Sociales', 'Sociología', 'Etnografía'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('5D05', 'Ciencias Sociales', 'Sociología', 'Temas especiales (Estudios de género, Temas sociales, Estudios de la familia, Trabajo social)'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('5E01', 'Ciencias Sociales', 'Derecho', 'Derecho'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('5E02', 'Ciencias Sociales', 'Derecho', 'Penal'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('5F01', 'Ciencias Sociales', 'Ciencias Políticas', 'Ciencias Políticas'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('5F02', 'Ciencias Sociales', 'Ciencias Políticas', 'Administración Pública'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('5F03', 'Ciencias Sociales', 'Ciencias Políticas', 'teoría organizacional'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('5G01', 'Ciencias Sociales', 'Geografía Social y Económica', 'Ciencias ambientales'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('5G02', 'Ciencias Sociales', 'Geografía Social y Económica', 'Geografía económica y cultural'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('5G03', 'Ciencias Sociales', 'Geografía Social y Económica', 'Estudios urbanos (planificación y desarrollo)'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('5G04', 'Ciencias Sociales', 'Geografía Social y Económica', 'Planificación del transporte y aspectos sociales del transporte'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('5H01', 'Ciencias Sociales', 'Periodismo y Comunicaciones', 'Periodismo'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('5H02', 'Ciencias Sociales', 'Periodismo y Comunicaciones', 'Ciencias de la Información (aspectos sociales)'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('5H03', 'Ciencias Sociales', 'Periodismo y Comunicaciones', 'Bibliotecología'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('5H04', 'Ciencias Sociales', 'Periodismo y Comunicaciones', 'Medios y comunicación social'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('5I01', 'Ciencias Sociales', 'Otras Ciencias Sociales', 'Ciencias Sociales, interdisciplinaria'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('5I02', 'Ciencias Sociales', 'Otras Ciencias Sociales', 'Otras Ciencias Sociales'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('6A01', 'Humanidades', 'Historia y Arqueología', 'Historia (historia de la ciencia y tecnología en 6C)'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('6A02', 'Humanidades', 'Historia y Arqueología', 'Arqueología'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('6A03', 'Humanidades', 'Historia y Arqueología', 'Historia de Colombia'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('6B01', 'Humanidades', 'Idiomas y Literatura', 'Estudios generales del lenguaje'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('6B02', 'Humanidades', 'Idiomas y Literatura', 'Idiomas específicos'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('6B03', 'Humanidades', 'Idiomas y Literatura', 'Estudios literarios'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('6B04', 'Humanidades', 'Idiomas y Literatura', 'Teoría literaria'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('6B05', 'Humanidades', 'Idiomas y Literatura', 'Literatura específica'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('6B06', 'Humanidades', 'Idiomas y Literatura', 'Lingüística'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('6C01', 'Humanidades', 'Otras historias', 'Historia de la Ciencia y la Tecnología'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('6C02', 'Humanidades', 'Otras historias', 'Otras historias especializadas (Se incluye Histora del Arte)'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('6D01', 'Humanidades', 'Arte', 'Artes plásticas y visules'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('6D02', 'Humanidades', 'Arte', 'Música y musicología'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('6D03', 'Humanidades', 'Arte', 'Danza o Artes danzarías'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('6D04', 'Humanidades', 'Arte', 'Teatro, dramaturgia o Artes escénicas'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('6D05', 'Humanidades', 'Arte', 'Otras artes'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('6D06', 'Humanidades', 'Arte', 'Artes audiovisuales'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('6D07', 'Humanidades', 'Arte', 'Arquitectura y urbanismo'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('6D08', 'Humanidades', 'Arte', 'Diseño'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('6E01', 'Humanidades', 'Otras Humanidades', 'Otras humanidades (Se incluye Estudios del folclor)'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    ('6E02', 'Humanidades', 'Otras Humanidades', 'Filosofía'),
    -- Completa la instruccion SQL anterior con un nombre, valor, filtro o cierre.
    ('6E03', 'Humanidades', 'Otras Humanidades', 'Teología');

-- objetivo_desarrollo_sostenible: 17 filas
-- Inicia la insercion de filas en la tabla indicada.
INSERT INTO objetivo_desarrollo_sostenible (id, nombre, categoria) VALUES
    -- Aporta valores o una fila al conjunto VALUES anterior.
    (1, 'Fin de la Pobreza', 'Social'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    (2, 'Hambre cero', 'Social'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    (3, 'Salud y bienestar', 'Social'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    (4, 'Educación de calidad', 'Social'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    (5, 'Igualdad de género', 'Social'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    (6, 'Agua limpia y saneamiento', 'Ambientales'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    (7, 'Energía asequible y no contaminante', 'Económicos'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    (8, 'Trabajo decente y crecimiento económico', 'Económicos'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    (9, 'Industria, Innovación e Infraestructura', 'Económicos'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    (10, 'Reducción de las desigualdades', 'Económicos'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    (11, 'Ciudades y Comunidades Sostenibles', 'Económicos'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    (12, 'Producción y consumo Responsables', 'Ambientales'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    (13, 'Acción por el clima', 'Ambientales'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    (14, 'Vida Submarina', 'Ambientales'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    (15, 'Vide de ecosistemas terrestres', 'Ambientales'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    (16, 'Paz, Justicia e instituciones sólidas', 'Estrategicos'),
    -- Completa la instruccion SQL anterior con un nombre, valor, filtro o cierre.
    (17, 'Alianzas para lograr los objetivos', 'Estrategicos');

-- area_aplicacion: 21 filas
-- Inicia la insercion de filas en la tabla indicada.
INSERT INTO area_aplicacion (id, nombre) VALUES
    -- Aporta valores o una fila al conjunto VALUES anterior.
    (1, 'Agricultura, ganadería, caza, silvicultura y pesca'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    (2, 'Explotación de minas y canteras'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    (3, 'Industriasmanufactureras'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    (4, 'Suministro de electricidad, gas, vapor y aire acondicionado'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    (5, 'Distribución de agua; evacuación y tratamiento de aguas residuales, gestión de desechos y actividades de saneamiento ambiental'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    (6, 'Construcción'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    (7, 'Comercio al por mayor y al por menor; reparación de vehículos automotores y motocicletas'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    (8, 'Transporte y almacenamiento'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    (9, 'Alojamiento y servicios de comida'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    (10, 'Información y comunicaciones'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    (11, 'Actividades financieras y de seguros'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    (12, 'Actividades inmobiliarias'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    (13, 'Actividades profesionales, científicas y técnicas'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    (14, 'Actividades de servicios administrativos y de apoyo'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    (15, 'Administración pública y defensa; planes de seguridad social de afiliación obligatoria'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    (16, 'Educación'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    (17, 'Actividades de atención de la salud humana y de asistencia social'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    (18, 'Actividades artísticas, de entretenimiento y recreación'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    (19, 'Otras actividades de servicios'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    (20, 'Actividades de los hogares en calidad de empleadores'),
    -- Completa la instruccion SQL anterior con un nombre, valor, filtro o cierre.
    (21, 'Actividades de organizaciones y entidades extraterritoriales');

-- ============================================================
-- Conteos esperados:
--   area_conocimiento                 218 filas
--   objetivo_desarrollo_sostenible     17 filas
--   area_aplicacion                    21 filas
-- ============================================================
