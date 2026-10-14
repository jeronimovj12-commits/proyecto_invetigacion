"""Pruebas de reglas e integridad con repositorios en memoria.

Ejecutar: python pruebas/prueba_v2.py (PostgreSQL no es necesario).
"""
import asyncio
from contextlib import asynccontextmanager
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from servicios.servicio_semillero import ServicioSemillero
from servicios.servicio_ac_linea import ServicioAcLinea
from models.semillero import Semillero, SemilleroActualizar, SemilleroReemplazo
from models.ac_linea import AcLineaActualizar
from pydantic import ValidationError


class RepositorioFalso:
    def __init__(self, claves):
        self.claves = claves
        self.filas = []
        self.referencias = {}
        self.dependientes = False

    @asynccontextmanager
    async def transaccion(self):
        yield

    async def referencia_activa(self, campo, valor):
        return valor in self.referencias.get(campo, set())

    async def tiene_dependientes(self, identidad):
        return self.dependientes

    async def obtener_todos(self, limite):
        return [{k: v for k, v in f.items() if k != 'activo'} for f in self.filas if f['activo']][:limite]

    async def obtener_por_id(self, identidad):
        return next(({k: v for k, v in f.items() if k != 'activo'} for f in self.filas
                     if f['activo'] and all(f[k] == v for k, v in identidad.items())), None)

    async def crear(self, datos):
        self.filas.append({**datos, 'activo': True})

    async def actualizar(self, identidad, datos):
        for fila in self.filas:
            if fila['activo'] and all(fila[k] == v for k, v in identidad.items()):
                fila.update(datos)
                return 1
        return 0

    async def eliminar_logico(self, identidad):
        return await self.actualizar(identidad, {'activo': False})


class PruebasIntegridad(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.repo = RepositorioFalso(('id',))
        self.repo.referencias = {'grupo_investigacion': {1}}
        self.servicio = ServicioSemillero(self.repo)
        self.datos = {'id': 7, 'nombre': 'Semillero de pruebas', 'fecha_fundacion': '2026-01-01', 'grupo_investigacion': 1}

    async def test_referencia_inexistente_no_escribe(self):
        with self.assertRaises(ValueError):
            await self.servicio.crear({**self.datos, 'grupo_investigacion': 999})
        self.assertEqual(self.repo.filas, [])

    async def test_referencia_inactiva_no_escribe(self):
        self.repo.referencias['grupo_investigacion'].clear()
        with self.assertRaises(ValueError):
            await self.servicio.crear(self.datos)
        self.assertEqual(self.repo.filas, [])

    async def test_patch_invalido_conserva_valores(self):
        await self.servicio.crear(self.datos)
        with self.assertRaises(ValueError):
            await self.servicio.actualizar({'id': 7}, {'grupo_investigacion': 999})
        self.assertEqual((await self.servicio.obtener({'id': 7}))['grupo_investigacion'], 1)

    async def test_patch_cambia_solo_nombre(self):
        await self.servicio.crear(self.datos)
        await self.servicio.actualizar({'id': 7}, {'nombre': 'Nuevo nombre'})
        fila = await self.servicio.obtener({'id': 7})
        self.assertEqual(fila['nombre'], 'Nuevo nombre')
        self.assertEqual(fila['fecha_fundacion'], self.datos['fecha_fundacion'])

    async def test_borrado_logico_y_segundo_borrado(self):
        await self.servicio.crear(self.datos)
        await self.servicio.eliminar({'id': 7})
        self.assertEqual(len(self.repo.filas), 1)
        self.assertFalse(self.repo.filas[0]['activo'])
        self.assertEqual(await self.servicio.listar(1000), [])
        with self.assertRaises(LookupError):
            await self.servicio.eliminar({'id': 7})

    async def test_padre_con_dependientes_no_se_desactiva(self):
        await self.servicio.crear(self.datos)
        self.repo.dependientes = True
        with self.assertRaises(ValueError):
            await self.servicio.eliminar({'id': 7})
        self.assertTrue(self.repo.filas[0]['activo'])

    async def test_clave_compuesta_y_cambio_de_relacion(self):
        repo = RepositorioFalso(('linea_investigacion', 'area_conocimiento'))
        repo.referencias = {'linea_investigacion': {1, 2}, 'area_conocimiento': {'1A01'}}
        servicio = ServicioAcLinea(repo)
        identidad = {'linea_investigacion': 1, 'area_conocimiento': '1A01'}
        await servicio.crear(identidad)
        await servicio.actualizar(identidad, {'linea_investigacion': 2})
        with self.assertRaises(LookupError):
            await servicio.obtener(identidad)
        self.assertEqual((await servicio.obtener({**identidad, 'linea_investigacion': 2}))['area_conocimiento'], '1A01')

    async def test_limite_y_patch_vacio(self):
        with self.assertRaises(ValueError):
            await self.servicio.listar(0)
        with self.assertRaises(ValueError):
            await self.servicio.actualizar({'id': 7}, {})


class PruebasContratos(unittest.TestCase):
    def test_put_obliga_a_enviar_todos_los_campos(self):
        with self.assertRaises(ValidationError):
            SemilleroReemplazo(nombre='Parcial')
        self.assertEqual(SemilleroActualizar(nombre='Parcial').model_dump(exclude_unset=True), {'nombre': 'Parcial'})

    def test_no_se_admite_reactivacion(self):
        with self.assertRaises(ValidationError):
            SemilleroActualizar(activo=True)

    def test_no_se_admite_nulo_en_fk_obligatoria(self):
        with self.assertRaises(ValidationError):
            SemilleroActualizar(grupo_investigacion=None)

    def test_codigo_de_area_sigue_siendo_texto(self):
        self.assertEqual(AcLineaActualizar(area_conocimiento='1A01').area_conocimiento, '1A01')
        with self.assertRaises(ValidationError):
            AcLineaActualizar(area_conocimiento='CODIGOLARGO')


if __name__ == '__main__':
    unittest.main(verbosity=2)
