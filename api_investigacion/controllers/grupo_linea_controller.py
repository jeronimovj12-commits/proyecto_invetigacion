# Ejecuta la instruccion indicada dentro del flujo actual.
"""Controlador HTTP: registra rutas, llama a servicios y convierte sus resultados o errores en respuestas HTTP."""
# Importa APIRouter, HTTPException, Response desde fastapi para usar esas definiciones.
from fastapi import APIRouter, HTTPException, Response
# Importa GrupoLinea, GrupoLineaReemplazo, GrupoLineaActualizar desde models.grupo_linea para usar esas definiciones.
from models.grupo_linea import GrupoLinea, GrupoLineaReemplazo, GrupoLineaActualizar
# Importa crear_servicio_grupo_linea desde servicios.ensamblador para usar esas definiciones.
from servicios.ensamblador import crear_servicio_grupo_linea

# Crea el router FastAPI que agrupa las rutas de este modulo.
router = APIRouter(prefix="/api/grupo_linea", tags=["grupo_linea"])

# Define la funcion _error con los parametros declarados; su bloque realiza esta operacion.
def _error(excepcion):
    # Asigna a estado el valor calculado a la derecha.
    estado = 404 if isinstance(excepcion, LookupError) else 400 if isinstance(excepcion, ValueError) else 500
    # Devuelve al llamador el resultado de la expresion indicada.
    return HTTPException(status_code=estado, detail={"estado": estado, "mensaje": "No se pudo completar la operación.", "detalle": str(excepcion)})

# Aplica @router.get a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@router.get("")
# Define la funcion listar con los parametros declarados; su bloque realiza esta operacion.
async def listar(limite: int = 1000):
    # Inicia un bloque cuya excepcion se manejara en los except siguientes.
    try:
        # Asigna a filas el valor calculado a la derecha.
        filas = await crear_servicio_grupo_linea().listar(limite)
        # Ejecuta el bloque siguiente solo cuando se cumple: not filas.
        if not filas:
            # Devuelve al llamador el resultado de la expresion indicada.
            return Response(status_code=204)
        # Devuelve al llamador el resultado de la expresion indicada.
        return {"tabla": "grupo_linea", "limite": limite, "total": len(filas), "datos": filas}
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except Exception as excepcion:
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise _error(excepcion)

# Aplica @router.get a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@router.get("/{grupo_investigacion}/{linea_investigacion}")
# Define la funcion obtener con los parametros declarados; su bloque realiza esta operacion.
async def obtener(grupo_investigacion: int, linea_investigacion: int):
    # Inicia un bloque cuya excepcion se manejara en los except siguientes.
    try:
        # Devuelve al llamador el resultado de la expresion indicada.
        return await crear_servicio_grupo_linea().obtener({"grupo_investigacion": grupo_investigacion, "linea_investigacion": linea_investigacion})
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except Exception as excepcion:
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise _error(excepcion)

# Aplica @router.post a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@router.post("")
# Define la funcion crear con los parametros declarados; su bloque realiza esta operacion.
async def crear(datos: GrupoLinea):
    # Inicia un bloque cuya excepcion se manejara en los except siguientes.
    try:
        # Espera que termine la operacion asincronica antes de continuar.
        await crear_servicio_grupo_linea().crear(datos.model_dump())
        # Devuelve al llamador el resultado de la expresion indicada.
        return {"estado": 200, "mensaje": "Registro creado."}
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except Exception as excepcion:
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise _error(excepcion)

# Aplica @router.put a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@router.put("/{grupo_investigacion}/{linea_investigacion}")
# Define la funcion reemplazar con los parametros declarados; su bloque realiza esta operacion.
async def reemplazar(grupo_investigacion: int, linea_investigacion: int, datos: GrupoLineaReemplazo):
    # Inicia un bloque cuya excepcion se manejara en los except siguientes.
    try:
        # Asigna a filas el valor calculado a la derecha.
        filas = await crear_servicio_grupo_linea().actualizar({"grupo_investigacion": grupo_investigacion, "linea_investigacion": linea_investigacion}, datos.model_dump())
        # Devuelve al llamador el resultado de la expresion indicada.
        return {"estado": 200, "mensaje": "Registro actualizado.", "filasAfectadas": filas}
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except Exception as excepcion:
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise _error(excepcion)

# Aplica @router.patch a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@router.patch("/{grupo_investigacion}/{linea_investigacion}")
# Define la funcion actualizar con los parametros declarados; su bloque realiza esta operacion.
async def actualizar(grupo_investigacion: int, linea_investigacion: int, datos: GrupoLineaActualizar):
    # Inicia un bloque cuya excepcion se manejara en los except siguientes.
    try:
        # Asigna a filas el valor calculado a la derecha.
        filas = await crear_servicio_grupo_linea().actualizar({"grupo_investigacion": grupo_investigacion, "linea_investigacion": linea_investigacion}, datos.model_dump(exclude_unset=True))
        # Devuelve al llamador el resultado de la expresion indicada.
        return {"estado": 200, "mensaje": "Registro actualizado.", "filasAfectadas": filas}
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except Exception as excepcion:
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise _error(excepcion)

# Aplica @router.delete a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@router.delete("/{grupo_investigacion}/{linea_investigacion}")
# Define la funcion eliminar con los parametros declarados; su bloque realiza esta operacion.
async def eliminar(grupo_investigacion: int, linea_investigacion: int):
    # Inicia un bloque cuya excepcion se manejara en los except siguientes.
    try:
        # Asigna a filas el valor calculado a la derecha.
        filas = await crear_servicio_grupo_linea().eliminar({"grupo_investigacion": grupo_investigacion, "linea_investigacion": linea_investigacion})
        # Devuelve al llamador el resultado de la expresion indicada.
        return {"estado": 200, "mensaje": "Registro retirado.", "filasAfectadas": filas}
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except Exception as excepcion:
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise _error(excepcion)
