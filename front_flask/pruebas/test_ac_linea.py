"""Pruebas de la pantalla Áreas de las líneas."""
import unittest
from unittest.mock import patch

import app as modulo


class PruebasFormularioAcLinea(unittest.TestCase):
    def setUp(self):
        modulo.app.config.update(TESTING=True)
        self.cliente = modulo.app.test_client()

    def test_guardado_se_bloquea_si_falta_cualquier_catalogo_activo(self):
        casos = (
            (
                (True, [], []),
                (True, [{'id': '1A01', 'disciplina': 'Matemáticas puras'}], []),
                'No hay líneas de investigación activas para asociar.',
            ),
            (
                (True, [{'id': 7, 'nombre': 'Línea de prueba'}], []),
                (True, [], []),
                'No hay áreas de conocimiento activas para asociar.',
            ),
        )
        for lineas, areas, mensaje in casos:
            with self.subTest(mensaje=mensaje):
                with patch.object(modulo.cliente_api, 'listar_linea_investigacion', return_value=lineas), \
                     patch.object(modulo.cliente_api, 'listar_areas_conocimiento', return_value=areas):
                    respuesta = self.cliente.get('/ac-linea/nuevo')
                html = respuesta.get_data(as_text=True)
                self.assertEqual(respuesta.status_code, 200)
                self.assertIn(mensaje, html)
                self.assertRegex(html, r'<button[^>]*disabled')

    def test_selectores_son_obligatorios_cuando_hay_opciones(self):
        with patch.object(modulo.cliente_api, 'listar_linea_investigacion', return_value=(
            True, [{'id': 7, 'nombre': 'Línea de prueba'}], []
        )), patch.object(modulo.cliente_api, 'listar_areas_conocimiento', return_value=(
            True, [{'id': '1A01', 'disciplina': 'Matemáticas puras'}], []
        )):
            respuesta = self.cliente.get('/ac-linea/nuevo')

        html = respuesta.get_data(as_text=True)
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn('id="linea_investigacion" name="linea_investigacion" required', html)
        self.assertIn('id="area_conocimiento" name="area_conocimiento" required', html)
        self.assertNotRegex(html, r'<button[^>]*disabled')


if __name__ == '__main__':
    unittest.main(verbosity=2)
