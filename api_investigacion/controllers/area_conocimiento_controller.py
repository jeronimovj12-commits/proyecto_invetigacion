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

# Importa APIRouter, HTTPException, Response desde fastapi para usar esas definiciones.
from fastapi import APIRouter, HTTPException, Response

# Importa (AreaConocimiento, desde models.area_conocimiento para usar esas definiciones.
from models.area_conocimiento import (AreaConocimiento,
                                      # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                                      AreaConocimientoActualizar,
                                      # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                                      AreaConocimientoReemplazo)
# Importa crear_servicio_area_conocimiento desde servicios.ensamblador para usar esas definiciones.
from servicios.ensamblador import crear_servicio_area_conocimiento

# Crea el router FastAPI que agrupa las rutas de este modulo.
router = APIRouter(prefix="/api", tags=["area_conocimiento"])

# Asigna a TABLA el valor calculado a la derecha.
TABLA = "area_conocimiento"


# Define la funcion _respuesta_publica con los parametros declarados; su bloque realiza esta operacion.
def _respuesta_publica(fila: dict) -> dict:
    # Ejecuta la instruccion indicada dentro del flujo actual.
    """Expone el JSON del contrato sin filtrar los nombres de PostgreSQL."""
    # Devuelve al llamador el resultado de la expresion indicada.
    return {
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        "id": fila["id"],
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        "granArea": fila["gran_area"],
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        "area": fila["area"],
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        "disciplina": fila["disciplina"],
    # Cierra la estructura abierta en las lineas anteriores.
    }


# Define la funcion _error con los parametros declarados; su bloque realiza esta operacion.
def _error(estado: int, mensaje: str, detalle: str) -> HTTPException:
    # Devuelve al llamador el resultado de la expresion indicada.
    return HTTPException(
        # Asigna a status_code el valor calculado a la derecha.
        status_code=estado,
        # Asigna a detail el valor calculado a la derecha.
        detail={"estado": estado, "mensaje": mensaje, "detalle": detalle},
    # Cierra la estructura abierta en las lineas anteriores.
    )


# ----------------------------------------------------------------------
# GET /api/area_conocimiento — Listar (query string ?limite=N)
# ----------------------------------------------------------------------
# Aplica @router.get a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@router.get(f"/{TABLA}")
# Define la funcion listar con los parametros declarados; su bloque realiza esta operacion.
async def listar(limite: int = 1000):
    # Inicia un bloque cuya excepcion se manejara en los except siguientes.
    try:
        # Asigna a servicio el valor calculado a la derecha.
        servicio = crear_servicio_area_conocimiento()
        # Asigna a filas el valor calculado a la derecha.
        filas = await servicio.listar(limite)
        # Ejecuta el bloque siguiente solo cuando se cumple: not filas.
        if not filas:
            # 204: éxito SIN contenido — "tabla vacía" no es un error.
            # Devuelve al llamador el resultado de la expresion indicada.
            return Response(status_code=204)
        # Devuelve al llamador el resultado de la expresion indicada.
        return {"tabla": TABLA, "limite": limite,
                # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                "total": len(filas), "datos": [_respuesta_publica(fila) for fila in filas]}
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except ValueError as excepcion:
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise _error(400, "Parámetros inválidos.", str(excepcion))
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except Exception as excepcion:
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise _error(500, "Error al consultar las áreas de conocimiento.",
                     # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                     str(excepcion))


# ----------------------------------------------------------------------
# GET /api/area_conocimiento/{id_area} — Obtener una
# ----------------------------------------------------------------------
# Aplica @router.get a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@router.get(f"/{TABLA}/{{id_area}}")
# Define la funcion obtener con los parametros declarados; su bloque realiza esta operacion.
async def obtener(id_area: str):
    # Inicia un bloque cuya excepcion se manejara en los except siguientes.
    try:
        # Asigna a servicio el valor calculado a la derecha.
        servicio = crear_servicio_area_conocimiento()
        # Devuelve al llamador el resultado de la expresion indicada.
        return _respuesta_publica(await servicio.obtener(id_area))
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except ValueError as excepcion:
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise _error(400, "Parámetros inválidos.", str(excepcion))
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except LookupError as excepcion:
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise _error(404, "Área de conocimiento no encontrada.", str(excepcion))
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except Exception as excepcion:
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise _error(500, "Error al consultar el área de conocimiento.",
                     # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                     str(excepcion))


# ----------------------------------------------------------------------
# POST /api/area_conocimiento — Crear
# ----------------------------------------------------------------------
# Aplica @router.post a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@router.post(f"/{TABLA}")
# Define la funcion crear con los parametros declarados; su bloque realiza esta operacion.
async def crear(area: AreaConocimiento):
    # Inicia un bloque cuya excepcion se manejara en los except siguientes.
    try:
        # Asigna a servicio el valor calculado a la derecha.
        servicio = crear_servicio_area_conocimiento()
        # Espera que termine la operacion asincronica antes de continuar.
        await servicio.crear(area.model_dump())
        # Devuelve al llamador el resultado de la expresion indicada.
        return {"estado": 200, "mensaje": "Área de conocimiento creada exitosamente."}
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except ValueError as excepcion:
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise _error(400, "Datos inválidos.", str(excepcion))
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except Exception as excepcion:
        # Aquí cae la llave duplicada: la defiende la base, no la API.
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise _error(500, "No se pudo crear el área de conocimiento.",
                     # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                     str(excepcion))


# ----------------------------------------------------------------------
# PUT /api/area_conocimiento/{id_area} — Reemplazo COMPLETO
# ----------------------------------------------------------------------
# Aplica @router.put a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@router.put(f"/{TABLA}/{{id_area}}")
# Define la funcion reemplazar con los parametros declarados; su bloque realiza esta operacion.
async def reemplazar(id_area: str, area: AreaConocimientoReemplazo):
    # Inicia un bloque cuya excepcion se manejara en los except siguientes.
    try:
        # Asigna a servicio el valor calculado a la derecha.
        servicio = crear_servicio_area_conocimiento()
        # PUT: el modelo exige TODOS los campos → se escriben los tres.
        # Asigna a filas el valor calculado a la derecha.
        filas = await servicio.actualizar(id_area, area.model_dump())
        # Devuelve al llamador el resultado de la expresion indicada.
        return {"estado": 200, "mensaje": "Área de conocimiento reemplazada.",
                # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                "filasAfectadas": filas}
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except ValueError as excepcion:
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise _error(400, "Parámetros inválidos.", str(excepcion))
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except LookupError as excepcion:
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise _error(404, "Área de conocimiento no encontrada.", str(excepcion))
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except Exception as excepcion:
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise _error(500, "No se pudo reemplazar el área de conocimiento.",
                     # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                     str(excepcion))


# ----------------------------------------------------------------------
# PATCH /api/area_conocimiento/{id_area} — Actualización PARCIAL
# ----------------------------------------------------------------------
# Aplica @router.patch a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@router.patch(f"/{TABLA}/{{id_area}}")
# Define la funcion actualizar con los parametros declarados; su bloque realiza esta operacion.
async def actualizar(id_area: str, area: AreaConocimientoActualizar):
    # Inicia un bloque cuya excepcion se manejara en los except siguientes.
    try:
        # Asigna a servicio el valor calculado a la derecha.
        servicio = crear_servicio_area_conocimiento()
        # PATCH: solo los campos que el cliente envió. Si no envió ninguno,
        # el servicio responde con ValueError → 400.
        # Asigna a datos el valor calculado a la derecha.
        datos = area.model_dump(exclude_none=True)
        # Asigna a filas el valor calculado a la derecha.
        filas = await servicio.actualizar(id_area, datos)
        # Devuelve al llamador el resultado de la expresion indicada.
        return {"estado": 200, "mensaje": "Área de conocimiento actualizada.",
                # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                "filasAfectadas": filas}
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except ValueError as excepcion:
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise _error(400, "Parámetros inválidos.", str(excepcion))
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except LookupError as excepcion:
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise _error(404, "Área de conocimiento no encontrada.", str(excepcion))
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except Exception as excepcion:
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise _error(500, "No se pudo actualizar el área de conocimiento.",
                     # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                     str(excepcion))


# ----------------------------------------------------------------------
# DELETE /api/area_conocimiento/{id_area} — Eliminar (LÓGICO)
# ----------------------------------------------------------------------
# Aplica @router.delete a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@router.delete(f"/{TABLA}/{{id_area}}")
# Define la funcion eliminar con los parametros declarados; su bloque realiza esta operacion.
async def eliminar(id_area: str):
    # Inicia un bloque cuya excepcion se manejara en los except siguientes.
    try:
        # Asigna a servicio el valor calculado a la derecha.
        servicio = crear_servicio_area_conocimiento()
        # Asigna a filas el valor calculado a la derecha.
        filas = await servicio.eliminar(id_area)
        # Devuelve al llamador el resultado de la expresion indicada.
        return {"estado": 200, "mensaje": "Área de conocimiento eliminada.",
                # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                "filasAfectadas": filas}
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except ValueError as excepcion:
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise _error(400, "Parámetros inválidos.", str(excepcion))
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except LookupError as excepcion:
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise _error(404, "Área de conocimiento no encontrada.", str(excepcion))
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except Exception as excepcion:
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise _error(500, "No se pudo eliminar el área de conocimiento.",
                     # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                     str(excepcion))
