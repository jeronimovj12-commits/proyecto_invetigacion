"""
prueba_capas.py — El servicio SIN base de datos.

Enchufa al servicio un repositorio de mentiras que guarda las filas en una
lista. Si esta prueba pasa con PostgreSQL apagado, la separación de capas es
real y no un dibujo: el servicio nunca supo que había un motor detrás.

Se corre con:  docker compose exec api-investigacion python pruebas/prueba_capas.py
"""

# Importa asynccontextmanager desde contextlib para usar esas definiciones.
from contextlib import asynccontextmanager
# Carga el modulo o los modulos asyncio.
import asyncio
# Carga el modulo o los modulos os.
import os
# Carga el modulo o los modulos sys.
import sys

# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importa ServicioAreaConocimiento desde servicios.servicio_area_conocimiento para usar esas definiciones.
from servicios.servicio_area_conocimiento import ServicioAreaConocimiento


# Define la clase RepositorioDeMentiras y agrupa su estado y operaciones.
class RepositorioDeMentiras:
    # Ejecuta la instruccion indicada dentro del flujo actual.
    """Cumple la interfaz del repositorio, pero guarda en una lista."""

    # Define la funcion __init__ con los parametros declarados; su bloque realiza esta operacion.
    def __init__(self):
        # Guarda en self._filas el valor necesario para reutilizarlo en otros metodos.
        self._filas: list[dict] = []

    # Aplica @asynccontextmanager a la declaracion que sigue; en rutas, registra el endpoint HTTP.
    @asynccontextmanager
    # Define la funcion transaccion con los parametros declarados; su bloque realiza esta operacion.
    async def transaccion(self):
        # Entrega un valor al iterador y conserva el estado de la funcion.
        yield

    # Define la funcion tiene_dependientes con los parametros declarados; su bloque realiza esta operacion.
    async def tiene_dependientes(self, id_area: str) -> bool:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False

    # Define la funcion obtener_todos con los parametros declarados; su bloque realiza esta operacion.
    async def obtener_todos(self, limite: int) -> list[dict]:
        # Asigna a activas el valor calculado a la derecha.
        activas = [fila for fila in self._filas if fila["activo"]]
        # Devuelve al llamador el resultado de la expresion indicada.
        return [{k: v for k, v in fila.items() if k != "activo"}
                # Recorre los elementos de la coleccion indicada y ejecuta el bloque para cada uno.
                for fila in activas[:limite]]

    # Define la funcion obtener_por_id con los parametros declarados; su bloque realiza esta operacion.
    async def obtener_por_id(self, id_area: str) -> dict | None:
        # Asigna a fila el valor calculado a la derecha.
        fila = next((f for f in self._filas
                     # Ejecuta el bloque siguiente solo cuando se cumple: f["id"] == id_area and f["activo"]), None).
                     if f["id"] == id_area and f["activo"]), None)
        # Devuelve al llamador el resultado de la expresion indicada.
        return ({k: v for k, v in fila.items() if k != "activo"}
                # Ejecuta el bloque siguiente solo cuando se cumple: fila else None).
                if fila else None)

    # Define la funcion crear con los parametros declarados; su bloque realiza esta operacion.
    async def crear(self, datos: dict) -> bool:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self._filas.append({**datos, "activo": True})
        # Devuelve al llamador el resultado de la expresion indicada.
        return True

    # Define la funcion actualizar con los parametros declarados; su bloque realiza esta operacion.
    async def actualizar(self, id_area: str, datos: dict) -> int:
        # Asigna a fila el valor calculado a la derecha.
        fila = next((f for f in self._filas
                     # Ejecuta el bloque siguiente solo cuando se cumple: f["id"] == id_area and f["activo"]), None).
                     if f["id"] == id_area and f["activo"]), None)
        # Ejecuta el bloque siguiente solo cuando se cumple: fila is None.
        if fila is None:
            # Devuelve al llamador el resultado de la expresion indicada.
            return 0
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        fila.update(datos)
        # Devuelve al llamador el resultado de la expresion indicada.
        return 1

    # Define la funcion eliminar_logico con los parametros declarados; su bloque realiza esta operacion.
    async def eliminar_logico(self, id_area: str) -> int:
        # Asigna a fila el valor calculado a la derecha.
        fila = next((f for f in self._filas
                     # Ejecuta el bloque siguiente solo cuando se cumple: f["id"] == id_area and f["activo"]), None).
                     if f["id"] == id_area and f["activo"]), None)
        # Ejecuta el bloque siguiente solo cuando se cumple: fila is None.
        if fila is None:
            # Devuelve al llamador el resultado de la expresion indicada.
            return 0
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        fila["activo"] = False
        # Devuelve al llamador el resultado de la expresion indicada.
        return 1


# Define la funcion revisar con los parametros declarados; su bloque realiza esta operacion.
def revisar(condicion: bool, mensaje_ok: str, mensaje_error: str) -> bool:
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    print(f"[{'OK' if condicion else 'ERROR'}] "
          # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
          f"{mensaje_ok if condicion else mensaje_error}")
    # Devuelve al llamador el resultado de la expresion indicada.
    return condicion


# Define la funcion main con los parametros declarados; su bloque realiza esta operacion.
async def main() -> int:
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    print("=== Prueba de capas — SIN base de datos ===")
    # Asigna a servicio el valor calculado a la derecha.
    servicio = ServicioAreaConocimiento(RepositorioDeMentiras())
    # Asigna a bien el valor calculado a la derecha.
    bien = True

    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    bien &= revisar(await servicio.listar(1000) == [],
                    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                    "El sistema arranca vacío.",
                    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                    "Arrancó con filas que nadie creó.")

    # Asigna a nueva el valor calculado a la derecha.
    nueva = {"id": "9A01", "gran_area": "Ingeniería",
             # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
             "area": "Ingeniería de Sistemas", "disciplina": "Software"}
    # Espera que termine la operacion asincronica antes de continuar.
    await servicio.crear(nueva)
    # Asigna a lista el valor calculado a la derecha.
    lista = await servicio.listar(1000)
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    bien &= revisar(len(lista) == 1 and lista[0]["id"] == "9A01",
                    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                    f"Área creada y listada: {lista[0]['disciplina']}",
                    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                    "La creación no se reflejó en el listado.")

    # Inicia un bloque cuya excepcion se manejara en los except siguientes.
    try:
        # Espera que termine la operacion asincronica antes de continuar.
        await servicio.obtener("NOEXISTE")
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        bien &= revisar(False, "", "Un id inexistente NO lanzó LookupError.")
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except LookupError:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        bien &= revisar(True, "Buscar un id inexistente lanza LookupError.", "")

    # Inicia un bloque cuya excepcion se manejara en los except siguientes.
    try:
        # Espera que termine la operacion asincronica antes de continuar.
        await servicio.listar(0)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        bien &= revisar(False, "", "limite = 0 NO lanzó ValueError.")
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except ValueError:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        bien &= revisar(True, "Límite menor o igual a cero rechazado.", "")

    # Inicia un bloque cuya excepcion se manejara en los except siguientes.
    try:
        # Espera que termine la operacion asincronica antes de continuar.
        await servicio.actualizar("9A01", {})
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        bien &= revisar(False, "", "Un cuerpo vacío NO lanzó ValueError.")
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except ValueError:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        bien &= revisar(True, "Cuerpo vacío en la actualización rechazado.", "")

    # Espera que termine la operacion asincronica antes de continuar.
    await servicio.actualizar("9A01", {"disciplina": "Ingeniería de Software"})
    # Asigna a tras el valor calculado a la derecha.
    tras = await servicio.obtener("9A01")
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    bien &= revisar(tras["disciplina"] == "Ingeniería de Software"
                    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                    and tras["area"] == "Ingeniería de Sistemas",
                    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                    "La actualización parcial cambió SOLO la disciplina.",
                    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                    "La actualización parcial tocó campos que no debía.")

    # Espera que termine la operacion asincronica antes de continuar.
    await servicio.eliminar("9A01")
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    bien &= revisar(await servicio.listar(1000) == [],
                    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                    "Tras el borrado, el sistema vuelve a estar vacío.", "")
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    bien &= revisar(len(servicio._repositorio._filas) == 1
                    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                    and servicio._repositorio._filas[0]["activo"] is False,
                    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                    "El borrado es lógico: la fila sigue guardada como inactiva.",
                    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                    "El repositorio falso borró físicamente la fila.")

    # Inicia un bloque cuya excepcion se manejara en los except siguientes.
    try:
        # Espera que termine la operacion asincronica antes de continuar.
        await servicio.eliminar("9A01")
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        bien &= revisar(False, "", "La segunda eliminación NO falló.")
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except LookupError:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        bien &= revisar(True,
                        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                        "Segunda eliminación rechazada: ya no existe.", "")

    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    print("=== Prueba de capas completada "
          # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
          f"{'CON ÉXITO' if bien else 'CON ERRORES'} ===")
    # Devuelve al llamador el resultado de la expresion indicada.
    return 0 if bien else 1


# Ejecuta el bloque siguiente solo cuando se cumple: __name__ == "__main__".
if __name__ == "__main__":
    # Lanza la excepcion indicada y detiene el flujo normal.
    raise SystemExit(asyncio.run(main()))
