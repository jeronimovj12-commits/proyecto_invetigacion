-- Auxiliar exclusivo de esta sesión psql; no instala funciones permanentes.
-- Las tablas se bloquean antes de comparar para evitar carreras entre cargas.
CREATE OR REPLACE FUNCTION pg_temp.cargar_v2(tabla regclass, clave text, datos jsonb)
RETURNS void LANGUAGE plpgsql AS $$
DECLARE existente jsonb;
BEGIN
    EXECUTE format('SELECT to_jsonb(t) FROM %s t WHERE to_jsonb(t)->$1 = $2', tabla)
        INTO existente USING clave, datos->clave;
    IF existente IS NOT NULL THEN
        IF existente IS DISTINCT FROM datos THEN
            RAISE EXCEPTION 'Conflicto en %, clave %: datos distintos o registro inactivo. No se sobrescribe ni reactiva. Se revierte toda la carga.', tabla, datos->clave;
        END IF;
        RAISE NOTICE 'Sin cambios: % clave % ya coincide y está activo', tabla, datos->clave;
    ELSE
        EXECUTE format('INSERT INTO %s SELECT * FROM jsonb_populate_record(NULL::%s, $1)', tabla, tabla)
            USING datos;
        RAISE NOTICE 'Insertado: % clave %', tabla, datos->clave;
    END IF;
END;
$$;
