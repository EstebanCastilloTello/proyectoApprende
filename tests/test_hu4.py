import unittest
import requests
import json

class UpdateTests(unittest.TestCase):
    valid_source_destination_request_data = None
    invalid_source_destination_request_data = None


    @classmethod
    def setUpClass(cls):
        cls.base_url = "http://localhost:8081/formularios/5"
        cls.valid_source_destination_request_data = {
            "nombre": "Juan Carlos",
            "apellido": "Bododoque",
            "email": "juancarlosb@sansano.usm.cl",
            "tipo_clase": "Presencial",
            "tipo_pago": "Paypal",
            "disponibildad": "2023-12-31",
            "hora_aproximada": "10:30:45.500000",
            "costo_clase": "1000000",
            "duracion_clase": "2"
        }

        cls.invalid_source_destination_request_data = {
            "nombre": """CElUe!0P#W?Fl?L6a8Arb<3yz7ZD$kTLq#19jHmXfItYw<6?K,5Fo!R9I?eNBtZ+@sDyWzTioqT(1o@zZUx6c-l$+3B2R;I8n>4(fB*4Ewm@e6s7oWqz1qTncD?2wHak3Vv$r7DgQz7F;5D@zJl)7iL'pQW!C#<sP1S-Tm3mAbx1m4n%cQo$-<N<M84HR;0Y@WTR%8rF*vnG<ra6<6F!CjLyEPPT#AIS<PO5B7oAgMK$U#-0a;HhL$C5tE<aN
""",
            "apellido": "Bododoque",
            "email": "juancarlosb@sansano.usm.cl",
            "tipo_clase": "Presencial",
            "tipo_pago": "Paypal",
            "disponibildad": "2023-12-31",
            "hora_aproximada": "10:30:45.500000",
            "costo_clase": "1000000",
            "duracion_clase": "2"
        }

    @classmethod
    def tearDown(cls):
        del valid_source_destination_request_data
        del invalid_source_destination_request_data_NOMBRE

    def test_update(cls):
        response = requests.post(cls.base_url, json=cls.valid_source_destination_request_data)
        
        resultado = json.load(response.json()["body"])["data"]

        cls.assertAlmostEqual("200", resultado)

    def test_update_invalid_name(cls):
        response = requests.post(cls.base_url, json=cls.invalid_source_destination_request_data)
        
        resultado = json.load(response.json()["body"])["data"]

        cls.assertAlmostEqual("400", resultado)

    def test_update_invalid_get(cls):
        response = requests.get(cls.base_url, json=cls.invalid_source_destination_request_data)
        
        resultado = json.load(response.json()["body"])["data"]

        cls.assertAlmostEqual("403", resultado)

if __name__ == '__main__':
    unittest.main()