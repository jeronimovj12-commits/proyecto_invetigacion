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

import os

from flask import Flask, flash, redirect, render_template, request, url_for

import cliente_api

app = Flask(__name__)

# `flash` guarda los avisos en la sesión, y la sesión va firmada: sin clave,
# Flask no arranca. En un proyecto real esto vive fuera de git.
app.secret_key = os.environ.get("CLAVE_SESION", "Paradigmas123!Sesion")

PUERTO = int(os.environ.get("PUERTO", 8078))


def _avisar(errores) -> None:
    """Cada error de la API se muestra como un aviso rojo, uno por línea."""
    for mensaje in errores:
        flash(mensaje, "error")


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
    texto = (texto or "").strip()
    if texto == "":
        return ""
    try:
        return int(texto)
    except ValueError:
        return texto


def _si_lleno(cuerpo: dict, campo: str, valor) -> None:
    """Mete el campo SOLO si la persona escribió algo.

    Es la mitad del contraste entre los dos botones de guardar: lo que no se
    diligencia **no viaja**, y la API deja ese campo como estaba.
    """
    if valor not in ("", None):
        cuerpo[campo] = valor


# ======================================================================
# EL INICIO
# ======================================================================


@app.route("/")
def inicio():
    return render_template("inicio.html")


# ======================================================================
# ÁREAS DE CONOCIMIENTO
# ======================================================================


@app.route("/areas-de-conocimiento")
def listar_areas_conocimiento():
    ok, filas, errores = cliente_api.listar_areas_conocimiento()
    if not ok:
        _avisar(errores)
    # Aun con error se pinta la pantalla: el usuario ve el aviso DENTRO de la
    # aplicación, no una página de error del servidor.
    return render_template("areas_conocimiento/lista.html", filas=filas)


@app.route("/areas-de-conocimiento/nuevo", methods=["GET", "POST"])
def crear_area_conocimiento():
    if request.method == "GET":
        return render_template("areas_conocimiento/formulario.html", ficha=None, editando=False)

    cuerpo = _cuerpo_completo(con_llave=True)
    ok, errores = cliente_api.crear_area_conocimiento(cuerpo)
    if ok:
        flash("Se agregó la ficha.", "exito")
        return redirect(url_for("listar_areas_conocimiento"))

    # Se devuelve el formulario CON lo que la persona había escrito: perder lo
    # digitado por un error de validación es castigarla dos veces.
    _avisar(errores)
    return render_template("areas_conocimiento/formulario.html", ficha=cuerpo, editando=False)


@app.route("/areas-de-conocimiento/<string:id>/editar", methods=["GET", "POST"])
def editar_area_conocimiento(id):
    if request.method == "GET":
        ok, ficha, errores = cliente_api.obtener_area_conocimiento(id)
        if not ok:
            _avisar(errores)
            return redirect(url_for("listar_areas_conocimiento"))
        return render_template("areas_conocimiento/formulario.html", ficha=ficha, editando=True)

    # ==================================================================
    # QUÉ BOTÓN SE OPRIMIÓ DECIDE QUÉ SE ENVÍA.
    # La diferencia NO está en un `if` de negocio: está en el CUERPO de la
    # petición. Uno manda un reemplazo completo y el otro solo lo llenado.
    # ==================================================================
    if request.form.get("verbo") == "completa":
        ok, errores = cliente_api.reemplazar_area_conocimiento(id, _cuerpo_completo())
    else:
        ok, errores = cliente_api.actualizar_area_conocimiento(id, _cuerpo_parcial())

    if ok:
        flash("Se guardaron los cambios.", "exito")
        return redirect(url_for("listar_areas_conocimiento"))

    _avisar(errores)
    ficha = dict(request.form)
    ficha["id"] = id
    return render_template("areas_conocimiento/formulario.html", ficha=ficha, editando=True)


@app.route("/areas-de-conocimiento/<string:id>/eliminar", methods=["POST"])
def eliminar_area_conocimiento(id):
    """Se exige POST a propósito: un enlace GET que borra lo puede disparar
    el navegador solo, al precargar la página."""
    ok, errores = cliente_api.eliminar_area_conocimiento(id)
    if ok:
        flash("Se retiró la ficha.", "exito")
    else:
        _avisar(errores)
    return redirect(url_for("listar_areas_conocimiento"))


# ======================================================================
# Los dos armadores del cuerpo
# ======================================================================


def _cuerpo_completo(con_llave: bool = False) -> dict:
    """Todos los campos, vayan llenos o no. Lo usan POST y PUT.

    Por eso un campo obligatorio en blanco se rechaza: viaja vacío, y la API
    dice que no cumple.
    """
    cuerpo = {
        "gran_area": request.form.get("gran_area", "").strip(),
        "area": request.form.get("area", "").strip(),
        "disciplina": request.form.get("disciplina", "").strip(),
    }

    if con_llave:
        cuerpo["id"] = request.form.get("id", "").strip()
    return cuerpo


def _cuerpo_parcial() -> dict:
    """Solo lo diligenciado. Lo usa PATCH.

    El mismo formulario a medio llenar que el reemplazo rechaza, aquí
    funciona — y lo que no se envía, la API lo deja como estaba.
    """
    cuerpo: dict = {}
    _si_lleno(cuerpo, "gran_area", request.form.get("gran_area", "").strip())
    _si_lleno(cuerpo, "area", request.form.get("area", "").strip())
    _si_lleno(cuerpo, "disciplina", request.form.get("disciplina", "").strip())
    return cuerpo


# ======================================================================
# La pantalla de «esa página no existe»
# ======================================================================


@app.errorhandler(404)
def no_encontrada(_error):
    """Con el marco de la aplicación puesto, no una página en blanco."""
    return render_template("no_encontrada.html"), 404




def _valor_formulario(campo, numerico=False, nullable=False):
    valor = request.form.get(campo, "").strip()
    if nullable and valor in ("", "__nulo__"):
        return None
    return _entero(valor) if numerico else valor


def _campos_cambiados(datos, ficha):
    return {campo: valor for campo, valor in datos.items() if valor != ficha.get(campo)}

def _opciones_docente():
    opciones, disponibles = {}, True
    ok, filas, errores = cliente_api.listar_linea_investigacion()
    opciones["linea_investigacion_principal"] = filas
    if not ok:
        _avisar(errores)
        disponibles = False
    return opciones, disponibles

def _cuerpo_docente(crear=False):
    cuerpo = {}
    if crear: cuerpo["cedula"] = _valor_formulario("cedula", numerico=True, nullable=False)
    cuerpo["nombres"] = _valor_formulario("nombres", numerico=False, nullable=False)
    cuerpo["apellidos"] = _valor_formulario("apellidos", numerico=False, nullable=False)
    cuerpo["genero"] = _valor_formulario("genero", numerico=False, nullable=False)
    cuerpo["cargo"] = _valor_formulario("cargo", numerico=False, nullable=False)
    cuerpo["fecha_nacimiento"] = _valor_formulario("fecha_nacimiento", numerico=False, nullable=False)
    cuerpo["correo"] = _valor_formulario("correo", numerico=False, nullable=False)
    cuerpo["telefono"] = _valor_formulario("telefono", numerico=False, nullable=False)
    cuerpo["url_cvlac"] = _valor_formulario("url_cvlac", numerico=False, nullable=False)
    cuerpo["fecha_actualizacion"] = _valor_formulario("fecha_actualizacion", numerico=False, nullable=False)
    cuerpo["escalafon"] = _valor_formulario("escalafon", numerico=False, nullable=False)
    cuerpo["perfil"] = _valor_formulario("perfil", numerico=False, nullable=False)
    cuerpo["cat_minciencia"] = _valor_formulario("cat_minciencia", numerico=False, nullable=True)
    cuerpo["conv_minciencia"] = _valor_formulario("conv_minciencia", numerico=False, nullable=False)
    cuerpo["nacionalidaad"] = _valor_formulario("nacionalidaad", numerico=False, nullable=False)
    cuerpo["linea_investigacion_principal"] = _valor_formulario("linea_investigacion_principal", numerico=True, nullable=True)
    return cuerpo

@app.route("/docente")
def listar_docente():
    ok, filas, errores = cliente_api.listar_docente()
    if not ok:
        _avisar(errores)
    return render_template("docente/lista.html", filas=filas)


@app.route("/docente/nuevo", methods=["GET", "POST"])
def crear_docente():
    opciones, disponibles = _opciones_docente()
    ficha = None
    if request.method == "POST":
        ficha = _cuerpo_docente(crear=True)
        ok, errores = cliente_api.crear_docente(ficha)
        if ok:
            flash("Se agregó la ficha.", "exito")
            return redirect(url_for("listar_docente"))
        _avisar(errores)
    return render_template("docente/formulario.html", ficha=ficha, editando=False, opciones=opciones, disponibles=disponibles)


@app.route("/docente/<int:cedula>/editar", methods=["GET", "POST"])
def editar_docente(cedula):
    identidad = {"cedula": cedula}
    ok, ficha, errores = cliente_api.obtener_docente(identidad)
    if not ok:
        _avisar(errores)
        return redirect(url_for("listar_docente"))
    opciones, disponibles = _opciones_docente()
    if request.method == "POST":
        datos = _cuerpo_docente()
        if request.form.get("verbo") == "completa":
            ok, errores = cliente_api.reemplazar_docente(identidad, datos)
        else:
            ok, errores = cliente_api.actualizar_docente(identidad, _campos_cambiados(datos, ficha))
        if ok:
            flash("Se guardaron los cambios.", "exito")
            return redirect(url_for("listar_docente"))
        _avisar(errores)
        ficha = {**ficha, **datos}
    return render_template("docente/formulario.html", ficha=ficha, editando=True, opciones=opciones, disponibles=disponibles)


@app.route("/docente/<int:cedula>/eliminar", methods=["POST"])
def eliminar_docente(cedula):
    ok, errores = cliente_api.eliminar_docente({"cedula": cedula})
    if ok:
        flash("Se retiró la ficha.", "exito")
    else:
        _avisar(errores)
    return redirect(url_for("listar_docente"))


def _opciones_grupo_investigacion():
    opciones, disponibles = {}, True
    ok, filas, errores = cliente_api.listar_universidad()
    opciones["universidsad"] = filas
    if not ok:
        _avisar(errores)
        disponibles = False
    return opciones, disponibles

def _cuerpo_grupo_investigacion(crear=False):
    cuerpo = {}
    if crear: cuerpo["id"] = _valor_formulario("id", numerico=True, nullable=False)
    cuerpo["nombre"] = _valor_formulario("nombre", numerico=False, nullable=False)
    cuerpo["url_gruplac"] = _valor_formulario("url_gruplac", numerico=False, nullable=True)
    cuerpo["categoria"] = _valor_formulario("categoria", numerico=False, nullable=True)
    cuerpo["convocatoria"] = _valor_formulario("convocatoria", numerico=False, nullable=True)
    cuerpo["fecha_fundacion"] = _valor_formulario("fecha_fundacion", numerico=False, nullable=False)
    cuerpo["universidsad"] = _valor_formulario("universidsad", numerico=True, nullable=True)
    cuerpo["interno"] = _valor_formulario("interno", numerico=True, nullable=False)
    cuerpo["ambito"] = _valor_formulario("ambito", numerico=False, nullable=False)
    return cuerpo

@app.route("/grupo-investigacion")
def listar_grupo_investigacion():
    ok, filas, errores = cliente_api.listar_grupo_investigacion()
    if not ok:
        _avisar(errores)
    return render_template("grupo_investigacion/lista.html", filas=filas)


@app.route("/grupo-investigacion/nuevo", methods=["GET", "POST"])
def crear_grupo_investigacion():
    opciones, disponibles = _opciones_grupo_investigacion()
    ficha = None
    if request.method == "POST":
        ficha = _cuerpo_grupo_investigacion(crear=True)
        ok, errores = cliente_api.crear_grupo_investigacion(ficha)
        if ok:
            flash("Se agregó la ficha.", "exito")
            return redirect(url_for("listar_grupo_investigacion"))
        _avisar(errores)
    return render_template("grupo_investigacion/formulario.html", ficha=ficha, editando=False, opciones=opciones, disponibles=disponibles)


@app.route("/grupo-investigacion/<int:id>/editar", methods=["GET", "POST"])
def editar_grupo_investigacion(id):
    identidad = {"id": id}
    ok, ficha, errores = cliente_api.obtener_grupo_investigacion(identidad)
    if not ok:
        _avisar(errores)
        return redirect(url_for("listar_grupo_investigacion"))
    opciones, disponibles = _opciones_grupo_investigacion()
    if request.method == "POST":
        datos = _cuerpo_grupo_investigacion()
        if request.form.get("verbo") == "completa":
            ok, errores = cliente_api.reemplazar_grupo_investigacion(identidad, datos)
        else:
            ok, errores = cliente_api.actualizar_grupo_investigacion(identidad, _campos_cambiados(datos, ficha))
        if ok:
            flash("Se guardaron los cambios.", "exito")
            return redirect(url_for("listar_grupo_investigacion"))
        _avisar(errores)
        ficha = {**ficha, **datos}
    return render_template("grupo_investigacion/formulario.html", ficha=ficha, editando=True, opciones=opciones, disponibles=disponibles)


@app.route("/grupo-investigacion/<int:id>/eliminar", methods=["POST"])
def eliminar_grupo_investigacion(id):
    ok, errores = cliente_api.eliminar_grupo_investigacion({"id": id})
    if ok:
        flash("Se retiró la ficha.", "exito")
    else:
        _avisar(errores)
    return redirect(url_for("listar_grupo_investigacion"))


def _opciones_semillero():
    opciones, disponibles = {}, True
    ok, filas, errores = cliente_api.listar_grupo_investigacion()
    opciones["grupo_investigacion"] = filas
    if not ok:
        _avisar(errores)
        disponibles = False
    return opciones, disponibles

def _cuerpo_semillero(crear=False):
    cuerpo = {}
    if crear: cuerpo["id"] = _valor_formulario("id", numerico=True, nullable=False)
    cuerpo["nombre"] = _valor_formulario("nombre", numerico=False, nullable=False)
    cuerpo["fecha_fundacion"] = _valor_formulario("fecha_fundacion", numerico=False, nullable=False)
    cuerpo["grupo_investigacion"] = _valor_formulario("grupo_investigacion", numerico=True, nullable=False)
    return cuerpo

@app.route("/semillero")
def listar_semillero():
    ok, filas, errores = cliente_api.listar_semillero()
    if not ok:
        _avisar(errores)
    return render_template("semillero/lista.html", filas=filas)


@app.route("/semillero/nuevo", methods=["GET", "POST"])
def crear_semillero():
    opciones, disponibles = _opciones_semillero()
    ficha = None
    if request.method == "POST":
        ficha = _cuerpo_semillero(crear=True)
        ok, errores = cliente_api.crear_semillero(ficha)
        if ok:
            flash("Se agregó la ficha.", "exito")
            return redirect(url_for("listar_semillero"))
        _avisar(errores)
    return render_template("semillero/formulario.html", ficha=ficha, editando=False, opciones=opciones, disponibles=disponibles)


@app.route("/semillero/<int:id>/editar", methods=["GET", "POST"])
def editar_semillero(id):
    identidad = {"id": id}
    ok, ficha, errores = cliente_api.obtener_semillero(identidad)
    if not ok:
        _avisar(errores)
        return redirect(url_for("listar_semillero"))
    opciones, disponibles = _opciones_semillero()
    if request.method == "POST":
        datos = _cuerpo_semillero()
        if request.form.get("verbo") == "completa":
            ok, errores = cliente_api.reemplazar_semillero(identidad, datos)
        else:
            ok, errores = cliente_api.actualizar_semillero(identidad, _campos_cambiados(datos, ficha))
        if ok:
            flash("Se guardaron los cambios.", "exito")
            return redirect(url_for("listar_semillero"))
        _avisar(errores)
        ficha = {**ficha, **datos}
    return render_template("semillero/formulario.html", ficha=ficha, editando=True, opciones=opciones, disponibles=disponibles)


@app.route("/semillero/<int:id>/eliminar", methods=["POST"])
def eliminar_semillero(id):
    ok, errores = cliente_api.eliminar_semillero({"id": id})
    if ok:
        flash("Se retiró la ficha.", "exito")
    else:
        _avisar(errores)
    return redirect(url_for("listar_semillero"))


def _opciones_participa_semillero():
    opciones, disponibles = {}, True
    ok, filas, errores = cliente_api.listar_docente()
    opciones["docente"] = filas
    if not ok:
        _avisar(errores)
        disponibles = False
    ok, filas, errores = cliente_api.listar_semillero()
    opciones["semillero"] = filas
    if not ok:
        _avisar(errores)
        disponibles = False
    return opciones, disponibles

def _cuerpo_participa_semillero(crear=False):
    cuerpo = {}
    cuerpo["docente"] = _valor_formulario("docente", numerico=True, nullable=False)
    cuerpo["semillero"] = _valor_formulario("semillero", numerico=True, nullable=False)
    cuerpo["rol"] = _valor_formulario("rol", numerico=False, nullable=False)
    cuerpo["fecha_inicio"] = _valor_formulario("fecha_inicio", numerico=False, nullable=False)
    cuerpo["fecha_fin"] = _valor_formulario("fecha_fin", numerico=False, nullable=True)
    return cuerpo

@app.route("/participa-semillero")
def listar_participa_semillero():
    ok, filas, errores = cliente_api.listar_participa_semillero()
    if not ok:
        _avisar(errores)
    return render_template("participa_semillero/lista.html", filas=filas)


@app.route("/participa-semillero/nuevo", methods=["GET", "POST"])
def crear_participa_semillero():
    opciones, disponibles = _opciones_participa_semillero()
    ficha = None
    if request.method == "POST":
        ficha = _cuerpo_participa_semillero(crear=True)
        ok, errores = cliente_api.crear_participa_semillero(ficha)
        if ok:
            flash("Se agregó la ficha.", "exito")
            return redirect(url_for("listar_participa_semillero"))
        _avisar(errores)
    return render_template("participa_semillero/formulario.html", ficha=ficha, editando=False, opciones=opciones, disponibles=disponibles)


@app.route("/participa-semillero/<int:docente>/<int:semillero>/editar", methods=["GET", "POST"])
def editar_participa_semillero(docente, semillero):
    identidad = {"docente": docente, "semillero": semillero}
    ok, ficha, errores = cliente_api.obtener_participa_semillero(identidad)
    if not ok:
        _avisar(errores)
        return redirect(url_for("listar_participa_semillero"))
    opciones, disponibles = _opciones_participa_semillero()
    if request.method == "POST":
        datos = _cuerpo_participa_semillero()
        if request.form.get("verbo") == "completa":
            ok, errores = cliente_api.reemplazar_participa_semillero(identidad, datos)
        else:
            ok, errores = cliente_api.actualizar_participa_semillero(identidad, _campos_cambiados(datos, ficha))
        if ok:
            flash("Se guardaron los cambios.", "exito")
            return redirect(url_for("listar_participa_semillero"))
        _avisar(errores)
        ficha = {**ficha, **datos}
    return render_template("participa_semillero/formulario.html", ficha=ficha, editando=True, opciones=opciones, disponibles=disponibles)


@app.route("/participa-semillero/<int:docente>/<int:semillero>/eliminar", methods=["POST"])
def eliminar_participa_semillero(docente, semillero):
    ok, errores = cliente_api.eliminar_participa_semillero({"docente": docente, "semillero": semillero})
    if ok:
        flash("Se retiró la ficha.", "exito")
    else:
        _avisar(errores)
    return redirect(url_for("listar_participa_semillero"))


def _opciones_participa_grupo():
    opciones, disponibles = {}, True
    ok, filas, errores = cliente_api.listar_docente()
    opciones["docente_cedula"] = filas
    if not ok:
        _avisar(errores)
        disponibles = False
    ok, filas, errores = cliente_api.listar_grupo_investigacion()
    opciones["grupo_investigacion_id"] = filas
    if not ok:
        _avisar(errores)
        disponibles = False
    return opciones, disponibles

def _cuerpo_participa_grupo(crear=False):
    cuerpo = {}
    cuerpo["docente_cedula"] = _valor_formulario("docente_cedula", numerico=True, nullable=False)
    cuerpo["grupo_investigacion_id"] = _valor_formulario("grupo_investigacion_id", numerico=True, nullable=False)
    cuerpo["rol"] = _valor_formulario("rol", numerico=False, nullable=False)
    cuerpo["fecha_inicio"] = _valor_formulario("fecha_inicio", numerico=False, nullable=False)
    cuerpo["fecha_fin"] = _valor_formulario("fecha_fin", numerico=False, nullable=True)
    return cuerpo

@app.route("/participa-grupo")
def listar_participa_grupo():
    ok, filas, errores = cliente_api.listar_participa_grupo()
    if not ok:
        _avisar(errores)
    return render_template("participa_grupo/lista.html", filas=filas)


@app.route("/participa-grupo/nuevo", methods=["GET", "POST"])
def crear_participa_grupo():
    opciones, disponibles = _opciones_participa_grupo()
    ficha = None
    if request.method == "POST":
        ficha = _cuerpo_participa_grupo(crear=True)
        ok, errores = cliente_api.crear_participa_grupo(ficha)
        if ok:
            flash("Se agregó la ficha.", "exito")
            return redirect(url_for("listar_participa_grupo"))
        _avisar(errores)
    return render_template("participa_grupo/formulario.html", ficha=ficha, editando=False, opciones=opciones, disponibles=disponibles)


@app.route("/participa-grupo/<int:docente_cedula>/<int:grupo_investigacion_id>/editar", methods=["GET", "POST"])
def editar_participa_grupo(docente_cedula, grupo_investigacion_id):
    identidad = {"docente_cedula": docente_cedula, "grupo_investigacion_id": grupo_investigacion_id}
    ok, ficha, errores = cliente_api.obtener_participa_grupo(identidad)
    if not ok:
        _avisar(errores)
        return redirect(url_for("listar_participa_grupo"))
    opciones, disponibles = _opciones_participa_grupo()
    if request.method == "POST":
        datos = _cuerpo_participa_grupo()
        if request.form.get("verbo") == "completa":
            ok, errores = cliente_api.reemplazar_participa_grupo(identidad, datos)
        else:
            ok, errores = cliente_api.actualizar_participa_grupo(identidad, _campos_cambiados(datos, ficha))
        if ok:
            flash("Se guardaron los cambios.", "exito")
            return redirect(url_for("listar_participa_grupo"))
        _avisar(errores)
        ficha = {**ficha, **datos}
    return render_template("participa_grupo/formulario.html", ficha=ficha, editando=True, opciones=opciones, disponibles=disponibles)


@app.route("/participa-grupo/<int:docente_cedula>/<int:grupo_investigacion_id>/eliminar", methods=["POST"])
def eliminar_participa_grupo(docente_cedula, grupo_investigacion_id):
    ok, errores = cliente_api.eliminar_participa_grupo({"docente_cedula": docente_cedula, "grupo_investigacion_id": grupo_investigacion_id})
    if ok:
        flash("Se retiró la ficha.", "exito")
    else:
        _avisar(errores)
    return redirect(url_for("listar_participa_grupo"))


def _opciones_semillero_linea():
    opciones, disponibles = {}, True
    ok, filas, errores = cliente_api.listar_semillero()
    opciones["semillero"] = filas
    if not ok:
        _avisar(errores)
        disponibles = False
    ok, filas, errores = cliente_api.listar_linea_investigacion()
    opciones["linea_investigacion"] = filas
    if not ok:
        _avisar(errores)
        disponibles = False
    return opciones, disponibles

def _cuerpo_semillero_linea(crear=False):
    cuerpo = {}
    cuerpo["semillero"] = _valor_formulario("semillero", numerico=True, nullable=False)
    cuerpo["linea_investigacion"] = _valor_formulario("linea_investigacion", numerico=True, nullable=False)
    return cuerpo

@app.route("/semillero-linea")
def listar_semillero_linea():
    ok, filas, errores = cliente_api.listar_semillero_linea()
    if not ok:
        _avisar(errores)
    return render_template("semillero_linea/lista.html", filas=filas)


@app.route("/semillero-linea/nuevo", methods=["GET", "POST"])
def crear_semillero_linea():
    opciones, disponibles = _opciones_semillero_linea()
    ficha = None
    if request.method == "POST":
        ficha = _cuerpo_semillero_linea(crear=True)
        ok, errores = cliente_api.crear_semillero_linea(ficha)
        if ok:
            flash("Se agregó la ficha.", "exito")
            return redirect(url_for("listar_semillero_linea"))
        _avisar(errores)
    return render_template("semillero_linea/formulario.html", ficha=ficha, editando=False, opciones=opciones, disponibles=disponibles)


@app.route("/semillero-linea/<int:semillero>/<int:linea_investigacion>/editar", methods=["GET", "POST"])
def editar_semillero_linea(semillero, linea_investigacion):
    identidad = {"semillero": semillero, "linea_investigacion": linea_investigacion}
    ok, ficha, errores = cliente_api.obtener_semillero_linea(identidad)
    if not ok:
        _avisar(errores)
        return redirect(url_for("listar_semillero_linea"))
    opciones, disponibles = _opciones_semillero_linea()
    if request.method == "POST":
        datos = _cuerpo_semillero_linea()
        if request.form.get("verbo") == "completa":
            ok, errores = cliente_api.reemplazar_semillero_linea(identidad, datos)
        else:
            ok, errores = cliente_api.actualizar_semillero_linea(identidad, _campos_cambiados(datos, ficha))
        if ok:
            flash("Se guardaron los cambios.", "exito")
            return redirect(url_for("listar_semillero_linea"))
        _avisar(errores)
        ficha = {**ficha, **datos}
    return render_template("semillero_linea/formulario.html", ficha=ficha, editando=True, opciones=opciones, disponibles=disponibles)


@app.route("/semillero-linea/<int:semillero>/<int:linea_investigacion>/eliminar", methods=["POST"])
def eliminar_semillero_linea(semillero, linea_investigacion):
    ok, errores = cliente_api.eliminar_semillero_linea({"semillero": semillero, "linea_investigacion": linea_investigacion})
    if ok:
        flash("Se retiró la ficha.", "exito")
    else:
        _avisar(errores)
    return redirect(url_for("listar_semillero_linea"))


def _opciones_grupo_linea():
    opciones, disponibles = {}, True
    ok, filas, errores = cliente_api.listar_grupo_investigacion()
    opciones["grupo_investigacion"] = filas
    if not ok:
        _avisar(errores)
        disponibles = False
    ok, filas, errores = cliente_api.listar_linea_investigacion()
    opciones["linea_investigacion"] = filas
    if not ok:
        _avisar(errores)
        disponibles = False
    return opciones, disponibles

def _cuerpo_grupo_linea(crear=False):
    cuerpo = {}
    cuerpo["grupo_investigacion"] = _valor_formulario("grupo_investigacion", numerico=True, nullable=False)
    cuerpo["linea_investigacion"] = _valor_formulario("linea_investigacion", numerico=True, nullable=False)
    return cuerpo

@app.route("/grupo-linea")
def listar_grupo_linea():
    ok, filas, errores = cliente_api.listar_grupo_linea()
    if not ok:
        _avisar(errores)
    return render_template("grupo_linea/lista.html", filas=filas)


@app.route("/grupo-linea/nuevo", methods=["GET", "POST"])
def crear_grupo_linea():
    opciones, disponibles = _opciones_grupo_linea()
    ficha = None
    if request.method == "POST":
        ficha = _cuerpo_grupo_linea(crear=True)
        ok, errores = cliente_api.crear_grupo_linea(ficha)
        if ok:
            flash("Se agregó la ficha.", "exito")
            return redirect(url_for("listar_grupo_linea"))
        _avisar(errores)
    return render_template("grupo_linea/formulario.html", ficha=ficha, editando=False, opciones=opciones, disponibles=disponibles)


@app.route("/grupo-linea/<int:grupo_investigacion>/<int:linea_investigacion>/editar", methods=["GET", "POST"])
def editar_grupo_linea(grupo_investigacion, linea_investigacion):
    identidad = {"grupo_investigacion": grupo_investigacion, "linea_investigacion": linea_investigacion}
    ok, ficha, errores = cliente_api.obtener_grupo_linea(identidad)
    if not ok:
        _avisar(errores)
        return redirect(url_for("listar_grupo_linea"))
    opciones, disponibles = _opciones_grupo_linea()
    if request.method == "POST":
        datos = _cuerpo_grupo_linea()
        if request.form.get("verbo") == "completa":
            ok, errores = cliente_api.reemplazar_grupo_linea(identidad, datos)
        else:
            ok, errores = cliente_api.actualizar_grupo_linea(identidad, _campos_cambiados(datos, ficha))
        if ok:
            flash("Se guardaron los cambios.", "exito")
            return redirect(url_for("listar_grupo_linea"))
        _avisar(errores)
        ficha = {**ficha, **datos}
    return render_template("grupo_linea/formulario.html", ficha=ficha, editando=True, opciones=opciones, disponibles=disponibles)


@app.route("/grupo-linea/<int:grupo_investigacion>/<int:linea_investigacion>/eliminar", methods=["POST"])
def eliminar_grupo_linea(grupo_investigacion, linea_investigacion):
    ok, errores = cliente_api.eliminar_grupo_linea({"grupo_investigacion": grupo_investigacion, "linea_investigacion": linea_investigacion})
    if ok:
        flash("Se retiró la ficha.", "exito")
    else:
        _avisar(errores)
    return redirect(url_for("listar_grupo_linea"))


def _opciones_ac_linea():
    opciones, disponibles = {}, True
    ok, filas, errores = cliente_api.listar_linea_investigacion()
    opciones["linea_investigacion"] = filas
    if not ok:
        _avisar(errores)
        disponibles = False
    ok, filas, errores = cliente_api.listar_areas_conocimiento()
    opciones["area_conocimiento"] = filas
    if not ok:
        _avisar(errores)
        disponibles = False
    return opciones, disponibles

def _cuerpo_ac_linea(crear=False):
    cuerpo = {}
    cuerpo["linea_investigacion"] = _valor_formulario("linea_investigacion", numerico=True, nullable=False)
    cuerpo["area_conocimiento"] = _valor_formulario("area_conocimiento", numerico=False, nullable=False)
    return cuerpo

@app.route("/ac-linea")
def listar_ac_linea():
    ok, filas, errores = cliente_api.listar_ac_linea()
    if not ok:
        _avisar(errores)
    return render_template("ac_linea/lista.html", filas=filas)


@app.route("/ac-linea/nuevo", methods=["GET", "POST"])
def crear_ac_linea():
    opciones, disponibles = _opciones_ac_linea()
    ficha = None
    if request.method == "POST":
        ficha = _cuerpo_ac_linea(crear=True)
        ok, errores = cliente_api.crear_ac_linea(ficha)
        if ok:
            flash("Se agregó la ficha.", "exito")
            return redirect(url_for("listar_ac_linea"))
        _avisar(errores)
    return render_template("ac_linea/formulario.html", ficha=ficha, editando=False, opciones=opciones, disponibles=disponibles)


@app.route("/ac-linea/<int:linea_investigacion>/<string:area_conocimiento>/editar", methods=["GET", "POST"])
def editar_ac_linea(linea_investigacion, area_conocimiento):
    identidad = {"linea_investigacion": linea_investigacion, "area_conocimiento": area_conocimiento}
    ok, ficha, errores = cliente_api.obtener_ac_linea(identidad)
    if not ok:
        _avisar(errores)
        return redirect(url_for("listar_ac_linea"))
    opciones, disponibles = _opciones_ac_linea()
    if request.method == "POST":
        datos = _cuerpo_ac_linea()
        if request.form.get("verbo") == "completa":
            ok, errores = cliente_api.reemplazar_ac_linea(identidad, datos)
        else:
            ok, errores = cliente_api.actualizar_ac_linea(identidad, _campos_cambiados(datos, ficha))
        if ok:
            flash("Se guardaron los cambios.", "exito")
            return redirect(url_for("listar_ac_linea"))
        _avisar(errores)
        ficha = {**ficha, **datos}
    return render_template("ac_linea/formulario.html", ficha=ficha, editando=True, opciones=opciones, disponibles=disponibles)


@app.route("/ac-linea/<int:linea_investigacion>/<string:area_conocimiento>/eliminar", methods=["POST"])
def eliminar_ac_linea(linea_investigacion, area_conocimiento):
    ok, errores = cliente_api.eliminar_ac_linea({"linea_investigacion": linea_investigacion, "area_conocimiento": area_conocimiento})
    if ok:
        flash("Se retiró la ficha.", "exito")
    else:
        _avisar(errores)
    return redirect(url_for("listar_ac_linea"))


def _opciones_ods_linea():
    opciones, disponibles = {}, True
    ok, filas, errores = cliente_api.listar_linea_investigacion()
    opciones["linea_investigacion"] = filas
    if not ok:
        _avisar(errores)
        disponibles = False
    ok, filas, errores = cliente_api.listar_objetivo_desarrollo_sostenible()
    opciones["ods"] = filas
    if not ok:
        _avisar(errores)
        disponibles = False
    return opciones, disponibles

def _cuerpo_ods_linea(crear=False):
    cuerpo = {}
    cuerpo["linea_investigacion"] = _valor_formulario("linea_investigacion", numerico=True, nullable=False)
    cuerpo["ods"] = _valor_formulario("ods", numerico=True, nullable=False)
    return cuerpo

@app.route("/ods-linea")
def listar_ods_linea():
    ok, filas, errores = cliente_api.listar_ods_linea()
    if not ok:
        _avisar(errores)
    return render_template("ods_linea/lista.html", filas=filas)


@app.route("/ods-linea/nuevo", methods=["GET", "POST"])
def crear_ods_linea():
    opciones, disponibles = _opciones_ods_linea()
    ficha = None
    if request.method == "POST":
        ficha = _cuerpo_ods_linea(crear=True)
        ok, errores = cliente_api.crear_ods_linea(ficha)
        if ok:
            flash("Se agregó la ficha.", "exito")
            return redirect(url_for("listar_ods_linea"))
        _avisar(errores)
    return render_template("ods_linea/formulario.html", ficha=ficha, editando=False, opciones=opciones, disponibles=disponibles)


@app.route("/ods-linea/<int:linea_investigacion>/<int:ods>/editar", methods=["GET", "POST"])
def editar_ods_linea(linea_investigacion, ods):
    identidad = {"linea_investigacion": linea_investigacion, "ods": ods}
    ok, ficha, errores = cliente_api.obtener_ods_linea(identidad)
    if not ok:
        _avisar(errores)
        return redirect(url_for("listar_ods_linea"))
    opciones, disponibles = _opciones_ods_linea()
    if request.method == "POST":
        datos = _cuerpo_ods_linea()
        if request.form.get("verbo") == "completa":
            ok, errores = cliente_api.reemplazar_ods_linea(identidad, datos)
        else:
            ok, errores = cliente_api.actualizar_ods_linea(identidad, _campos_cambiados(datos, ficha))
        if ok:
            flash("Se guardaron los cambios.", "exito")
            return redirect(url_for("listar_ods_linea"))
        _avisar(errores)
        ficha = {**ficha, **datos}
    return render_template("ods_linea/formulario.html", ficha=ficha, editando=True, opciones=opciones, disponibles=disponibles)


@app.route("/ods-linea/<int:linea_investigacion>/<int:ods>/eliminar", methods=["POST"])
def eliminar_ods_linea(linea_investigacion, ods):
    ok, errores = cliente_api.eliminar_ods_linea({"linea_investigacion": linea_investigacion, "ods": ods})
    if ok:
        flash("Se retiró la ficha.", "exito")
    else:
        _avisar(errores)
    return redirect(url_for("listar_ods_linea"))


def _opciones_aa_linea():
    opciones, disponibles = {}, True
    ok, filas, errores = cliente_api.listar_area_aplicacion()
    opciones["area_aplicacion"] = filas
    if not ok:
        _avisar(errores)
        disponibles = False
    ok, filas, errores = cliente_api.listar_linea_investigacion()
    opciones["linea_investigacion"] = filas
    if not ok:
        _avisar(errores)
        disponibles = False
    return opciones, disponibles

def _cuerpo_aa_linea(crear=False):
    cuerpo = {}
    cuerpo["area_aplicacion"] = _valor_formulario("area_aplicacion", numerico=True, nullable=False)
    cuerpo["linea_investigacion"] = _valor_formulario("linea_investigacion", numerico=True, nullable=False)
    return cuerpo

@app.route("/aa-linea")
def listar_aa_linea():
    ok, filas, errores = cliente_api.listar_aa_linea()
    if not ok:
        _avisar(errores)
    return render_template("aa_linea/lista.html", filas=filas)


@app.route("/aa-linea/nuevo", methods=["GET", "POST"])
def crear_aa_linea():
    opciones, disponibles = _opciones_aa_linea()
    ficha = None
    if request.method == "POST":
        ficha = _cuerpo_aa_linea(crear=True)
        ok, errores = cliente_api.crear_aa_linea(ficha)
        if ok:
            flash("Se agregó la ficha.", "exito")
            return redirect(url_for("listar_aa_linea"))
        _avisar(errores)
    return render_template("aa_linea/formulario.html", ficha=ficha, editando=False, opciones=opciones, disponibles=disponibles)


@app.route("/aa-linea/<int:area_aplicacion>/<int:linea_investigacion>/editar", methods=["GET", "POST"])
def editar_aa_linea(area_aplicacion, linea_investigacion):
    identidad = {"area_aplicacion": area_aplicacion, "linea_investigacion": linea_investigacion}
    ok, ficha, errores = cliente_api.obtener_aa_linea(identidad)
    if not ok:
        _avisar(errores)
        return redirect(url_for("listar_aa_linea"))
    opciones, disponibles = _opciones_aa_linea()
    if request.method == "POST":
        datos = _cuerpo_aa_linea()
        if request.form.get("verbo") == "completa":
            ok, errores = cliente_api.reemplazar_aa_linea(identidad, datos)
        else:
            ok, errores = cliente_api.actualizar_aa_linea(identidad, _campos_cambiados(datos, ficha))
        if ok:
            flash("Se guardaron los cambios.", "exito")
            return redirect(url_for("listar_aa_linea"))
        _avisar(errores)
        ficha = {**ficha, **datos}
    return render_template("aa_linea/formulario.html", ficha=ficha, editando=True, opciones=opciones, disponibles=disponibles)


@app.route("/aa-linea/<int:area_aplicacion>/<int:linea_investigacion>/eliminar", methods=["POST"])
def eliminar_aa_linea(area_aplicacion, linea_investigacion):
    ok, errores = cliente_api.eliminar_aa_linea({"area_aplicacion": area_aplicacion, "linea_investigacion": linea_investigacion})
    if ok:
        flash("Se retiró la ficha.", "exito")
    else:
        _avisar(errores)
    return redirect(url_for("listar_aa_linea"))



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PUERTO, debug=True)
