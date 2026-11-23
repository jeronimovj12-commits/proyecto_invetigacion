# Ejecuta la instruccion indicada dentro del flujo actual.
"""Integración HTTP v3 en una base nueva; sin tocar pruebas reservadas del equipo."""
# Carga el modulo o los modulos asyncio.
import asyncio
# Carga el modulo o los modulos os.
import os
# Carga el modulo o los modulos secrets.
import secrets
# Carga el modulo o los modulos unittest.
import unittest
# Importa text desde sqlalchemy para usar esas definiciones.
from sqlalchemy import text
# Carga el modulo o los modulos prueba_autenticacion_v3 as base.
import prueba_autenticacion_v3 as base
# Importa TokensJWT desde seguridad.adaptadores para usar esas definiciones.
from seguridad.adaptadores import TokensJWT

# Define la clase AdministracionHTTP y agrupa su estado y operaciones.
class AdministracionHTTP(base.AutenticacionHTTP):
    # Define la funcion administrador con los parametros declarados; su bloque realiza esta operacion.
    def administrador(self):
        # Devuelve al llamador el resultado de la expresion indicada.
        return TokensJWT(base.CONFIG).emitir(1, 0)

    # Define la funcion api con los parametros declarados; su bloque realiza esta operacion.
    def api(self, metodo, ruta, datos=None):
        # Devuelve al llamador el resultado de la expresion indicada.
        return base.pedir(metodo, ruta, datos, self.administrador())

    # Define la funcion test_matriz_todas_las_rutas_directas con los parametros declarados; su bloque realiza esta operacion.
    async def test_matriz_todas_las_rutas_directas(self):
        # Asigna a contrato el valor calculado a la derecha.
        contrato = base.pedir('GET', '/openapi.json')[1]
        # Asigna a token el valor calculado a la derecha.
        token = self.token()
        # Asigna a total el valor calculado a la derecha.
        total = 0
        # Recorre los elementos de la coleccion indicada y ejecuta el bloque para cada uno.
        for ruta, operaciones in contrato['paths'].items():
            # Ejecuta el bloque siguiente solo cuando se cumple: not ruta.startswith('/api/') or ruta in ('/api/login', '/api/logout', '/api/sesion').
            if not ruta.startswith('/api/') or ruta in ('/api/login', '/api/logout', '/api/sesion'):
                # Salta al siguiente ciclo de la repeticion.
                continue
            # Carga el modulo o los modulos re.
            import re
            # Asigna a ruta_real el valor calculado a la derecha.
            ruta_real = re.sub(r'\{[^}]+\}', '999999', ruta)
            # Recorre los elementos de la coleccion indicada y ejecuta el bloque para cada uno.
            for metodo in operaciones:
                # Ejecuta el bloque siguiente solo cuando se cumple: metodo not in ('get', 'post', 'put', 'patch', 'delete').
                if metodo not in ('get', 'post', 'put', 'patch', 'delete'):
                    # Salta al siguiente ciclo de la repeticion.
                    continue
                # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                self.assertEqual(operaciones[metodo].get('security'), [{'HTTPBearer': []}], ruta)
                # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                total += 1
                # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                self.assertEqual(base.pedir(metodo.upper(), ruta_real, {} if metodo != 'get' else None)[0], 401, ruta)
                # Ejecuta el bloque siguiente solo cuando se cumple: metodo != 'get' or ruta.split('/')[2] in ('usuario', 'rol', 'rol_usuario').
                if metodo != 'get' or ruta.split('/')[2] in ('usuario', 'rol', 'rol_usuario'):
                    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                    self.assertEqual(base.pedir(metodo.upper(), ruta_real, {}, token)[0], 403, ruta)
                # Define el caso alternativo cuando las condiciones anteriores no se cumplen.
                else:
                    # Asigna a estado el valor calculado a la derecha.
                    estado = base.pedir('GET', ruta_real, token=token)[0]
                    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                    self.assertIn(estado, (200, 204, 404, 422), ruta)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertGreater(total, 60)
        # Espera que termine la operacion asincronica antes de continuar.
        await self.sql('UPDATE rol_usuario SET activo=FALSE WHERE usuario_id=:id', id=self.usuario)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(base.pedir('GET', '/api/area_conocimiento', token=token)[0], 403)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        print('Operaciones protegidas verificadas:', total)

    # Define la funcion test_crud_y_secretos con los parametros declarados; su bloque realiza esta operacion.
    async def test_crud_y_secretos(self):
        # Asigna a nombre el valor calculado a la derecha.
        nombre = 'NUEVO_' + secrets.token_hex(6)
        # Asigna a clave el valor calculado a la derecha.
        clave = secrets.token_urlsafe(24)
        # Asigna a datos el valor calculado a la derecha.
        datos = {'username': nombre, 'email': nombre+'@example.invalid', 'password': clave}
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        estado, usuario, _ = self.api('POST', '/api/usuario', datos)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(estado, 201)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertNotIn('password', usuario)
        # Asigna a uid el valor calculado a la derecha.
        uid = usuario['id']
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.api('POST', '/api/usuario', datos)[0], 409)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(base.pedir('POST', '/api/login', {'username': nombre, 'password': clave})[0], 403)
        # Asigna a rid el valor calculado a la derecha.
        rid = (await self.sql("SELECT id FROM rol WHERE nombre='consulta'")).scalar_one()
        # Asigna a relacion el valor calculado a la derecha.
        relacion = {'usuario_id': uid, 'rol_id': rid}
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.api('POST', '/api/rol_usuario', relacion)[0], 201)
        # Asigna a token el valor calculado a la derecha.
        token = base.pedir('POST', '/api/login', {'username': nombre, 'password': clave})[1]['access_token']
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.api('GET', f'/api/usuario/{uid}')[0], 200)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.api('PUT', f'/api/usuario/{uid}', {'email': 'incompleto@example.invalid'})[0], 422)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.api('PATCH', f'/api/usuario/{uid}', {'password': clave, 'activo': True})[0], 422)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.api('PATCH', f'/api/usuario/{uid}', {'password': None})[0], 422)
        # Asigna a nueva el valor calculado a la derecha.
        nueva = secrets.token_urlsafe(24)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.api('PATCH', f'/api/usuario/{uid}', {'password': nueva})[0], 200)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(base.pedir('GET', '/api/sesion', token=token)[0], 401)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.api('DELETE', f'/api/rol_usuario/{uid}/{rid}')[0], 200)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.api('POST', '/api/rol_usuario', relacion)[0], 409)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertFalse((await self.sql('SELECT activo FROM rol_usuario WHERE usuario_id=:id AND rol_id=:rid', id=uid, rid=rid)).scalar_one())
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.api('DELETE', f'/api/usuario/{uid}')[0], 200)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.api('GET', f'/api/usuario/{uid}')[0], 404)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertFalse((await self.sql('SELECT activo FROM usuario WHERE id=:id', id=uid)).scalar_one())
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        estado, rol, _ = self.api('POST', '/api/rol', {'nombre': nombre, 'descripcion': 'Prueba'})
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(estado, 201)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.api('PUT', f"/api/rol/{rol['id']}", {'nombre': nombre, 'descripcion': 'Cambio'})[0], 200)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.api('PATCH', f"/api/rol/{rol['id']}", {'descripcion': None})[0], 200)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.api('DELETE', f"/api/rol/{rol['id']}")[0], 200)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.api('POST', '/api/rol_usuario', {'usuario_id': self.usuario, 'rol_id': rol['id']})[0], 409)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.api('POST', '/api/rol_usuario', {'usuario_id': 999999, 'rol_id': rid})[0], 409)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.api('PATCH', '/api/usuario/999999', {'email':'x@example.invalid'})[0], 404)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.api('PATCH', '/api/rol/999999', {})[0], 409)

    # Define la funcion test_edicion_logica_asignaciones con los parametros declarados; su bloque realiza esta operacion.
    async def test_edicion_logica_asignaciones(self):
        # Asigna a consulta el valor calculado a la derecha.
        consulta = (await self.sql("SELECT id FROM rol WHERE nombre='consulta'")).scalar_one()
        # Asigna a admin el valor calculado a la derecha.
        admin = (await self.sql("SELECT id FROM rol WHERE nombre='administrador'")).scalar_one()
        # Asigna a token el valor calculado a la derecha.
        token = self.token()
        # Asigna a origen el valor calculado a la derecha.
        origen = f'/api/rol_usuario/{self.usuario}/{consulta}'
        # Sin cambio es idempotente; cuerpos parciales y tipos conservan contrato.
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.api('PATCH', origen, {'rol_id':consulta})[0], 200)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.api('PUT', origen, {'rol_id':consulta})[0], 422)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.api('PATCH', origen, {'rol_id':None})[0], 422)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.api('PATCH', origen, {})[0], 409)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.api('PATCH', origen, {'rol_id':999999})[0], 409)
        # Asigna a rid el valor calculado a la derecha.
        rid = self.api('POST', '/api/rol', {'nombre':'R_'+secrets.token_hex(6)})[1]['id']
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.api('PATCH', origen, {'rol_id':rid})[0], 200)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.api('GET', origen)[0], 404)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertFalse((await self.sql('SELECT activo FROM rol_usuario WHERE usuario_id=:id AND rol_id=:rid', id=self.usuario,rid=consulta)).scalar_one())
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(base.pedir('GET','/api/sesion',token=token)[0],403)
        # Asigna a nuevo el valor calculado a la derecha.
        nuevo = f'/api/rol_usuario/{self.usuario}/{rid}'
        # Destino retirado no se reactiva; el origen se conserva ante conflicto.
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.api('PATCH', nuevo, {'rol_id':consulta})[0], 409)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.api('GET', nuevo)[0], 200)
        # Asigna a nombre el valor calculado a la derecha.
        nombre = 'DESTINO_'+secrets.token_hex(6)
        # Asigna a uid el valor calculado a la derecha.
        uid = self.api('POST','/api/usuario', {'username':nombre,'email':nombre+'@example.invalid','password':secrets.token_urlsafe(24)})[1]['id']
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.api('PUT', nuevo, {'usuario_id':uid,'rol_id':consulta})[0],200)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.api('GET',nuevo)[0],404)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.api('GET',f'/api/rol_usuario/{uid}/{consulta}')[0],200)
        # Un destino activo también hace rollback y no pierde la asignación original.
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.api('POST','/api/rol_usuario', {'usuario_id':uid,'rol_id':rid})[0],201)
        # Asigna a destino el valor calculado a la derecha.
        destino = f'/api/rol_usuario/{uid}/{rid}'
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.api('PATCH',destino,{'rol_id':consulta})[0],409)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.api('GET',destino)[0],200)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.api('PATCH',origen,{'rol_id':admin})[0],404)
        # Cambiar el último administrador a consulta no confirma ni retira el original.
        # Asigna a ultimo el valor calculado a la derecha.
        ultimo = f'/api/rol_usuario/1/{admin}'
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.api('PATCH',ultimo,{'rol_id':consulta})[0],409)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.api('GET',ultimo)[0],200)

    # Define la funcion test_regresion_crud_dominio_con_administrador con los parametros declarados; su bloque realiza esta operacion.
    async def test_regresion_crud_dominio_con_administrador(self):
        # Importa CASOS desde humo_v2 para usar esas definiciones.
        from humo_v2 import CASOS
        # Carga el modulo o los modulos random.
        import random
        # Asigna a numero el valor calculado a la derecha.
        numero = random.randint(1000000000, 2000000000)
        # Espera que termine la operacion asincronica antes de continuar.
        await self.sql("INSERT INTO universidad(id,nombre,tipo,ciudad,activo) VALUES (:id,'Prueba v3','Prueba','Prueba',TRUE)", id=numero)
        # Espera que termine la operacion asincronica antes de continuar.
        await self.sql("INSERT INTO linea_investigacion(id,nombre,descripcion,activo) VALUES (:id,'Prueba v3','Prueba de regresión v3',TRUE)", id=numero)
        # Asigna a creados el valor calculado a la derecha.
        creados = []
        # Recorre los elementos de la coleccion indicada y ejecuta el bloque para cada uno.
        for caso in CASOS:
            # Asigna a tabla el valor calculado a la derecha.
            tabla = caso['tabla']
            # Asigna a datos el valor calculado a la derecha.
            datos = {k: numero if v == '__ID__' else v for k,v in caso['datos'].items()}
            # Asigna a ruta el valor calculado a la derecha.
            ruta = '/api/'+tabla+'/'+'/'.join(str(datos[k]) for k in caso['claves'])
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            self.assertEqual(self.api('POST','/api/'+tabla,datos)[0],200,tabla)
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            creados.append((caso,datos,ruta))
            # Asigna a original el valor calculado a la derecha.
            original = self.api('GET',ruta)[1]
            # Asigna a cuerpo el valor calculado a la derecha.
            cuerpo = {k:datos[k] for k in caso['mutables']}
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            self.assertEqual(self.api('PUT',ruta,cuerpo)[0],200,tabla)
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            self.assertEqual(self.api('PATCH',ruta,{})[0],400,tabla)
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            self.assertEqual(self.api('PATCH',ruta,{caso['fk']:-999999999})[0],400,tabla)
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            self.assertEqual(self.api('GET',ruta)[1],original,tabla)
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            self.assertEqual(self.api('PATCH',ruta,{caso['mutables'][0]:cuerpo[caso['mutables'][0]]})[0],200,tabla)
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            cuerpo.pop(caso['mutables'][0])
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            self.assertEqual(self.api('PUT',ruta,cuerpo)[0],422,tabla)
        # Recorre los elementos de la coleccion indicada y ejecuta el bloque para cada uno.
        for tabla in ('docente','grupo_investigacion','semillero'):
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            self.assertEqual(self.api('DELETE','/api/'+tabla+'/'+str(numero))[0],400)
        # Recorre los elementos de la coleccion indicada y ejecuta el bloque para cada uno.
        for caso,datos,ruta in reversed(creados):
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            self.assertEqual(self.api('DELETE',ruta)[0],200,caso['tabla'])
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            self.assertEqual(self.api('GET',ruta)[0],404,caso['tabla'])
            # Asigna a donde el valor calculado a la derecha.
            donde = ' AND '.join(k+'=:'+k for k in caso['claves'])
            # Asigna a activo el valor calculado a la derecha.
            activo = (await self.sql('SELECT activo FROM '+caso['tabla']+' WHERE '+donde, **{k:datos[k] for k in caso['claves']})).scalar_one()
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            self.assertIs(activo,False)
        # Área de conocimiento v1 también conserva reemplazo/parcial y retiro lógico.
        # Asigna a codigo el valor calculado a la derecha.
        codigo = 'T'+secrets.token_hex(2)
        # Asigna a datos el valor calculado a la derecha.
        datos = {'id':codigo,'granArea':'Prueba','area':'Prueba','disciplina':'Prueba'}
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.api('POST','/api/area_conocimiento',datos)[0],200)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.api('PATCH','/api/area_conocimiento/'+codigo,{'disciplina':'Cambio'})[0],200)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.api('GET','/api/area_conocimiento/'+codigo)[1]['disciplina'],'Cambio')
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.api('DELETE','/api/area_conocimiento/'+codigo)[0],200)

    # Define la funcion test_ultimo_administrador_y_concurrencia con los parametros declarados; su bloque realiza esta operacion.
    async def test_ultimo_administrador_y_concurrencia(self):
        # Asigna a rid el valor calculado a la derecha.
        rid = (await self.sql("SELECT id FROM rol WHERE nombre='administrador'")).scalar_one()
        # Recorre los elementos de la coleccion indicada y ejecuta el bloque para cada uno.
        for ruta in ('/api/usuario/1', f'/api/rol/{rid}', f'/api/rol_usuario/1/{rid}'):
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            self.assertEqual(self.api('DELETE', ruta)[0], 409)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.api('PATCH', f'/api/rol/{rid}', {'nombre':'otro'})[0], 409)
        # Dos bajas simultáneas no pueden confirmar la pérdida de ambos administradores.
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.api('POST', '/api/rol_usuario', {'usuario_id': self.usuario, 'rol_id': rid})[0], 201)
        # Asigna a rutas el valor calculado a la derecha.
        rutas = [f'/api/rol_usuario/1/{rid}', f'/api/rol_usuario/{self.usuario}/{rid}']
        # Asigna a respuestas el valor calculado a la derecha.
        respuestas = await asyncio.gather(*(asyncio.to_thread(self.api, 'DELETE', ruta) for ruta in rutas))
        # Asigna a estados el valor calculado a la derecha.
        estados = sorted(r[0] for r in respuestas)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertIn(estados, ([200, 409], [200, 403]))
        # Asigna a cantidad el valor calculado a la derecha.
        cantidad = (await self.sql("""SELECT count(*) FROM usuario u JOIN rol_usuario ru ON u.id=ru.usuario_id
            JOIN rol r ON r.id=ru.rol_id WHERE u.activo IS TRUE AND ru.activo IS TRUE AND r.activo IS TRUE AND r.nombre='administrador'""")).scalar_one()  # Termina el literal multilinea y completa la instruccion que lo contiene.
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(cantidad, 1)

# Ejecuta el bloque siguiente solo cuando se cumple: __name__ == '__main__'.
if __name__ == '__main__':
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    asyncio.run(base.preparar())
    # Inicia un bloque cuya excepcion se manejara en los except siguientes.
    try:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        base.arrancar()
        # Asigna a suite el valor calculado a la derecha.
        suite = unittest.TestSuite(AdministracionHTTP(nombre) for nombre in AdministracionHTTP.__dict__ if nombre.startswith('test_'))
        # Asigna a resultado el valor calculado a la derecha.
        resultado = unittest.TextTestRunner(verbosity=2).run(suite)
    # Ejecuta este bloque al final, haya ocurrido o no una excepcion.
    finally:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        base.detener()
    # Lanza la excepcion indicada y detiene el flujo normal.
    raise SystemExit(0 if resultado.wasSuccessful() else 1)
