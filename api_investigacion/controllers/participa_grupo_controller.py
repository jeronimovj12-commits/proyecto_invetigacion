from fastapi import APIRouter, HTTPException, Response
from models.participa_grupo import ParticipaGrupo, ParticipaGrupoReemplazo, ParticipaGrupoActualizar
from servicios.ensamblador import crear_servicio_participa_grupo

router = APIRouter(prefix="/api/participa_grupo", tags=["participa_grupo"])

def _error(excepcion):
    estado = 404 if isinstance(excepcion, LookupError) else 400 if isinstance(excepcion, ValueError) else 500
    return HTTPException(status_code=estado, detail={"estado": estado, "mensaje": "No se pudo completar la operación.", "detalle": str(excepcion)})

@router.get("")
async def listar(limite: int = 1000):
    try:
        filas = await crear_servicio_participa_grupo().listar(limite)
        if not filas:
            return Response(status_code=204)
        return {"tabla": "participa_grupo", "limite": limite, "total": len(filas), "datos": filas}
    except Exception as excepcion:
        raise _error(excepcion)

@router.get("/{docente_cedula}/{grupo_investigacion_id}")
async def obtener(docente_cedula: int, grupo_investigacion_id: int):
    try:
        return await crear_servicio_participa_grupo().obtener({"docente_cedula": docente_cedula, "grupo_investigacion_id": grupo_investigacion_id})
    except Exception as excepcion:
        raise _error(excepcion)

@router.post("")
async def crear(datos: ParticipaGrupo):
    try:
        await crear_servicio_participa_grupo().crear(datos.model_dump())
        return {"estado": 200, "mensaje": "Registro creado."}
    except Exception as excepcion:
        raise _error(excepcion)

@router.put("/{docente_cedula}/{grupo_investigacion_id}")
async def reemplazar(docente_cedula: int, grupo_investigacion_id: int, datos: ParticipaGrupoReemplazo):
    try:
        filas = await crear_servicio_participa_grupo().actualizar({"docente_cedula": docente_cedula, "grupo_investigacion_id": grupo_investigacion_id}, datos.model_dump())
        return {"estado": 200, "mensaje": "Registro actualizado.", "filasAfectadas": filas}
    except Exception as excepcion:
        raise _error(excepcion)

@router.patch("/{docente_cedula}/{grupo_investigacion_id}")
async def actualizar(docente_cedula: int, grupo_investigacion_id: int, datos: ParticipaGrupoActualizar):
    try:
        filas = await crear_servicio_participa_grupo().actualizar({"docente_cedula": docente_cedula, "grupo_investigacion_id": grupo_investigacion_id}, datos.model_dump(exclude_unset=True))
        return {"estado": 200, "mensaje": "Registro actualizado.", "filasAfectadas": filas}
    except Exception as excepcion:
        raise _error(excepcion)

@router.delete("/{docente_cedula}/{grupo_investigacion_id}")
async def eliminar(docente_cedula: int, grupo_investigacion_id: int):
    try:
        filas = await crear_servicio_participa_grupo().eliminar({"docente_cedula": docente_cedula, "grupo_investigacion_id": grupo_investigacion_id})
        return {"estado": 200, "mensaje": "Registro retirado.", "filasAfectadas": filas}
    except Exception as excepcion:
        raise _error(excepcion)
