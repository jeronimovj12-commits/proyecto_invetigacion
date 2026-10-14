from fastapi import APIRouter, HTTPException, Response
from models.grupo_investigacion import GrupoInvestigacion, GrupoInvestigacionReemplazo, GrupoInvestigacionActualizar
from servicios.ensamblador import crear_servicio_grupo_investigacion

router = APIRouter(prefix="/api/grupo_investigacion", tags=["grupo_investigacion"])

def _error(excepcion):
    estado = 404 if isinstance(excepcion, LookupError) else 400 if isinstance(excepcion, ValueError) else 500
    return HTTPException(status_code=estado, detail={"estado": estado, "mensaje": "No se pudo completar la operación.", "detalle": str(excepcion)})

@router.get("")
async def listar(limite: int = 1000):
    try:
        filas = await crear_servicio_grupo_investigacion().listar(limite)
        if not filas:
            return Response(status_code=204)
        return {"tabla": "grupo_investigacion", "limite": limite, "total": len(filas), "datos": filas}
    except Exception as excepcion:
        raise _error(excepcion)

@router.get("/{id}")
async def obtener(id: int):
    try:
        return await crear_servicio_grupo_investigacion().obtener({"id": id})
    except Exception as excepcion:
        raise _error(excepcion)

@router.post("")
async def crear(datos: GrupoInvestigacion):
    try:
        await crear_servicio_grupo_investigacion().crear(datos.model_dump())
        return {"estado": 200, "mensaje": "Registro creado."}
    except Exception as excepcion:
        raise _error(excepcion)

@router.put("/{id}")
async def reemplazar(id: int, datos: GrupoInvestigacionReemplazo):
    try:
        filas = await crear_servicio_grupo_investigacion().actualizar({"id": id}, datos.model_dump())
        return {"estado": 200, "mensaje": "Registro actualizado.", "filasAfectadas": filas}
    except Exception as excepcion:
        raise _error(excepcion)

@router.patch("/{id}")
async def actualizar(id: int, datos: GrupoInvestigacionActualizar):
    try:
        filas = await crear_servicio_grupo_investigacion().actualizar({"id": id}, datos.model_dump(exclude_unset=True))
        return {"estado": 200, "mensaje": "Registro actualizado.", "filasAfectadas": filas}
    except Exception as excepcion:
        raise _error(excepcion)

@router.delete("/{id}")
async def eliminar(id: int):
    try:
        filas = await crear_servicio_grupo_investigacion().eliminar({"id": id})
        return {"estado": 200, "mensaje": "Registro retirado.", "filasAfectadas": filas}
    except Exception as excepcion:
        raise _error(excepcion)
