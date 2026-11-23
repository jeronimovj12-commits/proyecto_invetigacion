"""
main.py — El arranque de la API del módulo Investigación.

Arma la aplicación y registra el router. Nada más: la lógica vive en las
capas, no aquí.

Arranque:  uvicorn main:app --port 8025 --reload
Contratos: http://localhost:8025/docs
"""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from controllers.area_conocimiento_controller import router as router_area

app = FastAPI(
    title="API Investigación",
    description="Módulo de Investigación — versión 1: el catálogo de "
                "áreas de conocimiento.",
    version="v1",
)

app.include_router(router_area)


def _mensaje_validacion(error: dict) -> str:
    """Traduce los errores de Pydantic al sobre definido por el proyecto."""
    ubicacion = error.get("loc", ())
    campo = str(ubicacion[-1]) if ubicacion else "solicitud"
    mensaje = error.get("msg", "dato inválido")

    if error.get("type") == "missing":
        return f"El campo {campo} es obligatorio."
    if error.get("type") == "string_too_long":
        return f"El campo {campo} supera la longitud permitida."
    if error.get("type") == "string_too_short":
        return f"El campo {campo} no puede estar vacío."
    if error.get("type") == "string_type":
        return f"El campo {campo} debe ser texto."
    if error.get("type") == "int_parsing":
        return "El parámetro limite debe ser un número entero."
    return f"El campo {campo} no es válido: {mensaje}."


@app.exception_handler(RequestValidationError)
async def error_validacion(_solicitud: Request, excepcion: RequestValidationError):
    errores = [_mensaje_validacion(error) for error in excepcion.errors()]
    return JSONResponse(
        status_code=422,
        content={
            "estado": 422,
            "mensaje": "Datos inválidos.",
            "detalle": "La petición no cumple el contrato.",
            "errores": errores,
        },
    )


@app.exception_handler(StarletteHTTPException)
async def error_http(_solicitud: Request, excepcion: StarletteHTTPException):
    """Quita el envoltorio estándar `detail` para respetar el sobre común."""
    if isinstance(excepcion.detail, dict) and "estado" in excepcion.detail:
        contenido = excepcion.detail
    else:
        contenido = {
            "estado": excepcion.status_code,
            "mensaje": "Solicitud no encontrada." if excepcion.status_code == 404 else "Error en la solicitud.",
            "detalle": str(excepcion.detail),
        }
    return JSONResponse(
        status_code=excepcion.status_code,
        content=contenido,
        headers=excepcion.headers,
    )


@app.get("/")
async def diagnostico():
    """Responde sin tocar la base: sirve para saber si la API está viva."""
    return {"mensaje": "API Investigación — módulo de áreas de conocimiento",
            "version": "v1", "contratos": "/docs"}
