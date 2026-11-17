# Ejecuta la instruccion indicada dentro del flujo actual.
"""Controlador HTTP: registra rutas, llama a servicios y convierte sus resultados o errores en respuestas HTTP."""
# Importa APIRouter, HTTPException, Response desde fastapi para usar esas definiciones.
from fastapi import APIRouter, HTTPException, Response
# Importa ParticipaSemillero, ParticipaSemilleroReemplazo, ParticipaSemilleroActualizar desde models.participa_semillero para usar esas definiciones.
from models.participa_semillero import ParticipaSemillero, ParticipaSemilleroReemplazo, ParticipaSemilleroActualizar
# Importa crear_servicio_participa_semillero desde servicios.ensamblador para usar esas definiciones.
from servicios.ensamblador import crear_servicio_participa_semillero

# Crea el router FastAPI que agrupa las rutas de este modulo.
router = APIRouter(prefix="/api/participa_semillero", tags=["participa_semillero"])

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
        filas = await crear_servicio_participa_semillero().listar(limite)
        # Ejecuta el bloque siguiente solo cuando se cumple: not filas.
        if not filas:
            # Devuelve al llamador el resultado de la expresion indicada.
            return Response(status_code=204)
        # Devuelve al llamador el resultado de la expresion indicada.
        return {"tabla": "participa_semillero", "limite": limite, "total": len(filas), "datos": filas}
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except Exception as excepcion:
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise _error(excepcion)

# Aplica @router.get a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@router.get("/{docente}/{semillero}")
# Define la funcion obtener con los parametros declarados; su bloque realiza esta operacion.
async def obtener(docente: int, semillero: int):
    # Inicia un bloque cuya excepcion se manejara en los except siguientes.
    try:
        # Devuelve al llamador el resultado de la expresion indicada.
        return await crear_servicio_participa_semillero().obtener({"docente": docente, "semillero": semillero})
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except Exception as excepcion:
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise _error(excepcion)

# Aplica @router.post a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@router.post("")
# Define la funcion crear con los parametros declarados; su bloque realiza esta operacion.
async def crear(datos: ParticipaSemillero):
    # Inicia un bloque cuya excepcion se manejara en los except siguientes.
    try:
        # Espera que termine la operacion asincronica antes de continuar.
        await crear_servicio_participa_semillero().crear(datos.model_dump())
        # Devuelve al llamador el resultado de la expresion indicada.
        return {"estado": 200, "mensaje": "Registro creado."}
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except Exception as excepcion:
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise _error(excepcion)

# Aplica @router.put a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@router.put("/{docente}/{semillero}")
# Define la funcion reemplazar con los parametros declarados; su bloque realiza esta operacion.
async def reemplazar(docente: int, semillero: int, datos: ParticipaSemilleroReemplazo):
    # Inicia un bloque cuya excepcion se manejara en los except siguientes.
    try:
        # Asigna a filas el valor calculado a la derecha.
        filas = await crear_servicio_participa_semillero().actualizar({"docente": docente, "semillero": semillero}, datos.model_dump())
        # Devuelve al llamador el resultado de la expresion indicada.
        return {"estado": 200, "mensaje": "Registro actualizado.", "filasAfectadas": filas}
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except Exception as excepcion:
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise _error(excepcion)

# Aplica @router.patch a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@router.patch("/{docente}/{semillero}")
# Define la funcion actualizar con los parametros declarados; su bloque realiza esta operacion.
async def actualizar(docente: int, semillero: int, datos: ParticipaSemilleroActualizar):
    # Inicia un bloque cuya excepcion se manejara en los except siguientes.
    try:
        # Asigna a filas el valor calculado a la derecha.
        filas = await crear_servicio_participa_semillero().actualizar({"docente": docente, "semillero": semillero}, datos.model_dump(exclude_unset=True))
        # Devuelve al llamador el resultado de la expresion indicada.
        return {"estado": 200, "mensaje": "Registro actualizado.", "filasAfectadas": filas}
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except Exception as excepcion:
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise _error(excepcion)

# Aplica @router.delete a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@router.delete("/{docente}/{semillero}")
# Define la funcion eliminar con los parametros declarados; su bloque realiza esta operacion.
async def eliminar(docente: int, semillero: int):
    # Inicia un bloque cuya excepcion se manejara en los except siguientes.
    try:
        # Asigna a filas el valor calculado a la derecha.
        filas = await crear_servicio_participa_semillero().eliminar({"docente": docente, "semillero": semillero})
        # Devuelve al llamador el resultado de la expresion indicada.
        return {"estado": 200, "mensaje": "Registro retirado.", "filasAfectadas": filas}
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except Exception as excepcion:
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise _error(excepcion)
