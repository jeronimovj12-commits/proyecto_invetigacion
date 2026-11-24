"""Prueba los servicios con repositorios de memoria para demostrar independencia del motor."""

import asyncio
import sys
from pathlib import Path

# La ruta se fija desde el archivo de prueba para ejecutarlo igual desde el contenedor o el directorio raíz.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from servicios.servicio_area_aplicacion import ServicioAreaAplicacion
from servicios.servicio_area_conocimiento import ServicioAreaConocimiento
from servicios.servicio_linea_investigacion import ServicioLineaInvestigacion
from servicios.servicio_objetivo_desarrollo_sostenible import ServicioObjetivoDesarrolloSostenible
from servicios.servicio_termino_clave import ServicioTerminoClave
from servicios.servicio_universidad import ServicioUniversidad


class RepositorioMemoria:
    """Conserva datos y estado activo para sustituir al adaptador PostgreSQL en pruebas."""

    def __init__(self, clave: str, autogenerar: bool = False):
        self.clave = clave
        self.autogenerar = autogenerar
        self.filas: list[dict] = []
        self.siguiente = 1

    async def obtener_todos(self, limite: int) -> list[dict]:
        return [
            {campo: valor for campo, valor in fila.items() if campo != "activo"}
            for fila in self.filas if fila["activo"]
        ][:limite]

    async def obtener_por_id(self, identificador):
        fila = next(
            (fila for fila in self.filas
             if fila[self.clave] == identificador and fila["activo"]),
            None,
        )
        return ({campo: valor for campo, valor in fila.items() if campo != "activo"}
                if fila else None)

    async def crear(self, datos: dict):
        fila = dict(datos)
        if self.autogenerar:
            fila[self.clave] = self.siguiente
            self.siguiente += 1
        self.filas.append({**fila, "activo": True})
        return fila[self.clave]

    async def actualizar(self, identificador, datos: dict) -> int:
        fila = next(
            (fila for fila in self.filas
             if fila[self.clave] == identificador and fila["activo"]),
            None,
        )
        if fila is None:
            return 0
        fila.update(datos)
        return 1

    async def eliminar_logico(self, identificador) -> int:
        fila = next(
            (fila for fila in self.filas
             if fila[self.clave] == identificador and fila["activo"]),
            None,
        )
        if fila is None:
            return 0
        fila["activo"] = False
        return 1


async def probar_servicio(servicio, datos: dict, clave: str, clave_automatica: bool = False):
    assert await servicio.listar(100) == []
    identificador = await servicio.crear(datos)
    if not clave_automatica:
        identificador = datos[clave]
    registro = await servicio.obtener(identificador)
    assert registro[clave] == identificador

    campo_actualizable = next(campo for campo in datos if campo != clave)
    await servicio.actualizar(identificador, {campo_actualizable: "Valor actualizado"})
    assert (await servicio.obtener(identificador))[campo_actualizable] == "Valor actualizado"

    await servicio.eliminar(identificador)
    assert await servicio.listar(100) == []
    try:
        await servicio.obtener(identificador)
    except LookupError:
        pass
    else:
        raise AssertionError("El registro retirado debió tratarse como inexistente.")

    try:
        await servicio.eliminar(identificador)
    except LookupError:
        pass
    else:
        raise AssertionError("Una segunda retirada debió producir LookupError.")


async def main():
    casos = [
        (ServicioAreaConocimiento, "id",
         {"id": "9Z01", "gran_area": "Ciencias", "area": "Datos", "disciplina": "Análisis"}),
        (ServicioObjetivoDesarrolloSostenible, "id",
         {"id": 90, "nombre": "Objetivo de prueba", "categoria": "Social"}),
        (ServicioAreaAplicacion, "id", {"id": 90, "nombre": "Área de prueba"}),
        (ServicioTerminoClave, "termino",
         {"termino": "prueba", "termino_ingles": "test"}),
        (ServicioUniversidad, "id",
         {"id": 90, "nombre": "Universidad de prueba", "tipo": "Pública", "ciudad": "Verde"}),
        (ServicioLineaInvestigacion, "id",
         {"nombre": "Línea de prueba", "descripcion": "Descripción de prueba"}),
    ]

    for clase_servicio, clave, datos in casos:
        autogenerar = clase_servicio is ServicioLineaInvestigacion
        repositorio = RepositorioMemoria(clave, autogenerar)
        await probar_servicio(clase_servicio(repositorio), datos, clave, autogenerar)

    servicio = ServicioAreaConocimiento(RepositorioMemoria("id"))
    for limite in (0, -1):
        try:
            await servicio.listar(limite)
        except ValueError:
            continue
        raise AssertionError("Los límites no positivos deben producir ValueError.")
    try:
        await servicio.actualizar("1A01", {})
    except ValueError:
        pass
    else:
        raise AssertionError("Un PATCH vacío debe producir ValueError.")

    print("Prueba de capas completada: seis servicios, reglas y borrado lógico verificados sin PostgreSQL.")


if __name__ == "__main__":
    asyncio.run(main())
