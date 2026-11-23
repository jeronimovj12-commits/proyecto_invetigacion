"""
prueba_capas.py — El servicio SIN base de datos.

Enchufa al servicio un repositorio de mentiras que guarda las filas en una
lista. Si esta prueba pasa con PostgreSQL apagado, la separación de capas es
real y no un dibujo: el servicio nunca supo que había un motor detrás.

Se corre con:  docker compose exec api-investigacion python pruebas/prueba_capas.py
"""

import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from servicios.servicio_area_conocimiento import ServicioAreaConocimiento


class RepositorioDeMentiras:
    """Cumple la interfaz del repositorio, pero guarda en una lista."""

    def __init__(self):
        self._filas: list[dict] = []

    async def obtener_todos(self, limite: int) -> list[dict]:
        activas = [fila for fila in self._filas if fila["activo"]]
        return [{k: v for k, v in fila.items() if k != "activo"}
                for fila in activas[:limite]]

    async def obtener_por_id(self, id_area: str) -> dict | None:
        fila = next((f for f in self._filas
                     if f["id"] == id_area and f["activo"]), None)
        return ({k: v for k, v in fila.items() if k != "activo"}
                if fila else None)

    async def crear(self, datos: dict) -> bool:
        self._filas.append({**datos, "activo": True})
        return True

    async def actualizar(self, id_area: str, datos: dict) -> int:
        fila = next((f for f in self._filas
                     if f["id"] == id_area and f["activo"]), None)
        if fila is None:
            return 0
        fila.update(datos)
        return 1

    async def eliminar_logico(self, id_area: str) -> int:
        fila = next((f for f in self._filas
                     if f["id"] == id_area and f["activo"]), None)
        if fila is None:
            return 0
        fila["activo"] = False
        return 1


def revisar(condicion: bool, mensaje_ok: str, mensaje_error: str) -> bool:
    print(f"[{'OK' if condicion else 'ERROR'}] "
          f"{mensaje_ok if condicion else mensaje_error}")
    return condicion


async def main() -> int:
    print("=== Prueba de capas — SIN base de datos ===")
    servicio = ServicioAreaConocimiento(RepositorioDeMentiras())
    bien = True

    bien &= revisar(await servicio.listar(1000) == [],
                    "El sistema arranca vacío.",
                    "Arrancó con filas que nadie creó.")

    nueva = {"id": "9A01", "gran_area": "Ingeniería",
             "area": "Ingeniería de Sistemas", "disciplina": "Software"}
    await servicio.crear(nueva)
    lista = await servicio.listar(1000)
    bien &= revisar(len(lista) == 1 and lista[0]["id"] == "9A01",
                    f"Área creada y listada: {lista[0]['disciplina']}",
                    "La creación no se reflejó en el listado.")

    try:
        await servicio.obtener("NOEXISTE")
        bien &= revisar(False, "", "Un id inexistente NO lanzó LookupError.")
    except LookupError:
        bien &= revisar(True, "Buscar un id inexistente lanza LookupError.", "")

    try:
        await servicio.listar(0)
        bien &= revisar(False, "", "limite = 0 NO lanzó ValueError.")
    except ValueError:
        bien &= revisar(True, "Límite menor o igual a cero rechazado.", "")

    try:
        await servicio.actualizar("9A01", {})
        bien &= revisar(False, "", "Un cuerpo vacío NO lanzó ValueError.")
    except ValueError:
        bien &= revisar(True, "Cuerpo vacío en la actualización rechazado.", "")

    await servicio.actualizar("9A01", {"disciplina": "Ingeniería de Software"})
    tras = await servicio.obtener("9A01")
    bien &= revisar(tras["disciplina"] == "Ingeniería de Software"
                    and tras["area"] == "Ingeniería de Sistemas",
                    "La actualización parcial cambió SOLO la disciplina.",
                    "La actualización parcial tocó campos que no debía.")

    await servicio.eliminar("9A01")
    bien &= revisar(await servicio.listar(1000) == [],
                    "Tras el borrado, el sistema vuelve a estar vacío.", "")
    bien &= revisar(len(servicio._repositorio._filas) == 1
                    and servicio._repositorio._filas[0]["activo"] is False,
                    "El borrado es lógico: la fila sigue guardada como inactiva.",
                    "El repositorio falso borró físicamente la fila.")

    try:
        await servicio.eliminar("9A01")
        bien &= revisar(False, "", "La segunda eliminación NO falló.")
    except LookupError:
        bien &= revisar(True,
                        "Segunda eliminación rechazada: ya no existe.", "")

    print("=== Prueba de capas completada "
          f"{'CON ÉXITO' if bien else 'CON ERRORES'} ===")
    return 0 if bien else 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
