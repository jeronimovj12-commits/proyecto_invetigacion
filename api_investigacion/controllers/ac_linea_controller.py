from fastapi import APIRouter, HTTPException, Response
from models.ac_linea import AcLinea, AcLineaReemplazo, AcLineaActualizar
from servicios.ensamblador import crear_servicio_ac_linea

router = APIRouter(prefix="/api/ac_linea", tags=["ac_linea"])

def _error(excepcion):
    estado = 404 if isinstance(excepcion, LookupError) else 400 if isinstance(excepcion, ValueError) else 500
    return HTTPException(status_code=estado, detail={"estado": estado, "mensaje": "No se pudo completar la operación.", "detalle": str(excepcion)})

@router.get("")
async def listar(limite: int = 1000):
    try:
        filas = await crear_servicio_ac_linea().listar(limite)
        if not filas:
            return Response(status_code=204)
        return {"tabla": "ac_linea", "limite": limite, "total": len(filas), "datos": filas}
    except Exception as excepcion:
        raise _error(excepcion)

@router.get("/{linea_investigacion}/{area_conocimiento}")
async def obtener(linea_investigacion: int, area_conocimiento: str):
    try:
        return await crear_servicio_ac_linea().obtener({"linea_investigacion": linea_investigacion, "area_conocimiento": area_conocimiento})
    except Exception as excepcion:
        raise _error(excepcion)

@router.post("")
async def crear(datos: AcLinea):
    try:
        await crear_servicio_ac_linea().crear(datos.model_dump())
        return {"estado": 200, "mensaje": "Registro creado."}
    except Exception as excepcion:
        raise _error(excepcion)

@router.put("/{linea_investigacion}/{area_conocimiento}")
async def reemplazar(linea_investigacion: int, area_conocimiento: str, datos: AcLineaReemplazo):
    try:
        filas = await crear_servicio_ac_linea().actualizar({"linea_investigacion": linea_investigacion, "area_conocimiento": area_conocimiento}, datos.model_dump())
        return {"estado": 200, "mensaje": "Registro actualizado.", "filasAfectadas": filas}
    except Exception as excepcion:
        raise _error(excepcion)

@router.patch("/{linea_investigacion}/{area_conocimiento}")
async def actualizar(linea_investigacion: int, area_conocimiento: str, datos: AcLineaActualizar):
    try:
        filas = await crear_servicio_ac_linea().actualizar({"linea_investigacion": linea_investigacion, "area_conocimiento": area_conocimiento}, datos.model_dump(exclude_unset=True))
        return {"estado": 200, "mensaje": "Registro actualizado.", "filasAfectadas": filas}
    except Exception as excepcion:
        raise _error(excepcion)

@router.delete("/{linea_investigacion}/{area_conocimiento}")
async def eliminar(linea_investigacion: int, area_conocimiento: str):
    try:
        filas = await crear_servicio_ac_linea().eliminar({"linea_investigacion": linea_investigacion, "area_conocimiento": area_conocimiento})
        return {"estado": 200, "mensaje": "Registro retirado.", "filasAfectadas": filas}
    except Exception as excepcion:
        raise _error(excepcion)
