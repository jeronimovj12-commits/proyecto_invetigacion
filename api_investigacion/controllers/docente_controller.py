from fastapi import APIRouter, HTTPException, Response
from models.docente import Docente, DocenteReemplazo, DocenteActualizar
from servicios.ensamblador import crear_servicio_docente

router = APIRouter(prefix="/api/docente", tags=["docente"])

def _error(excepcion):
    estado = 404 if isinstance(excepcion, LookupError) else 400 if isinstance(excepcion, ValueError) else 500
    return HTTPException(status_code=estado, detail={"estado": estado, "mensaje": "No se pudo completar la operación.", "detalle": str(excepcion)})

@router.get("")
async def listar(limite: int = 1000):
    try:
        filas = await crear_servicio_docente().listar(limite)
        if not filas:
            return Response(status_code=204)
        return {"tabla": "docente", "limite": limite, "total": len(filas), "datos": filas}
    except Exception as excepcion:
        raise _error(excepcion)

@router.get("/{cedula}")
async def obtener(cedula: int):
    try:
        return await crear_servicio_docente().obtener({"cedula": cedula})
    except Exception as excepcion:
        raise _error(excepcion)

@router.post("")
async def crear(datos: Docente):
    try:
        await crear_servicio_docente().crear(datos.model_dump())
        return {"estado": 200, "mensaje": "Registro creado."}
    except Exception as excepcion:
        raise _error(excepcion)

@router.put("/{cedula}")
async def reemplazar(cedula: int, datos: DocenteReemplazo):
    try:
        filas = await crear_servicio_docente().actualizar({"cedula": cedula}, datos.model_dump())
        return {"estado": 200, "mensaje": "Registro actualizado.", "filasAfectadas": filas}
    except Exception as excepcion:
        raise _error(excepcion)

@router.patch("/{cedula}")
async def actualizar(cedula: int, datos: DocenteActualizar):
    try:
        filas = await crear_servicio_docente().actualizar({"cedula": cedula}, datos.model_dump(exclude_unset=True))
        return {"estado": 200, "mensaje": "Registro actualizado.", "filasAfectadas": filas}
    except Exception as excepcion:
        raise _error(excepcion)

@router.delete("/{cedula}")
async def eliminar(cedula: int):
    try:
        filas = await crear_servicio_docente().eliminar({"cedula": cedula})
        return {"estado": 200, "mensaje": "Registro retirado.", "filasAfectadas": filas}
    except Exception as excepcion:
        raise _error(excepcion)
