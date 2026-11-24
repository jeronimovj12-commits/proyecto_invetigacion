"""El login es público; solo entrega un JWT tras verificar cuenta y roles activos."""

from fastapi import APIRouter, HTTPException

from models.login import LoginCrear
from seguridad.jwt_handler import crear_token
from servicios.ensamblador import crear_servicio_usuario


router = APIRouter(tags=["autenticación"])


@router.post("/api/login")
async def iniciar_sesion(datos: LoginCrear):
    usuario = await crear_servicio_usuario().autenticar(datos.username, datos.password)
    if usuario is None:
        raise HTTPException(
            status_code=401,
            detail={
                "estado": 401,
                "mensaje": "Credenciales inválidas.",
                "detalle": "Usuario o contraseña incorrectos, o cuenta inactiva.",
            },
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = crear_token({"sub": str(usuario["id"]), "username": usuario["username"]})
    return {
        "accessToken": token,
        "tokenType": "bearer",
        "usuario": {
            "id": usuario["id"],
            "username": usuario["username"],
            "email": usuario["email"],
            "nombreCompleto": usuario["nombre_completo"],
            "roles": usuario["roles"],
        },
    }
