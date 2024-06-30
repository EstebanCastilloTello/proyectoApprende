import unittest
import requests
import json

class TestCreateForm(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_url = "http://localhost:8081/formularios/"
        print("Inicio de pruebas para 'createForm'")

    @classmethod
    def tearDownClass(cls):
        print("Pruebas completadas para 'createForm'")

    def test_create_form_success(self):
        # Datos de prueba para un formulario exitoso
        data = {
            'nombre': 'Juan',
            'apellido': 'Pérez',
            'email': 'juan.perez@example.com',
            'tipo_clase': 'Online',
            'tipo_pago': 'Paypal',
            'disponibilidad': '2022-09-01',
            'hora_aproximada': '15:00:00',
            'costo_clase': 50,
            'duracion_clase': 60
        }
        response = requests.post(self.base_url, json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, 'Formulario creado')

    def test_create_form_failure_due_to_missing_field(self):
        # Datos de prueba faltando el campo 'email'
        data = {
            'nombre': 'Juan',
            'apellido': 'Pérez',
            'tipo_clase': 'Online',
            'tipo_pago': 'Paypal',
            'disponibilidad': '2022-09-01',
            'hora_aproximada': '15:00:00',
            'costo_clase': 50,
            'duracion_clase': 60
        }
        response = requests.post(self.base_url, json=data)
        self.assertEqual(response.status_code, 500)
        self.assertIn('Error al crear el formulario', response.text)
        
    def test_create_form_failure_with_excessive_cost(self):
        data = {
            'nombre': 'Ana',
            'apellido': 'López',
            'email': 'ana.lopez@example.com',
            'tipo_clase': 'Presencial',
            'tipo_pago': 'Transferencia Bancaria',
            'disponibilidad': '2022-10-01',
            'hora_aproximada': '10:00:00',
            'costo_clase': 1001,  # Valor ligeramente por encima del máximo permitido
            'duracion_clase': 60
        }
        response = requests.post(self.base_url, json=data)
        self.assertIn(response.status_code in [400, 500])
        self.assertIn('Error', response.text)

if __name__ == '__main__':
    unittest.main()
