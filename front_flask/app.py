"""Vistas Flask sin acceso a datos; la interfaz conoce únicamente las respuestas HTTP en JSON."""

import os
from functools import wraps

from flask import (
    Flask, abort, flash, redirect, render_template, request, session, url_for,
)
from werkzeug.middleware.proxy_fix import ProxyFix

import cliente_api

app = Flask(__name__)
# ProxyFix reconstruye esquema y host confiables para que las cookies de sesión funcionen tras HTTPS.
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
# Una clave estable del entorno firma la sesión sin incrustar un secreto en el código.
app.secret_key = os.getenv("FLASK_SECRET_KEY")
if not app.secret_key:
    raise RuntimeError("La variable de entorno FLASK_SECRET_KEY es obligatoria.")

_ENDPOINTS_ADMIN = {
    "listar_usuarios", "crear_usuario", "editar_usuario", "eliminar_usuario",
    "listar_roles", "crear_rol", "editar_rol", "eliminar_rol",
    "listar_rol_usuario", "crear_rol_usuario", "eliminar_rol_usuario",
}


@app.context_processor
def exponer_contexto_sesion():
    usuario = session.get("usuario")
    roles = usuario.get("roles", []) if usuario else []
    return {
        "usuario_actual": usuario,
        "es_admin": "ADMIN" in roles,
        "puede_escribir": bool({"ADMIN", "INVESTIGADOR"}.intersection(roles)),
    }


@app.before_request
def proteger_vistas():
    if request.endpoint in {"static", "login", "logout"}:
        return None
    usuario = session.get("usuario")
    if not session.get("accessToken") or not usuario:
        return redirect(url_for("login", siguiente=request.path))

    roles = set(usuario.get("roles", []))
    if request.endpoint in _ENDPOINTS_ADMIN and "ADMIN" not in roles:
        abort(403)
    if request.method == "POST" and not roles.intersection({"ADMIN", "INVESTIGADOR"}):
        abort(403)
    if request.path.endswith(("/nuevo", "/editar")) and not roles.intersection(
        {"ADMIN", "INVESTIGADOR"}
    ):
        abort(403)
    return None

RECURSOS = {
    "areas_conocimiento": {
        "titulo": "Áreas de conocimiento", "clave": "id", "clave_entera": False,
        "endpoint_lista": "listar_areas_conocimiento",
        "endpoint_nuevo": "crear_area_conocimiento",
        "endpoint_editar": "editar_area_conocimiento",
        "endpoint_eliminar": "eliminar_area_conocimiento",
        "campos": [
            {"nombre": "id", "etiqueta": "Código", "maximo": 6, "clave": True},
            {"nombre": "gran_area", "etiqueta": "Gran área", "maximo": 60},
            {"nombre": "area", "etiqueta": "Área", "maximo": 60},
            {"nombre": "disciplina", "etiqueta": "Disciplina", "maximo": 150},
        ],
        "listar": cliente_api.listar_areas_conocimiento,
        "obtener": cliente_api.obtener_area_conocimiento,
        "crear": cliente_api.crear_area_conocimiento,
        "put": cliente_api.reemplazar_area_conocimiento,
        "patch": cliente_api.actualizar_area_conocimiento,
        "eliminar": cliente_api.eliminar_area_conocimiento,
    },
    "ods": {
        "titulo": "Objetivos de desarrollo sostenible", "clave": "id", "clave_entera": True,
        "endpoint_lista": "listar_ods", "endpoint_editar": "editar_ods",
        "endpoint_nuevo": "crear_ods",
        "endpoint_eliminar": "eliminar_ods",
        "campos": [
            {"nombre": "id", "etiqueta": "Número", "maximo": 10, "clave": True, "numero": True},
            {"nombre": "nombre", "etiqueta": "Nombre", "maximo": 60},
            {"nombre": "categoria", "etiqueta": "Categoría", "maximo": 45},
        ],
        "listar": cliente_api.listar_objetivos_desarrollo_sostenible,
        "obtener": cliente_api.obtener_objetivo_desarrollo_sostenible,
        "crear": cliente_api.crear_objetivo_desarrollo_sostenible,
        "put": cliente_api.reemplazar_objetivo_desarrollo_sostenible,
        "patch": cliente_api.actualizar_objetivo_desarrollo_sostenible,
        "eliminar": cliente_api.eliminar_objetivo_desarrollo_sostenible,
    },
    "areas_aplicacion": {
        "titulo": "Áreas de aplicación", "clave": "id", "clave_entera": True,
        "endpoint_lista": "listar_areas_aplicacion",
        "endpoint_nuevo": "crear_area_aplicacion",
        "endpoint_editar": "editar_area_aplicacion",
        "endpoint_eliminar": "eliminar_area_aplicacion",
        "campos": [
            {"nombre": "id", "etiqueta": "Número", "maximo": 10, "clave": True, "numero": True},
            {"nombre": "nombre", "etiqueta": "Nombre", "maximo": 150},
        ],
        "listar": cliente_api.listar_areas_aplicacion,
        "obtener": cliente_api.obtener_area_aplicacion,
        "crear": cliente_api.crear_area_aplicacion,
        "put": cliente_api.reemplazar_area_aplicacion,
        "patch": cliente_api.actualizar_area_aplicacion,
        "eliminar": cliente_api.eliminar_area_aplicacion,
    },
    "terminos_clave": {
        "titulo": "Términos clave", "clave": "termino", "clave_entera": False,
        "endpoint_lista": "listar_terminos_clave",
        "endpoint_nuevo": "crear_termino_clave",
        "endpoint_editar": "editar_termino_clave",
        "endpoint_eliminar": "eliminar_termino_clave",
        "campos": [
            {"nombre": "termino", "etiqueta": "Término", "maximo": 30, "clave": True},
            {"nombre": "termino_ingles", "etiqueta": "Término en inglés", "maximo": 30, "nullable": True},
        ],
        "listar": cliente_api.listar_terminos_clave,
        "obtener": cliente_api.obtener_termino_clave,
        "crear": cliente_api.crear_termino_clave,
        "put": cliente_api.reemplazar_termino_clave,
        "patch": cliente_api.actualizar_termino_clave,
        "eliminar": cliente_api.eliminar_termino_clave,
    },
    "universidades": {
        "titulo": "Universidades", "clave": "id", "clave_entera": True,
        "endpoint_lista": "listar_universidades",
        "endpoint_nuevo": "crear_universidad",
        "endpoint_editar": "editar_universidad",
        "endpoint_eliminar": "eliminar_universidad",
        "campos": [
            {"nombre": "id", "etiqueta": "Número", "maximo": 10, "clave": True, "numero": True},
            {"nombre": "nombre", "etiqueta": "Nombre", "maximo": 60},
            {"nombre": "tipo", "etiqueta": "Tipo", "maximo": 45},
            {"nombre": "ciudad", "etiqueta": "Ciudad", "maximo": 45},
        ],
        "listar": cliente_api.listar_universidades,
        "obtener": cliente_api.obtener_universidad,
        "crear": cliente_api.crear_universidad,
        "put": cliente_api.reemplazar_universidad,
        "patch": cliente_api.actualizar_universidad,
        "eliminar": cliente_api.eliminar_universidad,
    },
    "lineas_investigacion": {
        "titulo": "Líneas de investigación", "clave": "id", "clave_entera": True,
        "endpoint_lista": "listar_lineas_investigacion",
        "endpoint_nuevo": "crear_linea_investigacion",
        "endpoint_editar": "editar_linea_investigacion",
        "endpoint_eliminar": "eliminar_linea_investigacion",
        "campos": [
            {"nombre": "id", "etiqueta": "Número", "maximo": 10, "clave": True, "solo_salida": True},
            {"nombre": "nombre", "etiqueta": "Nombre", "maximo": 45},
            {"nombre": "descripcion", "etiqueta": "Descripción", "maximo": 256, "multilinea": True},
        ],
        "listar": cliente_api.listar_lineas_investigacion,
        "obtener": cliente_api.obtener_linea_investigacion,
        "crear": cliente_api.crear_linea_investigacion,
        "put": cliente_api.reemplazar_linea_investigacion,
        "patch": cliente_api.actualizar_linea_investigacion,
        "eliminar": cliente_api.eliminar_linea_investigacion,
    },
    "docentes": {
        "titulo": "Docentes", "clave": "cedula",
        "parametros_ruta": (("identificador", "cedula"),),
        "endpoint_lista": "listar_docentes", "endpoint_nuevo": "crear_docente",
        "endpoint_editar": "editar_docente", "endpoint_eliminar": "eliminar_docente",
        "campos": [
            {"nombre": "cedula", "etiqueta": "Cédula", "numero": True, "clave": True},
            {"nombre": "nombres", "etiqueta": "Nombres", "maximo": 60},
            {"nombre": "apellidos", "etiqueta": "Apellidos", "maximo": 60},
            {"nombre": "genero", "etiqueta": "Género", "maximo": 12},
            {"nombre": "cargo", "etiqueta": "Cargo", "maximo": 30},
            {"nombre": "fecha_nacimiento", "etiqueta": "Fecha de nacimiento", "tipo": "date"},
            {"nombre": "correo", "etiqueta": "Correo", "maximo": 70},
            {"nombre": "telefono", "etiqueta": "Teléfono", "maximo": 20},
            {"nombre": "url_cvlac", "etiqueta": "URL CVLAC", "maximo": 128},
            {"nombre": "fecha_actualizacion", "etiqueta": "Fecha de actualización", "tipo": "date"},
            {"nombre": "escalafon", "etiqueta": "Escalafón", "maximo": 45},
            {"nombre": "perfil", "etiqueta": "Perfil", "multilinea": True},
            {"nombre": "cat_minciencia", "etiqueta": "Categoría MinCiencias", "maximo": 45, "nullable": True},
            {"nombre": "conv_minciencia", "etiqueta": "Convocatoria MinCiencias", "maximo": 45},
            {"nombre": "nacionalidad", "etiqueta": "Nacionalidad", "maximo": 45},
            {
                "nombre": "linea_investigacion_principal", "etiqueta": "Línea de investigación principal",
                "nullable": True, "numero": True,
                "catalogo": {"listar": cliente_api.listar_lineas_investigacion, "valor": "id", "etiqueta": ("nombre",)},
            },
        ],
        "listar": cliente_api.listar_docentes, "obtener": cliente_api.obtener_docente,
        "crear": cliente_api.crear_docente, "put": cliente_api.reemplazar_docente,
        "patch": cliente_api.actualizar_docente, "eliminar": cliente_api.eliminar_docente,
    },
    "grupos_investigacion": {
        "titulo": "Grupos de investigación", "clave": "id",
        "parametros_ruta": (("identificador", "id"),),
        "endpoint_lista": "listar_grupos_investigacion", "endpoint_nuevo": "crear_grupo_investigacion",
        "endpoint_editar": "editar_grupo_investigacion", "endpoint_eliminar": "eliminar_grupo_investigacion",
        "campos": [
            {"nombre": "id", "etiqueta": "Código", "numero": True, "clave": True},
            {"nombre": "nombre", "etiqueta": "Nombre", "maximo": 60},
            {"nombre": "url_gruplac", "etiqueta": "URL GrupLAC", "maximo": 128, "nullable": True},
            {"nombre": "categoria", "etiqueta": "Categoría", "maximo": 10, "nullable": True},
            {"nombre": "convocatoria", "etiqueta": "Convocatoria", "maximo": 10, "nullable": True},
            {"nombre": "fecha_fundacion", "etiqueta": "Fecha de fundación", "tipo": "date"},
            {
                "nombre": "universidad", "etiqueta": "Universidad", "nullable": True, "numero": True,
                "catalogo": {"listar": cliente_api.listar_universidades, "valor": "id", "etiqueta": ("nombre",)},
            },
            {"nombre": "interno", "etiqueta": "¿Es interno?", "numero": True},
            {"nombre": "ambito", "etiqueta": "Ámbito", "maximo": 45},
        ],
        "listar": cliente_api.listar_grupos_investigacion, "obtener": cliente_api.obtener_grupo_investigacion,
        "crear": cliente_api.crear_grupo_investigacion, "put": cliente_api.reemplazar_grupo_investigacion,
        "patch": cliente_api.actualizar_grupo_investigacion, "eliminar": cliente_api.eliminar_grupo_investigacion,
    },
    "semilleros": {
        "titulo": "Semilleros", "clave": "id",
        "parametros_ruta": (("identificador", "id"),),
        "endpoint_lista": "listar_semilleros", "endpoint_nuevo": "crear_semillero",
        "endpoint_editar": "editar_semillero", "endpoint_eliminar": "eliminar_semillero",
        "campos": [
            {"nombre": "id", "etiqueta": "Código", "numero": True, "clave": True},
            {"nombre": "nombre", "etiqueta": "Nombre", "maximo": 60},
            {"nombre": "fecha_fundacion", "etiqueta": "Fecha de fundación", "tipo": "date"},
            {
                "nombre": "grupo_investigacion", "etiqueta": "Grupo de investigación", "numero": True,
                "catalogo": {"listar": cliente_api.listar_grupos_investigacion, "valor": "id", "etiqueta": ("nombre",)},
            },
        ],
        "listar": cliente_api.listar_semilleros, "obtener": cliente_api.obtener_semillero,
        "crear": cliente_api.crear_semillero, "put": cliente_api.reemplazar_semillero,
        "patch": cliente_api.actualizar_semillero, "eliminar": cliente_api.eliminar_semillero,
    },
    "participa_grupo": {
        "titulo": "Participación en grupos", "clave": "docente_cedula",
        "parametros_ruta": (("docente_cedula", "docente_cedula"), ("grupo_investigacion_id", "grupo_investigacion_id")),
        "endpoint_lista": "listar_participaciones_grupo", "endpoint_nuevo": "crear_participacion_grupo",
        "endpoint_editar": "editar_participacion_grupo", "endpoint_eliminar": "eliminar_participacion_grupo",
        "campos": [
            {
                "nombre": "docente_cedula", "etiqueta": "Docente", "numero": True, "clave": True,
                "catalogo": {"listar": cliente_api.listar_docentes, "valor": "cedula", "etiqueta": ("nombres", "apellidos")},
            },
            {
                "nombre": "grupo_investigacion_id", "etiqueta": "Grupo de investigación", "numero": True, "clave": True,
                "catalogo": {"listar": cliente_api.listar_grupos_investigacion, "valor": "id", "etiqueta": ("nombre",)},
            },
            {"nombre": "rol", "etiqueta": "Rol", "maximo": 15},
            {"nombre": "fecha_inicio", "etiqueta": "Fecha de inicio", "tipo": "date"},
            {"nombre": "fecha_fin", "etiqueta": "Fecha de finalización", "tipo": "date", "nullable": True},
        ],
        "listar": cliente_api.listar_participaciones_grupo,
        "obtener": cliente_api.obtener_participacion_grupo,
        "crear": cliente_api.crear_participacion_grupo,
        "put": cliente_api.reemplazar_participacion_grupo,
        "patch": cliente_api.actualizar_participacion_grupo,
        "eliminar": cliente_api.eliminar_participacion_grupo,
    },
    "participa_semillero": {
        "titulo": "Participación en semilleros", "clave": "docente",
        "parametros_ruta": (("docente", "docente"), ("semillero", "semillero")),
        "endpoint_lista": "listar_participaciones_semillero", "endpoint_nuevo": "crear_participacion_semillero",
        "endpoint_editar": "editar_participacion_semillero", "endpoint_eliminar": "eliminar_participacion_semillero",
        "campos": [
            {
                "nombre": "docente", "etiqueta": "Docente", "numero": True, "clave": True,
                "catalogo": {"listar": cliente_api.listar_docentes, "valor": "cedula", "etiqueta": ("nombres", "apellidos")},
            },
            {
                "nombre": "semillero", "etiqueta": "Semillero", "numero": True, "clave": True,
                "catalogo": {"listar": cliente_api.listar_semilleros, "valor": "id", "etiqueta": ("nombre",)},
            },
            {"nombre": "rol", "etiqueta": "Rol", "maximo": 15},
            {"nombre": "fecha_inicio", "etiqueta": "Fecha de inicio", "tipo": "date"},
            {"nombre": "fecha_fin", "etiqueta": "Fecha de finalización", "tipo": "date", "nullable": True},
        ],
        "listar": cliente_api.listar_participaciones_semillero,
        "obtener": cliente_api.obtener_participacion_semillero,
        "crear": cliente_api.crear_participacion_semillero,
        "put": cliente_api.reemplazar_participacion_semillero,
        "patch": cliente_api.actualizar_participacion_semillero,
        "eliminar": cliente_api.eliminar_participacion_semillero,
    },
    "grupo_linea": {
        "titulo": "Grupo – Línea de investigación", "clave": "grupo_investigacion",
        "editable": False,
        "parametros_ruta": (
            ("grupo_investigacion", "grupo_investigacion"),
            ("linea_investigacion", "linea_investigacion"),
        ),
        "endpoint_lista": "listar_grupo_linea", "endpoint_nuevo": "crear_grupo_linea",
        "endpoint_eliminar": "eliminar_grupo_linea",
        "campos": [
            {
                "nombre": "grupo_investigacion", "etiqueta": "Grupo de investigación",
                "numero": True, "clave": True,
                "catalogo": {
                    "listar": cliente_api.listar_grupos_investigacion, "valor": "id",
                    "etiqueta": ("nombre",),
                },
            },
            {
                "nombre": "linea_investigacion", "etiqueta": "Línea de investigación",
                "numero": True, "clave": True,
                "catalogo": {
                    "listar": cliente_api.listar_lineas_investigacion, "valor": "id",
                    "etiqueta": ("nombre",),
                },
            },
        ],
        "listar": cliente_api.listar_grupo_linea, "crear": cliente_api.crear_grupo_linea,
        "eliminar": cliente_api.eliminar_grupo_linea,
    },
    "semillero_linea": {
        "titulo": "Semillero – Línea de investigación", "clave": "semillero",
        "editable": False,
        "parametros_ruta": (
            ("semillero", "semillero"),
            ("linea_investigacion", "linea_investigacion"),
        ),
        "endpoint_lista": "listar_semillero_linea", "endpoint_nuevo": "crear_semillero_linea",
        "endpoint_eliminar": "eliminar_semillero_linea",
        "campos": [
            {
                "nombre": "semillero", "etiqueta": "Semillero", "numero": True, "clave": True,
                "catalogo": {
                    "listar": cliente_api.listar_semilleros, "valor": "id",
                    "etiqueta": ("nombre",),
                },
            },
            {
                "nombre": "linea_investigacion", "etiqueta": "Línea de investigación",
                "numero": True, "clave": True,
                "catalogo": {
                    "listar": cliente_api.listar_lineas_investigacion, "valor": "id",
                    "etiqueta": ("nombre",),
                },
            },
        ],
        "listar": cliente_api.listar_semillero_linea, "crear": cliente_api.crear_semillero_linea,
        "eliminar": cliente_api.eliminar_semillero_linea,
    },
    "ac_linea": {
        "titulo": "Área de conocimiento – Línea", "clave": "linea_investigacion",
        "editable": False,
        "parametros_ruta": (
            ("linea_investigacion", "linea_investigacion"),
            ("area_conocimiento", "area_conocimiento"),
        ),
        "endpoint_lista": "listar_ac_linea", "endpoint_nuevo": "crear_ac_linea",
        "endpoint_eliminar": "eliminar_ac_linea",
        "campos": [
            {
                "nombre": "linea_investigacion", "etiqueta": "Línea de investigación",
                "numero": True, "clave": True,
                "catalogo": {
                    "listar": cliente_api.listar_lineas_investigacion, "valor": "id",
                    "etiqueta": ("nombre",),
                },
            },
            {
                "nombre": "area_conocimiento", "etiqueta": "Área de conocimiento",
                "clave": True,
                "catalogo": {
                    "listar": cliente_api.listar_areas_conocimiento, "valor": "id",
                    "etiqueta": ("gran_area", "area", "disciplina"),
                },
            },
        ],
        "listar": cliente_api.listar_ac_linea, "crear": cliente_api.crear_ac_linea,
        "eliminar": cliente_api.eliminar_ac_linea,
    },
    "ods_linea": {
        "titulo": "Objetivo de desarrollo sostenible – Línea", "clave": "linea_investigacion",
        "editable": False,
        "parametros_ruta": (
            ("linea_investigacion", "linea_investigacion"),
            ("ods", "ods"),
        ),
        "endpoint_lista": "listar_ods_linea", "endpoint_nuevo": "crear_ods_linea",
        "endpoint_eliminar": "eliminar_ods_linea",
        "campos": [
            {
                "nombre": "linea_investigacion", "etiqueta": "Línea de investigación",
                "numero": True, "clave": True,
                "catalogo": {
                    "listar": cliente_api.listar_lineas_investigacion, "valor": "id",
                    "etiqueta": ("nombre",),
                },
            },
            {
                "nombre": "ods", "etiqueta": "Objetivo de desarrollo sostenible",
                "numero": True, "clave": True,
                "catalogo": {
                    "listar": cliente_api.listar_objetivos_desarrollo_sostenible, "valor": "id",
                    "etiqueta": ("nombre",),
                },
            },
        ],
        "listar": cliente_api.listar_ods_linea, "crear": cliente_api.crear_ods_linea,
        "eliminar": cliente_api.eliminar_ods_linea,
    },
    "aa_linea": {
        "titulo": "Área de aplicación – Línea", "clave": "area_aplicacion",
        "editable": False,
        "parametros_ruta": (
            ("area_aplicacion", "area_aplicacion"),
            ("linea_investigacion", "linea_investigacion"),
        ),
        "endpoint_lista": "listar_aa_linea", "endpoint_nuevo": "crear_aa_linea",
        "endpoint_eliminar": "eliminar_aa_linea",
        "campos": [
            {
                "nombre": "area_aplicacion", "etiqueta": "Área de aplicación",
                "numero": True, "clave": True,
                "catalogo": {
                    "listar": cliente_api.listar_areas_aplicacion, "valor": "id",
                    "etiqueta": ("nombre",),
                },
            },
            {
                "nombre": "linea_investigacion", "etiqueta": "Línea de investigación",
                "numero": True, "clave": True,
                "catalogo": {
                    "listar": cliente_api.listar_lineas_investigacion, "valor": "id",
                    "etiqueta": ("nombre",),
                },
            },
        ],
        "listar": cliente_api.listar_aa_linea, "crear": cliente_api.crear_aa_linea,
        "eliminar": cliente_api.eliminar_aa_linea,
    },
    "roles": {
        "titulo": "Roles", "clave": "id",
        "endpoint_lista": "listar_roles", "endpoint_nuevo": "crear_rol",
        "endpoint_editar": "editar_rol", "endpoint_eliminar": "eliminar_rol",
        "campos": [
            {"nombre": "id", "etiqueta": "Número", "numero": True, "clave": True, "solo_salida": True},
            {"nombre": "nombre", "etiqueta": "Nombre", "maximo": 100},
            {"nombre": "descripcion", "etiqueta": "Descripción", "multilinea": True, "nullable": True},
            {"nombre": "fecha_creacion", "etiqueta": "Fecha de creación", "solo_salida": True},
        ],
        "listar": cliente_api.listar_roles, "obtener": cliente_api.obtener_rol,
        "crear": cliente_api.crear_rol, "put": cliente_api.reemplazar_rol,
        "patch": cliente_api.actualizar_rol, "eliminar": cliente_api.eliminar_rol,
    },
    "usuarios": {
        "titulo": "Usuarios", "clave": "id",
        "endpoint_lista": "listar_usuarios", "endpoint_nuevo": "crear_usuario",
        "endpoint_editar": "editar_usuario", "endpoint_eliminar": "eliminar_usuario",
        "campos": [
            {"nombre": "id", "etiqueta": "Número", "numero": True, "clave": True, "solo_salida": True},
            {"nombre": "username", "etiqueta": "Nombre de usuario", "maximo": 100},
            {
                "nombre": "password", "etiqueta": "Contraseña", "tipo": "password",
                "maximo": 72, "sensible": True, "oculto_listado": True,
            },
            {"nombre": "email", "etiqueta": "Correo", "maximo": 150},
            {"nombre": "nombre_completo", "etiqueta": "Nombre completo", "maximo": 200, "nullable": True},
            {"nombre": "fecha_creacion", "etiqueta": "Fecha de creación", "solo_salida": True},
            {"nombre": "fecha_actualizacion", "etiqueta": "Última actualización", "solo_salida": True},
        ],
        "listar": cliente_api.listar_usuarios, "obtener": cliente_api.obtener_usuario,
        "crear": cliente_api.crear_usuario, "put": cliente_api.reemplazar_usuario,
        "patch": cliente_api.actualizar_usuario, "eliminar": cliente_api.eliminar_usuario,
    },
    "rol_usuario": {
        "titulo": "Asignación de roles", "clave": "usuario_id", "editable": False,
        "parametros_ruta": (("usuario_id", "usuario_id"), ("rol_id", "rol_id")),
        "endpoint_lista": "listar_rol_usuario", "endpoint_nuevo": "crear_rol_usuario",
        "endpoint_eliminar": "eliminar_rol_usuario",
        "campos": [
            {
                "nombre": "usuario_id", "etiqueta": "Usuario", "numero": True, "clave": True,
                "catalogo": {
                    "listar": cliente_api.listar_usuarios, "valor": "id",
                    "etiqueta": ("username", "nombre_completo"),
                },
            },
            {
                "nombre": "rol_id", "etiqueta": "Rol", "numero": True, "clave": True,
                "catalogo": {
                    "listar": cliente_api.listar_roles, "valor": "id",
                    "etiqueta": ("nombre",),
                },
            },
        ],
        "listar": cliente_api.listar_asignaciones_rol,
        "crear": cliente_api.crear_asignacion_rol,
        "eliminar": cliente_api.eliminar_asignacion_rol,
    },
}

GRUPOS_RECURSOS = {
    "Catálogos Base (v1)": (
        "areas_conocimiento", "ods", "areas_aplicacion", "terminos_clave",
        "universidades", "lineas_investigacion",
    ),
    "Relacionales (v2)": (
        "docentes", "grupos_investigacion", "semilleros", "participa_grupo",
        "participa_semillero", "grupo_linea", "semillero_linea", "ac_linea",
        "ods_linea", "aa_linea",
    ),
    "Administración": ("usuarios", "roles", "rol_usuario"),
}


def _valores_formulario(recurso: dict, edicion: bool) -> dict:
    valores = {}
    for campo in recurso["campos"]:
        nombre = campo["nombre"]
        if campo.get("solo_salida") or (edicion and campo.get("clave")):
            continue
        valor = request.form.get(nombre, "").strip()
        if campo.get("sensible") and not valor:
            continue
        if campo.get("numero") and valor:
            try:
                valor = int(valor)
            except ValueError:
                pass
        if campo.get("nullable") and valor == "":
            valor = None
        valores[nombre] = valor
    return valores


def _parametros_ruta(recurso: dict, ficha: dict) -> dict:
    parametros = recurso.get("parametros_ruta")
    if parametros:
        return {nombre: ficha.get(campo) for nombre, campo in parametros}
    return {"identificador": ficha.get(recurso["clave"])}


def _url_recurso(endpoint: str, recurso: dict, ficha: dict) -> str:
    return url_for(endpoint, **_parametros_ruta(recurso, ficha))


def _preparar_formulario(
    recurso: dict, ficha: dict, editando: bool, endpoint: str,
    avisos: list[str] | None = None,
):
    opciones = {}
    mensajes = list(avisos or [])
    for campo in recurso["campos"]:
        catalogo = campo.get("catalogo")
        if not catalogo:
            continue
        ok, filas, errores = catalogo["listar"]()
        opciones[campo["nombre"]] = []
        if not ok:
            mensajes.extend(errores)
            filas = []
        elif not filas:
            mensajes.append(f"No hay opciones activas para «{campo['etiqueta']}».")
        for fila in filas:
            opciones[campo["nombre"]].append({
                "valor": fila[catalogo["valor"]],
                "etiqueta": " · ".join(str(fila.get(nombre, "")) for nombre in catalogo["etiqueta"]),
            })
        valor_actual = ficha.get(campo["nombre"])
        if valor_actual not in (None, "") and not any(
            str(opcion["valor"]) == str(valor_actual) for opcion in opciones[campo["nombre"]]
        ):
            opciones[campo["nombre"]].append({
                "valor": valor_actual,
                "etiqueta": f"Selección actual: {valor_actual}",
            })
    accion = (
        _url_recurso(endpoint, recurso, ficha)
        if editando else url_for(endpoint)
    )
    return render_template(
        "catalogos/formulario.html", recurso=recurso, ficha=ficha,
        editando=editando, endpoint=endpoint, accion=accion,
        opciones=opciones, avisos=mensajes,
    )


def _listar(recurso: dict, endpoint: str, avisos: list[str] | None = None):
    ok, filas, errores = recurso["listar"]()
    mensajes = list(avisos or [])
    if request.args.get("aviso"):
        mensajes.append(request.args["aviso"])
    if not ok:
        mensajes.extend(errores)
        filas = []
    filas_vista = []
    for fila in filas:
        fila_vista = dict(fila)
        if recurso.get("editable", True):
            fila_vista["_editar_url"] = _url_recurso(recurso["endpoint_editar"], recurso, fila)
        fila_vista["_eliminar_url"] = _url_recurso(recurso["endpoint_eliminar"], recurso, fila)
        filas_vista.append(fila_vista)
    return render_template(
        "catalogos/lista.html",
        recurso=recurso,
        filas=filas_vista,
        endpoint=endpoint,
        avisos=mensajes,
    )


def _nuevo(recurso: dict, endpoint: str, endpoint_lista: str):
    if request.method == "GET":
        return _preparar_formulario(recurso, {}, False, endpoint)
    valores = _valores_formulario(recurso, False)
    ok, _respuesta, errores = recurso["crear"](valores)
    if ok:
        return redirect(url_for(endpoint_lista, aviso="La ficha se guardó correctamente."))
    return _preparar_formulario(recurso, request.form, False, endpoint, errores)


def _editar(recurso: dict, identificadores: tuple, endpoint: str, endpoint_lista: str):
    if request.method == "GET":
        ok, ficha, errores = recurso["obtener"](*identificadores)
        if not ok:
            return _listar(recurso, recurso["endpoint_nuevo"], errores)
        return _preparar_formulario(recurso, ficha, True, endpoint)

    verbo = request.form.get("verbo")
    valores = _valores_formulario(recurso, True)
    if verbo == "completa":
        ok, _respuesta, errores = recurso["put"](*identificadores, valores)
    else:
        cambios = {}
        for campo, valor in valores.items():
            original = request.form.get(f"original__{campo}", "")
            actual = "" if valor is None else str(valor)
            if actual != original:
                cambios[campo] = valor
        ok, _respuesta, errores = recurso["patch"](*identificadores, cambios)
    if ok:
        return redirect(url_for(endpoint_lista, aviso="Los cambios se guardaron correctamente."))
    ficha = dict(request.form)
    for (nombre_parametro, campo_clave), identificador in zip(
        recurso.get("parametros_ruta", (("identificador", recurso["clave"]),)),
        identificadores,
    ):
        ficha[campo_clave] = identificador
    return _preparar_formulario(recurso, ficha, True, endpoint, errores)


def _eliminar(recurso: dict, identificadores: tuple, endpoint_lista: str):
    ok, _respuesta, errores = recurso["eliminar"](*identificadores)
    aviso = "La ficha se retiró correctamente." if ok else None
    return _listar(recurso, recurso["endpoint_nuevo"], [aviso] if aviso else errores)


@app.get("/")
def inicio():
    return render_template("inicio.html", recursos=RECURSOS, grupos_recursos=GRUPOS_RECURSOS)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if session.get("accessToken"):
            return redirect(url_for("inicio"))
        return render_template("login.html", avisos=[request.args["aviso"]] if request.args.get("aviso") else [])

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    ok, respuesta, errores = cliente_api.iniciar_sesion(
        {"username": username, "password": password}
    )
    if not ok:
        return render_template("login.html", avisos=errores), 401

    session.clear()
    session["accessToken"] = respuesta["access_token"]
    session["usuario"] = respuesta["usuario"]
    siguiente = request.form.get("siguiente", "")
    if siguiente.startswith("/") and not siguiente.startswith("//"):
        return redirect(siguiente)
    return redirect(url_for("inicio"))


@app.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/areas-de-conocimiento")
def listar_areas_conocimiento():
    return _listar(RECURSOS["areas_conocimiento"], "crear_area_conocimiento")


@app.route("/areas-de-conocimiento/nuevo", methods=["GET", "POST"])
def crear_area_conocimiento():
    return _nuevo(RECURSOS["areas_conocimiento"], "crear_area_conocimiento", "listar_areas_conocimiento")


@app.route("/areas-de-conocimiento/<string:identificador>/editar", methods=["GET", "POST"])
def editar_area_conocimiento(identificador):
    return _editar(RECURSOS["areas_conocimiento"], (identificador,), "editar_area_conocimiento",
                   "listar_areas_conocimiento")


@app.post("/areas-de-conocimiento/<string:identificador>/eliminar")
def eliminar_area_conocimiento(identificador):
    return _eliminar(RECURSOS["areas_conocimiento"], (identificador,), "listar_areas_conocimiento")


@app.route("/ods")
def listar_ods():
    return _listar(RECURSOS["ods"], "crear_ods")


@app.route("/ods/nuevo", methods=["GET", "POST"])
def crear_ods():
    return _nuevo(RECURSOS["ods"], "crear_ods", "listar_ods")


@app.route("/ods/<int:identificador>/editar", methods=["GET", "POST"])
def editar_ods(identificador):
    return _editar(RECURSOS["ods"], (identificador,), "editar_ods", "listar_ods")


@app.post("/ods/<int:identificador>/eliminar")
def eliminar_ods(identificador):
    return _eliminar(RECURSOS["ods"], (identificador,), "listar_ods")


@app.route("/areas-aplicacion")
def listar_areas_aplicacion():
    return _listar(RECURSOS["areas_aplicacion"], "crear_area_aplicacion")


@app.route("/areas-aplicacion/nuevo", methods=["GET", "POST"])
def crear_area_aplicacion():
    return _nuevo(RECURSOS["areas_aplicacion"], "crear_area_aplicacion", "listar_areas_aplicacion")


@app.route("/areas-aplicacion/<int:identificador>/editar", methods=["GET", "POST"])
def editar_area_aplicacion(identificador):
    return _editar(RECURSOS["areas_aplicacion"], (identificador,), "editar_area_aplicacion",
                   "listar_areas_aplicacion")


@app.post("/areas-aplicacion/<int:identificador>/eliminar")
def eliminar_area_aplicacion(identificador):
    return _eliminar(RECURSOS["areas_aplicacion"], (identificador,), "listar_areas_aplicacion")


@app.route("/terminos-clave")
def listar_terminos_clave():
    return _listar(RECURSOS["terminos_clave"], "crear_termino_clave")


@app.route("/terminos-clave/nuevo", methods=["GET", "POST"])
def crear_termino_clave():
    return _nuevo(RECURSOS["terminos_clave"], "crear_termino_clave", "listar_terminos_clave")


@app.route("/terminos-clave/<string:identificador>/editar", methods=["GET", "POST"])
def editar_termino_clave(identificador):
    return _editar(RECURSOS["terminos_clave"], (identificador,), "editar_termino_clave",
                   "listar_terminos_clave")


@app.post("/terminos-clave/<string:identificador>/eliminar")
def eliminar_termino_clave(identificador):
    return _eliminar(RECURSOS["terminos_clave"], (identificador,), "listar_terminos_clave")


@app.route("/universidades")
def listar_universidades():
    return _listar(RECURSOS["universidades"], "crear_universidad")


@app.route("/universidades/nuevo", methods=["GET", "POST"])
def crear_universidad():
    return _nuevo(RECURSOS["universidades"], "crear_universidad", "listar_universidades")


@app.route("/universidades/<int:identificador>/editar", methods=["GET", "POST"])
def editar_universidad(identificador):
    return _editar(RECURSOS["universidades"], (identificador,), "editar_universidad",
                   "listar_universidades")


@app.post("/universidades/<int:identificador>/eliminar")
def eliminar_universidad(identificador):
    return _eliminar(RECURSOS["universidades"], (identificador,), "listar_universidades")


@app.route("/lineas-investigacion")
def listar_lineas_investigacion():
    return _listar(RECURSOS["lineas_investigacion"], "crear_linea_investigacion")


@app.route("/lineas-investigacion/nuevo", methods=["GET", "POST"])
def crear_linea_investigacion():
    return _nuevo(RECURSOS["lineas_investigacion"], "crear_linea_investigacion",
                  "listar_lineas_investigacion")


@app.route("/lineas-investigacion/<int:identificador>/editar", methods=["GET", "POST"])
def editar_linea_investigacion(identificador):
    return _editar(RECURSOS["lineas_investigacion"], (identificador,), "editar_linea_investigacion",
                   "listar_lineas_investigacion")


@app.post("/lineas-investigacion/<int:identificador>/eliminar")
def eliminar_linea_investigacion(identificador):
    return _eliminar(RECURSOS["lineas_investigacion"], (identificador,), "listar_lineas_investigacion")


@app.route("/docentes")
def listar_docentes():
    return _listar(RECURSOS["docentes"], "crear_docente")


@app.route("/docentes/nuevo", methods=["GET", "POST"])
def crear_docente():
    return _nuevo(RECURSOS["docentes"], "crear_docente", "listar_docentes")


@app.route("/docentes/<int:identificador>/editar", methods=["GET", "POST"])
def editar_docente(identificador):
    return _editar(RECURSOS["docentes"], (identificador,), "editar_docente", "listar_docentes")


@app.post("/docentes/<int:identificador>/eliminar")
def eliminar_docente(identificador):
    return _eliminar(RECURSOS["docentes"], (identificador,), "listar_docentes")


@app.route("/grupos-investigacion")
def listar_grupos_investigacion():
    return _listar(RECURSOS["grupos_investigacion"], "crear_grupo_investigacion")


@app.route("/grupos-investigacion/nuevo", methods=["GET", "POST"])
def crear_grupo_investigacion():
    return _nuevo(RECURSOS["grupos_investigacion"], "crear_grupo_investigacion",
                  "listar_grupos_investigacion")


@app.route("/grupos-investigacion/<int:identificador>/editar", methods=["GET", "POST"])
def editar_grupo_investigacion(identificador):
    return _editar(RECURSOS["grupos_investigacion"], (identificador,),
                   "editar_grupo_investigacion", "listar_grupos_investigacion")


@app.post("/grupos-investigacion/<int:identificador>/eliminar")
def eliminar_grupo_investigacion(identificador):
    return _eliminar(RECURSOS["grupos_investigacion"], (identificador,),
                     "listar_grupos_investigacion")


@app.route("/semilleros")
def listar_semilleros():
    return _listar(RECURSOS["semilleros"], "crear_semillero")


@app.route("/semilleros/nuevo", methods=["GET", "POST"])
def crear_semillero():
    return _nuevo(RECURSOS["semilleros"], "crear_semillero", "listar_semilleros")


@app.route("/semilleros/<int:identificador>/editar", methods=["GET", "POST"])
def editar_semillero(identificador):
    return _editar(RECURSOS["semilleros"], (identificador,), "editar_semillero",
                   "listar_semilleros")


@app.post("/semilleros/<int:identificador>/eliminar")
def eliminar_semillero(identificador):
    return _eliminar(RECURSOS["semilleros"], (identificador,), "listar_semilleros")


@app.route("/participa-grupo")
def listar_participaciones_grupo():
    return _listar(RECURSOS["participa_grupo"], "crear_participacion_grupo")


@app.route("/participa-grupo/nuevo", methods=["GET", "POST"])
def crear_participacion_grupo():
    return _nuevo(RECURSOS["participa_grupo"], "crear_participacion_grupo",
                  "listar_participaciones_grupo")


@app.route(
    "/participa-grupo/<int:docente_cedula>/<int:grupo_investigacion_id>/editar",
    methods=["GET", "POST"],
)
def editar_participacion_grupo(docente_cedula, grupo_investigacion_id):
    return _editar(
        RECURSOS["participa_grupo"], (docente_cedula, grupo_investigacion_id),
        "editar_participacion_grupo", "listar_participaciones_grupo",
    )


@app.post("/participa-grupo/<int:docente_cedula>/<int:grupo_investigacion_id>/eliminar")
def eliminar_participacion_grupo(docente_cedula, grupo_investigacion_id):
    return _eliminar(
        RECURSOS["participa_grupo"], (docente_cedula, grupo_investigacion_id),
        "listar_participaciones_grupo",
    )


@app.route("/participa-semillero")
def listar_participaciones_semillero():
    return _listar(RECURSOS["participa_semillero"], "crear_participacion_semillero")


@app.route("/participa-semillero/nuevo", methods=["GET", "POST"])
def crear_participacion_semillero():
    return _nuevo(RECURSOS["participa_semillero"], "crear_participacion_semillero",
                  "listar_participaciones_semillero")


@app.route("/participa-semillero/<int:docente>/<int:semillero>/editar", methods=["GET", "POST"])
def editar_participacion_semillero(docente, semillero):
    return _editar(
        RECURSOS["participa_semillero"], (docente, semillero),
        "editar_participacion_semillero", "listar_participaciones_semillero",
    )


@app.post("/participa-semillero/<int:docente>/<int:semillero>/eliminar")
def eliminar_participacion_semillero(docente, semillero):
    return _eliminar(
        RECURSOS["participa_semillero"], (docente, semillero),
        "listar_participaciones_semillero",
    )


@app.route("/grupo-linea")
def listar_grupo_linea():
    return _listar(RECURSOS["grupo_linea"], "crear_grupo_linea")


@app.route("/grupo-linea/nuevo", methods=["GET", "POST"])
def crear_grupo_linea():
    return _nuevo(RECURSOS["grupo_linea"], "crear_grupo_linea", "listar_grupo_linea")


@app.post("/grupo-linea/<int:grupo_investigacion>/<int:linea_investigacion>/eliminar")
def eliminar_grupo_linea(grupo_investigacion, linea_investigacion):
    return _eliminar(
        RECURSOS["grupo_linea"], (grupo_investigacion, linea_investigacion),
        "listar_grupo_linea",
    )


@app.route("/semillero-linea")
def listar_semillero_linea():
    return _listar(RECURSOS["semillero_linea"], "crear_semillero_linea")


@app.route("/semillero-linea/nuevo", methods=["GET", "POST"])
def crear_semillero_linea():
    return _nuevo(RECURSOS["semillero_linea"], "crear_semillero_linea", "listar_semillero_linea")


@app.post("/semillero-linea/<int:semillero>/<int:linea_investigacion>/eliminar")
def eliminar_semillero_linea(semillero, linea_investigacion):
    return _eliminar(
        RECURSOS["semillero_linea"], (semillero, linea_investigacion),
        "listar_semillero_linea",
    )


@app.route("/ac-linea")
def listar_ac_linea():
    return _listar(RECURSOS["ac_linea"], "crear_ac_linea")


@app.route("/ac-linea/nuevo", methods=["GET", "POST"])
def crear_ac_linea():
    return _nuevo(RECURSOS["ac_linea"], "crear_ac_linea", "listar_ac_linea")


@app.post("/ac-linea/<int:linea_investigacion>/<string:area_conocimiento>/eliminar")
def eliminar_ac_linea(linea_investigacion, area_conocimiento):
    return _eliminar(
        RECURSOS["ac_linea"], (linea_investigacion, area_conocimiento),
        "listar_ac_linea",
    )


@app.route("/ods-linea")
def listar_ods_linea():
    return _listar(RECURSOS["ods_linea"], "crear_ods_linea")


@app.route("/ods-linea/nuevo", methods=["GET", "POST"])
def crear_ods_linea():
    return _nuevo(RECURSOS["ods_linea"], "crear_ods_linea", "listar_ods_linea")


@app.post("/ods-linea/<int:linea_investigacion>/<int:ods>/eliminar")
def eliminar_ods_linea(linea_investigacion, ods):
    return _eliminar(
        RECURSOS["ods_linea"], (linea_investigacion, ods), "listar_ods_linea",
    )


@app.route("/aa-linea")
def listar_aa_linea():
    return _listar(RECURSOS["aa_linea"], "crear_aa_linea")


@app.route("/aa-linea/nuevo", methods=["GET", "POST"])
def crear_aa_linea():
    return _nuevo(RECURSOS["aa_linea"], "crear_aa_linea", "listar_aa_linea")


@app.post("/aa-linea/<int:area_aplicacion>/<int:linea_investigacion>/eliminar")
def eliminar_aa_linea(area_aplicacion, linea_investigacion):
    return _eliminar(
        RECURSOS["aa_linea"], (area_aplicacion, linea_investigacion),
        "listar_aa_linea",
    )


@app.route("/roles")
def listar_roles():
    return _listar(RECURSOS["roles"], "crear_rol")


@app.route("/roles/nuevo", methods=["GET", "POST"])
def crear_rol():
    return _nuevo(RECURSOS["roles"], "crear_rol", "listar_roles")


@app.route("/roles/<int:identificador>/editar", methods=["GET", "POST"])
def editar_rol(identificador):
    return _editar(RECURSOS["roles"], (identificador,), "editar_rol", "listar_roles")


@app.post("/roles/<int:identificador>/eliminar")
def eliminar_rol(identificador):
    return _eliminar(RECURSOS["roles"], (identificador,), "listar_roles")


@app.route("/usuarios")
def listar_usuarios():
    return _listar(RECURSOS["usuarios"], "crear_usuario")


@app.route("/usuarios/nuevo", methods=["GET", "POST"])
def crear_usuario():
    return _nuevo(RECURSOS["usuarios"], "crear_usuario", "listar_usuarios")


@app.route("/usuarios/<int:identificador>/editar", methods=["GET", "POST"])
def editar_usuario(identificador):
    return _editar(RECURSOS["usuarios"], (identificador,), "editar_usuario", "listar_usuarios")


@app.post("/usuarios/<int:identificador>/eliminar")
def eliminar_usuario(identificador):
    return _eliminar(RECURSOS["usuarios"], (identificador,), "listar_usuarios")


@app.route("/rol-usuario")
def listar_rol_usuario():
    return _listar(RECURSOS["rol_usuario"], "crear_rol_usuario")


@app.route("/rol-usuario/nuevo", methods=["GET", "POST"])
def crear_rol_usuario():
    return _nuevo(RECURSOS["rol_usuario"], "crear_rol_usuario", "listar_rol_usuario")


@app.post("/rol-usuario/<int:usuario_id>/<int:rol_id>/eliminar")
def eliminar_rol_usuario(usuario_id, rol_id):
    return _eliminar(
        RECURSOS["rol_usuario"], (usuario_id, rol_id), "listar_rol_usuario",
    )


@app.errorhandler(404)
def no_encontrada(_error):
    return render_template("no_encontrada.html"), 404


@app.errorhandler(403)
def sin_permisos(_error):
    return render_template("no_autorizada.html"), 403


@app.errorhandler(cliente_api.SesionExpirada)
def sesion_expirada(_error):
    return redirect(url_for("login", aviso="La sesión venció. Ingresa de nuevo."))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8078, debug=True)
