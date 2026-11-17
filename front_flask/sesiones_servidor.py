# Ejecuta la instruccion indicada dentro del flujo actual.
"""Sesiones del front en SQLite local al servidor; la cookie nunca contiene JWT."""
# Importa contextmanager desde contextlib para usar esas definiciones.
from contextlib import contextmanager
# Carga el modulo o los modulos hashlib.
import hashlib
# Carga el modulo o los modulos os.
import os
# Importa Path desde pathlib para usar esas definiciones.
from pathlib import Path
# Carga el modulo o los modulos secrets.
import secrets
# Carga el modulo o los modulos sqlite3.
import sqlite3
# Carga el modulo o los modulos time.
import time

# Define la clase SesionesServidor y agrupa su estado y operaciones.
class SesionesServidor:
    # Define la funcion __init__ con los parametros declarados; su bloque realiza esta operacion.
    def __init__(self, ruta):
        # Guarda en self.ruta el valor necesario para reutilizarlo en otros metodos.
        self.ruta = ruta
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        Path(ruta).parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        # Abre el recurso y asegura su cierre al salir del bloque.
        with self._conexion() as conexion:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            conexion.execute('CREATE TABLE IF NOT EXISTS sesion (id TEXT PRIMARY KEY, token TEXT NOT NULL, vence REAL NOT NULL)')
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        os.chmod(ruta, 0o600)

    # Aplica @contextmanager a la declaracion que sigue; en rutas, registra el endpoint HTTP.
    @contextmanager
    # Define la funcion _conexion con los parametros declarados; su bloque realiza esta operacion.
    def _conexion(self):
        # Asigna a conexion el valor calculado a la derecha.
        conexion = sqlite3.connect(self.ruta, timeout=10)
        # Inicia un bloque cuya excepcion se manejara en los except siguientes.
        try:
            # Abre el recurso y asegura su cierre al salir del bloque.
            with conexion:
                # Entrega un valor al iterador y conserva el estado de la funcion.
                yield conexion
        # Ejecuta este bloque al final, haya ocurrido o no una excepcion.
        finally:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            conexion.close()

    # Aplica @staticmethod a la declaracion que sigue; en rutas, registra el endpoint HTTP.
    @staticmethod
    # Define la funcion _id con los parametros declarados; su bloque realiza esta operacion.
    def _id(sid):
        # Devuelve al llamador el resultado de la expresion indicada.
        return hashlib.sha256(sid.encode()).hexdigest()

    # Define la funcion crear con los parametros declarados; su bloque realiza esta operacion.
    def crear(self, token, segundos):
        # Asigna a sid el valor calculado a la derecha.
        sid = secrets.token_urlsafe(32)
        # Abre el recurso y asegura su cierre al salir del bloque.
        with self._conexion() as conexion:
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            conexion.execute('DELETE FROM sesion WHERE vence <= ?', (time.time(),))
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            conexion.execute('INSERT INTO sesion VALUES (?, ?, ?)', (self._id(sid), token, time.time() + segundos))
        # Devuelve al llamador el resultado de la expresion indicada.
        return sid

    # Define la funcion obtener con los parametros declarados; su bloque realiza esta operacion.
    def obtener(self, sid):
        # Ejecuta el bloque siguiente solo cuando se cumple: not sid.
        if not sid:
            # Devuelve al llamador el resultado de la expresion indicada.
            return None
        # Abre el recurso y asegura su cierre al salir del bloque.
        with self._conexion() as conexion:
            # Asigna a fila el valor calculado a la derecha.
            fila = conexion.execute('SELECT token FROM sesion WHERE id=? AND vence>?', (self._id(sid), time.time())).fetchone()
        # Devuelve al llamador el resultado de la expresion indicada.
        return fila[0] if fila else None

    # Define la funcion retirar con los parametros declarados; su bloque realiza esta operacion.
    def retirar(self, sid):
        # Ejecuta el bloque siguiente solo cuando se cumple: sid.
        if sid:
            # Abre el recurso y asegura su cierre al salir del bloque.
            with self._conexion() as conexion:
                # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                conexion.execute('DELETE FROM sesion WHERE id=?', (self._id(sid),))
