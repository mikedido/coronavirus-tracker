import unittest
from app import app


class TestApiRoutes(unittest.TestCase):
    def test_api_recovered(self):
        response = self.app.get('/v1/recovered')
        assert response.status_code == 200

    def test_api_deaths(self):
        response = self.app.get('/v1/deaths')
        assert response.status_code == 200

    def test_api_confirmed(self):
        response = self.app.get('/v1/confirmed')
        assert response.status_code == 200

    def test_api_deaths_by_country(self):
        response = self.app.get('/v1/deaths/fr')
        assert response.status_code == 200

    def test_api_confirmed_by_country(self):
        response = self.app.get('/v1/confirmed/fr')
        assert response.status_code == 200

    def test_api_recovered_by_country(self):
        response = self.app.get('/v1/recovered/fr')
        assert response.status_code == 200

    def test_api_deaths_by_country_and_province(self):
        response = self.app.get('/v1/deaths/CN')
        assert response.status_code == 200

    def test_api_confirmed_by_country_and_province(self):
        response = self.app.get('/v1/confirmed/cn')
        assert response.status_code == 200

    def test_api_all(self):
        response = self.app.get('/v1/all')
        assert response.status_code == 200

    def test_api_all_regrouped(self):
        response = self.app.get('/v1/all/grouped')
        assert response.status_code == 200

    def test_api_country_information(self):
        response = self.app.get('/v1/country/dz')
        assert response.status_code == 200

    def setUp(self):
        self.app = app.test_client()

    def tearDown(slef):
        pass
