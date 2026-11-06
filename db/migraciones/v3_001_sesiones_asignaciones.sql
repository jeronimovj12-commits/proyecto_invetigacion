\set ON_ERROR_STOP on
BEGIN;
SET LOCAL search_path = public, pg_temp;
LOCK TABLE usuario, rol, rol_usuario IN ACCESS EXCLUSIVE MODE;
-- No se intenta reparar silenciosamente un esquema distinto al entregado.
DO $$
DECLARE esperado record; real record;
BEGIN
    FOR esperado IN SELECT * FROM (VALUES
        ('usuario','id','integer',NULL::integer,'NO'),
        ('usuario','username','character varying',100,'NO'),
        ('usuario','password','character varying',255,'NO'),
        ('usuario','email','character varying',150,'NO'),
        ('usuario','nombre_completo','character varying',200,'YES'),
        ('usuario','activo','boolean',NULL,'YES'),
        ('usuario','fecha_creacion','timestamp without time zone',NULL,'YES'),
        ('usuario','fecha_actualizacion','timestamp without time zone',NULL,'YES'),
        ('rol','id','integer',NULL,'NO'),
        ('rol','nombre','character varying',100,'NO'),
        ('rol','descripcion','text',NULL,'YES'),
        ('rol','activo','boolean',NULL,'YES'),
        ('rol','fecha_creacion','timestamp without time zone',NULL,'YES'),
        ('rol_usuario','usuario_id','integer',NULL,'NO'),
        ('rol_usuario','rol_id','integer',NULL,'NO')
    ) AS columnas(tabla,columna,tipo,longitud,anulable) LOOP
        SELECT * INTO real FROM information_schema.columns
        WHERE table_schema='public' AND table_name=esperado.tabla AND column_name=esperado.columna;
        IF NOT FOUND OR real.data_type <> esperado.tipo
           OR real.character_maximum_length IS DISTINCT FROM esperado.longitud
           OR real.is_nullable <> esperado.anulable THEN
            RAISE EXCEPTION 'Esquema incompatible: %.%. No se aplicó la migración.', esperado.tabla, esperado.columna;
        END IF;
    END LOOP;
    IF EXISTS (SELECT 1 FROM information_schema.columns
        WHERE table_schema='public' AND table_name IN ('usuario','rol','rol_usuario')
        AND column_name NOT IN ('id','username','password','email','nombre_completo','activo',
            'fecha_creacion','fecha_actualizacion','nombre','descripcion','usuario_id','rol_id','version_sesion')) THEN
        RAISE EXCEPTION 'Esquema incompatible: columnas adicionales no previstas';
    END IF;
    FOR esperado IN SELECT * FROM (VALUES
        ('usuario','PRIMARY KEY (id)'), ('usuario','UNIQUE (username)'),
        ('usuario','UNIQUE (email)'), ('rol','PRIMARY KEY (id)'), ('rol','UNIQUE (nombre)'),
        ('rol_usuario','PRIMARY KEY (usuario_id, rol_id)'),
        ('rol_usuario','FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE CASCADE'),
        ('rol_usuario','FOREIGN KEY (rol_id) REFERENCES rol(id) ON DELETE CASCADE')
    ) AS restricciones(tabla,definicion) LOOP
        IF NOT EXISTS (SELECT 1 FROM pg_constraint
            WHERE conrelid=to_regclass('public.' || esperado.tabla)
            AND pg_get_constraintdef(oid)=esperado.definicion) THEN
            RAISE EXCEPTION 'Esquema incompatible: restricción de % ausente: %', esperado.tabla, esperado.definicion;
        END IF;
    END LOOP;
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema='public'
        AND table_name='usuario' AND column_name='version_sesion'
        AND (data_type <> 'integer' OR is_nullable <> 'NO' OR column_default IS DISTINCT FROM '0')) THEN
        RAISE EXCEPTION 'Esquema incompatible: usuario.version_sesion debe ser integer NOT NULL DEFAULT 0';
    END IF;
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema='public'
        AND table_name='rol_usuario' AND column_name='activo'
        AND (data_type <> 'boolean' OR is_nullable <> 'NO' OR column_default IS DISTINCT FROM 'true')) THEN
        RAISE EXCEPTION 'Esquema incompatible: rol_usuario.activo debe ser boolean NOT NULL DEFAULT TRUE';
    END IF;
END;
$$;
ALTER TABLE usuario ADD COLUMN IF NOT EXISTS version_sesion integer NOT NULL DEFAULT 0;
ALTER TABLE rol_usuario ADD COLUMN IF NOT EXISTS activo boolean NOT NULL DEFAULT TRUE;
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM usuario WHERE version_sesion < 0) THEN
        RAISE EXCEPTION 'Esquema incompatible: versiones de sesión negativas';
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conrelid='public.usuario'::regclass
        AND conname='usuario_version_sesion_no_negativa') THEN
        ALTER TABLE usuario ADD CONSTRAINT usuario_version_sesion_no_negativa CHECK (version_sesion >= 0);
    ELSIF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conrelid='public.usuario'::regclass
        AND conname='usuario_version_sesion_no_negativa' AND contype='c'
        AND convalidated AND pg_get_constraintdef(oid)='CHECK ((version_sesion >= 0))') THEN
        RAISE EXCEPTION 'Restricción incompatible para version_sesion';
    END IF;
END;
$$;
COMMIT;
