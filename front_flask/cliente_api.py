"""
cliente_api.py — La capa de DATOS del front.

Es al front lo que el repositorio es a la API: la ÚNICA pieza que sabe dónde
viven los datos —en la API, nunca en la base— y la única que habla HTTP.
Traduce cada respuesta a `(ok, datos, errores)` para que las plantillas no
tengan que saber qué es un 422.

======================================================================
UNA FUNCIÓN POR OPERACIÓN, CON EL NOMBRE DEL RECURSO ADENTRO
======================================================================

`listar_areas_conocimiento`, `crear_area_conocimiento`… no una `listar(recurso)` genérica.
Cuando la v2 traiga más tablas habrá más funciones, no un parámetro más — es
la regla de las rutas específicas (sección 6.1 de la metodología del curso),
aplicada del lado del front.

======================================================================
LO QUE ESTE ARCHIVO NO HACE, Y ES LO MÁS IMPORTANTE
======================================================================

No abre ninguna conexión a PostgreSQL. No hay un solo `import asyncpg` en
todo el front, y no lo va a haber: es el artículo de la constitución que dice
que el front no toca la base.

Y aquí la tentación es MAYOR que en otros proyectos, porque **la API también
está en Python** y está en la carpeta de al lado: bastaría un
`sys.path.append("../api_investigacion")` para importar sus modelos y sus
servicios. Funcionaría. Y estaría mal — los dos dejarían de ser procesos
independientes, y renombrar un método adentro de la API rompería el front
**sin que nadie tocara el contrato**.

Por eso este archivo trabaja con **diccionarios**, no con objetos de la API:
lo que llega es lo que el JSON traía, ni más ni menos.
"""

# Carga el modulo o los modulos os.
import os
# Carga el modulo o los modulos re.
import re

# Carga el modulo o los modulos requests.
import requests

# El hostname INTERNO del compose, jamás localhost: dentro de un contenedor,
# localhost es él mismo.
# Asigna a URL_API el valor calculado a la derecha.
URL_API = os.environ.get("URL_API_INVESTIGACION", "http://localhost:8025")
if URL_API and "://" not in URL_API:
    URL_API = "http://" + URL_API

TIEMPO_MAXIMO = float(os.environ.get("TIEMPO_MAXIMO", "10"))  # segundos

# Asigna a NO_DISPONIBLE el valor calculado a la derecha.
NO_DISPONIBLE = ["El servicio no está disponible. ¿Está arriba la API?"]


# Define la funcion _llamar con los parametros declarados; su bloque realiza esta operacion.
def _llamar(metodo: str, ruta: str, **kwargs):
    """Ejecuta la petición y unifica un solo caso: «la API no responde».

    Devuelve None cuando NO hubo respuesta —API caída, tiempo agotado—, que
    es distinto de «respondió con un error». Un 404 es la API funcionando y
    diciendo que esa ficha no existe; un None es que no hay con quién hablar.
    """
    # Importa g, has_request_context desde flask para usar esas definiciones.
    from flask import g, has_request_context
    # Importa SesionTerminada, AccesoDenegado desde errores_seguridad para usar esas definiciones.
    from errores_seguridad import SesionTerminada, AccesoDenegado
    # Ejecuta el bloque siguiente solo cuando se cumple: has_request_context() and getattr(g, 'token_api', None).
    if has_request_context() and getattr(g, 'token_api', None):
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        kwargs['headers'] = {**kwargs.get('headers', {}), 'Authorization': 'Bearer ' + g.token_api}
    # Inicia un bloque cuya excepcion se manejara en los except siguientes.
    try:
        # Asigna a respuesta el valor calculado a la derecha.
        respuesta = requests.request(
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            metodo, f"{URL_API}{ruta}", timeout=TIEMPO_MAXIMO, **kwargs
        # Cierra la estructura abierta en las lineas anteriores.
        )
        # Ejecuta el bloque siguiente solo cuando se cumple: has_request_context() and getattr(g, 'token_api', None).
        if has_request_context() and getattr(g, 'token_api', None):
            # Ejecuta el bloque siguiente solo cuando se cumple: respuesta.status_code == 401.
            if respuesta.status_code == 401:
                # Lanza la excepcion indicada y detiene el flujo normal.
                raise SesionTerminada()
            # Ejecuta el bloque siguiente solo cuando se cumple: respuesta.status_code == 403.
            if respuesta.status_code == 403:
                # Lanza la excepcion indicada y detiene el flujo normal.
                raise AccesoDenegado()
        # Devuelve al llamador el resultado de la expresion indicada.
        return respuesta
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except requests.RequestException:
        # Devuelve al llamador el resultado de la expresion indicada.
        return None


# Define la funcion _cuerpo con los parametros declarados; su bloque realiza esta operacion.
def _cuerpo(respuesta):
    # Ejecuta la instruccion indicada dentro del flujo actual.
    """El JSON, o un diccionario vacío si no vino JSON."""
    # Inicia un bloque cuya excepcion se manejara en los except siguientes.
    try:
        # Devuelve al llamador el resultado de la expresion indicada.
        return respuesta.json()
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except ValueError:
        # Devuelve al llamador el resultado de la expresion indicada.
        return {}


# Define la funcion _mensajes con los parametros declarados; su bloque realiza esta operacion.
def _mensajes(respuesta) -> list[str]:
    """Traduce a texto los errores que produce ESTA API.

    **Es el único sitio del front que conoce el formato del error.** Si
    mañana la API cambia el sobre, se cambia aquí y en ninguna plantilla.

    Hay dos formatos, y no es un descuido: FastAPI valida con Pydantic y
    devuelve el 422 en SU formato —`{"detail": [{"loc": [...], "msg": ...}]}`—
    mientras los demás errores llegan con el sobre del proyecto,
    `{"detail": {"estado", "mensaje", "detalle"}}`. Los dos se traducen
    aquí a una lista de frases en español.
    """
    # Asigna a cuerpo el valor calculado a la derecha.
    cuerpo = _cuerpo(respuesta)
    # Asigna a errores el valor calculado a la derecha.
    errores = cuerpo.get("errores")
    # Ejecuta el bloque siguiente solo cuando se cumple: isinstance(errores, list) and errores.
    if isinstance(errores, list) and errores:
        # Asigna a etiquetas el valor calculado a la derecha.
        etiquetas = ETIQUETAS
        # Asigna a frases el valor calculado a la derecha.
        frases = []
        # Recorre los elementos de la coleccion indicada y ejecuta el bloque para cada uno.
        for error in errores:
            # Asigna a frase el valor calculado a la derecha.
            frase = str(error)
            # Recorre los elementos de la coleccion indicada y ejecuta el bloque para cada uno.
            for campo, etiqueta in etiquetas.items():
                # Asigna a frase el valor calculado a la derecha.
                frase = re.sub(r"\b" + re.escape(campo) + r"\b", etiqueta, frase)
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            frases.append(frase)
        # Devuelve al llamador el resultado de la expresion indicada.
        return frases
    # Asigna a detalle el valor calculado a la derecha.
    detalle = cuerpo.get("detail")

    # El 422 de Pydantic: una entrada por campo que no cumplió.
    # Ejecuta el bloque siguiente solo cuando se cumple: isinstance(detalle, list) and detalle.
    if isinstance(detalle, list) and detalle:
        # Asigna a frases el valor calculado a la derecha.
        frases = []
        # Recorre los elementos de la coleccion indicada y ejecuta el bloque para cada uno.
        for fallo in detalle:
            # Ejecuta el bloque siguiente solo cuando se cumple: not isinstance(fallo, dict).
            if not isinstance(fallo, dict):
                # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                frases.append(str(fallo))
                # Salta al siguiente ciclo de la repeticion.
                continue
            # `loc` viene como ("body", "nombre_del_campo"): la primera parte
            # es ruido para el usuario.
            # Asigna a partes el valor calculado a la derecha.
            partes = [str(p) for p in fallo.get("loc", []) if p != "body"]
            # Asigna a campo el valor calculado a la derecha.
            campo = partes[-1] if partes else ""
            # Asigna a mensaje el valor calculado a la derecha.
            mensaje = fallo.get("msg", "dato inválido")
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            frases.append(_en_espanol(campo, str(mensaje)) if campo else str(mensaje))
        # Devuelve al llamador el resultado de la expresion indicada.
        return frases

    # El sobre del proyecto.
    # Ejecuta el bloque siguiente solo cuando se cumple: isinstance(detalle, dict).
    if isinstance(detalle, dict):
        # Asigna a partes el valor calculado a la derecha.
        partes = [detalle.get("mensaje", ""), detalle.get("detalle", "")]
        # Asigna a partes el valor calculado a la derecha.
        partes = [p for p in partes if p]
        # Ejecuta el bloque siguiente solo cuando se cumple: partes.
        if partes:
            # Devuelve al llamador el resultado de la expresion indicada.
            return partes
    # Ejecuta el bloque siguiente solo cuando se cumple: isinstance(detalle, str) and detalle.
    if isinstance(detalle, str) and detalle:
        # Devuelve al llamador el resultado de la expresion indicada.
        return [detalle]

    # Asigna a partes el valor calculado a la derecha.
    partes = [cuerpo.get("mensaje", ""), cuerpo.get("detalle", "")]
    # Asigna a partes el valor calculado a la derecha.
    partes = [p for p in partes if p]
    # Devuelve al llamador el resultado de la expresion indicada.
    return partes or ["No se pudo completar la operación."]


# ----------------------------------------------------------------------
# DE LA JERGA DE PYDANTIC AL ESPAÑOL DEL USUARIO
# ----------------------------------------------------------------------
#
# FastAPI valida con Pydantic, y Pydantic reporta en inglés y con el nombre
# de la columna: «nombre: String should have at least 1 character».
#
# Eso está bien para quien lee Swagger y está mal delante de un usuario. Es
# un defecto que **solo se ve cuando existe una pantalla** — con la API sola,
# nadie se inmuta.
#
# Se traduce AQUÍ y no en la API porque traducir es trabajo de la capa de
# presentación: la misma API podría atender mañana a un cliente en otro
# idioma, y el mensaje correcto en ese caso no sería éste.

# Cómo se llama cada campo en la pantalla. El usuario nunca ve `cant_graduados`.
# Asigna a ETIQUETAS el valor calculado a la derecha.
ETIQUETAS = {
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    "id": "Código",
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    "gran_area": "Gran área",
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    "area": "Área",
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    "disciplina": "Disciplina",
# Cierra la estructura abierta en las lineas anteriores.
}

# Los mensajes que Pydantic produce con más frecuencia. La comparación es por
# fragmento, no exacta, porque el texto trae el número adentro
# («at least 1 character»).
# Asigna a TRADUCCIONES el valor calculado a la derecha.
TRADUCCIONES = (
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ("field required", "es obligatorio"),
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ("Field required", "es obligatorio"),
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ("String should have at least", "no puede quedar vacío"),
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ("String should have at most", "es demasiado largo"),
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ("Input should be a valid integer", "debe ser un número entero"),
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ("Input should be a valid number", "debe ser un número"),
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ("Input should be a valid date", "debe ser una fecha válida"),
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ("Input should be greater than or equal to 0", "no puede ser negativo"),
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ("Input should be greater than or equal to 1", "debe ser mayor que cero"),
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ("unable to parse string as an integer", "debe ser un número entero"),
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ("unable to parse string as a number", "debe ser un número"),
# Cierra la estructura abierta en las lineas anteriores.
)


# Define la funcion _en_espanol con los parametros declarados; su bloque realiza esta operacion.
def _en_espanol(campo: str, mensaje: str) -> str:
    # Ejecuta la instruccion indicada dentro del flujo actual.
    """Arma la frase que ve el usuario: «Nombre no puede quedar vacío»."""
    # Asigna a etiqueta el valor calculado a la derecha.
    etiqueta = ETIQUETAS.get(campo, campo)
    # Recorre los elementos de la coleccion indicada y ejecuta el bloque para cada uno.
    for ingles, espanol in TRADUCCIONES:
        # Ejecuta el bloque siguiente solo cuando se cumple: ingles in mensaje.
        if ingles in mensaje:
            # Devuelve al llamador el resultado de la expresion indicada.
            return f"{etiqueta} {espanol}."
    # Si es un mensaje que no conocemos, se muestra tal cual: es preferible
    # un texto raro a esconderle al usuario que algo falló.
    # Devuelve al llamador el resultado de la expresion indicada.
    return f"{etiqueta}: {mensaje}"


# Define la funcion _fila_para_pantalla con los parametros declarados; su bloque realiza esta operacion.
def _fila_para_pantalla(fila: dict) -> dict:
    # Ejecuta la instruccion indicada dentro del flujo actual.
    """Adapta el JSON público al nombre local que usan las plantillas."""
    # Asigna a fila el valor calculado a la derecha.
    fila = dict(fila)
    # Ejecuta el bloque siguiente solo cuando se cumple: "granArea" in fila.
    if "granArea" in fila:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        fila["gran_area"] = fila.pop("granArea")
    # Devuelve al llamador el resultado de la expresion indicada.
    return fila


# Define la funcion _datos_para_api con los parametros declarados; su bloque realiza esta operacion.
def _datos_para_api(datos: dict) -> dict:
    # Ejecuta la instruccion indicada dentro del flujo actual.
    """La pantalla conserva snake_case; el contrato HTTP usa granArea."""
    # Asigna a datos el valor calculado a la derecha.
    datos = dict(datos)
    # Ejecuta el bloque siguiente solo cuando se cumple: "gran_area" in datos.
    if "gran_area" in datos:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        datos["granArea"] = datos.pop("gran_area")
    # Devuelve al llamador el resultado de la expresion indicada.
    return datos


# ----------------------------------------------------------------------
# ÁREAS DE CONOCIMIENTO  ·  /api/area_conocimiento
# ----------------------------------------------------------------------


# Define la funcion listar_areas_conocimiento con los parametros declarados; su bloque realiza esta operacion.
def listar_areas_conocimiento(limite: int = 1000):
    # Ejecuta la instruccion indicada dentro del flujo actual.
    """GET → (ok, lista, errores). El 204 es «no hay ninguno», y NO es error."""
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("GET", f"/api/area_conocimiento?limite={limite}")
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, [], NO_DISPONIBLE
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta.status_code == 204.
    if respuesta.status_code == 204:
        # Devuelve al llamador el resultado de la expresion indicada.
        return True, [], []
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta.status_code == 200.
    if respuesta.status_code == 200:
        # Devuelve al llamador el resultado de la expresion indicada.
        return True, [_fila_para_pantalla(fila)
                      # Recorre los elementos de la coleccion indicada y ejecuta el bloque para cada uno.
                      for fila in _cuerpo(respuesta).get("datos", [])], []
    # Devuelve al llamador el resultado de la expresion indicada.
    return False, [], _mensajes(respuesta)


# Define la funcion obtener_area_conocimiento con los parametros declarados; su bloque realiza esta operacion.
def obtener_area_conocimiento(id):
    # Ejecuta la instruccion indicada dentro del flujo actual.
    """GET de una ficha → (ok, diccionario, errores)."""
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("GET", f"/api/area_conocimiento/{id}")
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, None, NO_DISPONIBLE
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta.status_code == 200.
    if respuesta.status_code == 200:
        # Devuelve al llamador el resultado de la expresion indicada.
        return True, _fila_para_pantalla(_cuerpo(respuesta)), []
    # Devuelve al llamador el resultado de la expresion indicada.
    return False, None, _mensajes(respuesta)


# Define la funcion crear_area_conocimiento con los parametros declarados; su bloque realiza esta operacion.
def crear_area_conocimiento(datos: dict):
    # Ejecuta la instruccion indicada dentro del flujo actual.
    """POST → (ok, errores)."""
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("POST", "/api/area_conocimiento", json=_datos_para_api(datos))
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, NO_DISPONIBLE
    # Devuelve al llamador el resultado de la expresion indicada.
    return (True, []) if respuesta.status_code == 200 else (False, _mensajes(respuesta))


# Define la funcion reemplazar_area_conocimiento con los parametros declarados; su bloque realiza esta operacion.
def reemplazar_area_conocimiento(id, datos: dict):
    # Ejecuta la instruccion indicada dentro del flujo actual.
    """PUT — «guardar la ficha completa»: todos los obligatorios viajan."""
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("PUT", f"/api/area_conocimiento/{id}", json=_datos_para_api(datos))
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, NO_DISPONIBLE
    # Devuelve al llamador el resultado de la expresion indicada.
    return (True, []) if respuesta.status_code == 200 else (False, _mensajes(respuesta))


# Define la funcion actualizar_area_conocimiento con los parametros declarados; su bloque realiza esta operacion.
def actualizar_area_conocimiento(id, datos: dict):
    # Ejecuta la instruccion indicada dentro del flujo actual.
    """PATCH — «guardar solo lo que cambié»: viaja solo lo diligenciado."""
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("PATCH", f"/api/area_conocimiento/{id}", json=_datos_para_api(datos))
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, NO_DISPONIBLE
    # Devuelve al llamador el resultado de la expresion indicada.
    return (True, []) if respuesta.status_code == 200 else (False, _mensajes(respuesta))


# Define la funcion eliminar_area_conocimiento con los parametros declarados; su bloque realiza esta operacion.
def eliminar_area_conocimiento(id):
    # Ejecuta la instruccion indicada dentro del flujo actual.
    """DELETE → (ok, errores). Retiro lógico: la ficha deja de listarse."""
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("DELETE", f"/api/area_conocimiento/{id}")
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, NO_DISPONIBLE
    # Devuelve al llamador el resultado de la expresion indicada.
    return (True, []) if respuesta.status_code == 200 else (False, _mensajes(respuesta))


# Importa quote desde urllib.parse para usar esas definiciones.
from urllib.parse import quote

# Define la funcion listar_docente con los parametros declarados; su bloque realiza esta operacion.
def listar_docente(limite: int = 1000):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("GET", f"/api/docente?limite={limite}")
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, [], NO_DISPONIBLE
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta.status_code == 204.
    if respuesta.status_code == 204:
        # Devuelve al llamador el resultado de la expresion indicada.
        return True, [], []
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta.status_code == 200.
    if respuesta.status_code == 200:
        # Devuelve al llamador el resultado de la expresion indicada.
        return True, _cuerpo(respuesta).get("datos", []), []
    # Devuelve al llamador el resultado de la expresion indicada.
    return False, [], _mensajes(respuesta)

# Define la funcion _ruta_docente con los parametros declarados; su bloque realiza esta operacion.
def _ruta_docente(identidad: dict):
    # Devuelve al llamador el resultado de la expresion indicada.
    return "/api/docente/" + "/".join(quote(str(identidad[campo]), safe="") for campo in ('cedula',))

# Define la funcion obtener_docente con los parametros declarados; su bloque realiza esta operacion.
def obtener_docente(identidad: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("GET", _ruta_docente(identidad))
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, None, NO_DISPONIBLE
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta.status_code == 200.
    if respuesta.status_code == 200:
        # Devuelve al llamador el resultado de la expresion indicada.
        return True, _cuerpo(respuesta), []
    # Devuelve al llamador el resultado de la expresion indicada.
    return False, None, _mensajes(respuesta)

# Define la funcion crear_docente con los parametros declarados; su bloque realiza esta operacion.
def crear_docente(datos: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("POST", '/api/docente', json=datos)
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, NO_DISPONIBLE
    # Devuelve al llamador el resultado de la expresion indicada.
    return (True, []) if respuesta.status_code == 200 else (False, _mensajes(respuesta))

# Define la funcion reemplazar_docente con los parametros declarados; su bloque realiza esta operacion.
def reemplazar_docente(identidad: dict, datos: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("PUT", _ruta_docente(identidad), json=datos)
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, NO_DISPONIBLE
    # Devuelve al llamador el resultado de la expresion indicada.
    return (True, []) if respuesta.status_code == 200 else (False, _mensajes(respuesta))

# Define la funcion actualizar_docente con los parametros declarados; su bloque realiza esta operacion.
def actualizar_docente(identidad: dict, datos: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("PATCH", _ruta_docente(identidad), json=datos)
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, NO_DISPONIBLE
    # Devuelve al llamador el resultado de la expresion indicada.
    return (True, []) if respuesta.status_code == 200 else (False, _mensajes(respuesta))

# Define la funcion eliminar_docente con los parametros declarados; su bloque realiza esta operacion.
def eliminar_docente(identidad: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("DELETE", _ruta_docente(identidad))
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, NO_DISPONIBLE
    # Devuelve al llamador el resultado de la expresion indicada.
    return (True, []) if respuesta.status_code == 200 else (False, _mensajes(respuesta))

# Define la funcion listar_grupo_investigacion con los parametros declarados; su bloque realiza esta operacion.
def listar_grupo_investigacion(limite: int = 1000):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("GET", f"/api/grupo_investigacion?limite={limite}")
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, [], NO_DISPONIBLE
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta.status_code == 204.
    if respuesta.status_code == 204:
        # Devuelve al llamador el resultado de la expresion indicada.
        return True, [], []
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta.status_code == 200.
    if respuesta.status_code == 200:
        # Devuelve al llamador el resultado de la expresion indicada.
        return True, _cuerpo(respuesta).get("datos", []), []
    # Devuelve al llamador el resultado de la expresion indicada.
    return False, [], _mensajes(respuesta)

# Define la funcion _ruta_grupo_investigacion con los parametros declarados; su bloque realiza esta operacion.
def _ruta_grupo_investigacion(identidad: dict):
    # Devuelve al llamador el resultado de la expresion indicada.
    return "/api/grupo_investigacion/" + "/".join(quote(str(identidad[campo]), safe="") for campo in ('id',))

# Define la funcion obtener_grupo_investigacion con los parametros declarados; su bloque realiza esta operacion.
def obtener_grupo_investigacion(identidad: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("GET", _ruta_grupo_investigacion(identidad))
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, None, NO_DISPONIBLE
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta.status_code == 200.
    if respuesta.status_code == 200:
        # Devuelve al llamador el resultado de la expresion indicada.
        return True, _cuerpo(respuesta), []
    # Devuelve al llamador el resultado de la expresion indicada.
    return False, None, _mensajes(respuesta)

# Define la funcion crear_grupo_investigacion con los parametros declarados; su bloque realiza esta operacion.
def crear_grupo_investigacion(datos: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("POST", '/api/grupo_investigacion', json=datos)
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, NO_DISPONIBLE
    # Devuelve al llamador el resultado de la expresion indicada.
    return (True, []) if respuesta.status_code == 200 else (False, _mensajes(respuesta))

# Define la funcion reemplazar_grupo_investigacion con los parametros declarados; su bloque realiza esta operacion.
def reemplazar_grupo_investigacion(identidad: dict, datos: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("PUT", _ruta_grupo_investigacion(identidad), json=datos)
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, NO_DISPONIBLE
    # Devuelve al llamador el resultado de la expresion indicada.
    return (True, []) if respuesta.status_code == 200 else (False, _mensajes(respuesta))

# Define la funcion actualizar_grupo_investigacion con los parametros declarados; su bloque realiza esta operacion.
def actualizar_grupo_investigacion(identidad: dict, datos: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("PATCH", _ruta_grupo_investigacion(identidad), json=datos)
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, NO_DISPONIBLE
    # Devuelve al llamador el resultado de la expresion indicada.
    return (True, []) if respuesta.status_code == 200 else (False, _mensajes(respuesta))

# Define la funcion eliminar_grupo_investigacion con los parametros declarados; su bloque realiza esta operacion.
def eliminar_grupo_investigacion(identidad: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("DELETE", _ruta_grupo_investigacion(identidad))
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, NO_DISPONIBLE
    # Devuelve al llamador el resultado de la expresion indicada.
    return (True, []) if respuesta.status_code == 200 else (False, _mensajes(respuesta))

# Define la funcion listar_semillero con los parametros declarados; su bloque realiza esta operacion.
def listar_semillero(limite: int = 1000):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("GET", f"/api/semillero?limite={limite}")
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, [], NO_DISPONIBLE
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta.status_code == 204.
    if respuesta.status_code == 204:
        # Devuelve al llamador el resultado de la expresion indicada.
        return True, [], []
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta.status_code == 200.
    if respuesta.status_code == 200:
        # Devuelve al llamador el resultado de la expresion indicada.
        return True, _cuerpo(respuesta).get("datos", []), []
    # Devuelve al llamador el resultado de la expresion indicada.
    return False, [], _mensajes(respuesta)

# Define la funcion _ruta_semillero con los parametros declarados; su bloque realiza esta operacion.
def _ruta_semillero(identidad: dict):
    # Devuelve al llamador el resultado de la expresion indicada.
    return "/api/semillero/" + "/".join(quote(str(identidad[campo]), safe="") for campo in ('id',))

# Define la funcion obtener_semillero con los parametros declarados; su bloque realiza esta operacion.
def obtener_semillero(identidad: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("GET", _ruta_semillero(identidad))
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, None, NO_DISPONIBLE
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta.status_code == 200.
    if respuesta.status_code == 200:
        # Devuelve al llamador el resultado de la expresion indicada.
        return True, _cuerpo(respuesta), []
    # Devuelve al llamador el resultado de la expresion indicada.
    return False, None, _mensajes(respuesta)

# Define la funcion crear_semillero con los parametros declarados; su bloque realiza esta operacion.
def crear_semillero(datos: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("POST", '/api/semillero', json=datos)
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, NO_DISPONIBLE
    # Devuelve al llamador el resultado de la expresion indicada.
    return (True, []) if respuesta.status_code == 200 else (False, _mensajes(respuesta))

# Define la funcion reemplazar_semillero con los parametros declarados; su bloque realiza esta operacion.
def reemplazar_semillero(identidad: dict, datos: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("PUT", _ruta_semillero(identidad), json=datos)
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, NO_DISPONIBLE
    # Devuelve al llamador el resultado de la expresion indicada.
    return (True, []) if respuesta.status_code == 200 else (False, _mensajes(respuesta))

# Define la funcion actualizar_semillero con los parametros declarados; su bloque realiza esta operacion.
def actualizar_semillero(identidad: dict, datos: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("PATCH", _ruta_semillero(identidad), json=datos)
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, NO_DISPONIBLE
    # Devuelve al llamador el resultado de la expresion indicada.
    return (True, []) if respuesta.status_code == 200 else (False, _mensajes(respuesta))

# Define la funcion eliminar_semillero con los parametros declarados; su bloque realiza esta operacion.
def eliminar_semillero(identidad: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("DELETE", _ruta_semillero(identidad))
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, NO_DISPONIBLE
    # Devuelve al llamador el resultado de la expresion indicada.
    return (True, []) if respuesta.status_code == 200 else (False, _mensajes(respuesta))

# Define la funcion listar_participa_semillero con los parametros declarados; su bloque realiza esta operacion.
def listar_participa_semillero(limite: int = 1000):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("GET", f"/api/participa_semillero?limite={limite}")
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, [], NO_DISPONIBLE
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta.status_code == 204.
    if respuesta.status_code == 204:
        # Devuelve al llamador el resultado de la expresion indicada.
        return True, [], []
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta.status_code == 200.
    if respuesta.status_code == 200:
        # Devuelve al llamador el resultado de la expresion indicada.
        return True, _cuerpo(respuesta).get("datos", []), []
    # Devuelve al llamador el resultado de la expresion indicada.
    return False, [], _mensajes(respuesta)

# Define la funcion _ruta_participa_semillero con los parametros declarados; su bloque realiza esta operacion.
def _ruta_participa_semillero(identidad: dict):
    # Devuelve al llamador el resultado de la expresion indicada.
    return "/api/participa_semillero/" + "/".join(quote(str(identidad[campo]), safe="") for campo in ('docente', 'semillero'))

# Define la funcion obtener_participa_semillero con los parametros declarados; su bloque realiza esta operacion.
def obtener_participa_semillero(identidad: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("GET", _ruta_participa_semillero(identidad))
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, None, NO_DISPONIBLE
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta.status_code == 200.
    if respuesta.status_code == 200:
        # Devuelve al llamador el resultado de la expresion indicada.
        return True, _cuerpo(respuesta), []
    # Devuelve al llamador el resultado de la expresion indicada.
    return False, None, _mensajes(respuesta)

# Define la funcion crear_participa_semillero con los parametros declarados; su bloque realiza esta operacion.
def crear_participa_semillero(datos: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("POST", '/api/participa_semillero', json=datos)
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, NO_DISPONIBLE
    # Devuelve al llamador el resultado de la expresion indicada.
    return (True, []) if respuesta.status_code == 200 else (False, _mensajes(respuesta))

# Define la funcion reemplazar_participa_semillero con los parametros declarados; su bloque realiza esta operacion.
def reemplazar_participa_semillero(identidad: dict, datos: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("PUT", _ruta_participa_semillero(identidad), json=datos)
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, NO_DISPONIBLE
    # Devuelve al llamador el resultado de la expresion indicada.
    return (True, []) if respuesta.status_code == 200 else (False, _mensajes(respuesta))

# Define la funcion actualizar_participa_semillero con los parametros declarados; su bloque realiza esta operacion.
def actualizar_participa_semillero(identidad: dict, datos: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("PATCH", _ruta_participa_semillero(identidad), json=datos)
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, NO_DISPONIBLE
    # Devuelve al llamador el resultado de la expresion indicada.
    return (True, []) if respuesta.status_code == 200 else (False, _mensajes(respuesta))

# Define la funcion eliminar_participa_semillero con los parametros declarados; su bloque realiza esta operacion.
def eliminar_participa_semillero(identidad: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("DELETE", _ruta_participa_semillero(identidad))
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, NO_DISPONIBLE
    # Devuelve al llamador el resultado de la expresion indicada.
    return (True, []) if respuesta.status_code == 200 else (False, _mensajes(respuesta))

# Define la funcion listar_participa_grupo con los parametros declarados; su bloque realiza esta operacion.
def listar_participa_grupo(limite: int = 1000):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("GET", f"/api/participa_grupo?limite={limite}")
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, [], NO_DISPONIBLE
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta.status_code == 204.
    if respuesta.status_code == 204:
        # Devuelve al llamador el resultado de la expresion indicada.
        return True, [], []
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta.status_code == 200.
    if respuesta.status_code == 200:
        # Devuelve al llamador el resultado de la expresion indicada.
        return True, _cuerpo(respuesta).get("datos", []), []
    # Devuelve al llamador el resultado de la expresion indicada.
    return False, [], _mensajes(respuesta)

# Define la funcion _ruta_participa_grupo con los parametros declarados; su bloque realiza esta operacion.
def _ruta_participa_grupo(identidad: dict):
    # Devuelve al llamador el resultado de la expresion indicada.
    return "/api/participa_grupo/" + "/".join(quote(str(identidad[campo]), safe="") for campo in ('docente_cedula', 'grupo_investigacion_id'))

# Define la funcion obtener_participa_grupo con los parametros declarados; su bloque realiza esta operacion.
def obtener_participa_grupo(identidad: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("GET", _ruta_participa_grupo(identidad))
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, None, NO_DISPONIBLE
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta.status_code == 200.
    if respuesta.status_code == 200:
        # Devuelve al llamador el resultado de la expresion indicada.
        return True, _cuerpo(respuesta), []
    # Devuelve al llamador el resultado de la expresion indicada.
    return False, None, _mensajes(respuesta)

# Define la funcion crear_participa_grupo con los parametros declarados; su bloque realiza esta operacion.
def crear_participa_grupo(datos: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("POST", '/api/participa_grupo', json=datos)
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, NO_DISPONIBLE
    # Devuelve al llamador el resultado de la expresion indicada.
    return (True, []) if respuesta.status_code == 200 else (False, _mensajes(respuesta))

# Define la funcion reemplazar_participa_grupo con los parametros declarados; su bloque realiza esta operacion.
def reemplazar_participa_grupo(identidad: dict, datos: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("PUT", _ruta_participa_grupo(identidad), json=datos)
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, NO_DISPONIBLE
    # Devuelve al llamador el resultado de la expresion indicada.
    return (True, []) if respuesta.status_code == 200 else (False, _mensajes(respuesta))

# Define la funcion actualizar_participa_grupo con los parametros declarados; su bloque realiza esta operacion.
def actualizar_participa_grupo(identidad: dict, datos: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("PATCH", _ruta_participa_grupo(identidad), json=datos)
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, NO_DISPONIBLE
    # Devuelve al llamador el resultado de la expresion indicada.
    return (True, []) if respuesta.status_code == 200 else (False, _mensajes(respuesta))

# Define la funcion eliminar_participa_grupo con los parametros declarados; su bloque realiza esta operacion.
def eliminar_participa_grupo(identidad: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("DELETE", _ruta_participa_grupo(identidad))
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, NO_DISPONIBLE
    # Devuelve al llamador el resultado de la expresion indicada.
    return (True, []) if respuesta.status_code == 200 else (False, _mensajes(respuesta))

# Define la funcion listar_semillero_linea con los parametros declarados; su bloque realiza esta operacion.
def listar_semillero_linea(limite: int = 1000):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("GET", f"/api/semillero_linea?limite={limite}")
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, [], NO_DISPONIBLE
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta.status_code == 204.
    if respuesta.status_code == 204:
        # Devuelve al llamador el resultado de la expresion indicada.
        return True, [], []
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta.status_code == 200.
    if respuesta.status_code == 200:
        # Devuelve al llamador el resultado de la expresion indicada.
        return True, _cuerpo(respuesta).get("datos", []), []
    # Devuelve al llamador el resultado de la expresion indicada.
    return False, [], _mensajes(respuesta)

# Define la funcion _ruta_semillero_linea con los parametros declarados; su bloque realiza esta operacion.
def _ruta_semillero_linea(identidad: dict):
    # Devuelve al llamador el resultado de la expresion indicada.
    return "/api/semillero_linea/" + "/".join(quote(str(identidad[campo]), safe="") for campo in ('semillero', 'linea_investigacion'))

# Define la funcion obtener_semillero_linea con los parametros declarados; su bloque realiza esta operacion.
def obtener_semillero_linea(identidad: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("GET", _ruta_semillero_linea(identidad))
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, None, NO_DISPONIBLE
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta.status_code == 200.
    if respuesta.status_code == 200:
        # Devuelve al llamador el resultado de la expresion indicada.
        return True, _cuerpo(respuesta), []
    # Devuelve al llamador el resultado de la expresion indicada.
    return False, None, _mensajes(respuesta)

# Define la funcion crear_semillero_linea con los parametros declarados; su bloque realiza esta operacion.
def crear_semillero_linea(datos: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("POST", '/api/semillero_linea', json=datos)
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, NO_DISPONIBLE
    # Devuelve al llamador el resultado de la expresion indicada.
    return (True, []) if respuesta.status_code == 200 else (False, _mensajes(respuesta))

# Define la funcion reemplazar_semillero_linea con los parametros declarados; su bloque realiza esta operacion.
def reemplazar_semillero_linea(identidad: dict, datos: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("PUT", _ruta_semillero_linea(identidad), json=datos)
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, NO_DISPONIBLE
    # Devuelve al llamador el resultado de la expresion indicada.
    return (True, []) if respuesta.status_code == 200 else (False, _mensajes(respuesta))

# Define la funcion actualizar_semillero_linea con los parametros declarados; su bloque realiza esta operacion.
def actualizar_semillero_linea(identidad: dict, datos: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("PATCH", _ruta_semillero_linea(identidad), json=datos)
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, NO_DISPONIBLE
    # Devuelve al llamador el resultado de la expresion indicada.
    return (True, []) if respuesta.status_code == 200 else (False, _mensajes(respuesta))

# Define la funcion eliminar_semillero_linea con los parametros declarados; su bloque realiza esta operacion.
def eliminar_semillero_linea(identidad: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("DELETE", _ruta_semillero_linea(identidad))
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, NO_DISPONIBLE
    # Devuelve al llamador el resultado de la expresion indicada.
    return (True, []) if respuesta.status_code == 200 else (False, _mensajes(respuesta))

# Define la funcion listar_grupo_linea con los parametros declarados; su bloque realiza esta operacion.
def listar_grupo_linea(limite: int = 1000):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("GET", f"/api/grupo_linea?limite={limite}")
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, [], NO_DISPONIBLE
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta.status_code == 204.
    if respuesta.status_code == 204:
        # Devuelve al llamador el resultado de la expresion indicada.
        return True, [], []
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta.status_code == 200.
    if respuesta.status_code == 200:
        # Devuelve al llamador el resultado de la expresion indicada.
        return True, _cuerpo(respuesta).get("datos", []), []
    # Devuelve al llamador el resultado de la expresion indicada.
    return False, [], _mensajes(respuesta)

# Define la funcion _ruta_grupo_linea con los parametros declarados; su bloque realiza esta operacion.
def _ruta_grupo_linea(identidad: dict):
    # Devuelve al llamador el resultado de la expresion indicada.
    return "/api/grupo_linea/" + "/".join(quote(str(identidad[campo]), safe="") for campo in ('grupo_investigacion', 'linea_investigacion'))

# Define la funcion obtener_grupo_linea con los parametros declarados; su bloque realiza esta operacion.
def obtener_grupo_linea(identidad: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("GET", _ruta_grupo_linea(identidad))
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, None, NO_DISPONIBLE
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta.status_code == 200.
    if respuesta.status_code == 200:
        # Devuelve al llamador el resultado de la expresion indicada.
        return True, _cuerpo(respuesta), []
    # Devuelve al llamador el resultado de la expresion indicada.
    return False, None, _mensajes(respuesta)

# Define la funcion crear_grupo_linea con los parametros declarados; su bloque realiza esta operacion.
def crear_grupo_linea(datos: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("POST", '/api/grupo_linea', json=datos)
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, NO_DISPONIBLE
    # Devuelve al llamador el resultado de la expresion indicada.
    return (True, []) if respuesta.status_code == 200 else (False, _mensajes(respuesta))

# Define la funcion reemplazar_grupo_linea con los parametros declarados; su bloque realiza esta operacion.
def reemplazar_grupo_linea(identidad: dict, datos: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("PUT", _ruta_grupo_linea(identidad), json=datos)
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, NO_DISPONIBLE
    # Devuelve al llamador el resultado de la expresion indicada.
    return (True, []) if respuesta.status_code == 200 else (False, _mensajes(respuesta))

# Define la funcion actualizar_grupo_linea con los parametros declarados; su bloque realiza esta operacion.
def actualizar_grupo_linea(identidad: dict, datos: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("PATCH", _ruta_grupo_linea(identidad), json=datos)
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, NO_DISPONIBLE
    # Devuelve al llamador el resultado de la expresion indicada.
    return (True, []) if respuesta.status_code == 200 else (False, _mensajes(respuesta))

# Define la funcion eliminar_grupo_linea con los parametros declarados; su bloque realiza esta operacion.
def eliminar_grupo_linea(identidad: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("DELETE", _ruta_grupo_linea(identidad))
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, NO_DISPONIBLE
    # Devuelve al llamador el resultado de la expresion indicada.
    return (True, []) if respuesta.status_code == 200 else (False, _mensajes(respuesta))

# Define la funcion listar_ac_linea con los parametros declarados; su bloque realiza esta operacion.
def listar_ac_linea(limite: int = 1000):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("GET", f"/api/ac_linea?limite={limite}")
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, [], NO_DISPONIBLE
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta.status_code == 204.
    if respuesta.status_code == 204:
        # Devuelve al llamador el resultado de la expresion indicada.
        return True, [], []
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta.status_code == 200.
    if respuesta.status_code == 200:
        # Devuelve al llamador el resultado de la expresion indicada.
        return True, _cuerpo(respuesta).get("datos", []), []
    # Devuelve al llamador el resultado de la expresion indicada.
    return False, [], _mensajes(respuesta)

# Define la funcion _ruta_ac_linea con los parametros declarados; su bloque realiza esta operacion.
def _ruta_ac_linea(identidad: dict):
    # Devuelve al llamador el resultado de la expresion indicada.
    return "/api/ac_linea/" + "/".join(quote(str(identidad[campo]), safe="") for campo in ('linea_investigacion', 'area_conocimiento'))

# Define la funcion obtener_ac_linea con los parametros declarados; su bloque realiza esta operacion.
def obtener_ac_linea(identidad: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("GET", _ruta_ac_linea(identidad))
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, None, NO_DISPONIBLE
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta.status_code == 200.
    if respuesta.status_code == 200:
        # Devuelve al llamador el resultado de la expresion indicada.
        return True, _cuerpo(respuesta), []
    # Devuelve al llamador el resultado de la expresion indicada.
    return False, None, _mensajes(respuesta)

# Define la funcion crear_ac_linea con los parametros declarados; su bloque realiza esta operacion.
def crear_ac_linea(datos: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("POST", '/api/ac_linea', json=datos)
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, NO_DISPONIBLE
    # Devuelve al llamador el resultado de la expresion indicada.
    return (True, []) if respuesta.status_code == 200 else (False, _mensajes(respuesta))

# Define la funcion reemplazar_ac_linea con los parametros declarados; su bloque realiza esta operacion.
def reemplazar_ac_linea(identidad: dict, datos: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("PUT", _ruta_ac_linea(identidad), json=datos)
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, NO_DISPONIBLE
    # Devuelve al llamador el resultado de la expresion indicada.
    return (True, []) if respuesta.status_code == 200 else (False, _mensajes(respuesta))

# Define la funcion actualizar_ac_linea con los parametros declarados; su bloque realiza esta operacion.
def actualizar_ac_linea(identidad: dict, datos: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("PATCH", _ruta_ac_linea(identidad), json=datos)
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, NO_DISPONIBLE
    # Devuelve al llamador el resultado de la expresion indicada.
    return (True, []) if respuesta.status_code == 200 else (False, _mensajes(respuesta))

# Define la funcion eliminar_ac_linea con los parametros declarados; su bloque realiza esta operacion.
def eliminar_ac_linea(identidad: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("DELETE", _ruta_ac_linea(identidad))
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, NO_DISPONIBLE
    # Devuelve al llamador el resultado de la expresion indicada.
    return (True, []) if respuesta.status_code == 200 else (False, _mensajes(respuesta))

# Define la funcion listar_ods_linea con los parametros declarados; su bloque realiza esta operacion.
def listar_ods_linea(limite: int = 1000):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("GET", f"/api/ods_linea?limite={limite}")
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, [], NO_DISPONIBLE
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta.status_code == 204.
    if respuesta.status_code == 204:
        # Devuelve al llamador el resultado de la expresion indicada.
        return True, [], []
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta.status_code == 200.
    if respuesta.status_code == 200:
        # Devuelve al llamador el resultado de la expresion indicada.
        return True, _cuerpo(respuesta).get("datos", []), []
    # Devuelve al llamador el resultado de la expresion indicada.
    return False, [], _mensajes(respuesta)

# Define la funcion _ruta_ods_linea con los parametros declarados; su bloque realiza esta operacion.
def _ruta_ods_linea(identidad: dict):
    # Devuelve al llamador el resultado de la expresion indicada.
    return "/api/ods_linea/" + "/".join(quote(str(identidad[campo]), safe="") for campo in ('linea_investigacion', 'ods'))

# Define la funcion obtener_ods_linea con los parametros declarados; su bloque realiza esta operacion.
def obtener_ods_linea(identidad: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("GET", _ruta_ods_linea(identidad))
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, None, NO_DISPONIBLE
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta.status_code == 200.
    if respuesta.status_code == 200:
        # Devuelve al llamador el resultado de la expresion indicada.
        return True, _cuerpo(respuesta), []
    # Devuelve al llamador el resultado de la expresion indicada.
    return False, None, _mensajes(respuesta)

# Define la funcion crear_ods_linea con los parametros declarados; su bloque realiza esta operacion.
def crear_ods_linea(datos: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("POST", '/api/ods_linea', json=datos)
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, NO_DISPONIBLE
    # Devuelve al llamador el resultado de la expresion indicada.
    return (True, []) if respuesta.status_code == 200 else (False, _mensajes(respuesta))

# Define la funcion reemplazar_ods_linea con los parametros declarados; su bloque realiza esta operacion.
def reemplazar_ods_linea(identidad: dict, datos: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("PUT", _ruta_ods_linea(identidad), json=datos)
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, NO_DISPONIBLE
    # Devuelve al llamador el resultado de la expresion indicada.
    return (True, []) if respuesta.status_code == 200 else (False, _mensajes(respuesta))

# Define la funcion actualizar_ods_linea con los parametros declarados; su bloque realiza esta operacion.
def actualizar_ods_linea(identidad: dict, datos: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("PATCH", _ruta_ods_linea(identidad), json=datos)
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, NO_DISPONIBLE
    # Devuelve al llamador el resultado de la expresion indicada.
    return (True, []) if respuesta.status_code == 200 else (False, _mensajes(respuesta))

# Define la funcion eliminar_ods_linea con los parametros declarados; su bloque realiza esta operacion.
def eliminar_ods_linea(identidad: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("DELETE", _ruta_ods_linea(identidad))
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, NO_DISPONIBLE
    # Devuelve al llamador el resultado de la expresion indicada.
    return (True, []) if respuesta.status_code == 200 else (False, _mensajes(respuesta))

# Define la funcion listar_aa_linea con los parametros declarados; su bloque realiza esta operacion.
def listar_aa_linea(limite: int = 1000):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("GET", f"/api/aa_linea?limite={limite}")
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, [], NO_DISPONIBLE
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta.status_code == 204.
    if respuesta.status_code == 204:
        # Devuelve al llamador el resultado de la expresion indicada.
        return True, [], []
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta.status_code == 200.
    if respuesta.status_code == 200:
        # Devuelve al llamador el resultado de la expresion indicada.
        return True, _cuerpo(respuesta).get("datos", []), []
    # Devuelve al llamador el resultado de la expresion indicada.
    return False, [], _mensajes(respuesta)

# Define la funcion _ruta_aa_linea con los parametros declarados; su bloque realiza esta operacion.
def _ruta_aa_linea(identidad: dict):
    # Devuelve al llamador el resultado de la expresion indicada.
    return "/api/aa_linea/" + "/".join(quote(str(identidad[campo]), safe="") for campo in ('area_aplicacion', 'linea_investigacion'))

# Define la funcion obtener_aa_linea con los parametros declarados; su bloque realiza esta operacion.
def obtener_aa_linea(identidad: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("GET", _ruta_aa_linea(identidad))
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, None, NO_DISPONIBLE
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta.status_code == 200.
    if respuesta.status_code == 200:
        # Devuelve al llamador el resultado de la expresion indicada.
        return True, _cuerpo(respuesta), []
    # Devuelve al llamador el resultado de la expresion indicada.
    return False, None, _mensajes(respuesta)

# Define la funcion crear_aa_linea con los parametros declarados; su bloque realiza esta operacion.
def crear_aa_linea(datos: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("POST", '/api/aa_linea', json=datos)
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, NO_DISPONIBLE
    # Devuelve al llamador el resultado de la expresion indicada.
    return (True, []) if respuesta.status_code == 200 else (False, _mensajes(respuesta))

# Define la funcion reemplazar_aa_linea con los parametros declarados; su bloque realiza esta operacion.
def reemplazar_aa_linea(identidad: dict, datos: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("PUT", _ruta_aa_linea(identidad), json=datos)
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, NO_DISPONIBLE
    # Devuelve al llamador el resultado de la expresion indicada.
    return (True, []) if respuesta.status_code == 200 else (False, _mensajes(respuesta))

# Define la funcion actualizar_aa_linea con los parametros declarados; su bloque realiza esta operacion.
def actualizar_aa_linea(identidad: dict, datos: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("PATCH", _ruta_aa_linea(identidad), json=datos)
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, NO_DISPONIBLE
    # Devuelve al llamador el resultado de la expresion indicada.
    return (True, []) if respuesta.status_code == 200 else (False, _mensajes(respuesta))

# Define la funcion eliminar_aa_linea con los parametros declarados; su bloque realiza esta operacion.
def eliminar_aa_linea(identidad: dict):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("DELETE", _ruta_aa_linea(identidad))
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, NO_DISPONIBLE
    # Devuelve al llamador el resultado de la expresion indicada.
    return (True, []) if respuesta.status_code == 200 else (False, _mensajes(respuesta))

# Define la funcion listar_universidad con los parametros declarados; su bloque realiza esta operacion.
def listar_universidad(limite: int = 1000):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("GET", f"/api/universidad?limite={limite}")
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, [], NO_DISPONIBLE
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta.status_code == 204.
    if respuesta.status_code == 204:
        # Devuelve al llamador el resultado de la expresion indicada.
        return True, [], []
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta.status_code == 200.
    if respuesta.status_code == 200:
        # Devuelve al llamador el resultado de la expresion indicada.
        return True, _cuerpo(respuesta).get("datos", []), []
    # Devuelve al llamador el resultado de la expresion indicada.
    return False, [], _mensajes(respuesta)

# Define la funcion listar_linea_investigacion con los parametros declarados; su bloque realiza esta operacion.
def listar_linea_investigacion(limite: int = 1000):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("GET", f"/api/linea_investigacion?limite={limite}")
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, [], NO_DISPONIBLE
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta.status_code == 204.
    if respuesta.status_code == 204:
        # Devuelve al llamador el resultado de la expresion indicada.
        return True, [], []
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta.status_code == 200.
    if respuesta.status_code == 200:
        # Devuelve al llamador el resultado de la expresion indicada.
        return True, _cuerpo(respuesta).get("datos", []), []
    # Devuelve al llamador el resultado de la expresion indicada.
    return False, [], _mensajes(respuesta)

# Define la funcion listar_objetivo_desarrollo_sostenible con los parametros declarados; su bloque realiza esta operacion.
def listar_objetivo_desarrollo_sostenible(limite: int = 1000):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("GET", f"/api/objetivo_desarrollo_sostenible?limite={limite}")
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, [], NO_DISPONIBLE
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta.status_code == 204.
    if respuesta.status_code == 204:
        # Devuelve al llamador el resultado de la expresion indicada.
        return True, [], []
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta.status_code == 200.
    if respuesta.status_code == 200:
        # Devuelve al llamador el resultado de la expresion indicada.
        return True, _cuerpo(respuesta).get("datos", []), []
    # Devuelve al llamador el resultado de la expresion indicada.
    return False, [], _mensajes(respuesta)

# Define la funcion listar_area_aplicacion con los parametros declarados; su bloque realiza esta operacion.
def listar_area_aplicacion(limite: int = 1000):
    # Asigna a respuesta el valor calculado a la derecha.
    respuesta = _llamar("GET", f"/api/area_aplicacion?limite={limite}")
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta is None.
    if respuesta is None:
        # Devuelve al llamador el resultado de la expresion indicada.
        return False, [], NO_DISPONIBLE
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta.status_code == 204.
    if respuesta.status_code == 204:
        # Devuelve al llamador el resultado de la expresion indicada.
        return True, [], []
    # Ejecuta el bloque siguiente solo cuando se cumple: respuesta.status_code == 200.
    if respuesta.status_code == 200:
        # Devuelve al llamador el resultado de la expresion indicada.
        return True, _cuerpo(respuesta).get("datos", []), []
    # Devuelve al llamador el resultado de la expresion indicada.
    return False, [], _mensajes(respuesta)


# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
ETIQUETAS.update({'id': 'Id', 'gran_area': 'Gran area', 'area': 'Area', 'disciplina': 'Disciplina', 'nombre': 'Nombre', 'categoria': 'Categoria', 'tipo': 'Tipo', 'ciudad': 'Ciudad', 'descripcion': 'Descripcion', 'cedula': 'Cedula', 'nombres': 'Nombres', 'apellidos': 'Apellidos', 'genero': 'Genero', 'cargo': 'Cargo', 'fecha_nacimiento': 'Fecha nacimiento', 'correo': 'Correo', 'telefono': 'Telefono', 'url_cvlac': 'Url cvlac', 'fecha_actualizacion': 'Fecha actualizacion', 'escalafon': 'Escalafon', 'perfil': 'Perfil', 'cat_minciencia': 'Cat minciencia', 'conv_minciencia': 'Conv minciencia', 'nacionalidaad': 'Nacionalidad', 'linea_investigacion_principal': 'Linea investigacion principal', 'url_gruplac': 'Url gruplac', 'convocatoria': 'Convocatoria', 'fecha_fundacion': 'Fecha fundacion', 'universidsad': 'Universidad', 'interno': 'Interno', 'ambito': 'Ambito', 'grupo_investigacion': 'Grupo investigacion', 'docente': 'Docente', 'semillero': 'Semillero', 'rol': 'Rol', 'fecha_inicio': 'Fecha inicio', 'fecha_fin': 'Fecha fin', 'docente_cedula': 'Docente', 'grupo_investigacion_id': 'Grupo de investigación', 'linea_investigacion': 'Linea investigacion', 'area_conocimiento': 'Area conocimiento', 'ods': 'Objetivo de desarrollo sostenible', 'area_aplicacion': 'Area aplicacion'})
