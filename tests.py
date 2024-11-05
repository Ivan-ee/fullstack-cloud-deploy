from app import app
import unittest


class Main(unittest.TestCase):
    def test_hello_docker(self):
        with app.test_client() as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b'Hello, Docker!')

    def test_get_data(self):
        with app.test_client() as client:
            response = client.get('/data')
            self.assertEqual(response.status_code, 200)

            response_data = response.get_json().get("data")
            self.assertEqual(response_data, "This is the data")
