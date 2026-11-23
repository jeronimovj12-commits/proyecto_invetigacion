"""
app.py — La capa de PRESENTACIÓN del sistema.

Estas son las vistas: reciben lo que el usuario hizo en el navegador, se lo
piden a `cliente_api`, y eligen qué plantilla mostrar. Nada más.

Las cuatro reglas de este archivo:

1. **No habla con la base de datos.** Ni siquiera sabe que existe PostgreSQL.
   Todo lo pide por HTTP a la API.
2. **No valida negocio.** Si un dato está mal, lo dice la API y aquí solo se
   muestra. Duplicar la regla en el front es tener dos dueños de la misma
   verdad.
3. **No importa nada de la API**, aunque las dos estén en Python y estén una
   al lado de la otra en el disco. Lo único que comparten es el JSON.
4. **No le habla al usuario en jerga.** Ni verbos, ni códigos de estado, ni
   nombres de tabla en la pantalla.

======================================================================
UNA PANTALLA POR TABLA, CON SU RUTA PROPIA
======================================================================

`/areas-de-conocimiento` — no `/tabla/<nombre>`. Una dirección con un hueco no es una
dirección de nada: un menú se arma con rutas que existen, y un marcador del
navegador apunta a una página, no a un molde.
"""

# Carga el modulo o los modulos os.
import os

# Importa Flask, flash, redirect, render_template, request, url_for desde flask para usar esas definiciones.
from flask import Flask, flash, redirect, render_template, request, url_for

# Carga el modulo o los modulos cliente_api.
import cliente_api

# Crea o configura la aplicacion web indicada por la expresion.
app = Flask(__name__)

# `flash` guarda los avisos en la sesión, y la sesión va firmada: sin clave,
# Flask no arranca. En un proyecto real esto vive fuera de git.
# Asigna a app.secret_key el valor calculado a la derecha.
app.secret_key = os.environ.get("CLAVE_SESION", "Paradigmas123!Sesion")

# Asigna a PUERTO el valor calculado a la derecha.
PUERTO = int(os.environ.get("PUERTO", 8078))


# Define la funcion _avisar con los parametros declarados; su bloque realiza esta operacion.
def _avisar(errores) -> None:
    # Ejecuta la instruccion indicada dentro del flujo actual.
    """Cada error de la API se muestra como un aviso rojo, uno por línea."""
    # Recorre los elementos de la coleccion indicada y ejecuta el bloque para cada uno.
    for mensaje in errores:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        flash(mensaje, "error")


# Define la funcion _entero con los parametros declarados; su bloque realiza esta operacion.
def _entero(texto: str):
    """El texto convertido a entero si lo es; si no, el texto tal cual.

    Parece una validación del lado del cliente, y hay que ser preciso porque
    no lo es. Un formulario HTML **solo produce texto**: el «12» que la
    persona escribió llega como "12". El contrato pide un número, y un número
    entre comillas haría que la API lo rechazara **siendo correcto**.

    Esto ajusta la FORMA del dato, que es trabajo del front, y no juzga su
    VALOR, que es trabajo de la API: si alguien escribió «doce», eso viaja
    como «doce» y la API responde 422.
    """
    # Asigna a texto el valor calculado a la derecha.
    texto = (texto or "").strip()
    # Ejecuta el bloque siguiente solo cuando se cumple: texto == "".
    if texto == "":
        # Devuelve al llamador el resultado de la expresion indicada.
        return ""
    # Inicia un bloque cuya excepcion se manejara en los except siguientes.
    try:
        # Devuelve al llamador el resultado de la expresion indicada.
        return int(texto)
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except ValueError:
        # Devuelve al llamador el resultado de la expresion indicada.
        return texto


# Define la funcion _si_lleno con los parametros declarados; su bloque realiza esta operacion.
def _si_lleno(cuerpo: dict, campo: str, valor) -> None:
    """Mete el campo SOLO si la persona escribió algo.

    Es la mitad del contraste entre los dos botones de guardar: lo que no se
    diligencia **no viaja**, y la API deja ese campo como estaba.
    """
    # Ejecuta el bloque siguiente solo cuando se cumple: valor not in ("", None).
    if valor not in ("", None):
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        cuerpo[campo] = valor


# ======================================================================
# EL INICIO
# ======================================================================


# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route("/")
# Define la funcion inicio con los parametros declarados; su bloque realiza esta operacion.
def inicio():
    # Devuelve al llamador el resultado de la expresion indicada.
    return render_template("inicio.html")


# ======================================================================
# ÁREAS DE CONOCIMIENTO
# ======================================================================


# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route("/areas-de-conocimiento")
# Define la funcion listar_areas_conocimiento con los parametros declarados; su bloque realiza esta operacion.
def listar_areas_conocimiento():
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, filas, errores = cliente_api.listar_areas_conocimiento()
    # Ejecuta el bloque siguiente solo cuando se cumple: not ok.
    if not ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
    # Aun con error se pinta la pantalla: el usuario ve el aviso DENTRO de la
    # aplicación, no una página de error del servidor.
    # Devuelve al llamador el resultado de la expresion indicada.
    return render_template("areas_conocimiento/lista.html", filas=filas)


# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route("/areas-de-conocimiento/nuevo", methods=["GET", "POST"])
# Define la funcion crear_area_conocimiento con los parametros declarados; su bloque realiza esta operacion.
def crear_area_conocimiento():
    # Ejecuta el bloque siguiente solo cuando se cumple: request.method == "GET".
    if request.method == "GET":
        # Devuelve al llamador el resultado de la expresion indicada.
        return render_template("areas_conocimiento/formulario.html", ficha=None, editando=False)

    # Asigna a cuerpo el valor calculado a la derecha.
    cuerpo = _cuerpo_completo(con_llave=True)
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, errores = cliente_api.crear_area_conocimiento(cuerpo)
    # Ejecuta el bloque siguiente solo cuando se cumple: ok.
    if ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        flash("Se agregó la ficha.", "exito")
        # Devuelve al llamador el resultado de la expresion indicada.
        return redirect(url_for("listar_areas_conocimiento"))

    # Se devuelve el formulario CON lo que la persona había escrito: perder lo
    # digitado por un error de validación es castigarla dos veces.
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    _avisar(errores)
    # Devuelve al llamador el resultado de la expresion indicada.
    return render_template("areas_conocimiento/formulario.html", ficha=cuerpo, editando=False)


# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route("/areas-de-conocimiento/<string:id>/editar", methods=["GET", "POST"])
# Define la funcion editar_area_conocimiento con los parametros declarados; su bloque realiza esta operacion.
def editar_area_conocimiento(id):
    # Ejecuta el bloque siguiente solo cuando se cumple: request.method == "GET".
    if request.method == "GET":
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        ok, ficha, errores = cliente_api.obtener_area_conocimiento(id)
        # Ejecuta el bloque siguiente solo cuando se cumple: not ok.
        if not ok:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            _avisar(errores)
            # Devuelve al llamador el resultado de la expresion indicada.
            return redirect(url_for("listar_areas_conocimiento"))
        # Devuelve al llamador el resultado de la expresion indicada.
        return render_template("areas_conocimiento/formulario.html", ficha=ficha, editando=True)

    # ==================================================================
    # QUÉ BOTÓN SE OPRIMIÓ DECIDE QUÉ SE ENVÍA.
    # La diferencia NO está en un `if` de negocio: está en el CUERPO de la
    # petición. Uno manda un reemplazo completo y el otro solo lo llenado.
    # ==================================================================
    # Ejecuta el bloque siguiente solo cuando se cumple: request.form.get("verbo") == "completa".
    if request.form.get("verbo") == "completa":
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        ok, errores = cliente_api.reemplazar_area_conocimiento(id, _cuerpo_completo())
    # Define el caso alternativo cuando las condiciones anteriores no se cumplen.
    else:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        ok, errores = cliente_api.actualizar_area_conocimiento(id, _cuerpo_parcial())

    # Ejecuta el bloque siguiente solo cuando se cumple: ok.
    if ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        flash("Se guardaron los cambios.", "exito")
        # Devuelve al llamador el resultado de la expresion indicada.
        return redirect(url_for("listar_areas_conocimiento"))

    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    _avisar(errores)
    # Asigna a ficha el valor calculado a la derecha.
    ficha = dict(request.form)
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ficha["id"] = id
    # Devuelve al llamador el resultado de la expresion indicada.
    return render_template("areas_conocimiento/formulario.html", ficha=ficha, editando=True)


# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route("/areas-de-conocimiento/<string:id>/eliminar", methods=["POST"])
# Define la funcion eliminar_area_conocimiento con los parametros declarados; su bloque realiza esta operacion.
def eliminar_area_conocimiento(id):
    """Se exige POST a propósito: un enlace GET que borra lo puede disparar
    el navegador solo, al precargar la página."""
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, errores = cliente_api.eliminar_area_conocimiento(id)
    # Ejecuta el bloque siguiente solo cuando se cumple: ok.
    if ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        flash("Se retiró la ficha.", "exito")
    # Define el caso alternativo cuando las condiciones anteriores no se cumplen.
    else:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
    # Devuelve al llamador el resultado de la expresion indicada.
    return redirect(url_for("listar_areas_conocimiento"))


# ======================================================================
# Los dos armadores del cuerpo
# ======================================================================


# Define la funcion _cuerpo_completo con los parametros declarados; su bloque realiza esta operacion.
def _cuerpo_completo(con_llave: bool = False) -> dict:
    """Todos los campos, vayan llenos o no. Lo usan POST y PUT.

    Por eso un campo obligatorio en blanco se rechaza: viaja vacío, y la API
    dice que no cumple.
    """
    # Asigna a cuerpo el valor calculado a la derecha.
    cuerpo = {
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        "gran_area": request.form.get("gran_area", "").strip(),
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        "area": request.form.get("area", "").strip(),
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        "disciplina": request.form.get("disciplina", "").strip(),
    # Cierra la estructura abierta en las lineas anteriores.
    }

    # Ejecuta el bloque siguiente solo cuando se cumple: con_llave.
    if con_llave:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        cuerpo["id"] = request.form.get("id", "").strip()
    # Devuelve al llamador el resultado de la expresion indicada.
    return cuerpo


# Define la funcion _cuerpo_parcial con los parametros declarados; su bloque realiza esta operacion.
def _cuerpo_parcial() -> dict:
    """Solo lo diligenciado. Lo usa PATCH.

    El mismo formulario a medio llenar que el reemplazo rechaza, aquí
    funciona — y lo que no se envía, la API lo deja como estaba.
    """
    # Asigna a cuerpo el valor calculado a la derecha.
    cuerpo: dict = {}
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    _si_lleno(cuerpo, "gran_area", request.form.get("gran_area", "").strip())
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    _si_lleno(cuerpo, "area", request.form.get("area", "").strip())
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    _si_lleno(cuerpo, "disciplina", request.form.get("disciplina", "").strip())
    # Devuelve al llamador el resultado de la expresion indicada.
    return cuerpo


# ======================================================================
# La pantalla de «esa página no existe»
# ======================================================================


# Aplica @app.errorhandler a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.errorhandler(404)
# Define la funcion no_encontrada con los parametros declarados; su bloque realiza esta operacion.
def no_encontrada(_error):
    # Ejecuta la instruccion indicada dentro del flujo actual.
    """Con el marco de la aplicación puesto, no una página en blanco."""
    # Devuelve al llamador el resultado de la expresion indicada.
    return render_template("no_encontrada.html"), 404




# Define la funcion _valor_formulario con los parametros declarados; su bloque realiza esta operacion.
def _valor_formulario(campo, numerico=False, nullable=False):
    # Asigna a valor el valor calculado a la derecha.
    valor = request.form.get(campo, "").strip()
    # Ejecuta el bloque siguiente solo cuando se cumple: nullable and valor in ("", "__nulo__").
    if nullable and valor in ("", "__nulo__"):
        # Devuelve al llamador el resultado de la expresion indicada.
        return None
    # Devuelve al llamador el resultado de la expresion indicada.
    return _entero(valor) if numerico else valor


# Define la funcion _campos_cambiados con los parametros declarados; su bloque realiza esta operacion.
def _campos_cambiados(datos, ficha):
    # Devuelve al llamador el resultado de la expresion indicada.
    return {campo: valor for campo, valor in datos.items() if valor != ficha.get(campo)}

# Define la funcion _opciones_docente con los parametros declarados; su bloque realiza esta operacion.
def _opciones_docente():
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones, disponibles = {}, True
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, filas, errores = cliente_api.listar_linea_investigacion()
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones["linea_investigacion_principal"] = filas
    # Ejecuta el bloque siguiente solo cuando se cumple: not ok.
    if not ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
        # Asigna a disponibles el valor calculado a la derecha.
        disponibles = False
    # Devuelve al llamador el resultado de la expresion indicada.
    return opciones, disponibles

# Define la funcion _cuerpo_docente con los parametros declarados; su bloque realiza esta operacion.
def _cuerpo_docente(crear=False):
    # Asigna a cuerpo el valor calculado a la derecha.
    cuerpo = {}
    # Ejecuta el bloque siguiente solo cuando se cumple: crear: cuerpo["cedula"] = _valor_formulario("cedula", numerico=True, nullable=False).
    if crear: cuerpo["cedula"] = _valor_formulario("cedula", numerico=True, nullable=False)
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    cuerpo["nombres"] = _valor_formulario("nombres", numerico=False, nullable=False)
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    cuerpo["apellidos"] = _valor_formulario("apellidos", numerico=False, nullable=False)
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    cuerpo["genero"] = _valor_formulario("genero", numerico=False, nullable=False)
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    cuerpo["cargo"] = _valor_formulario("cargo", numerico=False, nullable=False)
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    cuerpo["fecha_nacimiento"] = _valor_formulario("fecha_nacimiento", numerico=False, nullable=False)
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    cuerpo["correo"] = _valor_formulario("correo", numerico=False, nullable=False)
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    cuerpo["telefono"] = _valor_formulario("telefono", numerico=False, nullable=False)
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    cuerpo["url_cvlac"] = _valor_formulario("url_cvlac", numerico=False, nullable=False)
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    cuerpo["fecha_actualizacion"] = _valor_formulario("fecha_actualizacion", numerico=False, nullable=False)
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    cuerpo["escalafon"] = _valor_formulario("escalafon", numerico=False, nullable=False)
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    cuerpo["perfil"] = _valor_formulario("perfil", numerico=False, nullable=False)
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    cuerpo["cat_minciencia"] = _valor_formulario("cat_minciencia", numerico=False, nullable=True)
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    cuerpo["conv_minciencia"] = _valor_formulario("conv_minciencia", numerico=False, nullable=False)
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    cuerpo["nacionalidaad"] = _valor_formulario("nacionalidaad", numerico=False, nullable=False)
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    cuerpo["linea_investigacion_principal"] = _valor_formulario("linea_investigacion_principal", numerico=True, nullable=True)
    # Devuelve al llamador el resultado de la expresion indicada.
    return cuerpo

# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route("/docente")
# Define la funcion listar_docente con los parametros declarados; su bloque realiza esta operacion.
def listar_docente():
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, filas, errores = cliente_api.listar_docente()
    # Ejecuta el bloque siguiente solo cuando se cumple: not ok.
    if not ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
    # Devuelve al llamador el resultado de la expresion indicada.
    return render_template("docente/lista.html", filas=filas)


# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route("/docente/nuevo", methods=["GET", "POST"])
# Define la funcion crear_docente con los parametros declarados; su bloque realiza esta operacion.
def crear_docente():
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones, disponibles = _opciones_docente()
    # Asigna a ficha el valor calculado a la derecha.
    ficha = None
    # Ejecuta el bloque siguiente solo cuando se cumple: request.method == "POST".
    if request.method == "POST":
        # Asigna a ficha el valor calculado a la derecha.
        ficha = _cuerpo_docente(crear=True)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        ok, errores = cliente_api.crear_docente(ficha)
        # Ejecuta el bloque siguiente solo cuando se cumple: ok.
        if ok:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            flash("Se agregó la ficha.", "exito")
            # Devuelve al llamador el resultado de la expresion indicada.
            return redirect(url_for("listar_docente"))
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
    # Devuelve al llamador el resultado de la expresion indicada.
    return render_template("docente/formulario.html", ficha=ficha, editando=False, opciones=opciones, disponibles=disponibles)


# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route("/docente/<int:cedula>/editar", methods=["GET", "POST"])
# Define la funcion editar_docente con los parametros declarados; su bloque realiza esta operacion.
def editar_docente(cedula):
    # Asigna a identidad el valor calculado a la derecha.
    identidad = {"cedula": cedula}
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, ficha, errores = cliente_api.obtener_docente(identidad)
    # Ejecuta el bloque siguiente solo cuando se cumple: not ok.
    if not ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
        # Devuelve al llamador el resultado de la expresion indicada.
        return redirect(url_for("listar_docente"))
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones, disponibles = _opciones_docente()
    # Ejecuta el bloque siguiente solo cuando se cumple: request.method == "POST".
    if request.method == "POST":
        # Asigna a datos el valor calculado a la derecha.
        datos = _cuerpo_docente()
        # Ejecuta el bloque siguiente solo cuando se cumple: request.form.get("verbo") == "completa".
        if request.form.get("verbo") == "completa":
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            ok, errores = cliente_api.reemplazar_docente(identidad, datos)
        # Define el caso alternativo cuando las condiciones anteriores no se cumplen.
        else:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            ok, errores = cliente_api.actualizar_docente(identidad, _campos_cambiados(datos, ficha))
        # Ejecuta el bloque siguiente solo cuando se cumple: ok.
        if ok:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            flash("Se guardaron los cambios.", "exito")
            # Devuelve al llamador el resultado de la expresion indicada.
            return redirect(url_for("listar_docente"))
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
        # Asigna a ficha el valor calculado a la derecha.
        ficha = {**ficha, **datos}
    # Devuelve al llamador el resultado de la expresion indicada.
    return render_template("docente/formulario.html", ficha=ficha, editando=True, opciones=opciones, disponibles=disponibles)


# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route("/docente/<int:cedula>/eliminar", methods=["POST"])
# Define la funcion eliminar_docente con los parametros declarados; su bloque realiza esta operacion.
def eliminar_docente(cedula):
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, errores = cliente_api.eliminar_docente({"cedula": cedula})
    # Ejecuta el bloque siguiente solo cuando se cumple: ok.
    if ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        flash("Se retiró la ficha.", "exito")
    # Define el caso alternativo cuando las condiciones anteriores no se cumplen.
    else:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
    # Devuelve al llamador el resultado de la expresion indicada.
    return redirect(url_for("listar_docente"))


# Define la funcion _opciones_grupo_investigacion con los parametros declarados; su bloque realiza esta operacion.
def _opciones_grupo_investigacion():
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones, disponibles = {}, True
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, filas, errores = cliente_api.listar_universidad()
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones["universidsad"] = filas
    # Ejecuta el bloque siguiente solo cuando se cumple: not ok.
    if not ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
        # Asigna a disponibles el valor calculado a la derecha.
        disponibles = False
    # Devuelve al llamador el resultado de la expresion indicada.
    return opciones, disponibles

# Define la funcion _cuerpo_grupo_investigacion con los parametros declarados; su bloque realiza esta operacion.
def _cuerpo_grupo_investigacion(crear=False):
    # Asigna a cuerpo el valor calculado a la derecha.
    cuerpo = {}
    # Ejecuta el bloque siguiente solo cuando se cumple: crear: cuerpo["id"] = _valor_formulario("id", numerico=True, nullable=False).
    if crear: cuerpo["id"] = _valor_formulario("id", numerico=True, nullable=False)
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    cuerpo["nombre"] = _valor_formulario("nombre", numerico=False, nullable=False)
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    cuerpo["url_gruplac"] = _valor_formulario("url_gruplac", numerico=False, nullable=True)
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    cuerpo["categoria"] = _valor_formulario("categoria", numerico=False, nullable=True)
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    cuerpo["convocatoria"] = _valor_formulario("convocatoria", numerico=False, nullable=True)
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    cuerpo["fecha_fundacion"] = _valor_formulario("fecha_fundacion", numerico=False, nullable=False)
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    cuerpo["universidsad"] = _valor_formulario("universidsad", numerico=True, nullable=True)
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    cuerpo["interno"] = _valor_formulario("interno", numerico=True, nullable=False)
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    cuerpo["ambito"] = _valor_formulario("ambito", numerico=False, nullable=False)
    # Devuelve al llamador el resultado de la expresion indicada.
    return cuerpo

# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route("/grupo-investigacion")
# Define la funcion listar_grupo_investigacion con los parametros declarados; su bloque realiza esta operacion.
def listar_grupo_investigacion():
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, filas, errores = cliente_api.listar_grupo_investigacion()
    # Ejecuta el bloque siguiente solo cuando se cumple: not ok.
    if not ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
    # Devuelve al llamador el resultado de la expresion indicada.
    return render_template("grupo_investigacion/lista.html", filas=filas)


# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route("/grupo-investigacion/nuevo", methods=["GET", "POST"])
# Define la funcion crear_grupo_investigacion con los parametros declarados; su bloque realiza esta operacion.
def crear_grupo_investigacion():
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones, disponibles = _opciones_grupo_investigacion()
    # Asigna a ficha el valor calculado a la derecha.
    ficha = None
    # Ejecuta el bloque siguiente solo cuando se cumple: request.method == "POST".
    if request.method == "POST":
        # Asigna a ficha el valor calculado a la derecha.
        ficha = _cuerpo_grupo_investigacion(crear=True)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        ok, errores = cliente_api.crear_grupo_investigacion(ficha)
        # Ejecuta el bloque siguiente solo cuando se cumple: ok.
        if ok:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            flash("Se agregó la ficha.", "exito")
            # Devuelve al llamador el resultado de la expresion indicada.
            return redirect(url_for("listar_grupo_investigacion"))
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
    # Devuelve al llamador el resultado de la expresion indicada.
    return render_template("grupo_investigacion/formulario.html", ficha=ficha, editando=False, opciones=opciones, disponibles=disponibles)


# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route("/grupo-investigacion/<int:id>/editar", methods=["GET", "POST"])
# Define la funcion editar_grupo_investigacion con los parametros declarados; su bloque realiza esta operacion.
def editar_grupo_investigacion(id):
    # Asigna a identidad el valor calculado a la derecha.
    identidad = {"id": id}
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, ficha, errores = cliente_api.obtener_grupo_investigacion(identidad)
    # Ejecuta el bloque siguiente solo cuando se cumple: not ok.
    if not ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
        # Devuelve al llamador el resultado de la expresion indicada.
        return redirect(url_for("listar_grupo_investigacion"))
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones, disponibles = _opciones_grupo_investigacion()
    # Ejecuta el bloque siguiente solo cuando se cumple: request.method == "POST".
    if request.method == "POST":
        # Asigna a datos el valor calculado a la derecha.
        datos = _cuerpo_grupo_investigacion()
        # Ejecuta el bloque siguiente solo cuando se cumple: request.form.get("verbo") == "completa".
        if request.form.get("verbo") == "completa":
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            ok, errores = cliente_api.reemplazar_grupo_investigacion(identidad, datos)
        # Define el caso alternativo cuando las condiciones anteriores no se cumplen.
        else:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            ok, errores = cliente_api.actualizar_grupo_investigacion(identidad, _campos_cambiados(datos, ficha))
        # Ejecuta el bloque siguiente solo cuando se cumple: ok.
        if ok:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            flash("Se guardaron los cambios.", "exito")
            # Devuelve al llamador el resultado de la expresion indicada.
            return redirect(url_for("listar_grupo_investigacion"))
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
        # Asigna a ficha el valor calculado a la derecha.
        ficha = {**ficha, **datos}
    # Devuelve al llamador el resultado de la expresion indicada.
    return render_template("grupo_investigacion/formulario.html", ficha=ficha, editando=True, opciones=opciones, disponibles=disponibles)


# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route("/grupo-investigacion/<int:id>/eliminar", methods=["POST"])
# Define la funcion eliminar_grupo_investigacion con los parametros declarados; su bloque realiza esta operacion.
def eliminar_grupo_investigacion(id):
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, errores = cliente_api.eliminar_grupo_investigacion({"id": id})
    # Ejecuta el bloque siguiente solo cuando se cumple: ok.
    if ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        flash("Se retiró la ficha.", "exito")
    # Define el caso alternativo cuando las condiciones anteriores no se cumplen.
    else:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
    # Devuelve al llamador el resultado de la expresion indicada.
    return redirect(url_for("listar_grupo_investigacion"))


# Define la funcion _opciones_semillero con los parametros declarados; su bloque realiza esta operacion.
def _opciones_semillero():
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones, disponibles = {}, True
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, filas, errores = cliente_api.listar_grupo_investigacion()
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones["grupo_investigacion"] = filas
    # Ejecuta el bloque siguiente solo cuando se cumple: not ok.
    if not ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
        # Asigna a disponibles el valor calculado a la derecha.
        disponibles = False
    # Devuelve al llamador el resultado de la expresion indicada.
    return opciones, disponibles

# Define la funcion _cuerpo_semillero con los parametros declarados; su bloque realiza esta operacion.
def _cuerpo_semillero(crear=False):
    # Asigna a cuerpo el valor calculado a la derecha.
    cuerpo = {}
    # Ejecuta el bloque siguiente solo cuando se cumple: crear: cuerpo["id"] = _valor_formulario("id", numerico=True, nullable=False).
    if crear: cuerpo["id"] = _valor_formulario("id", numerico=True, nullable=False)
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    cuerpo["nombre"] = _valor_formulario("nombre", numerico=False, nullable=False)
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    cuerpo["fecha_fundacion"] = _valor_formulario("fecha_fundacion", numerico=False, nullable=False)
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    cuerpo["grupo_investigacion"] = _valor_formulario("grupo_investigacion", numerico=True, nullable=False)
    # Devuelve al llamador el resultado de la expresion indicada.
    return cuerpo

# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route("/semillero")
# Define la funcion listar_semillero con los parametros declarados; su bloque realiza esta operacion.
def listar_semillero():
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, filas, errores = cliente_api.listar_semillero()
    # Ejecuta el bloque siguiente solo cuando se cumple: not ok.
    if not ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
    # Devuelve al llamador el resultado de la expresion indicada.
    return render_template("semillero/lista.html", filas=filas)


# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route("/semillero/nuevo", methods=["GET", "POST"])
# Define la funcion crear_semillero con los parametros declarados; su bloque realiza esta operacion.
def crear_semillero():
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones, disponibles = _opciones_semillero()
    # Asigna a ficha el valor calculado a la derecha.
    ficha = None
    # Ejecuta el bloque siguiente solo cuando se cumple: request.method == "POST".
    if request.method == "POST":
        # Asigna a ficha el valor calculado a la derecha.
        ficha = _cuerpo_semillero(crear=True)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        ok, errores = cliente_api.crear_semillero(ficha)
        # Ejecuta el bloque siguiente solo cuando se cumple: ok.
        if ok:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            flash("Se agregó la ficha.", "exito")
            # Devuelve al llamador el resultado de la expresion indicada.
            return redirect(url_for("listar_semillero"))
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
    # Devuelve al llamador el resultado de la expresion indicada.
    return render_template("semillero/formulario.html", ficha=ficha, editando=False, opciones=opciones, disponibles=disponibles)


# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route("/semillero/<int:id>/editar", methods=["GET", "POST"])
# Define la funcion editar_semillero con los parametros declarados; su bloque realiza esta operacion.
def editar_semillero(id):
    # Asigna a identidad el valor calculado a la derecha.
    identidad = {"id": id}
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, ficha, errores = cliente_api.obtener_semillero(identidad)
    # Ejecuta el bloque siguiente solo cuando se cumple: not ok.
    if not ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
        # Devuelve al llamador el resultado de la expresion indicada.
        return redirect(url_for("listar_semillero"))
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones, disponibles = _opciones_semillero()
    # Ejecuta el bloque siguiente solo cuando se cumple: request.method == "POST".
    if request.method == "POST":
        # Asigna a datos el valor calculado a la derecha.
        datos = _cuerpo_semillero()
        # Ejecuta el bloque siguiente solo cuando se cumple: request.form.get("verbo") == "completa".
        if request.form.get("verbo") == "completa":
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            ok, errores = cliente_api.reemplazar_semillero(identidad, datos)
        # Define el caso alternativo cuando las condiciones anteriores no se cumplen.
        else:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            ok, errores = cliente_api.actualizar_semillero(identidad, _campos_cambiados(datos, ficha))
        # Ejecuta el bloque siguiente solo cuando se cumple: ok.
        if ok:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            flash("Se guardaron los cambios.", "exito")
            # Devuelve al llamador el resultado de la expresion indicada.
            return redirect(url_for("listar_semillero"))
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
        # Asigna a ficha el valor calculado a la derecha.
        ficha = {**ficha, **datos}
    # Devuelve al llamador el resultado de la expresion indicada.
    return render_template("semillero/formulario.html", ficha=ficha, editando=True, opciones=opciones, disponibles=disponibles)


# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route("/semillero/<int:id>/eliminar", methods=["POST"])
# Define la funcion eliminar_semillero con los parametros declarados; su bloque realiza esta operacion.
def eliminar_semillero(id):
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, errores = cliente_api.eliminar_semillero({"id": id})
    # Ejecuta el bloque siguiente solo cuando se cumple: ok.
    if ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        flash("Se retiró la ficha.", "exito")
    # Define el caso alternativo cuando las condiciones anteriores no se cumplen.
    else:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
    # Devuelve al llamador el resultado de la expresion indicada.
    return redirect(url_for("listar_semillero"))


# Define la funcion _opciones_participa_semillero con los parametros declarados; su bloque realiza esta operacion.
def _opciones_participa_semillero():
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones, disponibles = {}, True
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, filas, errores = cliente_api.listar_docente()
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones["docente"] = filas
    # Ejecuta el bloque siguiente solo cuando se cumple: not ok.
    if not ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
        # Asigna a disponibles el valor calculado a la derecha.
        disponibles = False
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, filas, errores = cliente_api.listar_semillero()
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones["semillero"] = filas
    # Ejecuta el bloque siguiente solo cuando se cumple: not ok.
    if not ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
        # Asigna a disponibles el valor calculado a la derecha.
        disponibles = False
    # Devuelve al llamador el resultado de la expresion indicada.
    return opciones, disponibles

# Define la funcion _cuerpo_participa_semillero con los parametros declarados; su bloque realiza esta operacion.
def _cuerpo_participa_semillero(crear=False):
    # Asigna a cuerpo el valor calculado a la derecha.
    cuerpo = {}
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    cuerpo["docente"] = _valor_formulario("docente", numerico=True, nullable=False)
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    cuerpo["semillero"] = _valor_formulario("semillero", numerico=True, nullable=False)
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    cuerpo["rol"] = _valor_formulario("rol", numerico=False, nullable=False)
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    cuerpo["fecha_inicio"] = _valor_formulario("fecha_inicio", numerico=False, nullable=False)
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    cuerpo["fecha_fin"] = _valor_formulario("fecha_fin", numerico=False, nullable=True)
    # Devuelve al llamador el resultado de la expresion indicada.
    return cuerpo

# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route("/participa-semillero")
# Define la funcion listar_participa_semillero con los parametros declarados; su bloque realiza esta operacion.
def listar_participa_semillero():
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, filas, errores = cliente_api.listar_participa_semillero()
    # Ejecuta el bloque siguiente solo cuando se cumple: not ok.
    if not ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
    # Devuelve al llamador el resultado de la expresion indicada.
    return render_template("participa_semillero/lista.html", filas=filas)


# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route("/participa-semillero/nuevo", methods=["GET", "POST"])
# Define la funcion crear_participa_semillero con los parametros declarados; su bloque realiza esta operacion.
def crear_participa_semillero():
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones, disponibles = _opciones_participa_semillero()
    # Asigna a ficha el valor calculado a la derecha.
    ficha = None
    # Ejecuta el bloque siguiente solo cuando se cumple: request.method == "POST".
    if request.method == "POST":
        # Asigna a ficha el valor calculado a la derecha.
        ficha = _cuerpo_participa_semillero(crear=True)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        ok, errores = cliente_api.crear_participa_semillero(ficha)
        # Ejecuta el bloque siguiente solo cuando se cumple: ok.
        if ok:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            flash("Se agregó la ficha.", "exito")
            # Devuelve al llamador el resultado de la expresion indicada.
            return redirect(url_for("listar_participa_semillero"))
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
    # Devuelve al llamador el resultado de la expresion indicada.
    return render_template("participa_semillero/formulario.html", ficha=ficha, editando=False, opciones=opciones, disponibles=disponibles)


# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route("/participa-semillero/<int:docente>/<int:semillero>/editar", methods=["GET", "POST"])
# Define la funcion editar_participa_semillero con los parametros declarados; su bloque realiza esta operacion.
def editar_participa_semillero(docente, semillero):
    # Asigna a identidad el valor calculado a la derecha.
    identidad = {"docente": docente, "semillero": semillero}
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, ficha, errores = cliente_api.obtener_participa_semillero(identidad)
    # Ejecuta el bloque siguiente solo cuando se cumple: not ok.
    if not ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
        # Devuelve al llamador el resultado de la expresion indicada.
        return redirect(url_for("listar_participa_semillero"))
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones, disponibles = _opciones_participa_semillero()
    # Ejecuta el bloque siguiente solo cuando se cumple: request.method == "POST".
    if request.method == "POST":
        # Asigna a datos el valor calculado a la derecha.
        datos = _cuerpo_participa_semillero()
        # Ejecuta el bloque siguiente solo cuando se cumple: request.form.get("verbo") == "completa".
        if request.form.get("verbo") == "completa":
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            ok, errores = cliente_api.reemplazar_participa_semillero(identidad, datos)
        # Define el caso alternativo cuando las condiciones anteriores no se cumplen.
        else:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            ok, errores = cliente_api.actualizar_participa_semillero(identidad, _campos_cambiados(datos, ficha))
        # Ejecuta el bloque siguiente solo cuando se cumple: ok.
        if ok:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            flash("Se guardaron los cambios.", "exito")
            # Devuelve al llamador el resultado de la expresion indicada.
            return redirect(url_for("listar_participa_semillero"))
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
        # Asigna a ficha el valor calculado a la derecha.
        ficha = {**ficha, **datos}
    # Devuelve al llamador el resultado de la expresion indicada.
    return render_template("participa_semillero/formulario.html", ficha=ficha, editando=True, opciones=opciones, disponibles=disponibles)


# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route("/participa-semillero/<int:docente>/<int:semillero>/eliminar", methods=["POST"])
# Define la funcion eliminar_participa_semillero con los parametros declarados; su bloque realiza esta operacion.
def eliminar_participa_semillero(docente, semillero):
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, errores = cliente_api.eliminar_participa_semillero({"docente": docente, "semillero": semillero})
    # Ejecuta el bloque siguiente solo cuando se cumple: ok.
    if ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        flash("Se retiró la ficha.", "exito")
    # Define el caso alternativo cuando las condiciones anteriores no se cumplen.
    else:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
    # Devuelve al llamador el resultado de la expresion indicada.
    return redirect(url_for("listar_participa_semillero"))


# Define la funcion _opciones_participa_grupo con los parametros declarados; su bloque realiza esta operacion.
def _opciones_participa_grupo():
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones, disponibles = {}, True
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, filas, errores = cliente_api.listar_docente()
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones["docente_cedula"] = filas
    # Ejecuta el bloque siguiente solo cuando se cumple: not ok.
    if not ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
        # Asigna a disponibles el valor calculado a la derecha.
        disponibles = False
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, filas, errores = cliente_api.listar_grupo_investigacion()
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones["grupo_investigacion_id"] = filas
    # Ejecuta el bloque siguiente solo cuando se cumple: not ok.
    if not ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
        # Asigna a disponibles el valor calculado a la derecha.
        disponibles = False
    # Devuelve al llamador el resultado de la expresion indicada.
    return opciones, disponibles

# Define la funcion _cuerpo_participa_grupo con los parametros declarados; su bloque realiza esta operacion.
def _cuerpo_participa_grupo(crear=False):
    # Asigna a cuerpo el valor calculado a la derecha.
    cuerpo = {}
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    cuerpo["docente_cedula"] = _valor_formulario("docente_cedula", numerico=True, nullable=False)
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    cuerpo["grupo_investigacion_id"] = _valor_formulario("grupo_investigacion_id", numerico=True, nullable=False)
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    cuerpo["rol"] = _valor_formulario("rol", numerico=False, nullable=False)
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    cuerpo["fecha_inicio"] = _valor_formulario("fecha_inicio", numerico=False, nullable=False)
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    cuerpo["fecha_fin"] = _valor_formulario("fecha_fin", numerico=False, nullable=True)
    # Devuelve al llamador el resultado de la expresion indicada.
    return cuerpo

# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route("/participa-grupo")
# Define la funcion listar_participa_grupo con los parametros declarados; su bloque realiza esta operacion.
def listar_participa_grupo():
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, filas, errores = cliente_api.listar_participa_grupo()
    # Ejecuta el bloque siguiente solo cuando se cumple: not ok.
    if not ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
    # Devuelve al llamador el resultado de la expresion indicada.
    return render_template("participa_grupo/lista.html", filas=filas)


# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route("/participa-grupo/nuevo", methods=["GET", "POST"])
# Define la funcion crear_participa_grupo con los parametros declarados; su bloque realiza esta operacion.
def crear_participa_grupo():
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones, disponibles = _opciones_participa_grupo()
    # Asigna a ficha el valor calculado a la derecha.
    ficha = None
    # Ejecuta el bloque siguiente solo cuando se cumple: request.method == "POST".
    if request.method == "POST":
        # Asigna a ficha el valor calculado a la derecha.
        ficha = _cuerpo_participa_grupo(crear=True)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        ok, errores = cliente_api.crear_participa_grupo(ficha)
        # Ejecuta el bloque siguiente solo cuando se cumple: ok.
        if ok:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            flash("Se agregó la ficha.", "exito")
            # Devuelve al llamador el resultado de la expresion indicada.
            return redirect(url_for("listar_participa_grupo"))
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
    # Devuelve al llamador el resultado de la expresion indicada.
    return render_template("participa_grupo/formulario.html", ficha=ficha, editando=False, opciones=opciones, disponibles=disponibles)


# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route("/participa-grupo/<int:docente_cedula>/<int:grupo_investigacion_id>/editar", methods=["GET", "POST"])
# Define la funcion editar_participa_grupo con los parametros declarados; su bloque realiza esta operacion.
def editar_participa_grupo(docente_cedula, grupo_investigacion_id):
    # Asigna a identidad el valor calculado a la derecha.
    identidad = {"docente_cedula": docente_cedula, "grupo_investigacion_id": grupo_investigacion_id}
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, ficha, errores = cliente_api.obtener_participa_grupo(identidad)
    # Ejecuta el bloque siguiente solo cuando se cumple: not ok.
    if not ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
        # Devuelve al llamador el resultado de la expresion indicada.
        return redirect(url_for("listar_participa_grupo"))
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones, disponibles = _opciones_participa_grupo()
    # Ejecuta el bloque siguiente solo cuando se cumple: request.method == "POST".
    if request.method == "POST":
        # Asigna a datos el valor calculado a la derecha.
        datos = _cuerpo_participa_grupo()
        # Ejecuta el bloque siguiente solo cuando se cumple: request.form.get("verbo") == "completa".
        if request.form.get("verbo") == "completa":
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            ok, errores = cliente_api.reemplazar_participa_grupo(identidad, datos)
        # Define el caso alternativo cuando las condiciones anteriores no se cumplen.
        else:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            ok, errores = cliente_api.actualizar_participa_grupo(identidad, _campos_cambiados(datos, ficha))
        # Ejecuta el bloque siguiente solo cuando se cumple: ok.
        if ok:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            flash("Se guardaron los cambios.", "exito")
            # Devuelve al llamador el resultado de la expresion indicada.
            return redirect(url_for("listar_participa_grupo"))
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
        # Asigna a ficha el valor calculado a la derecha.
        ficha = {**ficha, **datos}
    # Devuelve al llamador el resultado de la expresion indicada.
    return render_template("participa_grupo/formulario.html", ficha=ficha, editando=True, opciones=opciones, disponibles=disponibles)


# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route("/participa-grupo/<int:docente_cedula>/<int:grupo_investigacion_id>/eliminar", methods=["POST"])
# Define la funcion eliminar_participa_grupo con los parametros declarados; su bloque realiza esta operacion.
def eliminar_participa_grupo(docente_cedula, grupo_investigacion_id):
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, errores = cliente_api.eliminar_participa_grupo({"docente_cedula": docente_cedula, "grupo_investigacion_id": grupo_investigacion_id})
    # Ejecuta el bloque siguiente solo cuando se cumple: ok.
    if ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        flash("Se retiró la ficha.", "exito")
    # Define el caso alternativo cuando las condiciones anteriores no se cumplen.
    else:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
    # Devuelve al llamador el resultado de la expresion indicada.
    return redirect(url_for("listar_participa_grupo"))


# Define la funcion _opciones_semillero_linea con los parametros declarados; su bloque realiza esta operacion.
def _opciones_semillero_linea():
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones, disponibles = {}, True
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, filas, errores = cliente_api.listar_semillero()
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones["semillero"] = filas
    # Ejecuta el bloque siguiente solo cuando se cumple: not ok.
    if not ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
        # Asigna a disponibles el valor calculado a la derecha.
        disponibles = False
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, filas, errores = cliente_api.listar_linea_investigacion()
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones["linea_investigacion"] = filas
    # Ejecuta el bloque siguiente solo cuando se cumple: not ok.
    if not ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
        # Asigna a disponibles el valor calculado a la derecha.
        disponibles = False
    # Devuelve al llamador el resultado de la expresion indicada.
    return opciones, disponibles

# Define la funcion _cuerpo_semillero_linea con los parametros declarados; su bloque realiza esta operacion.
def _cuerpo_semillero_linea(crear=False):
    # Asigna a cuerpo el valor calculado a la derecha.
    cuerpo = {}
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    cuerpo["semillero"] = _valor_formulario("semillero", numerico=True, nullable=False)
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    cuerpo["linea_investigacion"] = _valor_formulario("linea_investigacion", numerico=True, nullable=False)
    # Devuelve al llamador el resultado de la expresion indicada.
    return cuerpo

# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route("/semillero-linea")
# Define la funcion listar_semillero_linea con los parametros declarados; su bloque realiza esta operacion.
def listar_semillero_linea():
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, filas, errores = cliente_api.listar_semillero_linea()
    # Ejecuta el bloque siguiente solo cuando se cumple: not ok.
    if not ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
    # Devuelve al llamador el resultado de la expresion indicada.
    return render_template("semillero_linea/lista.html", filas=filas)


# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route("/semillero-linea/nuevo", methods=["GET", "POST"])
# Define la funcion crear_semillero_linea con los parametros declarados; su bloque realiza esta operacion.
def crear_semillero_linea():
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones, disponibles = _opciones_semillero_linea()
    # Asigna a ficha el valor calculado a la derecha.
    ficha = None
    # Ejecuta el bloque siguiente solo cuando se cumple: request.method == "POST".
    if request.method == "POST":
        # Asigna a ficha el valor calculado a la derecha.
        ficha = _cuerpo_semillero_linea(crear=True)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        ok, errores = cliente_api.crear_semillero_linea(ficha)
        # Ejecuta el bloque siguiente solo cuando se cumple: ok.
        if ok:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            flash("Se agregó la ficha.", "exito")
            # Devuelve al llamador el resultado de la expresion indicada.
            return redirect(url_for("listar_semillero_linea"))
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
    # Devuelve al llamador el resultado de la expresion indicada.
    return render_template("semillero_linea/formulario.html", ficha=ficha, editando=False, opciones=opciones, disponibles=disponibles)


# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route("/semillero-linea/<int:semillero>/<int:linea_investigacion>/editar", methods=["GET", "POST"])
# Define la funcion editar_semillero_linea con los parametros declarados; su bloque realiza esta operacion.
def editar_semillero_linea(semillero, linea_investigacion):
    # Asigna a identidad el valor calculado a la derecha.
    identidad = {"semillero": semillero, "linea_investigacion": linea_investigacion}
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, ficha, errores = cliente_api.obtener_semillero_linea(identidad)
    # Ejecuta el bloque siguiente solo cuando se cumple: not ok.
    if not ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
        # Devuelve al llamador el resultado de la expresion indicada.
        return redirect(url_for("listar_semillero_linea"))
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones, disponibles = _opciones_semillero_linea()
    # Ejecuta el bloque siguiente solo cuando se cumple: request.method == "POST".
    if request.method == "POST":
        # Asigna a datos el valor calculado a la derecha.
        datos = _cuerpo_semillero_linea()
        # Ejecuta el bloque siguiente solo cuando se cumple: request.form.get("verbo") == "completa".
        if request.form.get("verbo") == "completa":
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            ok, errores = cliente_api.reemplazar_semillero_linea(identidad, datos)
        # Define el caso alternativo cuando las condiciones anteriores no se cumplen.
        else:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            ok, errores = cliente_api.actualizar_semillero_linea(identidad, _campos_cambiados(datos, ficha))
        # Ejecuta el bloque siguiente solo cuando se cumple: ok.
        if ok:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            flash("Se guardaron los cambios.", "exito")
            # Devuelve al llamador el resultado de la expresion indicada.
            return redirect(url_for("listar_semillero_linea"))
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
        # Asigna a ficha el valor calculado a la derecha.
        ficha = {**ficha, **datos}
    # Devuelve al llamador el resultado de la expresion indicada.
    return render_template("semillero_linea/formulario.html", ficha=ficha, editando=True, opciones=opciones, disponibles=disponibles)


# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route("/semillero-linea/<int:semillero>/<int:linea_investigacion>/eliminar", methods=["POST"])
# Define la funcion eliminar_semillero_linea con los parametros declarados; su bloque realiza esta operacion.
def eliminar_semillero_linea(semillero, linea_investigacion):
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, errores = cliente_api.eliminar_semillero_linea({"semillero": semillero, "linea_investigacion": linea_investigacion})
    # Ejecuta el bloque siguiente solo cuando se cumple: ok.
    if ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        flash("Se retiró la ficha.", "exito")
    # Define el caso alternativo cuando las condiciones anteriores no se cumplen.
    else:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
    # Devuelve al llamador el resultado de la expresion indicada.
    return redirect(url_for("listar_semillero_linea"))


# Define la funcion _opciones_grupo_linea con los parametros declarados; su bloque realiza esta operacion.
def _opciones_grupo_linea():
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones, disponibles = {}, True
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, filas, errores = cliente_api.listar_grupo_investigacion()
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones["grupo_investigacion"] = filas
    # Ejecuta el bloque siguiente solo cuando se cumple: not ok.
    if not ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
        # Asigna a disponibles el valor calculado a la derecha.
        disponibles = False
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, filas, errores = cliente_api.listar_linea_investigacion()
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones["linea_investigacion"] = filas
    # Ejecuta el bloque siguiente solo cuando se cumple: not ok.
    if not ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
        # Asigna a disponibles el valor calculado a la derecha.
        disponibles = False
    # Devuelve al llamador el resultado de la expresion indicada.
    return opciones, disponibles

# Define la funcion _cuerpo_grupo_linea con los parametros declarados; su bloque realiza esta operacion.
def _cuerpo_grupo_linea(crear=False):
    # Asigna a cuerpo el valor calculado a la derecha.
    cuerpo = {}
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    cuerpo["grupo_investigacion"] = _valor_formulario("grupo_investigacion", numerico=True, nullable=False)
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    cuerpo["linea_investigacion"] = _valor_formulario("linea_investigacion", numerico=True, nullable=False)
    # Devuelve al llamador el resultado de la expresion indicada.
    return cuerpo

# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route("/grupo-linea")
# Define la funcion listar_grupo_linea con los parametros declarados; su bloque realiza esta operacion.
def listar_grupo_linea():
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, filas, errores = cliente_api.listar_grupo_linea()
    # Ejecuta el bloque siguiente solo cuando se cumple: not ok.
    if not ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
    # Devuelve al llamador el resultado de la expresion indicada.
    return render_template("grupo_linea/lista.html", filas=filas)


# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route("/grupo-linea/nuevo", methods=["GET", "POST"])
# Define la funcion crear_grupo_linea con los parametros declarados; su bloque realiza esta operacion.
def crear_grupo_linea():
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones, disponibles = _opciones_grupo_linea()
    # Asigna a ficha el valor calculado a la derecha.
    ficha = None
    # Ejecuta el bloque siguiente solo cuando se cumple: request.method == "POST".
    if request.method == "POST":
        # Asigna a ficha el valor calculado a la derecha.
        ficha = _cuerpo_grupo_linea(crear=True)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        ok, errores = cliente_api.crear_grupo_linea(ficha)
        # Ejecuta el bloque siguiente solo cuando se cumple: ok.
        if ok:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            flash("Se agregó la ficha.", "exito")
            # Devuelve al llamador el resultado de la expresion indicada.
            return redirect(url_for("listar_grupo_linea"))
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
    # Devuelve al llamador el resultado de la expresion indicada.
    return render_template("grupo_linea/formulario.html", ficha=ficha, editando=False, opciones=opciones, disponibles=disponibles)


# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route("/grupo-linea/<int:grupo_investigacion>/<int:linea_investigacion>/editar", methods=["GET", "POST"])
# Define la funcion editar_grupo_linea con los parametros declarados; su bloque realiza esta operacion.
def editar_grupo_linea(grupo_investigacion, linea_investigacion):
    # Asigna a identidad el valor calculado a la derecha.
    identidad = {"grupo_investigacion": grupo_investigacion, "linea_investigacion": linea_investigacion}
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, ficha, errores = cliente_api.obtener_grupo_linea(identidad)
    # Ejecuta el bloque siguiente solo cuando se cumple: not ok.
    if not ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
        # Devuelve al llamador el resultado de la expresion indicada.
        return redirect(url_for("listar_grupo_linea"))
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones, disponibles = _opciones_grupo_linea()
    # Ejecuta el bloque siguiente solo cuando se cumple: request.method == "POST".
    if request.method == "POST":
        # Asigna a datos el valor calculado a la derecha.
        datos = _cuerpo_grupo_linea()
        # Ejecuta el bloque siguiente solo cuando se cumple: request.form.get("verbo") == "completa".
        if request.form.get("verbo") == "completa":
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            ok, errores = cliente_api.reemplazar_grupo_linea(identidad, datos)
        # Define el caso alternativo cuando las condiciones anteriores no se cumplen.
        else:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            ok, errores = cliente_api.actualizar_grupo_linea(identidad, _campos_cambiados(datos, ficha))
        # Ejecuta el bloque siguiente solo cuando se cumple: ok.
        if ok:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            flash("Se guardaron los cambios.", "exito")
            # Devuelve al llamador el resultado de la expresion indicada.
            return redirect(url_for("listar_grupo_linea"))
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
        # Asigna a ficha el valor calculado a la derecha.
        ficha = {**ficha, **datos}
    # Devuelve al llamador el resultado de la expresion indicada.
    return render_template("grupo_linea/formulario.html", ficha=ficha, editando=True, opciones=opciones, disponibles=disponibles)


# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route("/grupo-linea/<int:grupo_investigacion>/<int:linea_investigacion>/eliminar", methods=["POST"])
# Define la funcion eliminar_grupo_linea con los parametros declarados; su bloque realiza esta operacion.
def eliminar_grupo_linea(grupo_investigacion, linea_investigacion):
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, errores = cliente_api.eliminar_grupo_linea({"grupo_investigacion": grupo_investigacion, "linea_investigacion": linea_investigacion})
    # Ejecuta el bloque siguiente solo cuando se cumple: ok.
    if ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        flash("Se retiró la ficha.", "exito")
    # Define el caso alternativo cuando las condiciones anteriores no se cumplen.
    else:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
    # Devuelve al llamador el resultado de la expresion indicada.
    return redirect(url_for("listar_grupo_linea"))


# Define la funcion _opciones_ac_linea con los parametros declarados; su bloque realiza esta operacion.
def _opciones_ac_linea():
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones, disponibles = {}, True
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, filas, errores = cliente_api.listar_linea_investigacion()
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones["linea_investigacion"] = filas
    # Ejecuta el bloque siguiente solo cuando se cumple: not ok.
    if not ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
        # Asigna a disponibles el valor calculado a la derecha.
        disponibles = False
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, filas, errores = cliente_api.listar_areas_conocimiento()
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones["area_conocimiento"] = filas
    # Ejecuta el bloque siguiente solo cuando se cumple: not ok.
    if not ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
        # Asigna a disponibles el valor calculado a la derecha.
        disponibles = False
    # Devuelve al llamador el resultado de la expresion indicada.
    return opciones, disponibles

# Define la funcion _cuerpo_ac_linea con los parametros declarados; su bloque realiza esta operacion.
def _cuerpo_ac_linea(crear=False):
    # Asigna a cuerpo el valor calculado a la derecha.
    cuerpo = {}
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    cuerpo["linea_investigacion"] = _valor_formulario("linea_investigacion", numerico=True, nullable=False)
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    cuerpo["area_conocimiento"] = _valor_formulario("area_conocimiento", numerico=False, nullable=False)
    # Devuelve al llamador el resultado de la expresion indicada.
    return cuerpo

# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route("/ac-linea")
# Define la funcion listar_ac_linea con los parametros declarados; su bloque realiza esta operacion.
def listar_ac_linea():
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, filas, errores = cliente_api.listar_ac_linea()
    # Ejecuta el bloque siguiente solo cuando se cumple: not ok.
    if not ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
    # Devuelve al llamador el resultado de la expresion indicada.
    return render_template("ac_linea/lista.html", filas=filas)


# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route("/ac-linea/nuevo", methods=["GET", "POST"])
# Define la funcion crear_ac_linea con los parametros declarados; su bloque realiza esta operacion.
def crear_ac_linea():
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones, disponibles = _opciones_ac_linea()
    # Asigna a ficha el valor calculado a la derecha.
    ficha = None
    # Ejecuta el bloque siguiente solo cuando se cumple: request.method == "POST".
    if request.method == "POST":
        # Asigna a ficha el valor calculado a la derecha.
        ficha = _cuerpo_ac_linea(crear=True)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        ok, errores = cliente_api.crear_ac_linea(ficha)
        # Ejecuta el bloque siguiente solo cuando se cumple: ok.
        if ok:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            flash("Se agregó la ficha.", "exito")
            # Devuelve al llamador el resultado de la expresion indicada.
            return redirect(url_for("listar_ac_linea"))
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
    # Devuelve al llamador el resultado de la expresion indicada.
    return render_template("ac_linea/formulario.html", ficha=ficha, editando=False, opciones=opciones, disponibles=disponibles)


# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route("/ac-linea/<int:linea_investigacion>/<string:area_conocimiento>/editar", methods=["GET", "POST"])
# Define la funcion editar_ac_linea con los parametros declarados; su bloque realiza esta operacion.
def editar_ac_linea(linea_investigacion, area_conocimiento):
    # Asigna a identidad el valor calculado a la derecha.
    identidad = {"linea_investigacion": linea_investigacion, "area_conocimiento": area_conocimiento}
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, ficha, errores = cliente_api.obtener_ac_linea(identidad)
    # Ejecuta el bloque siguiente solo cuando se cumple: not ok.
    if not ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
        # Devuelve al llamador el resultado de la expresion indicada.
        return redirect(url_for("listar_ac_linea"))
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones, disponibles = _opciones_ac_linea()
    # Ejecuta el bloque siguiente solo cuando se cumple: request.method == "POST".
    if request.method == "POST":
        # Asigna a datos el valor calculado a la derecha.
        datos = _cuerpo_ac_linea()
        # Ejecuta el bloque siguiente solo cuando se cumple: request.form.get("verbo") == "completa".
        if request.form.get("verbo") == "completa":
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            ok, errores = cliente_api.reemplazar_ac_linea(identidad, datos)
        # Define el caso alternativo cuando las condiciones anteriores no se cumplen.
        else:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            ok, errores = cliente_api.actualizar_ac_linea(identidad, _campos_cambiados(datos, ficha))
        # Ejecuta el bloque siguiente solo cuando se cumple: ok.
        if ok:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            flash("Se guardaron los cambios.", "exito")
            # Devuelve al llamador el resultado de la expresion indicada.
            return redirect(url_for("listar_ac_linea"))
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
        # Asigna a ficha el valor calculado a la derecha.
        ficha = {**ficha, **datos}
    # Devuelve al llamador el resultado de la expresion indicada.
    return render_template("ac_linea/formulario.html", ficha=ficha, editando=True, opciones=opciones, disponibles=disponibles)


# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route("/ac-linea/<int:linea_investigacion>/<string:area_conocimiento>/eliminar", methods=["POST"])
# Define la funcion eliminar_ac_linea con los parametros declarados; su bloque realiza esta operacion.
def eliminar_ac_linea(linea_investigacion, area_conocimiento):
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, errores = cliente_api.eliminar_ac_linea({"linea_investigacion": linea_investigacion, "area_conocimiento": area_conocimiento})
    # Ejecuta el bloque siguiente solo cuando se cumple: ok.
    if ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        flash("Se retiró la ficha.", "exito")
    # Define el caso alternativo cuando las condiciones anteriores no se cumplen.
    else:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
    # Devuelve al llamador el resultado de la expresion indicada.
    return redirect(url_for("listar_ac_linea"))


# Define la funcion _opciones_ods_linea con los parametros declarados; su bloque realiza esta operacion.
def _opciones_ods_linea():
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones, disponibles = {}, True
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, filas, errores = cliente_api.listar_linea_investigacion()
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones["linea_investigacion"] = filas
    # Ejecuta el bloque siguiente solo cuando se cumple: not ok.
    if not ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
        # Asigna a disponibles el valor calculado a la derecha.
        disponibles = False
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, filas, errores = cliente_api.listar_objetivo_desarrollo_sostenible()
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones["ods"] = filas
    # Ejecuta el bloque siguiente solo cuando se cumple: not ok.
    if not ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
        # Asigna a disponibles el valor calculado a la derecha.
        disponibles = False
    # Devuelve al llamador el resultado de la expresion indicada.
    return opciones, disponibles

# Define la funcion _cuerpo_ods_linea con los parametros declarados; su bloque realiza esta operacion.
def _cuerpo_ods_linea(crear=False):
    # Asigna a cuerpo el valor calculado a la derecha.
    cuerpo = {}
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    cuerpo["linea_investigacion"] = _valor_formulario("linea_investigacion", numerico=True, nullable=False)
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    cuerpo["ods"] = _valor_formulario("ods", numerico=True, nullable=False)
    # Devuelve al llamador el resultado de la expresion indicada.
    return cuerpo

# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route("/ods-linea")
# Define la funcion listar_ods_linea con los parametros declarados; su bloque realiza esta operacion.
def listar_ods_linea():
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, filas, errores = cliente_api.listar_ods_linea()
    # Ejecuta el bloque siguiente solo cuando se cumple: not ok.
    if not ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
    # Devuelve al llamador el resultado de la expresion indicada.
    return render_template("ods_linea/lista.html", filas=filas)


# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route("/ods-linea/nuevo", methods=["GET", "POST"])
# Define la funcion crear_ods_linea con los parametros declarados; su bloque realiza esta operacion.
def crear_ods_linea():
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones, disponibles = _opciones_ods_linea()
    # Asigna a ficha el valor calculado a la derecha.
    ficha = None
    # Ejecuta el bloque siguiente solo cuando se cumple: request.method == "POST".
    if request.method == "POST":
        # Asigna a ficha el valor calculado a la derecha.
        ficha = _cuerpo_ods_linea(crear=True)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        ok, errores = cliente_api.crear_ods_linea(ficha)
        # Ejecuta el bloque siguiente solo cuando se cumple: ok.
        if ok:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            flash("Se agregó la ficha.", "exito")
            # Devuelve al llamador el resultado de la expresion indicada.
            return redirect(url_for("listar_ods_linea"))
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
    # Devuelve al llamador el resultado de la expresion indicada.
    return render_template("ods_linea/formulario.html", ficha=ficha, editando=False, opciones=opciones, disponibles=disponibles)


# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route("/ods-linea/<int:linea_investigacion>/<int:ods>/editar", methods=["GET", "POST"])
# Define la funcion editar_ods_linea con los parametros declarados; su bloque realiza esta operacion.
def editar_ods_linea(linea_investigacion, ods):
    # Asigna a identidad el valor calculado a la derecha.
    identidad = {"linea_investigacion": linea_investigacion, "ods": ods}
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, ficha, errores = cliente_api.obtener_ods_linea(identidad)
    # Ejecuta el bloque siguiente solo cuando se cumple: not ok.
    if not ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
        # Devuelve al llamador el resultado de la expresion indicada.
        return redirect(url_for("listar_ods_linea"))
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones, disponibles = _opciones_ods_linea()
    # Ejecuta el bloque siguiente solo cuando se cumple: request.method == "POST".
    if request.method == "POST":
        # Asigna a datos el valor calculado a la derecha.
        datos = _cuerpo_ods_linea()
        # Ejecuta el bloque siguiente solo cuando se cumple: request.form.get("verbo") == "completa".
        if request.form.get("verbo") == "completa":
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            ok, errores = cliente_api.reemplazar_ods_linea(identidad, datos)
        # Define el caso alternativo cuando las condiciones anteriores no se cumplen.
        else:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            ok, errores = cliente_api.actualizar_ods_linea(identidad, _campos_cambiados(datos, ficha))
        # Ejecuta el bloque siguiente solo cuando se cumple: ok.
        if ok:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            flash("Se guardaron los cambios.", "exito")
            # Devuelve al llamador el resultado de la expresion indicada.
            return redirect(url_for("listar_ods_linea"))
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
        # Asigna a ficha el valor calculado a la derecha.
        ficha = {**ficha, **datos}
    # Devuelve al llamador el resultado de la expresion indicada.
    return render_template("ods_linea/formulario.html", ficha=ficha, editando=True, opciones=opciones, disponibles=disponibles)


# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route("/ods-linea/<int:linea_investigacion>/<int:ods>/eliminar", methods=["POST"])
# Define la funcion eliminar_ods_linea con los parametros declarados; su bloque realiza esta operacion.
def eliminar_ods_linea(linea_investigacion, ods):
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, errores = cliente_api.eliminar_ods_linea({"linea_investigacion": linea_investigacion, "ods": ods})
    # Ejecuta el bloque siguiente solo cuando se cumple: ok.
    if ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        flash("Se retiró la ficha.", "exito")
    # Define el caso alternativo cuando las condiciones anteriores no se cumplen.
    else:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
    # Devuelve al llamador el resultado de la expresion indicada.
    return redirect(url_for("listar_ods_linea"))


# Define la funcion _opciones_aa_linea con los parametros declarados; su bloque realiza esta operacion.
def _opciones_aa_linea():
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones, disponibles = {}, True
    # Asigna a mensajes el valor calculado a la derecha.
    mensajes = []
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, filas, errores = cliente_api.listar_area_aplicacion()
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones["area_aplicacion"] = filas
    # Ejecuta el bloque siguiente solo cuando se cumple: not ok.
    if not ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
        # Asigna a disponibles el valor calculado a la derecha.
        disponibles = False
    # Prueba esta condicion alternativa si las anteriores fueron falsas.
    elif not filas:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        mensajes.append("No hay áreas de aplicación activas para seleccionar.")
        # Asigna a disponibles el valor calculado a la derecha.
        disponibles = False
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, filas, errores = cliente_api.listar_linea_investigacion()
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones["linea_investigacion"] = filas
    # Ejecuta el bloque siguiente solo cuando se cumple: not ok.
    if not ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
        # Asigna a disponibles el valor calculado a la derecha.
        disponibles = False
    # Prueba esta condicion alternativa si las anteriores fueron falsas.
    elif not filas:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        mensajes.append("No hay líneas de investigación activas para seleccionar.")
        # Asigna a disponibles el valor calculado a la derecha.
        disponibles = False
    # Devuelve al llamador el resultado de la expresion indicada.
    return opciones, disponibles, " ".join(mensajes)

# Define la funcion _cuerpo_aa_linea con los parametros declarados; su bloque realiza esta operacion.
def _cuerpo_aa_linea(crear=False):
    # Asigna a cuerpo el valor calculado a la derecha.
    cuerpo = {}
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    cuerpo["area_aplicacion"] = _valor_formulario("area_aplicacion", numerico=True, nullable=False)
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    cuerpo["linea_investigacion"] = _valor_formulario("linea_investigacion", numerico=True, nullable=False)
    # Devuelve al llamador el resultado de la expresion indicada.
    return cuerpo

# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route("/aa-linea")
# Define la funcion listar_aa_linea con los parametros declarados; su bloque realiza esta operacion.
def listar_aa_linea():
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, filas, errores = cliente_api.listar_aa_linea()
    # Ejecuta el bloque siguiente solo cuando se cumple: not ok.
    if not ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
    # Devuelve al llamador el resultado de la expresion indicada.
    return render_template("aa_linea/lista.html", filas=filas)


# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route("/aa-linea/nuevo", methods=["GET", "POST"])
# Define la funcion crear_aa_linea con los parametros declarados; su bloque realiza esta operacion.
def crear_aa_linea():
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones, disponibles, mensaje_opciones = _opciones_aa_linea()
    # Asigna a ficha el valor calculado a la derecha.
    ficha = None
    # Ejecuta el bloque siguiente solo cuando se cumple: request.method == "POST".
    if request.method == "POST":
        # Asigna a ficha el valor calculado a la derecha.
        ficha = _cuerpo_aa_linea(crear=True)
        # Ejecuta el bloque siguiente solo cuando se cumple: not disponibles.
        if not disponibles:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            _avisar([mensaje_opciones])
        # Prueba esta condicion alternativa si las anteriores fueron falsas.
        elif not ficha["linea_investigacion"]:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            _avisar(["Selecciona una línea de investigación"])
        # Define el caso alternativo cuando las condiciones anteriores no se cumplen.
        else:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            ok, errores = cliente_api.crear_aa_linea(ficha)
            # Ejecuta el bloque siguiente solo cuando se cumple: ok.
            if ok:
                # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                flash("Se agregó la ficha.", "exito")
                # Devuelve al llamador el resultado de la expresion indicada.
                return redirect(url_for("listar_aa_linea"))
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            _avisar(errores)
    # Devuelve al llamador el resultado de la expresion indicada.
    return render_template("aa_linea/formulario.html", ficha=ficha, editando=False,
                           # Asigna a opciones el valor calculado a la derecha.
                           opciones=opciones, disponibles=disponibles,
                           # Asigna a mensaje_opciones el valor calculado a la derecha.
                           mensaje_opciones=mensaje_opciones)


# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route("/aa-linea/<int:area_aplicacion>/<int:linea_investigacion>/editar", methods=["GET", "POST"])
# Define la funcion editar_aa_linea con los parametros declarados; su bloque realiza esta operacion.
def editar_aa_linea(area_aplicacion, linea_investigacion):
    # Asigna a identidad el valor calculado a la derecha.
    identidad = {"area_aplicacion": area_aplicacion, "linea_investigacion": linea_investigacion}
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, ficha, errores = cliente_api.obtener_aa_linea(identidad)
    # Ejecuta el bloque siguiente solo cuando se cumple: not ok.
    if not ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
        # Devuelve al llamador el resultado de la expresion indicada.
        return redirect(url_for("listar_aa_linea"))
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    opciones, disponibles, mensaje_opciones = _opciones_aa_linea()
    # Ejecuta el bloque siguiente solo cuando se cumple: request.method == "POST".
    if request.method == "POST":
        # Asigna a datos el valor calculado a la derecha.
        datos = _cuerpo_aa_linea()
        # Ejecuta el bloque siguiente solo cuando se cumple: not disponibles.
        if not disponibles:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            _avisar([mensaje_opciones])
            # Asigna a ok el valor calculado a la derecha.
            ok = False
            # Asigna a errores el valor calculado a la derecha.
            errores = []
        # Prueba esta condicion alternativa si las anteriores fueron falsas.
        elif not datos["linea_investigacion"]:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            _avisar(["Selecciona una línea de investigación"])
            # Asigna a ok el valor calculado a la derecha.
            ok = False
            # Asigna a errores el valor calculado a la derecha.
            errores = []
        # Prueba esta condicion alternativa si las anteriores fueron falsas.
        elif request.form.get("verbo") == "completa":
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            ok, errores = cliente_api.reemplazar_aa_linea(identidad, datos)
        # Define el caso alternativo cuando las condiciones anteriores no se cumplen.
        else:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            ok, errores = cliente_api.actualizar_aa_linea(identidad, _campos_cambiados(datos, ficha))
        # Ejecuta el bloque siguiente solo cuando se cumple: ok.
        if ok:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            flash("Se guardaron los cambios.", "exito")
            # Devuelve al llamador el resultado de la expresion indicada.
            return redirect(url_for("listar_aa_linea"))
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
        # Asigna a ficha el valor calculado a la derecha.
        ficha = {**ficha, **datos}
    # Devuelve al llamador el resultado de la expresion indicada.
    return render_template("aa_linea/formulario.html", ficha=ficha, editando=True,
                           # Asigna a opciones el valor calculado a la derecha.
                           opciones=opciones, disponibles=disponibles,
                           # Asigna a mensaje_opciones el valor calculado a la derecha.
                           mensaje_opciones=mensaje_opciones)


# Aplica @app.route a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@app.route("/aa-linea/<int:area_aplicacion>/<int:linea_investigacion>/eliminar", methods=["POST"])
# Define la funcion eliminar_aa_linea con los parametros declarados; su bloque realiza esta operacion.
def eliminar_aa_linea(area_aplicacion, linea_investigacion):
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    ok, errores = cliente_api.eliminar_aa_linea({"area_aplicacion": area_aplicacion, "linea_investigacion": linea_investigacion})
    # Ejecuta el bloque siguiente solo cuando se cumple: ok.
    if ok:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        flash("Se retiró la ficha.", "exito")
    # Define el caso alternativo cuando las condiciones anteriores no se cumplen.
    else:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        _avisar(errores)
    # Devuelve al llamador el resultado de la expresion indicada.
    return redirect(url_for("listar_aa_linea"))



# Ejecuta el bloque siguiente solo cuando se cumple: __name__ == "__main__".
if __name__ == "__main__":
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    app.run(host="0.0.0.0", port=PUERTO, debug=True)
