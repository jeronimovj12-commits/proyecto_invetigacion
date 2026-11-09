from fastapi import APIRouter, HTTPException, Response
from models.participa_semillero import ParticipaSemillero, ParticipaSemilleroReemplazo, ParticipaSemilleroActualizar
from servicios.ensamblador import crear_servicio_participa_semillero

router = APIRouter(prefix="/api/participa_semillero", tags=["participa_semillero"])

def _error(excepcion):
    estado = 404 if isinstance(excepcion, LookupError) else 400 if isinstance(excepcion, ValueError) else 500
    return HTTPException(status_code=estado, detail={"estado": estado, "mensaje": "No se pudo completar la operación.", "detalle": str(excepcion)})

@router.get("")
async def listar(limite: int = 1000):
    try:
        filas = await crear_servicio_participa_semillero().listar(limite)
        if not filas:
            return Response(status_code=204)
        return {"tabla": "participa_semillero", "limite": limite, "total": len(filas), "datos": filas}
    except Exception as excepcion:
        raise _error(excepcion)

@router.get("/{docente}/{semillero}")
async def obtener(docente: int, semillero: int):
    try:
        return await crear_servicio_participa_semillero().obtener({"docente": docente, "semillero": semillero})
    except Exception as excepcion:
        raise _error(excepcion)

@router.post("")
async def crear(datos: ParticipaSemillero):
    try:
        await crear_servicio_participa_semillero().crear(datos.model_dump())
        return {"estado": 200, "mensaje": "Registro creado."}
    except Exception as excepcion:
        raise _error(excepcion)

@router.put("/{docente}/{semillero}")
async def reemplazar(docente: int, semillero: int, datos: ParticipaSemilleroReemplazo):
    try:
        filas = await crear_servicio_participa_semillero().actualizar({"docente": docente, "semillero": semillero}, datos.model_dump())
        return {"estado": 200, "mensaje": "Registro actualizado.", "filasAfectadas": filas}
    except Exception as excepcion:
        raise _error(excepcion)

@router.patch("/{docente}/{semillero}")
async def actualizar(docente: int, semillero: int, datos: ParticipaSemilleroActualizar):
    try:
        filas = await crear_servicio_participa_semillero().actualizar({"docente": docente, "semillero": semillero}, datos.model_dump(exclude_unset=True))
        return {"estado": 200, "mensaje": "Registro actualizado.", "filasAfectadas": filas}
    except Exception as excepcion:
        raise _error(excepcion)

@router.delete("/{docente}/{semillero}")
async def eliminar(docente: int, semillero: int):
    try:
        filas = await crear_servicio_participa_semillero().eliminar({"docente": docente, "semillero": semillero})
        return {"estado": 200, "mensaje": "Registro retirado.", "filasAfectadas": filas}
    except Exception as excepcion:
        raise _error(excepcion)
