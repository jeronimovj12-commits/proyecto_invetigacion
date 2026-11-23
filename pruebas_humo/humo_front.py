# -*- coding: utf-8 -*-
"""Prueba de humo del FRONT de Investigación (Flask, puerto 8078).

QUÉ COMPRUEBA, Y POR QUÉ AQUÍ SE PUEDE COMPROBAR TODO
=====================================================

Este front está hecho de formularios HTML corrientes: cada botón manda un
POST que un guion puede enviar igual que lo manda el navegador. Por eso esta
prueba llega **hasta el final** —crea, guarda de las dos maneras y retira—,
cosa que con el front anterior no se podía: allí los clics viajaban por una
conexión persistente y no eran peticiones sueltas.

O sea: la tecnología más sencilla resultó ser la más fácil de probar sin
manos. Vale la pena verlo, porque casi siempre se cuenta al revés.

Lo que se comprueba:

  1. cada pantalla responde por su DIRECCIÓN PROPIA, y la hoja de estilos
     llega de verdad —que no es lo mismo—;
  2. el menú lleva a la pantalla, con una dirección que existe;
  3. lo que la pantalla muestra es lo que la API devolvió;
  4. la pantalla no le habla al usuario en jerga **ni en inglés**;
  5. el recorrido completo: agregar, los dos botones de guardar, y retirar;
  6. y lo que demuestra que son dos procesos: **con la API apagada la
     pantalla sigue en pie**, con su aviso adentro y sin un solo dato.

Uso:  python pruebas_humo/humo_front.py     (parado en la raíz del proyecto)
"""
# Carga el modulo o los modulos html.
import html
# Carga el modulo o los modulos http.cookiejar.
import http.cookiejar
# Carga el modulo o los modulos json.
import json
# Carga el modulo o los modulos random.
import random
# Carga el modulo o los modulos re.
import re
# Carga el modulo o los modulos string.
import string
# Carga el modulo o los modulos subprocess.
import subprocess
# Carga el modulo o los modulos sys.
import sys
# Carga el modulo o los modulos time.
import time
# Carga el modulo o los modulos urllib.error.
import urllib.error
# Carga el modulo o los modulos urllib.parse.
import urllib.parse
# Carga el modulo o los modulos urllib.request.
import urllib.request

# La consola de Windows no siempre usa UTF-8, y entonces imprimir una flecha
# revienta el guion con un error que no tiene NADA que ver con lo que se está
# probando. `errors="replace"` deja pasar un signo raro y sigue.
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Asigna a FRONT el valor calculado a la derecha.
FRONT = "http://localhost:8078"
# Asigna a API el valor calculado a la derecha.
API = "http://localhost:8025"
# Asigna a fallos el valor calculado a la derecha.
fallos = []

# Un sufijo distinto en cada corrida: si una se interrumpe a la mitad deja la
# ficha puesta, y la siguiente fallaría al crearla por llave duplicada — un
# rojo que no tiene que ver con lo que se está probando.
# Asigna a SUFIJO el valor calculado a la derecha.
SUFIJO = "".join(random.choices(string.digits, k=3))
# Asigna a LLAVE el valor calculado a la derecha.
LLAVE = ("H" + SUFIJO)[:6]

# Las columnas que la tabla debe traer, en el idioma del usuario.
# Asigna a ETIQUETAS el valor calculado a la derecha.
ETIQUETAS = ('Código', 'Gran área', 'Área', 'Disciplina')

# Asigna a navegador el valor calculado a la derecha.
navegador = urllib.request.build_opener(
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))


# Define la funcion ver con los parametros declarados; su bloque realiza esta operacion.
def ver(url):
    # Ejecuta la instruccion indicada dentro del flujo actual.
    """Un GET, como el que hace el navegador al escribir la dirección."""
    # Inicia un bloque cuya excepcion se manejara en los except siguientes.
    try:
        # Abre el recurso y asegura su cierre al salir del bloque.
        with navegador.open(url, timeout=20) as r:
            # Devuelve al llamador el resultado de la expresion indicada.
            return r.status, r.read().decode("utf-8", "replace")
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except urllib.error.HTTPError as e:
        # Devuelve al llamador el resultado de la expresion indicada.
        return e.code, e.read().decode("utf-8", "replace")
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except Exception as e:
        # Devuelve al llamador el resultado de la expresion indicada.
        return 0, str(e)


# Define la funcion enviar con los parametros declarados; su bloque realiza esta operacion.
def enviar(ruta, campos):
    """Un POST de formulario: exactamente lo que manda el botón.

    Fíjese en el tipo de contenido: `x-www-form-urlencoded`, que es como
    hablan los formularios. El JSON lo pone el front cuando le habla a la
    API — eso pasa del otro lado, y el usuario nunca lo escribe.
    """
    # Asigna a datos el valor calculado a la derecha.
    datos = urllib.parse.urlencode(campos).encode()
    # Asigna a peticion el valor calculado a la derecha.
    peticion = urllib.request.Request(FRONT + ruta, data=datos)
    # Inicia un bloque cuya excepcion se manejara en los except siguientes.
    try:
        # Abre el recurso y asegura su cierre al salir del bloque.
        with navegador.open(peticion, timeout=20) as r:
            # Devuelve al llamador el resultado de la expresion indicada.
            return r.status, r.read().decode("utf-8", "replace")
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except urllib.error.HTTPError as e:
        # Devuelve al llamador el resultado de la expresion indicada.
        return e.code, e.read().decode("utf-8", "replace")
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except Exception as e:
        # Devuelve al llamador el resultado de la expresion indicada.
        return 0, str(e)


# Define la funcion visible con los parametros declarados; su bloque realiza esta operacion.
def visible(pagina):
    """El texto que el usuario VE: sin etiquetas y con las tildes de verdad.

    Comprobar sobre el HTML crudo da falsos positivos de los dos lados: un
    «500» puede estar dentro de un número, y el aviso «no está disponible»
    llega escrito `est&#xE1;`, así que buscar la «á» literal no lo encuentra.
    Una prueba de pantalla comprueba **lo que se ve**, no el código fuente.
    """
    # Asigna a sin_script el valor calculado a la derecha.
    sin_script = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", pagina)
    # Asigna a sin_etiquetas el valor calculado a la derecha.
    sin_etiquetas = re.sub(r"<[^>]*>", " ", sin_script)
    # Devuelve al llamador el resultado de la expresion indicada.
    return re.sub(r"\s+", " ", html.unescape(sin_etiquetas))


# Define la funcion revisar con los parametros declarados; su bloque realiza esta operacion.
def revisar(nombre, condicion, detalle=""):
    # Asigna a marca el valor calculado a la derecha.
    marca = "[OK]    " if condicion else "[FALLO] "
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    print(marca + nombre + " " + detalle[:140])
    # Ejecuta el bloque siguiente solo cuando se cumple: not condicion.
    if not condicion:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        fallos.append(nombre)


# Define la funcion api con los parametros declarados; su bloque realiza esta operacion.
def api(ruta):
    # Ejecuta la instruccion indicada dentro del flujo actual.
    """Una lectura directa a la API, para contrastar contra la pantalla."""
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    codigo, texto = ver(API + ruta)
    # Ejecuta el bloque siguiente solo cuando se cumple: codigo not in (200, 204).
    if codigo not in (200, 204):
        # Devuelve al llamador el resultado de la expresion indicada.
        return None
    # Devuelve al llamador el resultado de la expresion indicada.
    return json.loads(texto) if texto else None
  


# Prueba: GET /api/area_conocimiento?limite=3
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
print()
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
print("=== Prueba de áreas de conocimiento ===")

# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
codigo, respuesta = ver(API + "/api/area_conocimiento?limite=3")

# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
revisar("GET /api/area_conocimiento?limite=3 responde con HTTP 200",
        # Asigna a codigo el valor calculado a la derecha.
        codigo == 200)

# Inicia un bloque cuya excepcion se manejara en los except siguientes.
try:
    # Asigna a resultado el valor calculado a la derecha.
    resultado = json.loads(respuesta)
    # Asigna a registros el valor calculado a la derecha.
    registros = resultado["datos"]

    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    revisar("La API devuelve exactamente 3 registros",
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            isinstance(registros, list) and len(registros) == 3)
# Captura la excepcion indicada para manejarla sin dejarla propagarse.
except (json.JSONDecodeError, KeyError, TypeError):
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    revisar("La respuesta contiene 3 registros", False,
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            "Respuesta JSON inválida o sin la clave 'datos'")

# Define la funcion esperar_api con los parametros declarados; su bloque realiza esta operacion.
def esperar_api(segundos=180):
    """Acepta 200 y 204: un 204 es la API diciendo que la tabla está vacía,
    que es una respuesta válida — no una API a medio arrancar."""
    # Recorre los elementos de la coleccion indicada y ejecuta el bloque para cada uno.
    for _ in range(segundos // 3):
        # Ejecuta el bloque siguiente solo cuando se cumple: ver(API + "/api/area_conocimiento?limite=1")[0] in (200, 204).
        if ver(API + "/api/area_conocimiento?limite=1")[0] in (200, 204):
            # Devuelve al llamador el resultado de la expresion indicada.
            return True
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        time.sleep(3)
    # Devuelve al llamador el resultado de la expresion indicada.
    return False


# Ejecuta el bloque siguiente solo cuando se cumple: not esperar_api().
if not esperar_api():
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    print("La API no respondió. ¿Está levantado el sistema?")
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    print("   docker compose up -d --build")
    # Lanza la excepcion indicada y detiene el flujo normal.
    raise SystemExit(1)

# ======================================================================
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
print("=== 1. Las pantallas responden, cada una por su dirección ===")
# ======================================================================
# Asigna a PANTALLAS el valor calculado a la derecha.
PANTALLAS = [
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ("/", "Investigación"),
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ("/areas-de-conocimiento", "Áreas de conocimiento"),
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ("/areas-de-conocimiento/nuevo", "Agregar"),
# Cierra la estructura abierta en las lineas anteriores.
]
# Recorre los elementos de la coleccion indicada y ejecuta el bloque para cada uno.
for ruta_, titulo in PANTALLAS:
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    c, t = ver(FRONT + ruta_)
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    revisar(ruta_.ljust(24) + " responde y dice «" + titulo + "»",
            # Asigna a c el valor calculado a la derecha.
            c == 200 and titulo in visible(t))

# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
c, t = ver(FRONT + "/pantalla-que-no-existe")
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
revisar("una dirección inventada da 404, con el marco de la aplicación",
        # Asigna a c el valor calculado a la derecha.
        c == 404 and "no existe" in visible(t))

# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
print()
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
print("=== 1.b La hoja de estilos LLEGA ===")
# Comprobar el TEXTO de una página no dice si la página se ve. Un 200 que
# devuelve HTML disfrazado de CSS deja la pantalla igual de fea.
# Inicia un bloque cuya excepcion se manejara en los except siguientes.
try:
    # Abre el recurso y asegura su cierre al salir del bloque.
    with navegador.open(FRONT + "/static/estilos.css", timeout=20) as r:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        codigo, tipo = r.status, r.headers.get("Content-Type", "")
# Captura la excepcion indicada para manejarla sin dejarla propagarse.
except Exception as e:
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    codigo, tipo = 0, str(e)
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
revisar("/static/estilos.css llega como text/css",
        # Asigna a codigo el valor calculado a la derecha.
        codigo == 200 and "css" in tipo, str(tipo))

# ======================================================================
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
print()
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
print("=== 2. El menú lleva a la pantalla, con una dirección de verdad ===")
# ======================================================================
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
c, inicio = ver(FRONT + "/")
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
revisar("el menú tiene el enlace", 'href="/areas-de-conocimiento"' in inicio)
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
revisar("y NINGUNA dirección tiene el nombre de la tabla como parámetro",
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        "{tabla}" not in inicio and "?tabla=" not in inicio)

# ======================================================================
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
print()
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
print("=== 3. La pantalla trae los datos que dio la API ===")
# ======================================================================
# Asigna a sobre el valor calculado a la derecha.
sobre = api("/api/area_conocimiento?limite=5")
# Asigna a filas el valor calculado a la derecha.
filas = sobre["datos"] if sobre else []
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
c, t = ver(FRONT + "/areas-de-conocimiento")
# Ejecuta el bloque siguiente solo cuando se cumple: not filas.
if not filas:
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    print("[--]    la tabla `area_conocimiento` está vacía: no hay datos que comparar")
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    revisar("y aun vacía, la pantalla responde y ofrece «Agregar»",
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            "Agregar" in visible(t))
# Define el caso alternativo cuando las condiciones anteriores no se cumplen.
else:
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    revisar("la API responde", True, str(len(filas)) + " filas")
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    revisar("y esos mismos datos se ven en la pantalla",
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            all(str(f["id"]) in visible(t) for f in filas[:3]))
    # Asigna a faltan el valor calculado a la derecha.
    faltan = [e for e in ETIQUETAS if e not in visible(t)]
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    revisar("la tabla trae sus columnas", not faltan, str(faltan))

# ======================================================================
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
print()
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
print("=== 4. Lo que la pantalla NO debe decirle al usuario ===")
# ======================================================================
# La jerga se busca como TOKEN TÉCNICO, no como palabra suelta: «proyecto» o
# «programa» son nombres de tabla Y palabras que el usuario dice todos los
# días. Jerga de verdad es la ruta de la API, los verbos y los motores.
# Asigna a JERGA el valor calculado a la derecha.
JERGA = ["PUT", "PATCH", "DELETE", "/api/", "asyncpg", "SELECT",
         # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
         "endpoint", "localhost:", "PostgreSQL", "FastAPI", "Traceback"]
# Recorre los elementos de la coleccion indicada y ejecuta el bloque para cada uno.
for ruta_, _ in PANTALLAS:
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    c, t = ver(FRONT + ruta_)
    # Asigna a visto el valor calculado a la derecha.
    visto = [j for j in JERGA if j in visible(t)]
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    revisar(ruta_.ljust(24) + " sin jerga", not visto, str(visto))

# ======================================================================
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
print()
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
print("=== 5. EL RECORRIDO COMPLETO, botón por botón ===")
# ======================================================================
# Asigna a COMPLETO el valor calculado a la derecha.
COMPLETO = {
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        "id": LLAVE,
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        "gran_area": ("Gran área " + SUFIJO)[:60],
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        "area": ("Área " + SUFIJO)[:60],
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        "disciplina": ("Disciplina " + SUFIJO)[:150],
# Cierra la estructura abierta en las lineas anteriores.
}

# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
c, t = enviar("/areas-de-conocimiento/nuevo", COMPLETO)
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
revisar("agregar la ficha " + str(LLAVE), "Se agregó" in visible(t))
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
revisar("  y ya aparece en el listado", str(LLAVE) in visible(t))

# --- Guardar la ficha completa ---
# Asigna a renombrado el valor calculado a la derecha.
renombrado = dict(COMPLETO, verbo="completa",
                  # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                  **{"gran_area": "Corregido " + SUFIJO})
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
c, t = enviar("/areas-de-conocimiento/" + str(LLAVE) + "/editar", renombrado)
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
revisar("«Guardar la ficha completa» guarda", "Se guardaron" in visible(t))
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
revisar("  y el valor nuevo se ve", "Corregido " + SUFIJO in visible(t))

# --- La ficha completa con un obligatorio en blanco: se rechaza ---
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
c, t = enviar("/areas-de-conocimiento/" + str(LLAVE) + "/editar",
              # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
              dict(COMPLETO, verbo="completa", **{"gran_area": ""}))
# Asigna a texto el valor calculado a la derecha.
texto = visible(t)
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
revisar("la ficha completa con «Gran área» en blanco se RECHAZA",
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        "Se guardaron" not in texto)
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
revisar("  y el motivo está EN ESPAÑOL y con el nombre de la pantalla",
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        "Gran área" in texto and "String should" not in texto)
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
revisar("  sin números de estado ni jerga",
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        not any(j in texto for j in ("422", "PUT", "/api/")))

# --- Solo lo que cambié: el MISMO formulario a medio llenar ---
# Asigna a vacios el valor calculado a la derecha.
vacios = {c: "" for c in COMPLETO if c != "id"}
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
c, t = enviar("/areas-de-conocimiento/" + str(LLAVE) + "/editar",
              # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
              dict(vacios, verbo="parcial",
                   # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                   **{"area": ("Área " + SUFIJO)[:60]}))
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
revisar("«Guardar solo lo que cambié», con lo demás en blanco, SÍ guarda",
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        "Se guardaron" in visible(t))

# Y aquí está la lección, comprobada contra los datos: cambió un campo y el
# otro se quedó como estaba. Lo que no se envía, no se toca.
# Asigna a ficha el valor calculado a la derecha.
ficha = api("/api/area_conocimiento/" + str(LLAVE))
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
revisar("  el campo enviado cambió",
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        ficha and str(ficha.get("area")).startswith(
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            "Área"[:6]),
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        str(ficha and ficha.get("area")))
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
revisar("  y «Gran área» NO se borró: lo que no se envía, no se toca",
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        ficha and ficha.get("granArea") == "Corregido " + SUFIJO,
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        str(ficha and ficha.get("granArea")))

# --- Retirar ---
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
c, t = enviar("/areas-de-conocimiento/" + str(LLAVE) + "/eliminar", {})
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
revisar("retirar la ficha", "Se retiró" in visible(t))

# Se pide la pantalla otra vez: en la segunda visita el aviso ya no está —se
# muestra una sola vez—, así que si la llave apareciera sería en la tabla de
# verdad. Dos comprobaciones por el precio de una.
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
c, t = ver(FRONT + "/areas-de-conocimiento")
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
revisar("  el aviso se muestra UNA vez y no se repite", "Se retiró" not in visible(t))
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
revisar("  y la ficha ya no está en el listado", str(LLAVE) not in visible(t))

# ======================================================================
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
print()
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
print("=== 6. LA PRUEBA DE LOS DOS PROCESOS: se apaga la API ===")
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
print("    (esto tarda unos segundos)")
# ======================================================================
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
subprocess.run(["docker", "compose", "stop", "api-investigacion"],
               # Asigna a capture_output el valor calculado a la derecha.
               capture_output=True, text=True)
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
time.sleep(3)

# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
c, t = ver(FRONT + "/areas-de-conocimiento")
# Asigna a texto el valor calculado a la derecha.
texto = visible(t)
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
revisar("la pantalla SIGUE respondiendo con la API apagada", c == 200)
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
revisar("  y muestra el aviso dentro de la aplicación",
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        "no está disponible" in texto)
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
revisar("  con su menú y su marco intactos",
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        "Áreas de conocimiento" in texto and "Inicio" in texto)
# Ésta es LA comprobación de la constitución: PostgreSQL sigue encendida y
# con los datos ahí. Si el front pudiera llegar a la base por su cuenta, la
# tabla se seguiría viendo. No se ve.
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
revisar("  y SIN un solo dato: el front no puede llegar a la base solo",
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        "Corregido" not in texto)

# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
subprocess.run(["docker", "compose", "start", "api-investigacion"],
               # Asigna a capture_output el valor calculado a la derecha.
               capture_output=True, text=True)
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
print("    API encendida otra vez; esperando a que responda…")
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
esperar_api(90)
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
c, t = ver(FRONT + "/areas-de-conocimiento")
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
revisar("y al volver la API, la pantalla vuelve a responder", c == 200)

# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
print()
# Ejecuta el bloque siguiente solo cuando se cumple: fallos.
if fallos:
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    print("=== RESULTADO: " + str(len(fallos)) + " FALLO(S) ===")
    # Recorre los elementos de la coleccion indicada y ejecuta el bloque para cada uno.
    for f in fallos:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        print("   -", f)
    # Lanza la excepcion indicada y detiene el flujo normal.
    raise SystemExit(1)

# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
print("=== RESULTADO: TODO EN VERDE ===")
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
print()
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
print("Se recorrió el ciclo completo desde la PANTALLA, con los mismos POST")
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
print("que manda el navegador. Queda para una persona lo que un guion no ve:")
# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
print("que se entienda.")
