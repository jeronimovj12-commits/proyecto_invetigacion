from fastapi import APIRouter, HTTPException, Response
from models.semillero_linea import SemilleroLinea, SemilleroLineaReemplazo, SemilleroLineaActualizar
from servicios.ensamblador import crear_servicio_semillero_linea

router = APIRouter(prefix="/api/semillero_linea", tags=["semillero_linea"])

def _error(excepcion):
    estado = 404 if isinstance(excepcion, LookupError) else 400 if isinstance(excepcion, ValueError) else 500
    return HTTPException(status_code=estado, detail={"estado": estado, "mensaje": "No se pudo completar la operación.", "detalle": str(excepcion)})

@router.get("")
async def listar(limite: int = 1000):
    try:
        filas = await crear_servicio_semillero_linea().listar(limite)
        if not filas:
            return Response(status_code=204)
        return {"tabla": "semillero_linea", "limite": limite, "total": len(filas), "datos": filas}
    except Exception as excepcion:
        raise _error(excepcion)

@router.get("/{semillero}/{linea_investigacion}")
async def obtener(semillero: int, linea_investigacion: int):
    try:
        return await crear_servicio_semillero_linea().obtener({"semillero": semillero, "linea_investigacion": linea_investigacion})
    except Exception as excepcion:
        raise _error(excepcion)

@router.post("")
async def crear(datos: SemilleroLinea):
    try:
        await crear_servicio_semillero_linea().crear(datos.model_dump())
        return {"estado": 200, "mensaje": "Registro creado."}
    except Exception as excepcion:
        raise _error(excepcion)

@router.put("/{semillero}/{linea_investigacion}")
async def reemplazar(semillero: int, linea_investigacion: int, datos: SemilleroLineaReemplazo):
    try:
        filas = await crear_servicio_semillero_linea().actualizar({"semillero": semillero, "linea_investigacion": linea_investigacion}, datos.model_dump())
        return {"estado": 200, "mensaje": "Registro actualizado.", "filasAfectadas": filas}
    except Exception as excepcion:
        raise _error(excepcion)

@router.patch("/{semillero}/{linea_investigacion}")
async def actualizar(semillero: int, linea_investigacion: int, datos: SemilleroLineaActualizar):
    try:
        filas = await crear_servicio_semillero_linea().actualizar({"semillero": semillero, "linea_investigacion": linea_investigacion}, datos.model_dump(exclude_unset=True))
        return {"estado": 200, "mensaje": "Registro actualizado.", "filasAfectadas": filas}
    except Exception as excepcion:
        raise _error(excepcion)

@router.delete("/{semillero}/{linea_investigacion}")
async def eliminar(semillero: int, linea_investigacion: int):
    try:
        filas = await crear_servicio_semillero_linea().eliminar({"semillero": semillero, "linea_investigacion": linea_investigacion})
        return {"estado": 200, "mensaje": "Registro retirado.", "filasAfectadas": filas}
    except Exception as excepcion:
        raise _error(excepcion)
