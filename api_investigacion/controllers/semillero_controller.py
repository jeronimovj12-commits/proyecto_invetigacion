from fastapi import APIRouter, HTTPException, Response
from models.semillero import Semillero, SemilleroReemplazo, SemilleroActualizar
from servicios.ensamblador import crear_servicio_semillero

router = APIRouter(prefix="/api/semillero", tags=["semillero"])

def _error(excepcion):
    estado = 404 if isinstance(excepcion, LookupError) else 400 if isinstance(excepcion, ValueError) else 500
    return HTTPException(status_code=estado, detail={"estado": estado, "mensaje": "No se pudo completar la operación.", "detalle": str(excepcion)})

@router.get("")
async def listar(limite: int = 1000):
    try:
        filas = await crear_servicio_semillero().listar(limite)
        if not filas:
            return Response(status_code=204)
        return {"tabla": "semillero", "limite": limite, "total": len(filas), "datos": filas}
    except Exception as excepcion:
        raise _error(excepcion)

@router.get("/{id}")
async def obtener(id: int):
    try:
        return await crear_servicio_semillero().obtener({"id": id})
    except Exception as excepcion:
        raise _error(excepcion)

@router.post("")
async def crear(datos: Semillero):
    try:
        await crear_servicio_semillero().crear(datos.model_dump())
        return {"estado": 200, "mensaje": "Registro creado."}
    except Exception as excepcion:
        raise _error(excepcion)

@router.put("/{id}")
async def reemplazar(id: int, datos: SemilleroReemplazo):
    try:
        filas = await crear_servicio_semillero().actualizar({"id": id}, datos.model_dump())
        return {"estado": 200, "mensaje": "Registro actualizado.", "filasAfectadas": filas}
    except Exception as excepcion:
        raise _error(excepcion)

@router.patch("/{id}")
async def actualizar(id: int, datos: SemilleroActualizar):
    try:
        filas = await crear_servicio_semillero().actualizar({"id": id}, datos.model_dump(exclude_unset=True))
        return {"estado": 200, "mensaje": "Registro actualizado.", "filasAfectadas": filas}
    except Exception as excepcion:
        raise _error(excepcion)

@router.delete("/{id}")
async def eliminar(id: int):
    try:
        filas = await crear_servicio_semillero().eliminar({"id": id})
        return {"estado": 200, "mensaje": "Registro retirado.", "filasAfectadas": filas}
    except Exception as excepcion:
        raise _error(excepcion)
