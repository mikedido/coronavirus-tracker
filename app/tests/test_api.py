import os
import unittest
from app import app

class TestApiRoutes(unittest.TestCase):
    def test_api_recovered(self):
        response = self.app.get('/api/recovered')
        assert response.status_code == 200

    def test_api_deaths(self):
        response = self.app.get('/api/deaths')
        assert response.status_code == 200

    def test_api_confirmed(self):
        response = self.app.get('/api/confirmed')
        assert response.status_code == 200

    def test_api_all(self):
        self.assertEqual(2, 2) 
        response = self.app.get('/api/all')
        assert response.status_code == 200
    
    def setUp(self):
        self.app = app.test_client()
    
    def tearDown(slef):
        pass