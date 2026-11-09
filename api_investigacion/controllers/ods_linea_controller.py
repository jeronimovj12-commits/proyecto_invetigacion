from fastapi import APIRouter, HTTPException, Response
from models.ods_linea import OdsLinea, OdsLineaReemplazo, OdsLineaActualizar
from servicios.ensamblador import crear_servicio_ods_linea

router = APIRouter(prefix="/api/ods_linea", tags=["ods_linea"])

def _error(excepcion):
    estado = 404 if isinstance(excepcion, LookupError) else 400 if isinstance(excepcion, ValueError) else 500
    return HTTPException(status_code=estado, detail={"estado": estado, "mensaje": "No se pudo completar la operación.", "detalle": str(excepcion)})

@router.get("")
async def listar(limite: int = 1000):
    try:
        filas = await crear_servicio_ods_linea().listar(limite)
        if not filas:
            return Response(status_code=204)
        return {"tabla": "ods_linea", "limite": limite, "total": len(filas), "datos": filas}
    except Exception as excepcion:
        raise _error(excepcion)

@router.get("/{linea_investigacion}/{ods}")
async def obtener(linea_investigacion: int, ods: int):
    try:
        return await crear_servicio_ods_linea().obtener({"linea_investigacion": linea_investigacion, "ods": ods})
    except Exception as excepcion:
        raise _error(excepcion)

@router.post("")
async def crear(datos: OdsLinea):
    try:
        await crear_servicio_ods_linea().crear(datos.model_dump())
        return {"estado": 200, "mensaje": "Registro creado."}
    except Exception as excepcion:
        raise _error(excepcion)

@router.put("/{linea_investigacion}/{ods}")
async def reemplazar(linea_investigacion: int, ods: int, datos: OdsLineaReemplazo):
    try:
        filas = await crear_servicio_ods_linea().actualizar({"linea_investigacion": linea_investigacion, "ods": ods}, datos.model_dump())
        return {"estado": 200, "mensaje": "Registro actualizado.", "filasAfectadas": filas}
    except Exception as excepcion:
        raise _error(excepcion)

@router.patch("/{linea_investigacion}/{ods}")
async def actualizar(linea_investigacion: int, ods: int, datos: OdsLineaActualizar):
    try:
        filas = await crear_servicio_ods_linea().actualizar({"linea_investigacion": linea_investigacion, "ods": ods}, datos.model_dump(exclude_unset=True))
        return {"estado": 200, "mensaje": "Registro actualizado.", "filasAfectadas": filas}
    except Exception as excepcion:
        raise _error(excepcion)

@router.delete("/{linea_investigacion}/{ods}")
async def eliminar(linea_investigacion: int, ods: int):
    try:
        filas = await crear_servicio_ods_linea().eliminar({"linea_investigacion": linea_investigacion, "ods": ods})
        return {"estado": 200, "mensaje": "Registro retirado.", "filasAfectadas": filas}
    except Exception as excepcion:
        raise _error(excepcion)
