# Ejecuta la instruccion indicada dentro del flujo actual.
"""Servicio de negocio: coordina las reglas del caso de uso con los repositorios sin ejecutar SQL directamente."""
# Importa IRepositorioAreaAplicacion desde repositorios.abstracciones.i_repositorio_area_aplicacion para usar esas definiciones.
from repositorios.abstracciones.i_repositorio_area_aplicacion import IRepositorioAreaAplicacion


# Define la clase ServicioAreaAplicacion y agrupa su estado y operaciones.
class ServicioAreaAplicacion:
    # Define la funcion __init__ con los parametros declarados; su bloque realiza esta operacion.
    def __init__(self, repositorio: IRepositorioAreaAplicacion):
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
