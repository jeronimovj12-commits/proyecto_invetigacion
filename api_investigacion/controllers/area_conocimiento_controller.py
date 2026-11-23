"""
Controlador — la capa HTTP.

Su único trabajo es traducir: recibe una petición, llama al servicio y
convierte lo que pase en un código de estado.

    ValueError   → 400   (la forma es válida, la regla no se cumple)
    LookupError  → 404
    lo demás     → 500

El 422 no aparece aquí: lo produce Pydantic ANTES de entrar, cuando el cuerpo
no tiene la forma declarada en models/.
"""

from fastapi import APIRouter, HTTPException, Response

from models.area_conocimiento import (AreaConocimiento,
                                      AreaConocimientoActualizar,
                                      AreaConocimientoReemplazo)
from servicios.ensamblador import crear_servicio_area_conocimiento

router = APIRouter(prefix="/api", tags=["area_conocimiento"])

TABLA = "area_conocimiento"


def _respuesta_publica(fila: dict) -> dict:
    """Expone el JSON del contrato sin filtrar los nombres de PostgreSQL."""
    return {
        "id": fila["id"],
        "granArea": fila["gran_area"],
        "area": fila["area"],
        "disciplina": fila["disciplina"],
    }


def _error(estado: int, mensaje: str, detalle: str) -> HTTPException:
    return HTTPException(
        status_code=estado,
        detail={"estado": estado, "mensaje": mensaje, "detalle": detalle},
    )


# ----------------------------------------------------------------------
# GET /api/area_conocimiento — Listar (query string ?limite=N)
# ----------------------------------------------------------------------
@router.get(f"/{TABLA}")
async def listar(limite: int = 1000):
    try:
        servicio = crear_servicio_area_conocimiento()
        filas = await servicio.listar(limite)
        if not filas:
            # 204: éxito SIN contenido — "tabla vacía" no es un error.
            return Response(status_code=204)
        return {"tabla": TABLA, "limite": limite,
                "total": len(filas), "datos": [_respuesta_publica(fila) for fila in filas]}
    except ValueError as excepcion:
        raise _error(400, "Parámetros inválidos.", str(excepcion))
    except Exception as excepcion:
        raise _error(500, "Error al consultar las áreas de conocimiento.",
                     str(excepcion))


# ----------------------------------------------------------------------
# GET /api/area_conocimiento/{id_area} — Obtener una
# ----------------------------------------------------------------------
@router.get(f"/{TABLA}/{{id_area}}")
async def obtener(id_area: str):
    try:
        servicio = crear_servicio_area_conocimiento()
        return _respuesta_publica(await servicio.obtener(id_area))
    except ValueError as excepcion:
        raise _error(400, "Parámetros inválidos.", str(excepcion))
    except LookupError as excepcion:
        raise _error(404, "Área de conocimiento no encontrada.", str(excepcion))
    except Exception as excepcion:
        raise _error(500, "Error al consultar el área de conocimiento.",
                     str(excepcion))


# ----------------------------------------------------------------------
# POST /api/area_conocimiento — Crear
# ----------------------------------------------------------------------
@router.post(f"/{TABLA}")
async def crear(area: AreaConocimiento):
    try:
        servicio = crear_servicio_area_conocimiento()
        await servicio.crear(area.model_dump())
        return {"estado": 200, "mensaje": "Área de conocimiento creada exitosamente."}
    except ValueError as excepcion:
        raise _error(400, "Datos inválidos.", str(excepcion))
    except Exception as excepcion:
        # Aquí cae la llave duplicada: la defiende la base, no la API.
        raise _error(500, "No se pudo crear el área de conocimiento.",
                     str(excepcion))


# ----------------------------------------------------------------------
# PUT /api/area_conocimiento/{id_area} — Reemplazo COMPLETO
# ----------------------------------------------------------------------
@router.put(f"/{TABLA}/{{id_area}}")
async def reemplazar(id_area: str, area: AreaConocimientoReemplazo):
    try:
        servicio = crear_servicio_area_conocimiento()
        # PUT: el modelo exige TODOS los campos → se escriben los tres.
        filas = await servicio.actualizar(id_area, area.model_dump())
        return {"estado": 200, "mensaje": "Área de conocimiento reemplazada.",
                "filasAfectadas": filas}
    except ValueError as excepcion:
        raise _error(400, "Parámetros inválidos.", str(excepcion))
    except LookupError as excepcion:
        raise _error(404, "Área de conocimiento no encontrada.", str(excepcion))
    except Exception as excepcion:
        raise _error(500, "No se pudo reemplazar el área de conocimiento.",
                     str(excepcion))


# ----------------------------------------------------------------------
# PATCH /api/area_conocimiento/{id_area} — Actualización PARCIAL
# ----------------------------------------------------------------------
@router.patch(f"/{TABLA}/{{id_area}}")
async def actualizar(id_area: str, area: AreaConocimientoActualizar):
    try:
        servicio = crear_servicio_area_conocimiento()
        # PATCH: solo los campos que el cliente envió. Si no envió ninguno,
        # el servicio responde con ValueError → 400.
        datos = area.model_dump(exclude_none=True)
        filas = await servicio.actualizar(id_area, datos)
        return {"estado": 200, "mensaje": "Área de conocimiento actualizada.",
                "filasAfectadas": filas}
    except ValueError as excepcion:
        raise _error(400, "Parámetros inválidos.", str(excepcion))
    except LookupError as excepcion:
        raise _error(404, "Área de conocimiento no encontrada.", str(excepcion))
    except Exception as excepcion:
        raise _error(500, "No se pudo actualizar el área de conocimiento.",
                     str(excepcion))


# ----------------------------------------------------------------------
# DELETE /api/area_conocimiento/{id_area} — Eliminar (LÓGICO)
# ----------------------------------------------------------------------
@router.delete(f"/{TABLA}/{{id_area}}")
async def eliminar(id_area: str):
    try:
        servicio = crear_servicio_area_conocimiento()
        filas = await servicio.eliminar(id_area)
        return {"estado": 200, "mensaje": "Área de conocimiento eliminada.",
                "filasAfectadas": filas}
    except ValueError as excepcion:
        raise _error(400, "Parámetros inválidos.", str(excepcion))
    except LookupError as excepcion:
        raise _error(404, "Área de conocimiento no encontrada.", str(excepcion))
    except Exception as excepcion:
        raise _error(500, "No se pudo eliminar el área de conocimiento.",
                     str(excepcion))
