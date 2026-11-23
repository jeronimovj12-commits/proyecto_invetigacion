"""Inicialización prudente de una base Render y migración v3 compatible."""
import asyncio
import os
from pathlib import Path
import re

import asyncpg


def database_url() -> str:
    url = os.environ["DB_POSTGRES"]
    if url.startswith("postgres://"):
        return "postgresql://" + url[len("postgres://"):]
    return url


async def main() -> None:
    connection = await asyncpg.connect(database_url(), timeout=20)
    try:
        tables = await connection.fetchval("""
            SELECT count(*) FROM pg_class c
            JOIN pg_namespace n ON n.oid = c.relnamespace
            WHERE n.nspname = 'public' AND c.relkind IN ('r', 'p')
        """)
        if tables == 0:
            print("Base vacía: inicializando esquema y catálogos.", flush=True)
            await connection.execute(Path("/db/init.sql").read_text(encoding="utf-8"))
        else:
            print(f"Base con {tables} tablas: se omite init.sql; no se borran datos.", flush=True)

        migration = Path("/db/migraciones/v3_001_sesiones_asignaciones.sql").read_text(encoding="utf-8")
        migration = re.sub(r"(?m)^\\set[^\n]*\n", "", migration)
        await connection.execute(migration)
        print("Migración v3 comprobada/aplicada.", flush=True)
    finally:
        await connection.close()


if __name__ == "__main__":
    asyncio.run(main())
