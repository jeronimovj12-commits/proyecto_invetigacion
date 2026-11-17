# Ejecuta la instruccion indicada dentro del flujo actual.
"""Controlador HTTP: registra rutas, llama a servicios y convierte sus resultados o errores en respuestas HTTP."""
# Importa APIRouter, HTTPException, Response desde fastapi para usar esas definiciones.
from fastapi import APIRouter, HTTPException, Response
# Importa crear_servicio_objetivo_desarrollo_sostenible desde servicios.ensamblador para usar esas definiciones.
from servicios.ensamblador import crear_servicio_objetivo_desarrollo_sostenible

# Crea el router FastAPI que agrupa las rutas de este modulo.
router = APIRouter(prefix="/api/objetivo_desarrollo_sostenible", tags=["objetivo_desarrollo_sostenible"])

# Define la funcion _error con los parametros declarados; su bloque realiza esta operacion.
def _error(excepcion):
    # Asigna a estado el valor calculado a la derecha.
    estado = 404 if isinstance(excepcion, LookupError) else 400 if isinstance(excepcion, ValueError) else 500
    # Devuelve al llamador el resultado de la expresion indicada.
    return HTTPException(status_code=estado, detail={"estado": estado, "mensaje": "No se pudo completar la operación.", "detalle": str(excepcion)})

# Aplica @router.get a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@router.get("")
# Define la funcion listar con los parametros declarados; su bloque realiza esta operacion.
async def listar(limite: int = 1000):
    # Inicia un bloque cuya excepcion se manejara en los except siguientes.
    try:
        # Asigna a filas el valor calculado a la derecha.
        filas = await crear_servicio_objetivo_desarrollo_sostenible().listar(limite)
        # Ejecuta el bloque siguiente solo cuando se cumple: not filas.
        if not filas:
            # Devuelve al llamador el resultado de la expresion indicada.
            return Response(status_code=204)
        # Devuelve al llamador el resultado de la expresion indicada.
        return {"tabla": "objetivo_desarrollo_sostenible", "limite": limite, "total": len(filas), "datos": filas}
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except Exception as excepcion:
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise _error(excepcion)

# Aplica @router.get a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@router.get("/{id}")
# Define la funcion obtener con los parametros declarados; su bloque realiza esta operacion.
async def obtener(id: int):
    # Inicia un bloque cuya excepcion se manejara en los except siguientes.
    try:
        # Devuelve al llamador el resultado de la expresion indicada.
        return await crear_servicio_objetivo_desarrollo_sostenible().obtener({"id": id})
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except Exception as excepcion:
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise _error(excepcion)

