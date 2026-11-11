# Prueba HTTP de la política v3 usando la misma base efímera que las suites
# de autenticación y administración. Las escrituras de consulta se rechazan
# antes de alcanzar los controladores.
import asyncio
import re
import unittest

import prueba_autenticacion_v3 as base
from seguridad.adaptadores import TokensJWT


class PermisosEquipoHTTP(base.AutenticacionHTTP):
    def test_matriz_lectura_consulta_y_acceso_administrador(self):
        contrato = base.pedir('GET', '/openapi.json')[1]
        token_consulta = self.token()
        token_administrador = TokensJWT(base.CONFIG).emitir(1, 0)
        operaciones = 0

        for ruta, metodos in contrato['paths'].items():
            if not ruta.startswith('/api/') or ruta in ('/api/login', '/api/logout', '/api/sesion'):
                continue
            ruta_real = re.sub(r'\{[^}]+\}', '999999', ruta)
            es_seguridad = ruta.split('/')[2] in ('usuario', 'rol', 'rol_usuario')

            for metodo in metodos:
                if metodo not in ('get', 'post', 'put', 'patch', 'delete'):
                    continue
                operaciones += 1
                datos = None if metodo == 'get' else {}

                estado_consulta = base.pedir(
                    metodo.upper(), ruta_real, datos, token_consulta
                )[0]
                if es_seguridad or metodo != 'get':
                    self.assertEqual(estado_consulta, 403, f'{metodo.upper()} {ruta}')
                else:
                    self.assertIn(estado_consulta, (200, 204, 404, 422), f'{metodo.upper()} {ruta}')

                estado_administrador = base.pedir(
                    metodo.upper(), ruta_real, datos, token_administrador
                )[0]
                self.assertNotIn(estado_administrador, (401, 403), f'{metodo.upper()} {ruta}')

        self.assertGreater(operaciones, 60)
        print('Operaciones con permisos verificados:', operaciones)


if __name__ == '__main__':
    asyncio.run(base.preparar())
    try:
        base.arrancar()
        nombres = [nombre for nombre in PermisosEquipoHTTP.__dict__ if nombre.startswith('test_')]
        suite = unittest.TestSuite(PermisosEquipoHTTP(nombre) for nombre in nombres)
        resultado = unittest.TextTestRunner(verbosity=2).run(suite)
    finally:
        base.detener()
    raise SystemExit(0 if resultado.wasSuccessful() else 1)
