"""Pruebas de reglas e integridad con repositorios en memoria.

Ejecutar: python pruebas/prueba_v2.py (PostgreSQL no es necesario).
"""
# Carga el modulo o los modulos asyncio.
import asyncio
# Importa asynccontextmanager desde contextlib para usar esas definiciones.
from contextlib import asynccontextmanager
# Importa Path desde pathlib para usar esas definiciones.
from pathlib import Path
# Carga el modulo o los modulos sys.
import sys
# Carga el modulo o los modulos unittest.
import unittest

# Ejecuta la instruccion o llamada indicada dentro del bloque actual.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Importa ServicioSemillero desde servicios.servicio_semillero para usar esas definiciones.
from servicios.servicio_semillero import ServicioSemillero
# Importa ServicioAcLinea desde servicios.servicio_ac_linea para usar esas definiciones.
from servicios.servicio_ac_linea import ServicioAcLinea
# Importa Semillero, SemilleroActualizar, SemilleroReemplazo desde models.semillero para usar esas definiciones.
from models.semillero import Semillero, SemilleroActualizar, SemilleroReemplazo
# Importa AcLineaActualizar desde models.ac_linea para usar esas definiciones.
from models.ac_linea import AcLineaActualizar
# Importa ValidationError desde pydantic para usar esas definiciones.
from pydantic import ValidationError


# Define la clase RepositorioFalso y agrupa su estado y operaciones.
class RepositorioFalso:
    # Define la funcion __init__ con los parametros declarados; su bloque realiza esta operacion.
    def __init__(self, claves):
        # Guarda en self.claves el valor necesario para reutilizarlo en otros metodos.
        self.claves = claves
        # Guarda en self.filas el valor necesario para reutilizarlo en otros metodos.
        self.filas = []
        # Guarda en self.referencias el valor necesario para reutilizarlo en otros metodos.
        self.referencias = {}
        # Guarda en self.dependientes el valor necesario para reutilizarlo en otros metodos.
        self.dependientes = False

    # Aplica @asynccontextmanager a la declaracion que sigue; en rutas, registra el endpoint HTTP.
    @asynccontextmanager
    # Define la funcion transaccion con los parametros declarados; su bloque realiza esta operacion.
    async def transaccion(self):
        # Entrega un valor al iterador y conserva el estado de la funcion.
        yield

    # Define la funcion referencia_activa con los parametros declarados; su bloque realiza esta operacion.
    async def referencia_activa(self, campo, valor):
        # Devuelve al llamador el resultado de la expresion indicada.
        return valor in self.referencias.get(campo, set())

    # Define la funcion tiene_dependientes con los parametros declarados; su bloque realiza esta operacion.
    async def tiene_dependientes(self, identidad):
        # Devuelve al llamador el resultado de la expresion indicada.
        return self.dependientes

    # Define la funcion obtener_todos con los parametros declarados; su bloque realiza esta operacion.
    async def obtener_todos(self, limite):
        # Devuelve al llamador el resultado de la expresion indicada.
        return [{k: v for k, v in f.items() if k != 'activo'} for f in self.filas if f['activo']][:limite]

    # Define la funcion obtener_por_id con los parametros declarados; su bloque realiza esta operacion.
    async def obtener_por_id(self, identidad):
        # Devuelve al llamador el resultado de la expresion indicada.
        return next(({k: v for k, v in f.items() if k != 'activo'} for f in self.filas
                     # Ejecuta el bloque siguiente solo cuando se cumple: f['activo'] and all(f[k] == v for k, v in identidad.items())), None).
                     if f['activo'] and all(f[k] == v for k, v in identidad.items())), None)

    # Define la funcion crear con los parametros declarados; su bloque realiza esta operacion.
    async def crear(self, datos):
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.filas.append({**datos, 'activo': True})

    # Define la funcion actualizar con los parametros declarados; su bloque realiza esta operacion.
    async def actualizar(self, identidad, datos):
        # Recorre los elementos de la coleccion indicada y ejecuta el bloque para cada uno.
        for fila in self.filas:
            # Ejecuta el bloque siguiente solo cuando se cumple: fila['activo'] and all(fila[k] == v for k, v in identidad.items()).
            if fila['activo'] and all(fila[k] == v for k, v in identidad.items()):
                # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
                fila.update(datos)
                # Devuelve al llamador el resultado de la expresion indicada.
                return 1
        # Devuelve al llamador el resultado de la expresion indicada.
        return 0

    # Define la funcion eliminar_logico con los parametros declarados; su bloque realiza esta operacion.
    async def eliminar_logico(self, identidad):
        # Devuelve al llamador el resultado de la expresion indicada.
        return await self.actualizar(identidad, {'activo': False})


# Define la clase PruebasIntegridad y agrupa su estado y operaciones.
class PruebasIntegridad(unittest.IsolatedAsyncioTestCase):
    # Define la funcion asyncSetUp con los parametros declarados; su bloque realiza esta operacion.
    async def asyncSetUp(self):
        # Guarda en self.repo el valor necesario para reutilizarlo en otros metodos.
        self.repo = RepositorioFalso(('id',))
        # Guarda en self.repo.referencias el valor necesario para reutilizarlo en otros metodos.
        self.repo.referencias = {'grupo_investigacion': {1}}
        # Guarda en self.servicio el valor necesario para reutilizarlo en otros metodos.
        self.servicio = ServicioSemillero(self.repo)
        # Guarda en self.datos el valor necesario para reutilizarlo en otros metodos.
        self.datos = {'id': 7, 'nombre': 'Semillero de pruebas', 'fecha_fundacion': '2026-01-01', 'grupo_investigacion': 1}

    # Define la funcion test_referencia_inexistente_no_escribe con los parametros declarados; su bloque realiza esta operacion.
    async def test_referencia_inexistente_no_escribe(self):
        # Abre el recurso y asegura su cierre al salir del bloque.
        with self.assertRaises(ValueError):
            # Espera que termine la operacion asincronica antes de continuar.
            await self.servicio.crear({**self.datos, 'grupo_investigacion': 999})
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.repo.filas, [])

    # Define la funcion test_referencia_inactiva_no_escribe con los parametros declarados; su bloque realiza esta operacion.
    async def test_referencia_inactiva_no_escribe(self):
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.repo.referencias['grupo_investigacion'].clear()
        # Abre el recurso y asegura su cierre al salir del bloque.
        with self.assertRaises(ValueError):
            # Espera que termine la operacion asincronica antes de continuar.
            await self.servicio.crear(self.datos)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(self.repo.filas, [])

    # Define la funcion test_patch_invalido_conserva_valores con los parametros declarados; su bloque realiza esta operacion.
    async def test_patch_invalido_conserva_valores(self):
        # Espera que termine la operacion asincronica antes de continuar.
        await self.servicio.crear(self.datos)
        # Abre el recurso y asegura su cierre al salir del bloque.
        with self.assertRaises(ValueError):
            # Espera que termine la operacion asincronica antes de continuar.
            await self.servicio.actualizar({'id': 7}, {'grupo_investigacion': 999})
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual((await self.servicio.obtener({'id': 7}))['grupo_investigacion'], 1)

    # Define la funcion test_patch_cambia_solo_nombre con los parametros declarados; su bloque realiza esta operacion.
    async def test_patch_cambia_solo_nombre(self):
        # Espera que termine la operacion asincronica antes de continuar.
        await self.servicio.crear(self.datos)
        # Espera que termine la operacion asincronica antes de continuar.
        await self.servicio.actualizar({'id': 7}, {'nombre': 'Nuevo nombre'})
        # Asigna a fila el valor calculado a la derecha.
        fila = await self.servicio.obtener({'id': 7})
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(fila['nombre'], 'Nuevo nombre')
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(fila['fecha_fundacion'], self.datos['fecha_fundacion'])

    # Define la funcion test_borrado_logico_y_segundo_borrado con los parametros declarados; su bloque realiza esta operacion.
    async def test_borrado_logico_y_segundo_borrado(self):
        # Espera que termine la operacion asincronica antes de continuar.
        await self.servicio.crear(self.datos)
        # Espera que termine la operacion asincronica antes de continuar.
        await self.servicio.eliminar({'id': 7})
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(len(self.repo.filas), 1)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertFalse(self.repo.filas[0]['activo'])
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(await self.servicio.listar(1000), [])
        # Abre el recurso y asegura su cierre al salir del bloque.
        with self.assertRaises(LookupError):
            # Espera que termine la operacion asincronica antes de continuar.
            await self.servicio.eliminar({'id': 7})

    # Define la funcion test_padre_con_dependientes_no_se_desactiva con los parametros declarados; su bloque realiza esta operacion.
    async def test_padre_con_dependientes_no_se_desactiva(self):
        # Espera que termine la operacion asincronica antes de continuar.
        await self.servicio.crear(self.datos)
        # Guarda en self.repo.dependientes el valor necesario para reutilizarlo en otros metodos.
        self.repo.dependientes = True
        # Abre el recurso y asegura su cierre al salir del bloque.
        with self.assertRaises(ValueError):
            # Espera que termine la operacion asincronica antes de continuar.
            await self.servicio.eliminar({'id': 7})
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertTrue(self.repo.filas[0]['activo'])

    # Define la funcion test_clave_compuesta_y_cambio_de_relacion con los parametros declarados; su bloque realiza esta operacion.
    async def test_clave_compuesta_y_cambio_de_relacion(self):
        # Asigna a repo el valor calculado a la derecha.
        repo = RepositorioFalso(('linea_investigacion', 'area_conocimiento'))
        # Asigna a repo.referencias el valor calculado a la derecha.
        repo.referencias = {'linea_investigacion': {1, 2}, 'area_conocimiento': {'1A01'}}
        # Asigna a servicio el valor calculado a la derecha.
        servicio = ServicioAcLinea(repo)
        # Asigna a identidad el valor calculado a la derecha.
        identidad = {'linea_investigacion': 1, 'area_conocimiento': '1A01'}
        # Espera que termine la operacion asincronica antes de continuar.
        await servicio.crear(identidad)
        # Espera que termine la operacion asincronica antes de continuar.
        await servicio.actualizar(identidad, {'linea_investigacion': 2})
        # Abre el recurso y asegura su cierre al salir del bloque.
        with self.assertRaises(LookupError):
            # Espera que termine la operacion asincronica antes de continuar.
            await servicio.obtener(identidad)
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual((await servicio.obtener({**identidad, 'linea_investigacion': 2}))['area_conocimiento'], '1A01')

    # Define la funcion test_limite_y_patch_vacio con los parametros declarados; su bloque realiza esta operacion.
    async def test_limite_y_patch_vacio(self):
        # Abre el recurso y asegura su cierre al salir del bloque.
        with self.assertRaises(ValueError):
            # Espera que termine la operacion asincronica antes de continuar.
            await self.servicio.listar(0)
        # Abre el recurso y asegura su cierre al salir del bloque.
        with self.assertRaises(ValueError):
            # Espera que termine la operacion asincronica antes de continuar.
            await self.servicio.actualizar({'id': 7}, {})


# Define la clase PruebasContratos y agrupa su estado y operaciones.
class PruebasContratos(unittest.TestCase):
    # Define la funcion test_put_obliga_a_enviar_todos_los_campos con los parametros declarados; su bloque realiza esta operacion.
    def test_put_obliga_a_enviar_todos_los_campos(self):
        # Abre el recurso y asegura su cierre al salir del bloque.
        with self.assertRaises(ValidationError):
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            SemilleroReemplazo(nombre='Parcial')
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(SemilleroActualizar(nombre='Parcial').model_dump(exclude_unset=True), {'nombre': 'Parcial'})

    # Define la funcion test_no_se_admite_reactivacion con los parametros declarados; su bloque realiza esta operacion.
    def test_no_se_admite_reactivacion(self):
        # Abre el recurso y asegura su cierre al salir del bloque.
        with self.assertRaises(ValidationError):
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            SemilleroActualizar(activo=True)

    # Define la funcion test_no_se_admite_nulo_en_fk_obligatoria con los parametros declarados; su bloque realiza esta operacion.
    def test_no_se_admite_nulo_en_fk_obligatoria(self):
        # Abre el recurso y asegura su cierre al salir del bloque.
        with self.assertRaises(ValidationError):
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            SemilleroActualizar(grupo_investigacion=None)

    # Define la funcion test_codigo_de_area_sigue_siendo_texto con los parametros declarados; su bloque realiza esta operacion.
    def test_codigo_de_area_sigue_siendo_texto(self):
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        self.assertEqual(AcLineaActualizar(area_conocimiento='1A01').area_conocimiento, '1A01')
        # Abre el recurso y asegura su cierre al salir del bloque.
        with self.assertRaises(ValidationError):
            # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
            AcLineaActualizar(area_conocimiento='CODIGOLARGO')


# Ejecuta el bloque siguiente solo cuando se cumple: __name__ == '__main__'.
if __name__ == '__main__':
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    unittest.main(verbosity=2)
