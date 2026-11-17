-- Directiva psql: configura el cliente antes de ejecutar el SQL.
\set ON_ERROR_STOP on
-- Directiva psql: configura el cliente antes de ejecutar el SQL.
\encoding UTF8
-- Carga voluntaria. Nunca se ejecuta desde docker-entrypoint-initdb.d.
-- Dos opciones por padre permiten cambiar las FK sin reutilizar claves retiradas.
-- Inicia la transaccion que agrupa estos cambios.
BEGIN;
-- Configura una opcion para esta sesion o transaccion.
SET LOCAL search_path = public, pg_temp;
-- Bloquea la tabla para controlar escrituras concurrentes.
LOCK TABLE universidad, linea_investigacion, docente, grupo_investigacion,
    -- Completa la instruccion SQL anterior con un nombre, valor, filtro o cierre.
    semillero, area_conocimiento, objetivo_desarrollo_sostenible, area_aplicacion
    -- Declara una columna con su tipo y restricciones.
    IN SHARE ROW EXCLUSIVE MODE;
-- Directiva psql: configura el cliente antes de ejecutar el SQL.
\ir carga_segura.sql
-- Inicia un bloque procedural que ejecuta validaciones o logica en la base.
DO $$
-- Inicia la transaccion que agrupa estos cambios.
BEGIN
    -- Ejecuta el bloque siguiente solo si se cumple la condicion SQL.
    IF NOT EXISTS (SELECT 1 FROM area_conocimiento WHERE activo)
       -- Agrega esta condicion al filtro anterior.
       OR NOT EXISTS (SELECT 1 FROM objetivo_desarrollo_sostenible WHERE activo)
       -- Agrega esta condicion al filtro anterior.
       OR NOT EXISTS (SELECT 1 FROM area_aplicacion WHERE activo) THEN
        -- Emite un aviso o error desde el bloque procedural.
        RAISE EXCEPTION 'Faltan áreas de conocimiento, ODS o áreas de aplicación activos. Cargue datos oficiales aprobados; no se crean sustitutos ni se reactivan filas.';
    -- Cierra el bloque o la instruccion SQL abierta.
    END IF;
-- Cierra el bloque o la instruccion SQL abierta.
END;
-- Cierra el bloque o la instruccion SQL abierta.
$$;
-- Inicia un bloque procedural que ejecuta validaciones o logica en la base.
DO $$
-- Declara variables locales del bloque procedural.
DECLARE numero integer; etiqueta text;
-- Inicia la transaccion que agrupa estos cambios.
BEGIN
    -- Declara una columna con su tipo y restricciones.
    FOR numero IN 1902000001..1902000002 LOOP
        -- Completa la instruccion SQL anterior con un nombre, valor, filtro o cierre.
        etiqueta := 'DEMO V2 ' || (numero - 1902000000);
        -- Declara una columna con su tipo y restricciones.
        PERFORM pg_temp.cargar_v2('universidad', 'id', jsonb_build_object(
            -- Completa la instruccion SQL anterior con un nombre, valor, filtro o cierre.
            'id', numero, 'nombre', etiqueta || ' Universidad ficticia',
            -- Completa la instruccion SQL anterior con un nombre, valor, filtro o cierre.
            'tipo', 'DEMO V2', 'ciudad', 'DEMO V2', 'activo', true));
        -- ID explícito alto; no se altera la secuencia SERIAL ni su valor actual.
        -- Declara una columna con su tipo y restricciones.
        PERFORM pg_temp.cargar_v2('linea_investigacion', 'id', jsonb_build_object(
            -- Completa la instruccion SQL anterior con un nombre, valor, filtro o cierre.
            'id', numero, 'nombre', etiqueta || ' Línea ficticia',
            -- Completa la instruccion SQL anterior con un nombre, valor, filtro o cierre.
            'descripcion', 'DEMO V2: datos ficticios para probar desplegables', 'activo', true));
        -- Declara una columna con su tipo y restricciones.
        PERFORM pg_temp.cargar_v2('docente', 'cedula', jsonb_build_object(
            -- Completa la instruccion SQL anterior con un nombre, valor, filtro o cierre.
            'cedula', numero, 'nombres', etiqueta, 'apellidos', 'DEMO V2',
            -- Completa la instruccion SQL anterior con un nombre, valor, filtro o cierre.
            'genero', 'DEMO V2', 'cargo', 'DEMO V2', 'fecha_nacimiento', '1990-01-01',
            -- Completa la instruccion SQL anterior con un nombre, valor, filtro o cierre.
            'correo', 'demo-v2-' || numero || '@example.invalid', 'telefono', 'DEMO V2',
            -- Completa la instruccion SQL anterior con un nombre, valor, filtro o cierre.
            'url_cvlac', 'https://example.invalid/demo-v2', 'fecha_actualizacion', '2026-11-05',
            -- Completa la instruccion SQL anterior con un nombre, valor, filtro o cierre.
            'escalafon', 'DEMO V2', 'perfil', 'DEMO V2: persona ficticia',
            -- Completa la instruccion SQL anterior con un nombre, valor, filtro o cierre.
            'cat_minciencia', NULL, 'conv_minciencia', 'DEMO V2',
            -- Completa la instruccion SQL anterior con un nombre, valor, filtro o cierre.
            'nacionalidaad', 'DEMO V2', 'linea_investigacion_principal', numero, 'activo', true));
        -- Declara una columna con su tipo y restricciones.
        PERFORM pg_temp.cargar_v2('grupo_investigacion', 'id', jsonb_build_object(
            -- Completa la instruccion SQL anterior con un nombre, valor, filtro o cierre.
            'id', numero, 'nombre', etiqueta || ' Grupo ficticio', 'url_gruplac', NULL,
            -- Completa la instruccion SQL anterior con un nombre, valor, filtro o cierre.
            'categoria', NULL, 'convocatoria', NULL, 'fecha_fundacion', '2026-01-01',
            -- Completa la instruccion SQL anterior con un nombre, valor, filtro o cierre.
            'universidsad', numero, 'interno', 1, 'ambito', 'DEMO V2', 'activo', true));
        -- Declara una columna con su tipo y restricciones.
        PERFORM pg_temp.cargar_v2('semillero', 'id', jsonb_build_object(
            -- Completa la instruccion SQL anterior con un nombre, valor, filtro o cierre.
            'id', numero, 'nombre', etiqueta || ' Semillero ficticio',
            -- Completa la instruccion SQL anterior con un nombre, valor, filtro o cierre.
            'fecha_fundacion', '2026-01-01', 'grupo_investigacion', numero, 'activo', true));
    -- Cierra el bloque o la instruccion SQL abierta.
    END LOOP;
-- Cierra el bloque o la instruccion SQL abierta.
END;
-- Cierra el bloque o la instruccion SQL abierta.
$$;
-- Confirma los cambios de la transaccion.
COMMIT;
