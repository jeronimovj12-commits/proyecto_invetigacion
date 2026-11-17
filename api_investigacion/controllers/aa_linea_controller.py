# Ejecuta la instruccion indicada dentro del flujo actual.
"""Controlador HTTP: registra rutas, llama a servicios y convierte sus resultados o errores en respuestas HTTP."""
# Importa APIRouter, HTTPException, Response desde fastapi para usar esas definiciones.
from fastapi import APIRouter, HTTPException, Response
# Importa AaLinea, AaLineaReemplazo, AaLineaActualizar desde models.aa_linea para usar esas definiciones.
from models.aa_linea import AaLinea, AaLineaReemplazo, AaLineaActualizar
# Importa crear_servicio_aa_linea desde servicios.ensamblador para usar esas definiciones.
from servicios.ensamblador import crear_servicio_aa_linea

# Crea el router FastAPI que agrupa las rutas de este modulo.
router = APIRouter(prefix="/api/aa_linea", tags=["aa_linea"])

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
        filas = await crear_servicio_aa_linea().listar(limite)
        # Ejecuta el bloque siguiente solo cuando se cumple: not filas.
        if not filas:
            # Devuelve al llamador el resultado de la expresion indicada.
            return Response(status_code=204)
        # Devuelve al llamador el resultado de la expresion indicada.
        return {"tabla": "aa_linea", "limite": limite, "total": len(filas), "datos": filas}
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except Exception as excepcion:
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise _error(excepcion)

# Aplica @router.get a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@router.get("/{area_aplicacion}/{linea_investigacion}")
# Define la funcion obtener con los parametros declarados; su bloque realiza esta operacion.
async def obtener(area_aplicacion: int, linea_investigacion: int):
    # Inicia un bloque cuya excepcion se manejara en los except siguientes.
    try:
        # Devuelve al llamador el resultado de la expresion indicada.
        return await crear_servicio_aa_linea().obtener({"area_aplicacion": area_aplicacion, "linea_investigacion": linea_investigacion})
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except Exception as excepcion:
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise _error(excepcion)

# Aplica @router.post a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@router.post("")
# Define la funcion crear con los parametros declarados; su bloque realiza esta operacion.
async def crear(datos: AaLinea):
    # Inicia un bloque cuya excepcion se manejara en los except siguientes.
    try:
        # Espera que termine la operacion asincronica antes de continuar.
        await crear_servicio_aa_linea().crear(datos.model_dump())
        # Devuelve al llamador el resultado de la expresion indicada.
        return {"estado": 200, "mensaje": "Registro creado."}
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except Exception as excepcion:
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise _error(excepcion)

# Aplica @router.put a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@router.put("/{area_aplicacion}/{linea_investigacion}")
# Define la funcion reemplazar con los parametros declarados; su bloque realiza esta operacion.
async def reemplazar(area_aplicacion: int, linea_investigacion: int, datos: AaLineaReemplazo):
    # Inicia un bloque cuya excepcion se manejara en los except siguientes.
    try:
        # Asigna a filas el valor calculado a la derecha.
        filas = await crear_servicio_aa_linea().actualizar({"area_aplicacion": area_aplicacion, "linea_investigacion": linea_investigacion}, datos.model_dump())
        # Devuelve al llamador el resultado de la expresion indicada.
        return {"estado": 200, "mensaje": "Registro actualizado.", "filasAfectadas": filas}
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except Exception as excepcion:
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise _error(excepcion)

# Aplica @router.patch a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@router.patch("/{area_aplicacion}/{linea_investigacion}")
# Define la funcion actualizar con los parametros declarados; su bloque realiza esta operacion.
async def actualizar(area_aplicacion: int, linea_investigacion: int, datos: AaLineaActualizar):
    # Inicia un bloque cuya excepcion se manejara en los except siguientes.
    try:
        # Asigna a filas el valor calculado a la derecha.
        filas = await crear_servicio_aa_linea().actualizar({"area_aplicacion": area_aplicacion, "linea_investigacion": linea_investigacion}, datos.model_dump(exclude_unset=True))
        # Devuelve al llamador el resultado de la expresion indicada.
        return {"estado": 200, "mensaje": "Registro actualizado.", "filasAfectadas": filas}
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except Exception as excepcion:
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise _error(excepcion)

# Aplica @router.delete a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@router.delete("/{area_aplicacion}/{linea_investigacion}")
# Define la funcion eliminar con los parametros declarados; su bloque realiza esta operacion.
async def eliminar(area_aplicacion: int, linea_investigacion: int):
    # Inicia un bloque cuya excepcion se manejara en los except siguientes.
    try:
        # Asigna a filas el valor calculado a la derecha.
        filas = await crear_servicio_aa_linea().eliminar({"area_aplicacion": area_aplicacion, "linea_investigacion": linea_investigacion})
        # Devuelve al llamador el resultado de la expresion indicada.
        return {"estado": 200, "mensaje": "Registro retirado.", "filasAfectadas": filas}
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except Exception as excepcion:
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise _error(excepcion)
