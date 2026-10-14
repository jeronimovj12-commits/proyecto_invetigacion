from fastapi import APIRouter, HTTPException, Response
from servicios.ensamblador import crear_servicio_area_aplicacion

router = APIRouter(prefix="/api/area_aplicacion", tags=["area_aplicacion"])

def _error(excepcion):
    estado = 404 if isinstance(excepcion, LookupError) else 400 if isinstance(excepcion, ValueError) else 500
    return HTTPException(status_code=estado, detail={"estado": estado, "mensaje": "No se pudo completar la operación.", "detalle": str(excepcion)})

@router.get("")
async def listar(limite: int = 1000):
    try:
        filas = await crear_servicio_area_aplicacion().listar(limite)
        if not filas:
            return Response(status_code=204)
        return {"tabla": "area_aplicacion", "limite": limite, "total": len(filas), "datos": filas}
    except Exception as excepcion:
        raise _error(excepcion)

@router.get("/{id}")
async def obtener(id: int):
    try:
        return await crear_servicio_area_aplicacion().obtener({"id": id})
    except Exception as excepcion:
        raise _error(excepcion)

