"""Integración HTTP v3 en una base nueva; sin tocar pruebas reservadas del equipo."""
import asyncio
import os
import secrets
import unittest
from sqlalchemy import text
import prueba_autenticacion_v3 as base
from seguridad.adaptadores import TokensJWT

class AdministracionHTTP(base.AutenticacionHTTP):
    def administrador(self):
        return TokensJWT(base.CONFIG).emitir(1, 0)

    def api(self, metodo, ruta, datos=None):
        return base.pedir(metodo, ruta, datos, self.administrador())

    async def test_matriz_todas_las_rutas_directas(self):
        contrato = base.pedir('GET', '/openapi.json')[1]
        token = self.token()
        total = 0
        for ruta, operaciones in contrato['paths'].items():
            if not ruta.startswith('/api/') or ruta in ('/api/login', '/api/logout', '/api/sesion'):
                continue
            import re
            ruta_real = re.sub(r'\{[^}]+\}', '999999', ruta)
            for metodo in operaciones:
                if metodo not in ('get', 'post', 'put', 'patch', 'delete'):
                    continue
                self.assertEqual(operaciones[metodo].get('security'), [{'HTTPBearer': []}], ruta)
                total += 1
                self.assertEqual(base.pedir(metodo.upper(), ruta_real, {} if metodo != 'get' else None)[0], 401, ruta)
                if metodo != 'get' or ruta.split('/')[2] in ('usuario', 'rol', 'rol_usuario'):
                    self.assertEqual(base.pedir(metodo.upper(), ruta_real, {}, token)[0], 403, ruta)
                else:
                    estado = base.pedir('GET', ruta_real, token=token)[0]
                    self.assertIn(estado, (200, 204, 404, 422), ruta)
        self.assertGreater(total, 60)
        await self.sql('UPDATE rol_usuario SET activo=FALSE WHERE usuario_id=:id', id=self.usuario)
        self.assertEqual(base.pedir('GET', '/api/area_conocimiento', token=token)[0], 403)
        print('Operaciones protegidas verificadas:', total)

    async def test_crud_y_secretos(self):
        nombre = 'NUEVO_' + secrets.token_hex(6)
        clave = secrets.token_urlsafe(24)
        datos = {'username': nombre, 'email': nombre+'@example.invalid', 'password': clave}
        estado, usuario, _ = self.api('POST', '/api/usuario', datos)
        self.assertEqual(estado, 201)
        self.assertNotIn('password', usuario)
        uid = usuario['id']
        self.assertEqual(self.api('POST', '/api/usuario', datos)[0], 409)
        self.assertEqual(base.pedir('POST', '/api/login', {'username': nombre, 'password': clave})[0], 403)
        rid = (await self.sql("SELECT id FROM rol WHERE nombre='consulta'")).scalar_one()
        relacion = {'usuario_id': uid, 'rol_id': rid}
        self.assertEqual(self.api('POST', '/api/rol_usuario', relacion)[0], 201)
        token = base.pedir('POST', '/api/login', {'username': nombre, 'password': clave})[1]['access_token']
        self.assertEqual(self.api('GET', f'/api/usuario/{uid}')[0], 200)
        self.assertEqual(self.api('PUT', f'/api/usuario/{uid}', {'email': 'incompleto@example.invalid'})[0], 422)
        self.assertEqual(self.api('PATCH', f'/api/usuario/{uid}', {'password': clave, 'activo': True})[0], 422)
        self.assertEqual(self.api('PATCH', f'/api/usuario/{uid}', {'password': None})[0], 422)
        nueva = secrets.token_urlsafe(24)
        self.assertEqual(self.api('PATCH', f'/api/usuario/{uid}', {'password': nueva})[0], 200)
        self.assertEqual(base.pedir('GET', '/api/sesion', token=token)[0], 401)
        self.assertEqual(self.api('DELETE', f'/api/rol_usuario/{uid}/{rid}')[0], 200)
        self.assertEqual(self.api('POST', '/api/rol_usuario', relacion)[0], 409)
        self.assertFalse((await self.sql('SELECT activo FROM rol_usuario WHERE usuario_id=:id AND rol_id=:rid', id=uid, rid=rid)).scalar_one())
        self.assertEqual(self.api('DELETE', f'/api/usuario/{uid}')[0], 200)
        self.assertEqual(self.api('GET', f'/api/usuario/{uid}')[0], 404)
        self.assertFalse((await self.sql('SELECT activo FROM usuario WHERE id=:id', id=uid)).scalar_one())
        estado, rol, _ = self.api('POST', '/api/rol', {'nombre': nombre, 'descripcion': 'Prueba'})
        self.assertEqual(estado, 201)
        self.assertEqual(self.api('PUT', f"/api/rol/{rol['id']}", {'nombre': nombre, 'descripcion': 'Cambio'})[0], 200)
        self.assertEqual(self.api('PATCH', f"/api/rol/{rol['id']}", {'descripcion': None})[0], 200)
        self.assertEqual(self.api('DELETE', f"/api/rol/{rol['id']}")[0], 200)
        self.assertEqual(self.api('POST', '/api/rol_usuario', {'usuario_id': self.usuario, 'rol_id': rol['id']})[0], 409)
        self.assertEqual(self.api('POST', '/api/rol_usuario', {'usuario_id': 999999, 'rol_id': rid})[0], 409)
        self.assertEqual(self.api('PATCH', '/api/usuario/999999', {'email':'x@example.invalid'})[0], 404)
        self.assertEqual(self.api('PATCH', '/api/rol/999999', {})[0], 409)

    async def test_regresion_crud_dominio_con_administrador(self):
        from humo_v2 import CASOS
        import random
        numero = random.randint(1000000000, 2000000000)
        await self.sql("INSERT INTO universidad(id,nombre,tipo,ciudad,activo) VALUES (:id,'Prueba v3','Prueba','Prueba',TRUE)", id=numero)
        await self.sql("INSERT INTO linea_investigacion(id,nombre,descripcion,activo) VALUES (:id,'Prueba v3','Prueba de regresión v3',TRUE)", id=numero)
        creados = []
        for caso in CASOS:
            tabla = caso['tabla']
            datos = {k: numero if v == '__ID__' else v for k,v in caso['datos'].items()}
            ruta = '/api/'+tabla+'/'+'/'.join(str(datos[k]) for k in caso['claves'])
            self.assertEqual(self.api('POST','/api/'+tabla,datos)[0],200,tabla)
            creados.append((caso,datos,ruta))
            original = self.api('GET',ruta)[1]
            cuerpo = {k:datos[k] for k in caso['mutables']}
            self.assertEqual(self.api('PUT',ruta,cuerpo)[0],200,tabla)
            self.assertEqual(self.api('PATCH',ruta,{})[0],400,tabla)
            self.assertEqual(self.api('PATCH',ruta,{caso['fk']:-999999999})[0],400,tabla)
            self.assertEqual(self.api('GET',ruta)[1],original,tabla)
            self.assertEqual(self.api('PATCH',ruta,{caso['mutables'][0]:cuerpo[caso['mutables'][0]]})[0],200,tabla)
            cuerpo.pop(caso['mutables'][0])
            self.assertEqual(self.api('PUT',ruta,cuerpo)[0],422,tabla)
        for tabla in ('docente','grupo_investigacion','semillero'):
            self.assertEqual(self.api('DELETE','/api/'+tabla+'/'+str(numero))[0],400)
        for caso,datos,ruta in reversed(creados):
            self.assertEqual(self.api('DELETE',ruta)[0],200,caso['tabla'])
            self.assertEqual(self.api('GET',ruta)[0],404,caso['tabla'])
            donde = ' AND '.join(k+'=:'+k for k in caso['claves'])
            activo = (await self.sql('SELECT activo FROM '+caso['tabla']+' WHERE '+donde, **{k:datos[k] for k in caso['claves']})).scalar_one()
            self.assertIs(activo,False)
        # Área de conocimiento v1 también conserva reemplazo/parcial y retiro lógico.
        codigo = 'T'+secrets.token_hex(2)
        datos = {'id':codigo,'granArea':'Prueba','area':'Prueba','disciplina':'Prueba'}
        self.assertEqual(self.api('POST','/api/area_conocimiento',datos)[0],200)
        self.assertEqual(self.api('PATCH','/api/area_conocimiento/'+codigo,{'disciplina':'Cambio'})[0],200)
        self.assertEqual(self.api('GET','/api/area_conocimiento/'+codigo)[1]['disciplina'],'Cambio')
        self.assertEqual(self.api('DELETE','/api/area_conocimiento/'+codigo)[0],200)

    async def test_ultimo_administrador_y_concurrencia(self):
        rid = (await self.sql("SELECT id FROM rol WHERE nombre='administrador'")).scalar_one()
        for ruta in ('/api/usuario/1', f'/api/rol/{rid}', f'/api/rol_usuario/1/{rid}'):
            self.assertEqual(self.api('DELETE', ruta)[0], 409)
        self.assertEqual(self.api('PATCH', f'/api/rol/{rid}', {'nombre':'otro'})[0], 409)
        # Dos bajas simultáneas no pueden confirmar la pérdida de ambos administradores.
        self.assertEqual(self.api('POST', '/api/rol_usuario', {'usuario_id': self.usuario, 'rol_id': rid})[0], 201)
        rutas = [f'/api/rol_usuario/1/{rid}', f'/api/rol_usuario/{self.usuario}/{rid}']
        respuestas = await asyncio.gather(*(asyncio.to_thread(self.api, 'DELETE', ruta) for ruta in rutas))
        estados = sorted(r[0] for r in respuestas)
        self.assertIn(estados, ([200, 409], [200, 403]))
        cantidad = (await self.sql("""SELECT count(*) FROM usuario u JOIN rol_usuario ru ON u.id=ru.usuario_id
            JOIN rol r ON r.id=ru.rol_id WHERE u.activo IS TRUE AND ru.activo IS TRUE AND r.activo IS TRUE AND r.nombre='administrador'""")).scalar_one()
        self.assertEqual(cantidad, 1)

if __name__ == '__main__':
    asyncio.run(base.preparar())
    try:
        base.arrancar()
        suite = unittest.TestSuite(AdministracionHTTP(nombre) for nombre in AdministracionHTTP.__dict__ if nombre.startswith('test_'))
        resultado = unittest.TextTestRunner(verbosity=2).run(suite)
    finally:
        base.detener()
    raise SystemExit(0 if resultado.wasSuccessful() else 1)
