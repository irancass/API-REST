import unittest
import json
from apirest import app
  

class APIDispositivosTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.headers = {'Content-Type': 'application/json'}

    def test1_agregarDispositivo(self):
        data = {"nombre": "Switch Cisco", "tipo": "Switch"}
        response = self.client.post('/dispositivos', data=json.dumps(data), headers=self.headers)
        self.assertEqual(response.status_code, 201)
        respuesta_json = response.get_json()
        self.assertIn("id", respuesta_json)
        self.assertEqual(respuesta_json["nombre"], "Switch Cisco")

    def test2_listarDispo(self):
        response = self.client.get('/dispositivos')
        self.assertEqual(response.status_code, 200)
        dispositivos = response.get_json()
        self.assertIsInstance(dispositivos, list)

    def test3_actualizarDispo(self):
        # Primero agregamos uno para tener un ID
        nuevo = {"nombre": "Router Cisco", "tipo": "Router"}
        post = self.client.post('/dispositivos', data=json.dumps(nuevo), headers=self.headers)
        dispositivo_id = post.get_json()["id"]

        # Ahora lo actualizamos
        actualizacion = {"nombre": "Router Cisco Actualizado"}
        put = self.client.put(f'/dispositivos/{dispositivo_id}', data=json.dumps(actualizacion), headers=self.headers)
        self.assertEqual(put.status_code, 200)
        actualizado = put.get_json()
        self.assertEqual(actualizado["nombre"], "Router Cisco Actualizado")

    def test4_eliminarDispo(self):
        # Agregamos uno para eliminar
        data = {"nombre": "Firewall SonicWall", "tipo": "Firewall"}
        post = self.client.post('/dispositivos', data=json.dumps(data), headers=self.headers)
        dispositivo_id = post.get_json()["id"]

        # Lo eliminamos
        delete = self.client.delete(f'/dispositivos/{dispositivo_id}')
        self.assertEqual(delete.status_code, 204)

        # Confirmamos que ya no existe
        get = self.client.get('/dispositivos')
        ids_actuales = [d["id"] for d in get.get_json()]
        self.assertNotIn(dispositivo_id, ids_actuales)

if __name__ == '__main__':
    unittest.main()
