"""
main.py — El arranque de la API del módulo Investigación.

Arma la aplicación y registra el router. Nada más: la lógica vive en las
capas, no aquí.

Arranque:  uvicorn main:app --port 8025 --reload
Contratos: http://localhost:8025/docs
"""

import os

# Importa FastAPI, Request desde fastapi para usar esas definiciones.
from fastapi import FastAPI, Request
# Importa RequestValidationError desde fastapi.exceptions para usar esas definiciones.
from fastapi.exceptions import RequestValidationError
# Importa JSONResponse desde fastapi.responses para usar esas definiciones.
from fastapi.responses import JSONResponse
# Importa HTTPException as StarletteHTTPException desde starlette.exceptions para usar esas definiciones.
from starlette.exceptions import HTTPException as StarletteHTTPException

# Importa router as router_area desde controllers.area_conocimiento_controller para usar esas definiciones.
from controllers.area_conocimiento_controller import router as router_area

# Crea o configura la aplicacion web indicada por la expresion.
app = FastAPI(
    # Asigna a title el valor calculado a la derecha.
    title="API Investigación",
    # Asigna a description el valor calculado a la derecha.
    description="Módulo Investigación — versión 2: relaciones y catálogos.",
    # Asigna a version el valor calculado a la derecha.
    version="v2",
    docs_url=None if os.environ.get("RENDER_PUBLIC_API") == "1" else "/docs",
    redoc_url=None if os.environ.get("RENDER_PUBLIC_API") == "1" else "/redoc",
    openapi_url=None if os.environ.get("RENDER_PUBLIC_API") == "1" else "/openapi.json",
# Cierra la estructura abierta en las lineas anteriores.
)

# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
app.include_router(router_area)


# Define la funcion _mensaje_validacion con los parametros declarados; su bloque realiza esta operacion.
def _mensaje_validacion(error: dict) -> str:
    # Ejecuta la instruccion indicada dentro del flujo actual.
    """Traduce los errores de Pydantic al sobre definido por el proyecto."""
    # Asigna a ubicacion el valor calculado a la derecha.
    ubicacion = error.get("loc", ())
    # Asigna a campo el valor calculado a la derecha.
    campo = str(ubicacion[-1]) if ubicacion else "solicitud"
    # Asigna a mensaje el valor calculado a la derecha.
    mensaje = error.get("msg", "dato inválido")

    # Ejecuta el bloque siguiente solo cuando se cumple: error.get("type") == "missing".
    if error.get("type") == "missing":
        # Devuelve al llamador el resultado de la expresion indicada.
        return f"El campo {campo} es obligatorio."
    # Ejecuta el bloque siguiente solo cuando se cumple: error.get("type") == "string_too_long".
    if error.get("type") == "string_too_long":
        # Devuelve al llamador el resultado de la expresion indicada.
        return f"El campo {campo} supera la longitud permitida."
    # Ejecuta el bloque siguiente solo cuando se cumple: error.get("type") == "string_too_short".
    if error.get("type") == "string_too_short":
        # Devuelve al llamador el resultado de la expresion indicada.
        return f"El campo {campo} no puede estar vacío."
    # Ejecuta el bloque siguiente solo cuando se cumple: error.get("type") == "string_type".
    if error.get("type") == "string_type":
        # Devuelve al llamador el resultado de la expresion indicada.
        return f"El campo {campo} debe ser texto."
    # Ejecuta el bloque siguiente solo cuando se cumple: error.get("type") == "int_parsing".
    if error.get("type") == "int_parsing":
        # Devuelve al llamador el resultado de la expresion indicada.
        return f"El campo {campo} debe ser un número entero."
    # Ejecuta el bloque siguiente solo cuando se cumple: error.get("type") == "extra_forbidden".
    if error.get("type") == "extra_forbidden":
        # Devuelve al llamador el resultado de la expresion indicada.
        return f"El campo {campo} no está permitido."
    # Ejecuta el bloque siguiente solo cuando se cumple: error.get("type", "").startswith("date").
    if error.get("type", "").startswith("date"):
        # Devuelve al llamador el resultado de la expresion indicada.
        return f"El campo {campo} debe ser una fecha válida."
    # Ejecuta el bloque siguiente solo cuando se cumple: error.get("type") == "value_error".
    if error.get("type") == "value_error":
        # Devuelve al llamador el resultado de la expresion indicada.
        return "Los campos enviados no admiten esos valores."
    # Devuelve al llamador el resultado de la expresion indicada.
    return f"El campo {campo} no es válido."


# Aplica @app.exception_handler a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.exception_handler(RequestValidationError)
# Define la funcion error_validacion con los parametros declarados; su bloque realiza esta operacion.
async def error_validacion(_solicitud: Request, excepcion: RequestValidationError):
    # Asigna a errores el valor calculado a la derecha.
    errores = [_mensaje_validacion(error) for error in excepcion.errors()]
    # Devuelve al llamador el resultado de la expresion indicada.
    return JSONResponse(
        # Asigna a status_code el valor calculado a la derecha.
        status_code=422,
        # Asigna a content el valor calculado a la derecha.
        content={
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            "estado": 422,
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            "mensaje": "Datos inválidos.",
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            "detalle": "La petición no cumple el contrato.",
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            "errores": errores,
        # Cierra la estructura abierta en las lineas anteriores.
        },
    # Cierra la estructura abierta en las lineas anteriores.
    )


# Aplica @app.exception_handler a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.exception_handler(StarletteHTTPException)
# Define la funcion error_http con los parametros declarados; su bloque realiza esta operacion.
async def error_http(_solicitud: Request, excepcion: StarletteHTTPException):
    # Ejecuta la instruccion indicada dentro del flujo actual.
    """Quita el envoltorio estándar `detail` para respetar el sobre común."""
    # Ejecuta el bloque siguiente solo cuando se cumple: isinstance(excepcion.detail, dict) and "estado" in excepcion.detail.
    if isinstance(excepcion.detail, dict) and "estado" in excepcion.detail:
        # Asigna a contenido el valor calculado a la derecha.
        contenido = excepcion.detail
    # Define el caso alternativo cuando las condiciones anteriores no se cumplen.
    else:
        # Asigna a contenido el valor calculado a la derecha.
        contenido = {
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            "estado": excepcion.status_code,
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            "mensaje": "Solicitud no encontrada." if excepcion.status_code == 404 else "Error en la solicitud.",
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            "detalle": str(excepcion.detail),
        # Cierra la estructura abierta en las lineas anteriores.
        }
    # Devuelve al llamador el resultado de la expresion indicada.
    return JSONResponse(
        # Asigna a status_code el valor calculado a la derecha.
        status_code=excepcion.status_code,
        # Asigna a content el valor calculado a la derecha.
        content=contenido,
        # Asigna a headers el valor calculado a la derecha.
        headers=excepcion.headers,
    # Cierra la estructura abierta en las lineas anteriores.
    )


# Aplica @app.get a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.get("/")
# Define la funcion diagnostico con los parametros declarados; su bloque realiza esta operacion.
async def diagnostico():
    # Ejecuta la instruccion indicada dentro del flujo actual.
    """Responde sin tocar la base: sirve para saber si la API está viva."""
    # Devuelve al llamador el resultado de la expresion indicada.
    return {"mensaje": "API Investigación — catálogos y relaciones",
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            "version": app.version, "contratos": "/docs"}

# Importa router as router_docente desde controllers.docente_controller para usar esas definiciones.
from controllers.docente_controller import router as router_docente
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
app.include_router(router_docente)

# Importa router as router_grupo_investigacion desde controllers.grupo_investigacion_controller para usar esas definiciones.
from controllers.grupo_investigacion_controller import router as router_grupo_investigacion
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
app.include_router(router_grupo_investigacion)

# Importa router as router_semillero desde controllers.semillero_controller para usar esas definiciones.
from controllers.semillero_controller import router as router_semillero
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
app.include_router(router_semillero)

# Importa router as router_participa_semillero desde controllers.participa_semillero_controller para usar esas definiciones.
from controllers.participa_semillero_controller import router as router_participa_semillero
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
app.include_router(router_participa_semillero)

# Importa router as router_participa_grupo desde controllers.participa_grupo_controller para usar esas definiciones.
from controllers.participa_grupo_controller import router as router_participa_grupo
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
app.include_router(router_participa_grupo)

# Importa router as router_semillero_linea desde controllers.semillero_linea_controller para usar esas definiciones.
from controllers.semillero_linea_controller import router as router_semillero_linea
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
app.include_router(router_semillero_linea)

# Importa router as router_grupo_linea desde controllers.grupo_linea_controller para usar esas definiciones.
from controllers.grupo_linea_controller import router as router_grupo_linea
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
app.include_router(router_grupo_linea)

# Importa router as router_ac_linea desde controllers.ac_linea_controller para usar esas definiciones.
from controllers.ac_linea_controller import router as router_ac_linea
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
app.include_router(router_ac_linea)

# Importa router as router_ods_linea desde controllers.ods_linea_controller para usar esas definiciones.
from controllers.ods_linea_controller import router as router_ods_linea
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
app.include_router(router_ods_linea)

# Importa router as router_aa_linea desde controllers.aa_linea_controller para usar esas definiciones.
from controllers.aa_linea_controller import router as router_aa_linea
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
app.include_router(router_aa_linea)

# Importa router as router_universidad desde controllers.universidad_controller para usar esas definiciones.
from controllers.universidad_controller import router as router_universidad
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
app.include_router(router_universidad)

# Importa router as router_linea_investigacion desde controllers.linea_investigacion_controller para usar esas definiciones.
from controllers.linea_investigacion_controller import router as router_linea_investigacion
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
app.include_router(router_linea_investigacion)

# Importa router as router_objetivo_desarrollo_sostenible desde controllers.objetivo_desarrollo_sostenible_controller para usar esas definiciones.
from controllers.objetivo_desarrollo_sostenible_controller import router as router_objetivo_desarrollo_sostenible
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
app.include_router(router_objetivo_desarrollo_sostenible)

# Importa router as router_area_aplicacion desde controllers.area_aplicacion_controller para usar esas definiciones.
from controllers.area_aplicacion_controller import router as router_area_aplicacion
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
app.include_router(router_area_aplicacion)
