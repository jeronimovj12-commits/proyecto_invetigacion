\set ON_ERROR_STOP on
\encoding UTF8
-- Carga voluntaria. Nunca se ejecuta desde docker-entrypoint-initdb.d.
-- Dos opciones por padre permiten cambiar las FK sin reutilizar claves retiradas.
BEGIN;
SET LOCAL search_path = public, pg_temp;
LOCK TABLE universidad, linea_investigacion, docente, grupo_investigacion,
    semillero, area_conocimiento, objetivo_desarrollo_sostenible, area_aplicacion
    IN SHARE ROW EXCLUSIVE MODE;
\ir carga_segura.sql
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM area_conocimiento WHERE activo)
       OR NOT EXISTS (SELECT 1 FROM objetivo_desarrollo_sostenible WHERE activo)
       OR NOT EXISTS (SELECT 1 FROM area_aplicacion WHERE activo) THEN
        RAISE EXCEPTION 'Faltan áreas de conocimiento, ODS o áreas de aplicación activos. Cargue datos oficiales aprobados; no se crean sustitutos ni se reactivan filas.';
    END IF;
END;
$$;
DO $$
DECLARE numero integer; etiqueta text;
BEGIN
    FOR numero IN 1902000001..1902000002 LOOP
        etiqueta := 'DEMO V2 ' || (numero - 1902000000);
        PERFORM pg_temp.cargar_v2('universidad', 'id', jsonb_build_object(
            'id', numero, 'nombre', etiqueta || ' Universidad ficticia',
            'tipo', 'DEMO V2', 'ciudad', 'DEMO V2', 'activo', true));
        -- ID explícito alto; no se altera la secuencia SERIAL ni su valor actual.
        PERFORM pg_temp.cargar_v2('linea_investigacion', 'id', jsonb_build_object(
            'id', numero, 'nombre', etiqueta || ' Línea ficticia',
            'descripcion', 'DEMO V2: datos ficticios para probar desplegables', 'activo', true));
        PERFORM pg_temp.cargar_v2('docente', 'cedula', jsonb_build_object(
            'cedula', numero, 'nombres', etiqueta, 'apellidos', 'DEMO V2',
            'genero', 'DEMO V2', 'cargo', 'DEMO V2', 'fecha_nacimiento', '1990-01-01',
            'correo', 'demo-v2-' || numero || '@example.invalid', 'telefono', 'DEMO V2',
            'url_cvlac', 'https://example.invalid/demo-v2', 'fecha_actualizacion', '2026-11-05',
            'escalafon', 'DEMO V2', 'perfil', 'DEMO V2: persona ficticia',
            'cat_minciencia', NULL, 'conv_minciencia', 'DEMO V2',
            'nacionalidaad', 'DEMO V2', 'linea_investigacion_principal', numero, 'activo', true));
        PERFORM pg_temp.cargar_v2('grupo_investigacion', 'id', jsonb_build_object(
            'id', numero, 'nombre', etiqueta || ' Grupo ficticio', 'url_gruplac', NULL,
            'categoria', NULL, 'convocatoria', NULL, 'fecha_fundacion', '2026-01-01',
            'universidsad', numero, 'interno', 1, 'ambito', 'DEMO V2', 'activo', true));
        PERFORM pg_temp.cargar_v2('semillero', 'id', jsonb_build_object(
            'id', numero, 'nombre', etiqueta || ' Semillero ficticio',
            'fecha_fundacion', '2026-01-01', 'grupo_investigacion', numero, 'activo', true));
    END LOOP;
END;
$$;
COMMIT;
