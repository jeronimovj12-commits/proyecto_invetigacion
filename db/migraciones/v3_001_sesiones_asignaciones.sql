-- Hace que psql termine con error si una instruccion SQL falla.
-- Directiva psql: configura el cliente antes de ejecutar el SQL.
\set ON_ERROR_STOP on
-- Agrupa validaciones y cambios para poder revertirlos ante un error.
-- Inicia la transaccion que agrupa estos cambios.
BEGIN;
-- Limita la busqueda de objetos a public y al esquema temporal de esta transaccion.
-- Configura una opcion para esta sesion o transaccion.
SET LOCAL search_path = public, pg_temp;
-- Bloquea escrituras concurrentes mientras se valida y modifica el esquema.
-- Bloquea la tabla para controlar escrituras concurrentes.
LOCK TABLE usuario, rol, rol_usuario IN ACCESS EXCLUSIVE MODE;
-- No se intenta reparar silenciosamente un esquema distinto al entregado.
-- Inicia un bloque procedural que ejecuta validaciones o logica en la base.
DO $$
-- Declara variables locales del bloque procedural.
DECLARE esperado record; real record;
-- Inicia la transaccion que agrupa estos cambios.
BEGIN
-- Recorre primero el listado de columnas base con sus tipos y limites esperados.
    -- Declara una columna con su tipo y restricciones.
    FOR esperado IN SELECT * FROM (VALUES
        -- Aporta valores o una fila al conjunto VALUES anterior.
        ('usuario','id','integer',NULL::integer,'NO'),
        -- Aporta valores o una fila al conjunto VALUES anterior.
        ('usuario','username','character varying',100,'NO'),
        -- Aporta valores o una fila al conjunto VALUES anterior.
        ('usuario','password','character varying',255,'NO'),
        -- Aporta valores o una fila al conjunto VALUES anterior.
        ('usuario','email','character varying',150,'NO'),
        -- Aporta valores o una fila al conjunto VALUES anterior.
        ('usuario','nombre_completo','character varying',200,'YES'),
        -- Aporta valores o una fila al conjunto VALUES anterior.
        ('usuario','activo','boolean',NULL,'YES'),
        -- Aporta valores o una fila al conjunto VALUES anterior.
        ('usuario','fecha_creacion','timestamp without time zone',NULL,'YES'),
        -- Aporta valores o una fila al conjunto VALUES anterior.
        ('usuario','fecha_actualizacion','timestamp without time zone',NULL,'YES'),
        -- Aporta valores o una fila al conjunto VALUES anterior.
        ('rol','id','integer',NULL,'NO'),
        -- Aporta valores o una fila al conjunto VALUES anterior.
        ('rol','nombre','character varying',100,'NO'),
        -- Aporta valores o una fila al conjunto VALUES anterior.
        ('rol','descripcion','text',NULL,'YES'),
        -- Aporta valores o una fila al conjunto VALUES anterior.
        ('rol','activo','boolean',NULL,'YES'),
        -- Aporta valores o una fila al conjunto VALUES anterior.
        ('rol','fecha_creacion','timestamp without time zone',NULL,'YES'),
        -- Aporta valores o una fila al conjunto VALUES anterior.
        ('rol_usuario','usuario_id','integer',NULL,'NO'),
        -- Aporta valores o una fila al conjunto VALUES anterior.
        ('rol_usuario','rol_id','integer',NULL,'NO')
    -- Cierra la lista de columnas, valores o argumentos abierta.
    ) AS columnas(tabla,columna,tipo,longitud,anulable) LOOP
-- Lee en el catalogo la definicion real de la columna que se esta validando.
        -- Inicia la consulta y selecciona los datos indicados.
        SELECT * INTO real FROM information_schema.columns
        -- Filtra las filas para que solo cumplan esta condicion.
        WHERE table_schema='public' AND table_name=esperado.tabla AND column_name=esperado.columna;
-- Rechaza la migracion si una columna falta o difiere en tipo, longitud o nulabilidad.
        -- Ejecuta el bloque siguiente solo si se cumple la condicion SQL.
        IF NOT FOUND OR real.data_type <> esperado.tipo
           -- Agrega esta condicion al filtro anterior.
           OR real.character_maximum_length IS DISTINCT FROM esperado.longitud
           -- Agrega esta condicion al filtro anterior.
           OR real.is_nullable <> esperado.anulable THEN
            -- Emite un aviso o error desde el bloque procedural.
            RAISE EXCEPTION 'Esquema incompatible: %.%. No se aplicó la migración.', esperado.tabla, esperado.columna;
        -- Cierra el bloque o la instruccion SQL abierta.
        END IF;
    -- Cierra el bloque o la instruccion SQL abierta.
    END LOOP;
-- Rechaza columnas adicionales no contempladas en las tablas de seguridad.
    -- Ejecuta el bloque siguiente solo si se cumple la condicion SQL.
    IF EXISTS (SELECT 1 FROM information_schema.columns
        -- Filtra las filas para que solo cumplan esta condicion.
        WHERE table_schema='public' AND table_name IN ('usuario','rol','rol_usuario')
        -- Agrega esta condicion al filtro anterior.
        AND column_name NOT IN ('id','username','password','email','nombre_completo','activo',
            -- Completa la instruccion SQL anterior con un nombre, valor, filtro o cierre.
            'fecha_creacion','fecha_actualizacion','nombre','descripcion','usuario_id','rol_id','version_sesion')) THEN
        -- Emite un aviso o error desde el bloque procedural.
        RAISE EXCEPTION 'Esquema incompatible: columnas adicionales no previstas';
    -- Cierra el bloque o la instruccion SQL abierta.
    END IF;
-- Recorre las claves y relaciones que el esquema base debe conservar.
    -- Declara una columna con su tipo y restricciones.
    FOR esperado IN SELECT * FROM (VALUES
        -- Aporta valores o una fila al conjunto VALUES anterior.
        ('usuario','PRIMARY KEY (id)'), ('usuario','UNIQUE (username)'),
        -- Aporta valores o una fila al conjunto VALUES anterior.
        ('usuario','UNIQUE (email)'), ('rol','PRIMARY KEY (id)'), ('rol','UNIQUE (nombre)'),
        -- Aporta valores o una fila al conjunto VALUES anterior.
        ('rol_usuario','PRIMARY KEY (usuario_id, rol_id)'),
        -- Aporta valores o una fila al conjunto VALUES anterior.
        ('rol_usuario','FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE CASCADE'),
        -- Aporta valores o una fila al conjunto VALUES anterior.
        ('rol_usuario','FOREIGN KEY (rol_id) REFERENCES rol(id) ON DELETE CASCADE')
    -- Cierra la lista de columnas, valores o argumentos abierta.
    ) AS restricciones(tabla,definicion) LOOP
-- Comprueba que cada clave o relacion tenga exactamente la definicion esperada.
        -- Ejecuta el bloque siguiente solo si se cumple la condicion SQL.
        IF NOT EXISTS (SELECT 1 FROM pg_constraint
            -- Filtra las filas para que solo cumplan esta condicion.
            WHERE conrelid=to_regclass('public.' || esperado.tabla)
            -- Agrega esta condicion al filtro anterior.
            AND pg_get_constraintdef(oid)=esperado.definicion) THEN
            -- Emite un aviso o error desde el bloque procedural.
            RAISE EXCEPTION 'Esquema incompatible: restricción de % ausente: %', esperado.tabla, esperado.definicion;
        -- Cierra el bloque o la instruccion SQL abierta.
        END IF;
    -- Cierra el bloque o la instruccion SQL abierta.
    END LOOP;
-- Si version_sesion ya existe, valida su tipo, default y nulabilidad.
    -- Ejecuta el bloque siguiente solo si se cumple la condicion SQL.
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema='public'
        -- Agrega esta condicion al filtro anterior.
        AND table_name='usuario' AND column_name='version_sesion'
        -- Agrega esta condicion al filtro anterior.
        AND (data_type <> 'integer' OR is_nullable <> 'NO' OR column_default IS DISTINCT FROM '0')) THEN
        -- Emite un aviso o error desde el bloque procedural.
        RAISE EXCEPTION 'Esquema incompatible: usuario.version_sesion debe ser integer NOT NULL DEFAULT 0';
    -- Cierra el bloque o la instruccion SQL abierta.
    END IF;
-- Si activo ya existe en rol_usuario, valida su tipo, default y nulabilidad.
    -- Ejecuta el bloque siguiente solo si se cumple la condicion SQL.
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema='public'
        -- Agrega esta condicion al filtro anterior.
        AND table_name='rol_usuario' AND column_name='activo'
        -- Agrega esta condicion al filtro anterior.
        AND (data_type <> 'boolean' OR is_nullable <> 'NO' OR column_default IS DISTINCT FROM 'true')) THEN
        -- Emite un aviso o error desde el bloque procedural.
        RAISE EXCEPTION 'Esquema incompatible: rol_usuario.activo debe ser boolean NOT NULL DEFAULT TRUE';
    -- Cierra el bloque o la instruccion SQL abierta.
    END IF;
-- Cierra el bloque o la instruccion SQL abierta.
END;
-- Cierra el bloque o la instruccion SQL abierta.
$$;
-- Agrega un contador de version por usuario; las filas previas reciben 0.
-- Modifica la estructura de la tabla indicada.
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS version_sesion integer NOT NULL DEFAULT 0;
-- Agrega el estado de cada asignacion; las asignaciones previas quedan activas.
-- Modifica la estructura de la tabla indicada.
ALTER TABLE rol_usuario ADD COLUMN IF NOT EXISTS activo boolean NOT NULL DEFAULT TRUE;
-- Inicia un bloque procedural que ejecuta validaciones o logica en la base.
DO $$
-- Inicia la transaccion que agrupa estos cambios.
BEGIN
-- Impide continuar si algun usuario tiene un contador de sesion negativo.
    -- Ejecuta el bloque siguiente solo si se cumple la condicion SQL.
    IF EXISTS (SELECT 1 FROM usuario WHERE version_sesion < 0) THEN
        -- Emite un aviso o error desde el bloque procedural.
        RAISE EXCEPTION 'Esquema incompatible: versiones de sesión negativas';
    -- Cierra el bloque o la instruccion SQL abierta.
    END IF;
-- Crea el CHECK si falta; si ya existe, el bloque siguiente verifica su definicion.
    -- Ejecuta el bloque siguiente solo si se cumple la condicion SQL.
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conrelid='public.usuario'::regclass
        -- Agrega esta condicion al filtro anterior.
        AND conname='usuario_version_sesion_no_negativa') THEN
        -- Modifica la estructura de la tabla indicada.
        ALTER TABLE usuario ADD CONSTRAINT usuario_version_sesion_no_negativa CHECK (version_sesion >= 0);
    -- Evalua una condicion alternativa dentro del bloque procedural.
    ELSIF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conrelid='public.usuario'::regclass
        -- Agrega esta condicion al filtro anterior.
        AND conname='usuario_version_sesion_no_negativa' AND contype='c'
        -- Agrega esta condicion al filtro anterior.
        AND convalidated AND pg_get_constraintdef(oid)='CHECK ((version_sesion >= 0))') THEN
        -- Emite un aviso o error desde el bloque procedural.
        RAISE EXCEPTION 'Restricción incompatible para version_sesion';
    -- Cierra el bloque o la instruccion SQL abierta.
    END IF;
-- Cierra el bloque o la instruccion SQL abierta.
END;
-- Cierra el bloque o la instruccion SQL abierta.
$$;
-- Confirma los cambios solo despues de superar todas las validaciones.
-- Confirma los cambios de la transaccion.
COMMIT;
