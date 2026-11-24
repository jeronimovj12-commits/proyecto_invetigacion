"""El hash bcrypt y JWT se encapsulan para no dispersar decisiones criptográficas."""

import os
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt


def hashear_contrasena(contrasena: str) -> str:
    datos = contrasena.encode("utf-8")
    if len(datos) > 72:
        raise ValueError("La contraseña no puede superar 72 bytes en UTF-8.")
    return bcrypt.hashpw(datos, bcrypt.gensalt()).decode("utf-8")


def verificar_contrasena(contrasena: str, hash_almacenado: str) -> bool:
    try:
        datos = contrasena.encode("utf-8")
        if len(datos) > 72:
            return False
        return bcrypt.checkpw(datos, hash_almacenado.encode("utf-8"))
    except (AttributeError, ValueError, TypeError):
        return False


def _configuracion_jwt() -> tuple[str, str, int]:
    secreto = os.environ.get("JWT_SECRET")
    algoritmo = os.environ.get("JWT_ALGORITHM", "HS256")
    if not secreto:
        raise RuntimeError("La variable de entorno JWT_SECRET es obligatoria.")
    if algoritmo != "HS256":
        raise RuntimeError("JWT_ALGORITHM debe ser HS256.")
    try:
        minutos = int(os.environ.get("JWT_EXPIRE_MINUTES", "120"))
    except ValueError as excepcion:
        raise RuntimeError("JWT_EXPIRE_MINUTES debe ser un entero positivo.") from excepcion
    if minutos <= 0:
        raise RuntimeError("JWT_EXPIRE_MINUTES debe ser un entero positivo.")
    return secreto, algoritmo, minutos


def crear_token(datos: dict) -> str:
    secreto, algoritmo, minutos = _configuracion_jwt()
    ahora = datetime.now(timezone.utc)
    carga = {
        **datos,
        "iat": ahora,
        "exp": ahora + timedelta(minutes=minutos),
    }
    return jwt.encode(carga, secreto, algorithm=algoritmo)


def decodificar_token(token: str) -> dict:
    secreto, algoritmo, _ = _configuracion_jwt()
    try:
        return jwt.decode(token, secreto, algorithms=[algoritmo])
    except jwt.InvalidTokenError as excepcion:
        raise ValueError("El token no es válido o expiró.") from excepcion
