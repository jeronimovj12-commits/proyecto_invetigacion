# Ejecuta la instruccion indicada dentro del flujo actual.
"""Controlador HTTP: registra rutas, llama a servicios y convierte sus resultados o errores en respuestas HTTP."""
# Importa Annotated desde typing para usar esas definiciones.
from typing import Annotated
# Importa APIRouter, Depends, HTTPException, Query desde fastapi para usar esas definiciones.
from fastapi import APIRouter, Depends, HTTPException, Query
# Importa UsuarioCrear, UsuarioEditar, RolCrear, RolEditar, AsignacionCrear, AsignacionEditar desde models.administracion para usar esas definiciones.
from models.administracion import UsuarioCrear, UsuarioEditar, RolCrear, RolEditar, AsignacionCrear, AsignacionEditar
# Importa IServicioSeguridad desde servicios.abstracciones.i_servicio_seguridad para usar esas definiciones.
from servicios.abstracciones.i_servicio_seguridad import IServicioSeguridad
# Importa crear_servicio_seguridad desde servicios.ensamblador_seguridad para usar esas definiciones.
from servicios.ensamblador_seguridad import crear_servicio_seguridad
# Importa ConflictoSeguridad, SeguridadNoEncontrada desde seguridad.errores_administracion para usar esas definiciones.
from seguridad.errores_administracion import ConflictoSeguridad, SeguridadNoEncontrada

# Crea el router FastAPI que agrupa las rutas de este modulo.
router = APIRouter(prefix='/api', tags=['administración'])
# Asigna a Servicio el valor calculado a la derecha.
Servicio = Annotated[IServicioSeguridad, Depends(crear_servicio_seguridad)]

# Define la funcion ejecutar con los parametros declarados; su bloque realiza esta operacion.
async def ejecutar(operacion):
    # Inicia un bloque cuya excepcion se manejara en los except siguientes.
    try:
        # Devuelve al llamador el resultado de la expresion indicada.
        return await operacion
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except ConflictoSeguridad as error:
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise HTTPException(409, {'estado': 409, 'mensaje': 'Operación rechazada.', 'detalle': str(error)}) from None
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except SeguridadNoEncontrada:
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise HTTPException(404, {'estado': 404, 'mensaje': 'Registro no encontrado.', 'detalle': 'No existe un registro activo.'}) from None
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except Exception:
        # Lanza la excepcion indicada y detiene el flujo normal.
        raise HTTPException(500, {'estado': 500, 'mensaje': 'No se pudo completar la operación.', 'detalle': 'Error interno de seguridad.'}) from None

# Define la funcion listado con los parametros declarados; su bloque realiza esta operacion.
async def listado(servicio, recurso, claves, limite):
    # Asigna a filas el valor calculado a la derecha.
    filas = await ejecutar(servicio.listar(recurso, claves, limite))
    # Devuelve al llamador el resultado de la expresion indicada.
    return {'tabla': recurso, 'limite': limite, 'total': len(filas), 'datos': filas}

# Aplica @router.get a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@router.get('/usuario')
# Define la funcion usuarios con los parametros declarados; su bloque realiza esta operacion.
async def usuarios(servicio: Servicio, limite: int = Query(100, ge=1, le=1000)):
    # Devuelve al llamador el resultado de la expresion indicada.
    return await listado(servicio, 'usuario', {}, limite)

# Aplica @router.get a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@router.get('/usuario/{id}')
# Define la funcion usuario con los parametros declarados; su bloque realiza esta operacion.
async def usuario(id: int, servicio: Servicio):
    # Devuelve al llamador el resultado de la expresion indicada.
    return await listado(servicio, 'usuario', {'id': id}, 1)

# Aplica @router.post a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@router.post('/usuario', status_code=201)
# Define la funcion crear_usuario con los parametros declarados; su bloque realiza esta operacion.
async def crear_usuario(datos: UsuarioCrear, servicio: Servicio):
    # Devuelve al llamador el resultado de la expresion indicada.
    return await ejecutar(servicio.guardar('usuario', {}, datos.model_dump(), True))

# Aplica @router.put a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@router.put('/usuario/{id}')
# Define la funcion reemplazar_usuario con los parametros declarados; su bloque realiza esta operacion.
async def reemplazar_usuario(id: int, datos: UsuarioCrear, servicio: Servicio):
    # Devuelve al llamador el resultado de la expresion indicada.
    return await ejecutar(servicio.guardar('usuario', {'id': id}, datos.model_dump()))

# Aplica @router.patch a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@router.patch('/usuario/{id}')
# Define la funcion editar_usuario con los parametros declarados; su bloque realiza esta operacion.
async def editar_usuario(id: int, datos: UsuarioEditar, servicio: Servicio):
    # Devuelve al llamador el resultado de la expresion indicada.
    return await ejecutar(servicio.guardar('usuario', {'id': id}, datos.model_dump(exclude_unset=True)))

# Aplica @router.delete a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@router.delete('/usuario/{id}')
# Define la funcion retirar_usuario con los parametros declarados; su bloque realiza esta operacion.
async def retirar_usuario(id: int, servicio: Servicio):
    # Espera que termine la operacion asincronica antes de continuar.
    await ejecutar(servicio.retirar('usuario', {'id': id}))
    # Devuelve al llamador el resultado de la expresion indicada.
    return {'estado': 200, 'mensaje': 'Cuenta retirada.'}

# Aplica @router.get a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@router.get('/rol')
# Define la funcion roles con los parametros declarados; su bloque realiza esta operacion.
async def roles(servicio: Servicio, limite: int = Query(100, ge=1, le=1000)):
    # Devuelve al llamador el resultado de la expresion indicada.
    return await listado(servicio, 'rol', {}, limite)

# Aplica @router.get a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@router.get('/rol/{id}')
# Define la funcion rol con los parametros declarados; su bloque realiza esta operacion.
async def rol(id: int, servicio: Servicio):
    # Devuelve al llamador el resultado de la expresion indicada.
    return await listado(servicio, 'rol', {'id': id}, 1)

# Aplica @router.post a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@router.post('/rol', status_code=201)
# Define la funcion crear_rol con los parametros declarados; su bloque realiza esta operacion.
async def crear_rol(datos: RolCrear, servicio: Servicio):
    # Devuelve al llamador el resultado de la expresion indicada.
    return await ejecutar(servicio.guardar('rol', {}, datos.model_dump(), True))

# Aplica @router.put a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@router.put('/rol/{id}')
# Define la funcion reemplazar_rol con los parametros declarados; su bloque realiza esta operacion.
async def reemplazar_rol(id: int, datos: RolCrear, servicio: Servicio):
    # Devuelve al llamador el resultado de la expresion indicada.
    return await ejecutar(servicio.guardar('rol', {'id': id}, datos.model_dump()))

# Aplica @router.patch a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@router.patch('/rol/{id}')
# Define la funcion editar_rol con los parametros declarados; su bloque realiza esta operacion.
async def editar_rol(id: int, datos: RolEditar, servicio: Servicio):
    # Devuelve al llamador el resultado de la expresion indicada.
    return await ejecutar(servicio.guardar('rol', {'id': id}, datos.model_dump(exclude_unset=True)))

# Aplica @router.delete a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@router.delete('/rol/{id}')
# Define la funcion retirar_rol con los parametros declarados; su bloque realiza esta operacion.
async def retirar_rol(id: int, servicio: Servicio):
    # Espera que termine la operacion asincronica antes de continuar.
    await ejecutar(servicio.retirar('rol', {'id': id}))
    # Devuelve al llamador el resultado de la expresion indicada.
    return {'estado': 200, 'mensaje': 'Rol retirado.'}

# Aplica @router.get a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@router.get('/rol_usuario')
# Define la funcion asignaciones con los parametros declarados; su bloque realiza esta operacion.
async def asignaciones(servicio: Servicio, limite: int = Query(100, ge=1, le=1000)):
    # Devuelve al llamador el resultado de la expresion indicada.
    return await listado(servicio, 'rol_usuario', {}, limite)

# Aplica @router.get a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@router.get('/rol_usuario/{usuario_id}/{rol_id}')
# Define la funcion asignacion con los parametros declarados; su bloque realiza esta operacion.
async def asignacion(usuario_id: int, rol_id: int, servicio: Servicio):
    # Devuelve al llamador el resultado de la expresion indicada.
    return await listado(servicio, 'rol_usuario', {'usuario_id': usuario_id, 'rol_id': rol_id}, 1)

# Aplica @router.post a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@router.post('/rol_usuario', status_code=201)
# Define la funcion asignar con los parametros declarados; su bloque realiza esta operacion.
async def asignar(datos: AsignacionCrear, servicio: Servicio):
    # Devuelve al llamador el resultado de la expresion indicada.
    return await ejecutar(servicio.guardar('rol_usuario', {}, datos.model_dump(), True))

# Aplica @router.delete a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@router.delete('/rol_usuario/{usuario_id}/{rol_id}')
# Define la funcion retirar_asignacion con los parametros declarados; su bloque realiza esta operacion.
async def retirar_asignacion(usuario_id: int, rol_id: int, servicio: Servicio):
    # Espera que termine la operacion asincronica antes de continuar.
    await ejecutar(servicio.retirar('rol_usuario', {'usuario_id': usuario_id, 'rol_id': rol_id}))
    # Devuelve al llamador el resultado de la expresion indicada.
    return {'estado': 200, 'mensaje': 'Asignación retirada.'}


# Aplica @router.put a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@router.put('/rol_usuario/{usuario_id}/{rol_id}')
# Define la funcion reemplazar_asignacion con los parametros declarados; su bloque realiza esta operacion.
async def reemplazar_asignacion(usuario_id: int, rol_id: int, datos: AsignacionCrear, servicio: Servicio):
    # Devuelve al llamador el resultado de la expresion indicada.
    return await ejecutar(servicio.guardar('rol_usuario', {'usuario_id': usuario_id, 'rol_id': rol_id}, datos.model_dump()))

# Aplica @router.patch a la declaracion que sigue; en rutas, registra el endpoint HTTP.
@router.patch('/rol_usuario/{usuario_id}/{rol_id}')
# Define la funcion editar_asignacion con los parametros declarados; su bloque realiza esta operacion.
async def editar_asignacion(usuario_id: int, rol_id: int, datos: AsignacionEditar, servicio: Servicio):
    # Devuelve al llamador el resultado de la expresion indicada.
    return await ejecutar(servicio.guardar('rol_usuario', {'usuario_id': usuario_id, 'rol_id': rol_id}, datos.model_dump(exclude_unset=True)))
