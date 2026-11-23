# Ejecuta la instruccion indicada dentro del flujo actual.
"""Servicio de negocio: coordina las reglas del caso de uso con los repositorios sin ejecutar SQL directamente."""
# Importa IRepositorioSemilleroLinea desde repositorios.abstracciones.i_repositorio_semillero_linea para usar esas definiciones.
from repositorios.abstracciones.i_repositorio_semillero_linea import IRepositorioSemilleroLinea


# Define la clase ServicioSemilleroLinea y agrupa su estado y operaciones.
class ServicioSemilleroLinea:
    # Define la funcion __init__ con los parametros declarados; su bloque realiza esta operacion.
    def __init__(self, repositorio: IRepositorioSemilleroLinea):
        # Guarda en self._repositorio el valor necesario para reutilizarlo en otros metodos.
        self._repositorio = repositorio

    # Define la funcion listar con los parametros declarados; su bloque realiza esta operacion.
    async def listar(self, limite: int) -> list[dict]:
        # Ejecuta el bloque siguiente solo cuando se cumple: limite <= 0.
        if limite <= 0:
            # Lanza la excepcion indicada y detiene el flujo normal.
            raise ValueError("El límite debe ser mayor que cero.")
        # Devuelve al llamador el resultado de la expresion indicada.
        return await self._repositorio.obtener_todos(limite)

    # Define la funcion obtener con los parametros declarados; su bloque realiza esta operacion.
    async def obtener(self, identidad: dict) -> dict:
        # Asigna a fila el valor calculado a la derecha.
        fila = await self._repositorio.obtener_por_id(identidad)
        # Ejecuta el bloque siguiente solo cuando se cumple: fila is None.
        if fila is None:
            # Lanza la excepcion indicada y detiene el flujo normal.
            raise LookupError("El registro no existe o está inactivo.")
        # Devuelve al llamador el resultado de la expresion indicada.
        return fila

    # Define la funcion _validar_referencias con los parametros declarados; su bloque realiza esta operacion.
    async def _validar_referencias(self, datos: dict) -> None:
        # Recorre los elementos de la coleccion indicada y ejecuta el bloque para cada uno.
        for campo in ('semillero', 'linea_investigacion'):
            # Ejecuta el bloque siguiente solo cuando se cumple: campo in datos and datos[campo] is not None.
            if campo in datos and datos[campo] is not None:
                # Ejecuta el bloque siguiente solo cuando se cumple: not await self._repositorio.referencia_activa(campo, datos[campo]).
                if not await self._repositorio.referencia_activa(campo, datos[campo]):
                    # Lanza la excepcion indicada y detiene el flujo normal.
                    raise ValueError(f"La referencia {campo} no existe o está inactiva.")

    # Define la funcion crear con los parametros declarados; su bloque realiza esta operacion.
    async def crear(self, datos: dict) -> None:
        # Abre el recurso asincronico y asegura su cierre al salir del bloque.
        async with self._repositorio.transaccion():
            # Espera que termine la operacion asincronica antes de continuar.
            await self._validar_referencias(datos)
            # Espera que termine la operacion asincronica antes de continuar.
            await self._repositorio.crear(datos)

    # Define la funcion actualizar con los parametros declarados; su bloque realiza esta operacion.
    async def actualizar(self, identidad: dict, datos: dict) -> int:
        # Abre el recurso asincronico y asegura su cierre al salir del bloque.
        async with self._repositorio.transaccion():
            # Ejecuta el bloque siguiente solo cuando se cumple: not datos.
            if not datos:
                # Lanza la excepcion indicada y detiene el flujo normal.
                raise ValueError("No se envió ningún campo para actualizar.")
            # Asigna a actual el valor calculado a la derecha.
            actual = await self.obtener(identidad)
            # Espera que termine la operacion asincronica antes de continuar.
            await self._validar_referencias({**actual, **datos})
            # Asigna a filas el valor calculado a la derecha.
            filas = await self._repositorio.actualizar(identidad, datos)
            # Ejecuta el bloque siguiente solo cuando se cumple: filas == 0.
            if filas == 0:
                # Lanza la excepcion indicada y detiene el flujo normal.
                raise LookupError("El registro no existe o está inactivo.")
            # Devuelve al llamador el resultado de la expresion indicada.
            return filas

    # Define la funcion eliminar con los parametros declarados; su bloque realiza esta operacion.
    async def eliminar(self, identidad: dict) -> int:
        # Abre el recurso asincronico y asegura su cierre al salir del bloque.
        async with self._repositorio.transaccion():
            # Espera que termine la operacion asincronica antes de continuar.
            await self.obtener(identidad)
            # Ejecuta el bloque siguiente solo cuando se cumple: await self._repositorio.tiene_dependientes(identidad).
            if await self._repositorio.tiene_dependientes(identidad):
                # Lanza la excepcion indicada y detiene el flujo normal.
                raise ValueError("El registro tiene relaciones activas. Retire primero esas relaciones.")
            # Asigna a filas el valor calculado a la derecha.
            filas = await self._repositorio.eliminar_logico(identidad)
            # Ejecuta el bloque siguiente solo cuando se cumple: filas == 0.
            if filas == 0:
                # Lanza la excepcion indicada y detiene el flujo normal.
                raise LookupError("El registro no existe o está inactivo.")
            # Devuelve al llamador el resultado de la expresion indicada.
            return filas
