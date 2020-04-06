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

    def test_api_deaths_by_country(self):
        response = self.app.get('/api/deaths/fr/')
        assert response.status_code == 200

    def test_api_confirmed_by_country(self):
        response = self.app.get('/api/confirmed/fr/')
        assert response.status_code == 200

    def test_api_recovered_by_country(self):
        response = self.app.get('/api/recovered/fr/')
        assert response.status_code == 200

    def test_api_deaths_by_country_and_province(self):
        response = self.app.get('/api/deaths/CN/Hubei')
        assert response.status_code == 200

    def test_api_confirmed_by_country_and_province(self):
        response = self.app.get('/api/confirmed/cn/hubei')
        assert response.status_code == 200

    def test_api_recovered_by_country_and_province(self):
        response = self.app.get('/api/recovered/cn/hubei')
        assert response.status_code == 200

    def test_api_all(self):
        response = self.app.get('/api/all')
        assert response.status_code == 200

    def test_api_all_regrouped(self):
        response = self.app.get('/api/all/regrouped')
        assert response.status_code == 200

    def setUp(self):
        self.app = app.test_client()

    def tearDown(slef):
        pass
