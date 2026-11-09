from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from models.administracion import UsuarioCrear, UsuarioEditar, RolCrear, RolEditar, AsignacionCrear, AsignacionEditar
from servicios.abstracciones.i_servicio_seguridad import IServicioSeguridad
from servicios.ensamblador_seguridad import crear_servicio_seguridad
from seguridad.errores_administracion import ConflictoSeguridad, SeguridadNoEncontrada

router = APIRouter(prefix='/api', tags=['administración'])
Servicio = Annotated[IServicioSeguridad, Depends(crear_servicio_seguridad)]

async def ejecutar(operacion):
    try:
        return await operacion
    except ConflictoSeguridad as error:
        raise HTTPException(409, {'estado': 409, 'mensaje': 'Operación rechazada.', 'detalle': str(error)}) from None
    except SeguridadNoEncontrada:
        raise HTTPException(404, {'estado': 404, 'mensaje': 'Registro no encontrado.', 'detalle': 'No existe un registro activo.'}) from None
    except Exception:
        raise HTTPException(500, {'estado': 500, 'mensaje': 'No se pudo completar la operación.', 'detalle': 'Error interno de seguridad.'}) from None

async def listado(servicio, recurso, claves, limite):
    filas = await ejecutar(servicio.listar(recurso, claves, limite))
    return {'tabla': recurso, 'limite': limite, 'total': len(filas), 'datos': filas}

@router.get('/usuario')
async def usuarios(servicio: Servicio, limite: int = Query(100, ge=1, le=1000)):
    return await listado(servicio, 'usuario', {}, limite)

@router.get('/usuario/{id}')
async def usuario(id: int, servicio: Servicio):
    return await listado(servicio, 'usuario', {'id': id}, 1)

@router.post('/usuario', status_code=201)
async def crear_usuario(datos: UsuarioCrear, servicio: Servicio):
    return await ejecutar(servicio.guardar('usuario', {}, datos.model_dump(), True))

@router.put('/usuario/{id}')
async def reemplazar_usuario(id: int, datos: UsuarioCrear, servicio: Servicio):
    return await ejecutar(servicio.guardar('usuario', {'id': id}, datos.model_dump()))

@router.patch('/usuario/{id}')
async def editar_usuario(id: int, datos: UsuarioEditar, servicio: Servicio):
    return await ejecutar(servicio.guardar('usuario', {'id': id}, datos.model_dump(exclude_unset=True)))

@router.delete('/usuario/{id}')
async def retirar_usuario(id: int, servicio: Servicio):
    await ejecutar(servicio.retirar('usuario', {'id': id}))
    return {'estado': 200, 'mensaje': 'Cuenta retirada.'}

@router.get('/rol')
async def roles(servicio: Servicio, limite: int = Query(100, ge=1, le=1000)):
    return await listado(servicio, 'rol', {}, limite)

@router.get('/rol/{id}')
async def rol(id: int, servicio: Servicio):
    return await listado(servicio, 'rol', {'id': id}, 1)

@router.post('/rol', status_code=201)
async def crear_rol(datos: RolCrear, servicio: Servicio):
    return await ejecutar(servicio.guardar('rol', {}, datos.model_dump(), True))

@router.put('/rol/{id}')
async def reemplazar_rol(id: int, datos: RolCrear, servicio: Servicio):
    return await ejecutar(servicio.guardar('rol', {'id': id}, datos.model_dump()))

@router.patch('/rol/{id}')
async def editar_rol(id: int, datos: RolEditar, servicio: Servicio):
    return await ejecutar(servicio.guardar('rol', {'id': id}, datos.model_dump(exclude_unset=True)))

@router.delete('/rol/{id}')
async def retirar_rol(id: int, servicio: Servicio):
    await ejecutar(servicio.retirar('rol', {'id': id}))
    return {'estado': 200, 'mensaje': 'Rol retirado.'}

@router.get('/rol_usuario')
async def asignaciones(servicio: Servicio, limite: int = Query(100, ge=1, le=1000)):
    return await listado(servicio, 'rol_usuario', {}, limite)

@router.get('/rol_usuario/{usuario_id}/{rol_id}')
async def asignacion(usuario_id: int, rol_id: int, servicio: Servicio):
    return await listado(servicio, 'rol_usuario', {'usuario_id': usuario_id, 'rol_id': rol_id}, 1)

@router.post('/rol_usuario', status_code=201)
async def asignar(datos: AsignacionCrear, servicio: Servicio):
    return await ejecutar(servicio.guardar('rol_usuario', {}, datos.model_dump(), True))

@router.delete('/rol_usuario/{usuario_id}/{rol_id}')
async def retirar_asignacion(usuario_id: int, rol_id: int, servicio: Servicio):
    await ejecutar(servicio.retirar('rol_usuario', {'usuario_id': usuario_id, 'rol_id': rol_id}))
    return {'estado': 200, 'mensaje': 'Asignación retirada.'}


@router.put('/rol_usuario/{usuario_id}/{rol_id}')
async def reemplazar_asignacion(usuario_id: int, rol_id: int, datos: AsignacionCrear, servicio: Servicio):
    return await ejecutar(servicio.guardar('rol_usuario', {'usuario_id': usuario_id, 'rol_id': rol_id}, datos.model_dump()))

@router.patch('/rol_usuario/{usuario_id}/{rol_id}')
async def editar_asignacion(usuario_id: int, rol_id: int, datos: AsignacionEditar, servicio: Servicio):
    return await ejecutar(servicio.guardar('rol_usuario', {'usuario_id': usuario_id, 'rol_id': rol_id}, datos.model_dump(exclude_unset=True)))
