\set ON_ERROR_STOP on
\encoding UTF8
BEGIN;
SET LOCAL search_path = public, pg_temp;
LOCK TABLE universidad IN SHARE ROW EXCLUSIVE MODE;
\ir carga_segura.sql
-- Fuente: Base de Datos v6.xlsx, hoja universidad, seis filas completas.
SELECT pg_temp.cargar_v2('universidad', 'id', jsonb_build_object(
    'id', id, 'nombre', nombre, 'tipo', tipo, 'ciudad', ciudad, 'activo', true))
FROM (VALUES
    (1, 'Universidad de San Buenaventura - Bogotá', 'Seccional', 'Bogotá'),
    (2, 'Universidad de San Buenaventura - Cali', 'Seccional', 'Cali'),
    (3, 'Universidad de San Buenaventura - Cartagena', 'Seccional', 'Cartagena'),
    (4, 'Universidad de San Buenaventura - Medellín', 'Seccional', 'Medellín'),
    (5, 'Universidad de San Buenaventura - Medellín', 'Extensión', 'Armenia'),
    (6, 'Universidad de San Buenaventura - Medellín', 'Extensión', 'Ibagué')
) AS fuente(id, nombre, tipo, ciudad);
COMMIT;
