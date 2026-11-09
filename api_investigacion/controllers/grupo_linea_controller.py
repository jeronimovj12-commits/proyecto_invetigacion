from fastapi import APIRouter, HTTPException, Response
from models.grupo_linea import GrupoLinea, GrupoLineaReemplazo, GrupoLineaActualizar
from servicios.ensamblador import crear_servicio_grupo_linea

router = APIRouter(prefix="/api/grupo_linea", tags=["grupo_linea"])

def _error(excepcion):
    estado = 404 if isinstance(excepcion, LookupError) else 400 if isinstance(excepcion, ValueError) else 500
    return HTTPException(status_code=estado, detail={"estado": estado, "mensaje": "No se pudo completar la operación.", "detalle": str(excepcion)})

@router.get("")
async def listar(limite: int = 1000):
    try:
        filas = await crear_servicio_grupo_linea().listar(limite)
        if not filas:
            return Response(status_code=204)
        return {"tabla": "grupo_linea", "limite": limite, "total": len(filas), "datos": filas}
    except Exception as excepcion:
        raise _error(excepcion)

@router.get("/{grupo_investigacion}/{linea_investigacion}")
async def obtener(grupo_investigacion: int, linea_investigacion: int):
    try:
        return await crear_servicio_grupo_linea().obtener({"grupo_investigacion": grupo_investigacion, "linea_investigacion": linea_investigacion})
    except Exception as excepcion:
        raise _error(excepcion)

@router.post("")
async def crear(datos: GrupoLinea):
    try:
        await crear_servicio_grupo_linea().crear(datos.model_dump())
        return {"estado": 200, "mensaje": "Registro creado."}
    except Exception as excepcion:
        raise _error(excepcion)

@router.put("/{grupo_investigacion}/{linea_investigacion}")
async def reemplazar(grupo_investigacion: int, linea_investigacion: int, datos: GrupoLineaReemplazo):
    try:
        filas = await crear_servicio_grupo_linea().actualizar({"grupo_investigacion": grupo_investigacion, "linea_investigacion": linea_investigacion}, datos.model_dump())
        return {"estado": 200, "mensaje": "Registro actualizado.", "filasAfectadas": filas}
    except Exception as excepcion:
        raise _error(excepcion)

@router.patch("/{grupo_investigacion}/{linea_investigacion}")
async def actualizar(grupo_investigacion: int, linea_investigacion: int, datos: GrupoLineaActualizar):
    try:
        filas = await crear_servicio_grupo_linea().actualizar({"grupo_investigacion": grupo_investigacion, "linea_investigacion": linea_investigacion}, datos.model_dump(exclude_unset=True))
        return {"estado": 200, "mensaje": "Registro actualizado.", "filasAfectadas": filas}
    except Exception as excepcion:
        raise _error(excepcion)

@router.delete("/{grupo_investigacion}/{linea_investigacion}")
async def eliminar(grupo_investigacion: int, linea_investigacion: int):
    try:
        filas = await crear_servicio_grupo_linea().eliminar({"grupo_investigacion": grupo_investigacion, "linea_investigacion": linea_investigacion})
        return {"estado": 200, "mensaje": "Registro retirado.", "filasAfectadas": filas}
    except Exception as excepcion:
        raise _error(excepcion)
