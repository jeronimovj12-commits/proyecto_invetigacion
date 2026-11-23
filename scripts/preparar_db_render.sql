-- Detiene psql ante cualquier error para no iniciar la API con una base incompleta.
\set ON_ERROR_STOP on

-- Serializa el arranque de instancias para que solo una inicialice la base vacía.
SELECT pg_advisory_lock(734902341);

-- Cuenta las tablas públicas; init.sql solo se ejecuta si no hay ninguna.
SELECT count(*) = 0 AS base_vacia
FROM information_schema.tables
WHERE table_schema = 'public' AND table_type = 'BASE TABLE'\gset

-- La instalación inicial del curso contiene exactamente 19 tablas.
\if :base_vacia
    \echo 'Base vacía: creando esquema y catálogos iniciales.'
    \i /db/init.sql
\else
    SELECT count(*) = 19 AS esquema_inicial_completo
    FROM information_schema.tables
    WHERE table_schema = 'public' AND table_type = 'BASE TABLE'\gset
    \if :esquema_inicial_completo
        \echo 'Esquema inicial presente: se conserva sin volver a cargarlo.'
    \else
        \echo 'Error: la base no está vacía y no tiene las 19 tablas esperadas; no se modifica.'
        \quit 1
    \endif
\endif

-- Aplica la migración v3 que valida el esquema y agrega las columnas de seguridad.
\i /db/migraciones/v3_001_sesiones_asignaciones.sql

-- Libera el bloqueo después de completar las verificaciones y cambios.
SELECT pg_advisory_unlock(734902341);
