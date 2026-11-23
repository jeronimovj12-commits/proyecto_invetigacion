"""
Servicio — la capa de NEGOCIO.

Depende solo de la interfaz del repositorio, así que no sabe qué motor hay
detrás: por eso se puede probar sin base de datos.

Comunica los problemas con excepciones, que el controlador traduce a códigos
HTTP. El servicio no sabe qué es un 404, y así debe ser.
"""

# Importa ( desde repositorios.abstracciones.i_repositorio_area_conocimiento para usar esas definiciones.
from repositorios.abstracciones.i_repositorio_area_conocimiento import (
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    IRepositorioAreaConocimiento,
# Cierra la estructura abierta en las lineas anteriores.
)


# Define la clase ServicioAreaConocimiento y agrupa su estado y operaciones.
class ServicioAreaConocimiento:
    # Ejecuta la instruccion indicada dentro del flujo actual.
    """Reglas de negocio del CRUD de area_conocimiento."""

    # Define la funcion __init__ con los parametros declarados; su bloque realiza esta operacion.
    def __init__(self, repositorio: IRepositorioAreaConocimiento):
        # Guarda en self._repositorio el valor necesario para reutilizarlo en otros metodos.
        self._repositorio = repositorio

    # Aplica @staticmethod a la declaracion que sigue; en rutas, registra el endpoint HTTP.
    @staticmethod
    # Define la funcion _validar_id con los parametros declarados; su bloque realiza esta operacion.
    def _validar_id(id_area: str) -> str:
        # Asigna a id_area el valor calculado a la derecha.
        id_area = (id_area or "").strip()
        # Ejecuta el bloque siguiente solo cuando se cumple: not id_area.
        if not id_area:
            # Lanza la excepcion indicada y detiene el flujo normal.
            raise ValueError("El id del área de conocimiento no puede estar vacío.")
        # Devuelve al llamador el resultado de la expresion indicada.
        return id_area

    # Define la funcion listar con los parametros declarados; su bloque realiza esta operacion.
    async def listar(self, limite: int) -> list[dict]:
        # La FORMA del dato es correcta (sí es un entero), así que esto es
        # 400 y no 422.
        # Ejecuta el bloque siguiente solo cuando se cumple: limite <= 0.
        if limite <= 0:
            # Lanza la excepcion indicada y detiene el flujo normal.
            raise ValueError("El límite debe ser un entero mayor que cero.")
        # Devuelve al llamador el resultado de la expresion indicada.
        return await self._repositorio.obtener_todos(limite)

    # Define la funcion obtener con los parametros declarados; su bloque realiza esta operacion.
    async def obtener(self, id_area: str) -> dict:
        # Asigna a id_area el valor calculado a la derecha.
        id_area = self._validar_id(id_area)
        # Asigna a fila el valor calculado a la derecha.
        fila = await self._repositorio.obtener_por_id(id_area)
        # Ejecuta el bloque siguiente solo cuando se cumple: fila is None.
        if fila is None:
            # Lanza la excepcion indicada y detiene el flujo normal.
            raise LookupError(
                # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                f"No existe un área con el código {id_area}.")
        # Devuelve al llamador el resultado de la expresion indicada.
        return fila

    # Define la funcion crear con los parametros declarados; su bloque realiza esta operacion.
    async def crear(self, datos: dict) -> None:
        # Espera que termine la operacion asincronica antes de continuar.
        await self._repositorio.crear(datos)

    # Define la funcion actualizar con los parametros declarados; su bloque realiza esta operacion.
    async def actualizar(self, id_area: str, datos: dict) -> int:
        # Asigna a id_area el valor calculado a la derecha.
        id_area = self._validar_id(id_area)
        # Sin esta comprobación el repositorio devolvería 0 filas, que en
        # toda la demás lógica significa "no existe" — y responderíamos 404
        # en vez del 400 que exige el contrato para un cuerpo vacío.
        # Ejecuta el bloque siguiente solo cuando se cumple: not datos.
        if not datos:
            # Lanza la excepcion indicada y detiene el flujo normal.
            raise ValueError("No se envió ningún campo para actualizar.")
        # Asigna a filas el valor calculado a la derecha.
        filas = await self._repositorio.actualizar(id_area, datos)
        # Ejecuta el bloque siguiente solo cuando se cumple: filas == 0.
        if filas == 0:
            # Lanza la excepcion indicada y detiene el flujo normal.
            raise LookupError(
                # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                f"No existe un área con el código {id_area}.")
        # Devuelve al llamador el resultado de la expresion indicada.
        return filas

    # Define la funcion eliminar con los parametros declarados; su bloque realiza esta operacion.
    async def eliminar(self, id_area: str) -> int:
        # Asigna a id_area el valor calculado a la derecha.
        id_area = self._validar_id(id_area)
        # Abre el recurso asincronico y asegura su cierre al salir del bloque.
        async with self._repositorio.transaccion():
            # Espera que termine la operacion asincronica antes de continuar.
            await self.obtener(id_area)
            # Ejecuta el bloque siguiente solo cuando se cumple: await self._repositorio.tiene_dependientes(id_area).
            if await self._repositorio.tiene_dependientes(id_area):
                # Lanza la excepcion indicada y detiene el flujo normal.
                raise ValueError("El área tiene líneas activas relacionadas. Retire primero esas relaciones.")
            # Asigna a filas el valor calculado a la derecha.
            filas = await self._repositorio.eliminar_logico(id_area)
            # Ejecuta el bloque siguiente solo cuando se cumple: filas == 0.
            if filas == 0:
                # Lanza la excepcion indicada y detiene el flujo normal.
                raise LookupError(f"No existe un área con el código {id_area}.")
            # Devuelve al llamador el resultado de la expresion indicada.
            return filas
