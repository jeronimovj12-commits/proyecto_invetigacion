"""Sesiones del front en SQLite local al servidor; la cookie nunca contiene JWT."""
from contextlib import contextmanager
import hashlib
import os
from pathlib import Path
import secrets
import sqlite3
import time

class SesionesServidor:
    def __init__(self, ruta):
        self.ruta = ruta
        Path(ruta).parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        with self._conexion() as conexion:
            conexion.execute('CREATE TABLE IF NOT EXISTS sesion (id TEXT PRIMARY KEY, token TEXT NOT NULL, vence REAL NOT NULL)')
        os.chmod(ruta, 0o600)

    @contextmanager
    def _conexion(self):
        conexion = sqlite3.connect(self.ruta, timeout=10)
        try:
            with conexion:
                yield conexion
        finally:
            conexion.close()

    @staticmethod
    def _id(sid):
        return hashlib.sha256(sid.encode()).hexdigest()

    def crear(self, token, segundos):
        sid = secrets.token_urlsafe(32)
        with self._conexion() as conexion:
            conexion.execute('DELETE FROM sesion WHERE vence <= ?', (time.time(),))
            conexion.execute('INSERT INTO sesion VALUES (?, ?, ?)', (self._id(sid), token, time.time() + segundos))
        return sid

    def obtener(self, sid):
        if not sid:
            return None
        with self._conexion() as conexion:
            fila = conexion.execute('SELECT token FROM sesion WHERE id=? AND vence>?', (self._id(sid), time.time())).fetchone()
        return fila[0] if fila else None

    def retirar(self, sid):
        if sid:
            with self._conexion() as conexion:
                conexion.execute('DELETE FROM sesion WHERE id=?', (self._id(sid),))
