-- Directiva psql: configura el cliente antes de ejecutar el SQL.
\set ON_ERROR_STOP on
-- Directiva psql: configura el cliente antes de ejecutar el SQL.
\encoding UTF8
-- Inicia la transaccion que agrupa estos cambios.
BEGIN;
-- Configura una opcion para esta sesion o transaccion.
SET LOCAL search_path = public, pg_temp;
-- Bloquea la tabla para controlar escrituras concurrentes.
LOCK TABLE universidad IN SHARE ROW EXCLUSIVE MODE;
-- Directiva psql: configura el cliente antes de ejecutar el SQL.
\ir carga_segura.sql
-- Fuente: Base de Datos v6.xlsx, hoja universidad, seis filas completas.
-- Inicia la consulta y selecciona los datos indicados.
SELECT pg_temp.cargar_v2('universidad', 'id', jsonb_build_object(
    -- Completa la instruccion SQL anterior con un nombre, valor, filtro o cierre.
    'id', id, 'nombre', nombre, 'tipo', tipo, 'ciudad', ciudad, 'activo', true))
-- Indica la tabla o subconsulta de donde provienen las filas.
FROM (VALUES
    -- Aporta valores o una fila al conjunto VALUES anterior.
    (1, 'Universidad de San Buenaventura - Bogotá', 'Seccional', 'Bogotá'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    (2, 'Universidad de San Buenaventura - Cali', 'Seccional', 'Cali'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    (3, 'Universidad de San Buenaventura - Cartagena', 'Seccional', 'Cartagena'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    (4, 'Universidad de San Buenaventura - Medellín', 'Seccional', 'Medellín'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    (5, 'Universidad de San Buenaventura - Medellín', 'Extensión', 'Armenia'),
    -- Aporta valores o una fila al conjunto VALUES anterior.
    (6, 'Universidad de San Buenaventura - Medellín', 'Extensión', 'Ibagué')
-- Cierra la lista de columnas, valores o argumentos abierta.
) AS fuente(id, nombre, tipo, ciudad);
-- Confirma los cambios de la transaccion.
COMMIT;
