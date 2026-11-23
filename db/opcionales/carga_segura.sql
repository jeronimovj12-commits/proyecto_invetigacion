-- Auxiliar exclusivo de esta sesión psql; no instala funciones permanentes.
-- Las tablas se bloquean antes de comparar para evitar carreras entre cargas.
-- Define la funcion SQL temporal/permanente nombrada en la instruccion.
CREATE OR REPLACE FUNCTION pg_temp.cargar_v2(tabla regclass, clave text, datos jsonb)
-- Declara una columna con su tipo y restricciones.
RETURNS void LANGUAGE plpgsql AS $$
-- Declara variables locales del bloque procedural.
DECLARE existente jsonb;
-- Inicia la transaccion que agrupa estos cambios.
BEGIN
    -- Declara una columna con su tipo y restricciones.
    EXECUTE format('SELECT to_jsonb(t) FROM %s t WHERE to_jsonb(t)->$1 = $2', tabla)
        -- Declara una columna con su tipo y restricciones.
        INTO existente USING clave, datos->clave;
    -- Ejecuta el bloque siguiente solo si se cumple la condicion SQL.
    IF existente IS NOT NULL THEN
        -- Ejecuta el bloque siguiente solo si se cumple la condicion SQL.
        IF existente IS DISTINCT FROM datos THEN
            -- Emite un aviso o error desde el bloque procedural.
            RAISE EXCEPTION 'Conflicto en %, clave %: datos distintos o registro inactivo. No se sobrescribe ni reactiva. Se revierte toda la carga.', tabla, datos->clave;
        -- Cierra el bloque o la instruccion SQL abierta.
        END IF;
        -- Emite un aviso o error desde el bloque procedural.
        RAISE NOTICE 'Sin cambios: % clave % ya coincide y está activo', tabla, datos->clave;
    -- Ejecuta el caso alternativo dentro del bloque procedural.
    ELSE
        -- Declara una columna con su tipo y restricciones.
        EXECUTE format('INSERT INTO %s SELECT * FROM jsonb_populate_record(NULL::%s, $1)', tabla, tabla)
            -- Declara una columna con su tipo y restricciones.
            USING datos;
        -- Emite un aviso o error desde el bloque procedural.
        RAISE NOTICE 'Insertado: % clave %', tabla, datos->clave;
    -- Cierra el bloque o la instruccion SQL abierta.
    END IF;
-- Cierra el bloque o la instruccion SQL abierta.
END;
-- Cierra el bloque o la instruccion SQL abierta.
$$;
