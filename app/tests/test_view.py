import unittest
from app import app


class TestViewsRoutes(unittest.TestCase):
    def test_index(self):
        response = self.app.get('/')
        assert response.status_code == 200

    def test_country(self):
        response = self.app.get('/fr/')
        assert response.status_code == 200

    def setUp(self):
        self.app = app.test_client()

    def tearDown(slef):
        pass
