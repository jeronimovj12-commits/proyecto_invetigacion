"""Composición HTTP; el lifespan siembra identidad y roles antes de aceptar peticiones."""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from controllers.aa_linea_controller import router as router_aa_linea
from controllers.ac_linea_controller import router as router_ac_linea
from controllers.area_aplicacion_controller import router as router_area_aplicacion
from controllers.area_conocimiento_controller import router as router_area_conocimiento
from controllers.docente_controller import router as router_docentes
from controllers.grupo_investigacion_controller import router as router_grupos
from controllers.grupo_linea_controller import router as router_grupo_linea
from controllers.linea_investigacion_controller import router as router_linea_investigacion
from controllers.login_controller import router as router_login
from controllers.ods_linea_controller import router as router_ods_linea
from controllers.objetivo_desarrollo_sostenible_controller import router as router_objetivos
from controllers.participa_grupo_controller import router as router_participa_grupo
from controllers.participa_semillero_controller import router as router_participa_semillero
from controllers.rol_controller import router as router_roles
from controllers.rol_usuario_controller import router as router_rol_usuario
from controllers.usuario_controller import router as router_usuarios
from controllers.semillero_controller import router as router_semilleros
from controllers.semillero_linea_controller import router as router_semillero_linea
from controllers.termino_clave_controller import router as router_terminos
from controllers.universidad_controller import router as router_universidades
from seguridad.arranque import sembrar_datos_iniciales


# Sembrar antes de aceptar solicitudes evita que un primer login compita con la inicialización de roles.
@asynccontextmanager
async def lifespan(_aplicacion: FastAPI):
    await sembrar_datos_iniciales()
    yield

app = FastAPI(
    title="API Investigación",
    description="Módulo de Investigación — versión 3, autenticación y RBAC.",
    version="v3",
    lifespan=lifespan,
)

app.include_router(router_login)
for router in (
    router_area_conocimiento,
    router_objetivos,
    router_area_aplicacion,
    router_terminos,
    router_universidades,
    router_linea_investigacion,
    router_docentes,
    router_grupos,
    router_semilleros,
    router_participa_grupo,
    router_participa_semillero,
    router_grupo_linea,
    router_semillero_linea,
    router_ac_linea,
    router_ods_linea,
    router_aa_linea,
):
    app.include_router(router)
for router in (router_roles, router_usuarios, router_rol_usuario):
    app.include_router(router)


def _mensaje_validacion(error: dict) -> str:
    ubicacion = error.get("loc", ())
    campo = str(ubicacion[-1]) if ubicacion else "solicitud"
    etiquetas = {"gran_area": "granArea", "termino_ingles": "terminoIngles"}
    campo = etiquetas.get(campo, campo)
    tipo = error.get("type")
    if tipo == "missing":
        return f"El campo {campo} es obligatorio."
    if tipo in {"string_too_long", "string_too_short"}:
        return f"El campo {campo} no cumple la longitud permitida."
    if tipo in {"int_parsing", "int_type"}:
        return f"El campo {campo} debe ser un número entero."
    if tipo == "extra_forbidden":
        return f"El campo {campo} no está permitido."
    return f"El campo {campo} no es válido."


@app.exception_handler(RequestValidationError)
async def error_validacion(_solicitud: Request, excepcion: RequestValidationError):
    # Un sobre propio y en español evita filtrar el texto interno de Pydantic a clientes distintos.
    return JSONResponse(
        status_code=422,
        content={
            "estado": 422,
            "mensaje": "Datos inválidos.",
            "detalle": "Error de validación en los campos enviados.",
            "errores": [_mensaje_validacion(error) for error in excepcion.errors()],
        },
    )


@app.exception_handler(StarletteHTTPException)
async def error_http(_solicitud: Request, excepcion: StarletteHTTPException):
    contenido = excepcion.detail
    if not isinstance(contenido, dict) or "estado" not in contenido:
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
    return {"mensaje": "API Investigación — v3", "version": "v3", "contratos": "/docs"}
