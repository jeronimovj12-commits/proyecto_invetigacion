#!/bin/sh
# Detiene el arranque ante errores y variables obligatorias ausentes.
set -eu

# Exige la conexión privada al PostgreSQL administrado por Render.
: "${DATABASE_URL:?Render debe proporcionar DATABASE_URL}"

# Prepara el esquema en una base vacía y aplica la migración idempotente de v3.
psql "$DATABASE_URL" -X -v ON_ERROR_STOP=1 -f /db/preparar_db_render.sql

# Inicia FastAPI en el puerto público que Render asignó al servicio.
exec uvicorn main_v3:app --host 0.0.0.0 --port "${PORT:-10000}" --no-access-log
