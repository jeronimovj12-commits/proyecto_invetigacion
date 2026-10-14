from fastapi import APIRouter, HTTPException, Response
from models.aa_linea import AaLinea, AaLineaReemplazo, AaLineaActualizar
from servicios.ensamblador import crear_servicio_aa_linea

router = APIRouter(prefix="/api/aa_linea", tags=["aa_linea"])

def _error(excepcion):
    estado = 404 if isinstance(excepcion, LookupError) else 400 if isinstance(excepcion, ValueError) else 500
    return HTTPException(status_code=estado, detail={"estado": estado, "mensaje": "No se pudo completar la operación.", "detalle": str(excepcion)})

@router.get("")
async def listar(limite: int = 1000):
    try:
        filas = await crear_servicio_aa_linea().listar(limite)
        if not filas:
            return Response(status_code=204)
        return {"tabla": "aa_linea", "limite": limite, "total": len(filas), "datos": filas}
    except Exception as excepcion:
        raise _error(excepcion)

@router.get("/{area_aplicacion}/{linea_investigacion}")
async def obtener(area_aplicacion: int, linea_investigacion: int):
    try:
        return await crear_servicio_aa_linea().obtener({"area_aplicacion": area_aplicacion, "linea_investigacion": linea_investigacion})
    except Exception as excepcion:
        raise _error(excepcion)

@router.post("")
async def crear(datos: AaLinea):
    try:
        await crear_servicio_aa_linea().crear(datos.model_dump())
        return {"estado": 200, "mensaje": "Registro creado."}
    except Exception as excepcion:
        raise _error(excepcion)

@router.put("/{area_aplicacion}/{linea_investigacion}")
async def reemplazar(area_aplicacion: int, linea_investigacion: int, datos: AaLineaReemplazo):
    try:
        filas = await crear_servicio_aa_linea().actualizar({"area_aplicacion": area_aplicacion, "linea_investigacion": linea_investigacion}, datos.model_dump())
        return {"estado": 200, "mensaje": "Registro actualizado.", "filasAfectadas": filas}
    except Exception as excepcion:
        raise _error(excepcion)

@router.patch("/{area_aplicacion}/{linea_investigacion}")
async def actualizar(area_aplicacion: int, linea_investigacion: int, datos: AaLineaActualizar):
    try:
        filas = await crear_servicio_aa_linea().actualizar({"area_aplicacion": area_aplicacion, "linea_investigacion": linea_investigacion}, datos.model_dump(exclude_unset=True))
        return {"estado": 200, "mensaje": "Registro actualizado.", "filasAfectadas": filas}
    except Exception as excepcion:
        raise _error(excepcion)

@router.delete("/{area_aplicacion}/{linea_investigacion}")
async def eliminar(area_aplicacion: int, linea_investigacion: int):
    try:
        filas = await crear_servicio_aa_linea().eliminar({"area_aplicacion": area_aplicacion, "linea_investigacion": linea_investigacion})
        return {"estado": 200, "mensaje": "Registro retirado.", "filasAfectadas": filas}
    except Exception as excepcion:
        raise _error(excepcion)
