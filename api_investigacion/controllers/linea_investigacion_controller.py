from fastapi import APIRouter, HTTPException, Response
from servicios.ensamblador import crear_servicio_linea_investigacion

router = APIRouter(prefix="/api/linea_investigacion", tags=["linea_investigacion"])

def _error(excepcion):
    estado = 404 if isinstance(excepcion, LookupError) else 400 if isinstance(excepcion, ValueError) else 500
    return HTTPException(status_code=estado, detail={"estado": estado, "mensaje": "No se pudo completar la operación.", "detalle": str(excepcion)})

@router.get("")
async def listar(limite: int = 1000):
    try:
        filas = await crear_servicio_linea_investigacion().listar(limite)
        if not filas:
            return Response(status_code=204)
        return {"tabla": "linea_investigacion", "limite": limite, "total": len(filas), "datos": filas}
    except Exception as excepcion:
        raise _error(excepcion)

@router.get("/{id}")
async def obtener(id: int):
    try:
        return await crear_servicio_linea_investigacion().obtener({"id": id})
    except Exception as excepcion:
        raise _error(excepcion)

