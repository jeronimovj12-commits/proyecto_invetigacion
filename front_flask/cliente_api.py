"""Adaptador HTTP del front; trabajar con JSON preserva el límite entre procesos."""

import os
from urllib.parse import quote

from flask import has_request_context, session
import requests

URL_API = os.environ.get("URL_API_INVESTIGACION", "http://localhost:8025").rstrip("/")
TIEMPO_MAXIMO = 8
NO_DISPONIBLE = ["El servicio no está disponible. Inténtalo de nuevo más tarde."]


class SesionExpirada(Exception):
    """Permite que Flask redirija al login al recibir un 401 desde la API."""


def _normalizar_respuesta(valor):
    if isinstance(valor, list):
        return [_normalizar_respuesta(fila) for fila in valor]
    if not isinstance(valor, dict):
        return valor
    nombres = {
        "accessToken": "access_token", "tokenType": "token_type",
        "granArea": "gran_area", "terminoIngles": "termino_ingles",
        "fechaNacimiento": "fecha_nacimiento", "urlCvlac": "url_cvlac",
        "fechaActualizacion": "fecha_actualizacion", "catMinciencia": "cat_minciencia",
        "convMinciencia": "conv_minciencia",
        "lineaInvestigacionPrincipal": "linea_investigacion_principal",
        "urlGruplac": "url_gruplac", "fechaFundacion": "fecha_fundacion",
        "grupoInvestigacion": "grupo_investigacion",
        "docenteCedula": "docente_cedula",
        "grupoInvestigacionId": "grupo_investigacion_id",
        "lineaInvestigacion": "linea_investigacion",
        "areaConocimiento": "area_conocimiento",
        "areaAplicacion": "area_aplicacion",
        "nombreCompleto": "nombre_completo",
        "fechaCreacion": "fecha_creacion",
        "fechaActualizacion": "fecha_actualizacion",
        "usuarioId": "usuario_id",
        "rolId": "rol_id",
        "fechaInicio": "fecha_inicio", "fechaFin": "fecha_fin",
    }
    return {nombres.get(campo, campo): _normalizar_respuesta(contenido)
            for campo, contenido in valor.items()}


def _cuerpo_api(datos: dict | None) -> dict | None:
    if datos is None:
        return None
    nombres = {
        "gran_area": "granArea", "termino_ingles": "terminoIngles",
        "fecha_nacimiento": "fechaNacimiento", "url_cvlac": "urlCvlac",
        "fecha_actualizacion": "fechaActualizacion", "cat_minciencia": "catMinciencia",
        "conv_minciencia": "convMinciencia",
        "linea_investigacion_principal": "lineaInvestigacionPrincipal",
        "url_gruplac": "urlGruplac", "fecha_fundacion": "fechaFundacion",
        "grupo_investigacion": "grupoInvestigacion",
        "docente_cedula": "docenteCedula",
        "grupo_investigacion_id": "grupoInvestigacionId",
        "linea_investigacion": "lineaInvestigacion",
        "area_conocimiento": "areaConocimiento",
        "area_aplicacion": "areaAplicacion",
        "nombre_completo": "nombreCompleto",
        "fecha_creacion": "fechaCreacion",
        "fecha_actualizacion": "fechaActualizacion",
        "usuario_id": "usuarioId",
        "rol_id": "rolId",
        "fecha_inicio": "fechaInicio", "fecha_fin": "fechaFin",
    }
    return {nombres.get(campo, campo): valor for campo, valor in datos.items()}


def _traducir_error(respuesta: requests.Response) -> list[str]:
    try:
        cuerpo = respuesta.json()
    except ValueError:
        return ["No se pudo completar la operación."]

    errores = cuerpo.get("errores")
    if isinstance(errores, list) and errores:
        return [str(error) for error in errores]

    detalle = cuerpo.get("detail", cuerpo.get("detalle"))
    if isinstance(detalle, dict):
        mensaje = detalle.get("detalle") or detalle.get("mensaje")
        return [str(mensaje)] if mensaje else ["No se pudo completar la operación."]
    if isinstance(detalle, list):
        traducciones = (
            ("Field required", "es obligatorio"),
            ("String should have at least", "no puede quedar vacío"),
            ("String should have at most", "supera la longitud permitida"),
            ("Input should be a valid integer", "debe ser un número entero"),
            ("Extra inputs are not permitted", "no está permitido"),
        )
        resultado = []
        for error in detalle:
            if not isinstance(error, dict):
                resultado.append(str(error))
                continue
            campo = str(error.get("loc", ["campo"])[-1])
            mensaje = str(error.get("msg", "dato inválido"))
            for ingles, espanol in traducciones:
                if ingles in mensaje:
                    mensaje = espanol
                    break
            resultado.append(f"El campo {campo} {mensaje}.")
        return resultado
    if isinstance(detalle, str) and detalle:
        return [detalle]
    mensaje = cuerpo.get("mensaje")
    return [str(mensaje)] if mensaje else ["No se pudo completar la operación."]


def _llamar(metodo: str, ruta: str, datos: dict | None = None,
            parametros: dict | None = None, listado: bool = False,
            autenticar: bool = True):
    token = session.get("accessToken") if has_request_context() and autenticar else None
    cabeceras = {"Authorization": f"Bearer {token}"} if token else {}
    try:
        respuesta = requests.request(
            metodo,
            f"{URL_API}{ruta}",
            json=_cuerpo_api(datos),
            params=parametros,
            timeout=TIEMPO_MAXIMO,
            headers=cabeceras,
        )
    except requests.exceptions.RequestException:
        return False, [] if listado else None, NO_DISPONIBLE

    if respuesta.status_code == 401 and token:
        session.clear()
        raise SesionExpirada()
    if listado and respuesta.status_code == 204:
        return True, [], []
    if respuesta.status_code == 200:
        try:
            contenido = respuesta.json()
        except ValueError:
            return False, [] if listado else None, ["La respuesta del servicio no tiene un formato válido."]
        if listado:
            return True, _normalizar_respuesta(contenido.get("datos", [])), []
        return True, _normalizar_respuesta(contenido), []
    return False, [] if listado else None, _traducir_error(respuesta)


def _id(valor) -> str:
    return quote(str(valor), safe="")


# Áreas de conocimiento: las funciones públicas nombran cada operación para mantener el contrato legible.
def listar_areas_conocimiento(limite: int = 1000):
    return _llamar("GET", "/api/area_conocimiento", parametros={"limite": limite}, listado=True)


def obtener_area_conocimiento(identificador: str):
    return _llamar("GET", f"/api/area_conocimiento/{_id(identificador)}")


def crear_area_conocimiento(datos: dict):
    return _llamar("POST", "/api/area_conocimiento", datos)


def reemplazar_area_conocimiento(identificador: str, datos: dict):
    return _llamar("PUT", f"/api/area_conocimiento/{_id(identificador)}", datos)


def actualizar_area_conocimiento(identificador: str, datos: dict):
    return _llamar("PATCH", f"/api/area_conocimiento/{_id(identificador)}", datos)


def eliminar_area_conocimiento(identificador: str):
    return _llamar("DELETE", f"/api/area_conocimiento/{_id(identificador)}")


# Objetivos de desarrollo sostenible: adaptadores separados impiden que las vistas decidan rutas HTTP.
def listar_objetivos_desarrollo_sostenible(limite: int = 1000):
    return _llamar("GET", "/api/objetivo_desarrollo_sostenible", parametros={"limite": limite}, listado=True)


def obtener_objetivo_desarrollo_sostenible(identificador: int):
    return _llamar("GET", f"/api/objetivo_desarrollo_sostenible/{_id(identificador)}")


def crear_objetivo_desarrollo_sostenible(datos: dict):
    return _llamar("POST", "/api/objetivo_desarrollo_sostenible", datos)


def reemplazar_objetivo_desarrollo_sostenible(identificador: int, datos: dict):
    return _llamar("PUT", f"/api/objetivo_desarrollo_sostenible/{_id(identificador)}", datos)


def actualizar_objetivo_desarrollo_sostenible(identificador: int, datos: dict):
    return _llamar("PATCH", f"/api/objetivo_desarrollo_sostenible/{_id(identificador)}", datos)


def eliminar_objetivo_desarrollo_sostenible(identificador: int):
    return _llamar("DELETE", f"/api/objetivo_desarrollo_sostenible/{_id(identificador)}")


# Áreas de aplicación.
def listar_areas_aplicacion(limite: int = 1000):
    return _llamar("GET", "/api/area_aplicacion", parametros={"limite": limite}, listado=True)


def obtener_area_aplicacion(identificador: int):
    return _llamar("GET", f"/api/area_aplicacion/{_id(identificador)}")


def crear_area_aplicacion(datos: dict):
    return _llamar("POST", "/api/area_aplicacion", datos)


def reemplazar_area_aplicacion(identificador: int, datos: dict):
    return _llamar("PUT", f"/api/area_aplicacion/{_id(identificador)}", datos)


def actualizar_area_aplicacion(identificador: int, datos: dict):
    return _llamar("PATCH", f"/api/area_aplicacion/{_id(identificador)}", datos)


def eliminar_area_aplicacion(identificador: int):
    return _llamar("DELETE", f"/api/area_aplicacion/{_id(identificador)}")


# Términos clave.
def listar_terminos_clave(limite: int = 1000):
    return _llamar("GET", "/api/termino_clave", parametros={"limite": limite}, listado=True)


def obtener_termino_clave(termino: str):
    return _llamar("GET", f"/api/termino_clave/{_id(termino)}")


def crear_termino_clave(datos: dict):
    return _llamar("POST", "/api/termino_clave", datos)


def reemplazar_termino_clave(termino: str, datos: dict):
    return _llamar("PUT", f"/api/termino_clave/{_id(termino)}", datos)


def actualizar_termino_clave(termino: str, datos: dict):
    return _llamar("PATCH", f"/api/termino_clave/{_id(termino)}", datos)


def eliminar_termino_clave(termino: str):
    return _llamar("DELETE", f"/api/termino_clave/{_id(termino)}")


# Universidades.
def listar_universidades(limite: int = 1000):
    return _llamar("GET", "/api/universidad", parametros={"limite": limite}, listado=True)


def obtener_universidad(identificador: int):
    return _llamar("GET", f"/api/universidad/{_id(identificador)}")


def crear_universidad(datos: dict):
    return _llamar("POST", "/api/universidad", datos)


def reemplazar_universidad(identificador: int, datos: dict):
    return _llamar("PUT", f"/api/universidad/{_id(identificador)}", datos)


def actualizar_universidad(identificador: int, datos: dict):
    return _llamar("PATCH", f"/api/universidad/{_id(identificador)}", datos)


def eliminar_universidad(identificador: int):
    return _llamar("DELETE", f"/api/universidad/{_id(identificador)}")


# Líneas de investigación.
def listar_lineas_investigacion(limite: int = 1000):
    return _llamar("GET", "/api/linea_investigacion", parametros={"limite": limite}, listado=True)


def obtener_linea_investigacion(identificador: int):
    return _llamar("GET", f"/api/linea_investigacion/{_id(identificador)}")


def crear_linea_investigacion(datos: dict):
    return _llamar("POST", "/api/linea_investigacion", datos)


def reemplazar_linea_investigacion(identificador: int, datos: dict):
    return _llamar("PUT", f"/api/linea_investigacion/{_id(identificador)}", datos)


def actualizar_linea_investigacion(identificador: int, datos: dict):
    return _llamar("PATCH", f"/api/linea_investigacion/{_id(identificador)}", datos)


def eliminar_linea_investigacion(identificador: int):
    return _llamar("DELETE", f"/api/linea_investigacion/{_id(identificador)}")


# Docentes: operaciones explícitas mantienen al navegador separado de los modelos internos de la API.
def listar_docentes(limite: int = 1000):
    return _llamar("GET", "/api/docente", parametros={"limite": limite}, listado=True)


def obtener_docente(cedula: int):
    return _llamar("GET", f"/api/docente/{_id(cedula)}")


def crear_docente(datos: dict):
    return _llamar("POST", "/api/docente", datos)


def reemplazar_docente(cedula: int, datos: dict):
    return _llamar("PUT", f"/api/docente/{_id(cedula)}", datos)


def actualizar_docente(cedula: int, datos: dict):
    return _llamar("PATCH", f"/api/docente/{_id(cedula)}", datos)


def eliminar_docente(cedula: int):
    return _llamar("DELETE", f"/api/docente/{_id(cedula)}")


# Grupos de investigación: la capa de presentación recibe universidad como valor de lista, no como campo digitado.
def listar_grupos_investigacion(limite: int = 1000):
    return _llamar("GET", "/api/grupo_investigacion", parametros={"limite": limite}, listado=True)


def obtener_grupo_investigacion(identificador: int):
    return _llamar("GET", f"/api/grupo_investigacion/{_id(identificador)}")


def crear_grupo_investigacion(datos: dict):
    return _llamar("POST", "/api/grupo_investigacion", datos)


def reemplazar_grupo_investigacion(identificador: int, datos: dict):
    return _llamar("PUT", f"/api/grupo_investigacion/{_id(identificador)}", datos)


def actualizar_grupo_investigacion(identificador: int, datos: dict):
    return _llamar("PATCH", f"/api/grupo_investigacion/{_id(identificador)}", datos)


def eliminar_grupo_investigacion(identificador: int):
    return _llamar("DELETE", f"/api/grupo_investigacion/{_id(identificador)}")


# Semilleros: la FK de grupo se selecciona con el catálogo activo que entrega el servicio.
def listar_semilleros(limite: int = 1000):
    return _llamar("GET", "/api/semillero", parametros={"limite": limite}, listado=True)


def obtener_semillero(identificador: int):
    return _llamar("GET", f"/api/semillero/{_id(identificador)}")


def crear_semillero(datos: dict):
    return _llamar("POST", "/api/semillero", datos)


def reemplazar_semillero(identificador: int, datos: dict):
    return _llamar("PUT", f"/api/semillero/{_id(identificador)}", datos)


def actualizar_semillero(identificador: int, datos: dict):
    return _llamar("PATCH", f"/api/semillero/{_id(identificador)}", datos)


def eliminar_semillero(identificador: int):
    return _llamar("DELETE", f"/api/semillero/{_id(identificador)}")


# Participación en grupo: ambas claves viajan por ruta en lectura, reemplazo, PATCH y borrado.
def listar_participaciones_grupo(limite: int = 1000):
    return _llamar("GET", "/api/participa_grupo", parametros={"limite": limite}, listado=True)


def obtener_participacion_grupo(docente_cedula: int, grupo_investigacion_id: int):
    return _llamar("GET", f"/api/participa_grupo/{_id(docente_cedula)}/{_id(grupo_investigacion_id)}")


def crear_participacion_grupo(datos: dict):
    return _llamar("POST", "/api/participa_grupo", datos)


def reemplazar_participacion_grupo(docente_cedula: int, grupo_investigacion_id: int, datos: dict):
    return _llamar("PUT", f"/api/participa_grupo/{_id(docente_cedula)}/{_id(grupo_investigacion_id)}", datos)


def actualizar_participacion_grupo(docente_cedula: int, grupo_investigacion_id: int, datos: dict):
    return _llamar("PATCH", f"/api/participa_grupo/{_id(docente_cedula)}/{_id(grupo_investigacion_id)}", datos)


def eliminar_participacion_grupo(docente_cedula: int, grupo_investigacion_id: int):
    return _llamar("DELETE", f"/api/participa_grupo/{_id(docente_cedula)}/{_id(grupo_investigacion_id)}")


# Participación en semillero: el identificador de ambas entidades se selecciona desde listas activas de la API.
def listar_participaciones_semillero(limite: int = 1000):
    return _llamar("GET", "/api/participa_semillero", parametros={"limite": limite}, listado=True)


def obtener_participacion_semillero(docente: int, semillero: int):
    return _llamar("GET", f"/api/participa_semillero/{_id(docente)}/{_id(semillero)}")


def crear_participacion_semillero(datos: dict):
    return _llamar("POST", "/api/participa_semillero", datos)


def reemplazar_participacion_semillero(docente: int, semillero: int, datos: dict):
    return _llamar("PUT", f"/api/participa_semillero/{_id(docente)}/{_id(semillero)}", datos)


def actualizar_participacion_semillero(docente: int, semillero: int, datos: dict):
    return _llamar("PATCH", f"/api/participa_semillero/{_id(docente)}/{_id(semillero)}", datos)


def eliminar_participacion_semillero(docente: int, semillero: int):
    return _llamar("DELETE", f"/api/participa_semillero/{_id(docente)}/{_id(semillero)}")


# Estas funciones explícitas mantienen rutas y nombres de claves visibles en la capa HTTP del front.
def listar_grupo_linea(limite: int = 1000):
    return _llamar("GET", "/api/grupo_linea", parametros={"limite": limite}, listado=True)


def obtener_grupo_linea(grupo_investigacion: int, linea_investigacion: int):
    return _llamar("GET", f"/api/grupo_linea/{_id(grupo_investigacion)}/{_id(linea_investigacion)}")


def crear_grupo_linea(datos: dict):
    return _llamar("POST", "/api/grupo_linea", datos)


def eliminar_grupo_linea(grupo_investigacion: int, linea_investigacion: int):
    return _llamar("DELETE", f"/api/grupo_linea/{_id(grupo_investigacion)}/{_id(linea_investigacion)}")


def listar_semillero_linea(limite: int = 1000):
    return _llamar("GET", "/api/semillero_linea", parametros={"limite": limite}, listado=True)


def obtener_semillero_linea(semillero: int, linea_investigacion: int):
    return _llamar("GET", f"/api/semillero_linea/{_id(semillero)}/{_id(linea_investigacion)}")


def crear_semillero_linea(datos: dict):
    return _llamar("POST", "/api/semillero_linea", datos)


def eliminar_semillero_linea(semillero: int, linea_investigacion: int):
    return _llamar("DELETE", f"/api/semillero_linea/{_id(semillero)}/{_id(linea_investigacion)}")


def listar_ac_linea(limite: int = 1000):
    return _llamar("GET", "/api/ac_linea", parametros={"limite": limite}, listado=True)


def obtener_ac_linea(linea_investigacion: int, area_conocimiento: str):
    return _llamar("GET", f"/api/ac_linea/{_id(linea_investigacion)}/{_id(area_conocimiento)}")


def crear_ac_linea(datos: dict):
    return _llamar("POST", "/api/ac_linea", datos)


def eliminar_ac_linea(linea_investigacion: int, area_conocimiento: str):
    return _llamar("DELETE", f"/api/ac_linea/{_id(linea_investigacion)}/{_id(area_conocimiento)}")


def listar_ods_linea(limite: int = 1000):
    return _llamar("GET", "/api/ods_linea", parametros={"limite": limite}, listado=True)


def obtener_ods_linea(linea_investigacion: int, ods: int):
    return _llamar("GET", f"/api/ods_linea/{_id(linea_investigacion)}/{_id(ods)}")


def crear_ods_linea(datos: dict):
    return _llamar("POST", "/api/ods_linea", datos)


def eliminar_ods_linea(linea_investigacion: int, ods: int):
    return _llamar("DELETE", f"/api/ods_linea/{_id(linea_investigacion)}/{_id(ods)}")


def listar_aa_linea(limite: int = 1000):
    return _llamar("GET", "/api/aa_linea", parametros={"limite": limite}, listado=True)


def obtener_aa_linea(area_aplicacion: int, linea_investigacion: int):
    return _llamar("GET", f"/api/aa_linea/{_id(area_aplicacion)}/{_id(linea_investigacion)}")


def crear_aa_linea(datos: dict):
    return _llamar("POST", "/api/aa_linea", datos)


def eliminar_aa_linea(area_aplicacion: int, linea_investigacion: int):
    return _llamar("DELETE", f"/api/aa_linea/{_id(area_aplicacion)}/{_id(linea_investigacion)}")


def iniciar_sesion(datos: dict):
    return _llamar("POST", "/api/login", datos, autenticar=False)


# Administración de roles: los adaptadores explícitos conservan cada verbo visible.
def listar_roles(limite: int = 1000):
    return _llamar("GET", "/api/rol", parametros={"limite": limite}, listado=True)


def obtener_rol(identificador: int):
    return _llamar("GET", f"/api/rol/{_id(identificador)}")


def crear_rol(datos: dict):
    return _llamar("POST", "/api/rol", datos)


def reemplazar_rol(identificador: int, datos: dict):
    return _llamar("PUT", f"/api/rol/{_id(identificador)}", datos)


def actualizar_rol(identificador: int, datos: dict):
    return _llamar("PATCH", f"/api/rol/{_id(identificador)}", datos)


def eliminar_rol(identificador: int):
    return _llamar("DELETE", f"/api/rol/{_id(identificador)}")


# Administración de usuarios; el cliente trabaja con JSON y no conoce hashes ni SQL.
def listar_usuarios(limite: int = 1000):
    return _llamar("GET", "/api/usuario", parametros={"limite": limite}, listado=True)


def obtener_usuario(identificador: int):
    return _llamar("GET", f"/api/usuario/{_id(identificador)}")


def crear_usuario(datos: dict):
    return _llamar("POST", "/api/usuario", datos)


def reemplazar_usuario(identificador: int, datos: dict):
    return _llamar("PUT", f"/api/usuario/{_id(identificador)}", datos)


def actualizar_usuario(identificador: int, datos: dict):
    return _llamar("PATCH", f"/api/usuario/{_id(identificador)}", datos)


def eliminar_usuario(identificador: int):
    return _llamar("DELETE", f"/api/usuario/{_id(identificador)}")


# La tabla de asignación no admite PUT/PATCH: su identidad es la pareja usuario-rol.
def listar_asignaciones_rol(limite: int = 1000):
    return _llamar("GET", "/api/rol_usuario", parametros={"limite": limite}, listado=True)


def obtener_asignacion_rol(usuario_id: int, rol_id: int):
    return _llamar("GET", f"/api/rol_usuario/{_id(usuario_id)}/{_id(rol_id)}")


def crear_asignacion_rol(datos: dict):
    return _llamar("POST", "/api/rol_usuario", datos)


def eliminar_asignacion_rol(usuario_id: int, rol_id: int):
    return _llamar("DELETE", f"/api/rol_usuario/{_id(usuario_id)}/{_id(rol_id)}")
