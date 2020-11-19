import unittest
from app import app
from app.services.request import Request

class TestRequest(unittest.TestCase):

    def test_get_data_info_country(self):
        self.assertTrue(self.request.get_data_info_country())
    
    def test_get_data_time_series_confirmed(self):
        self.assertTrue(self.request.get_data_time_series('confirmed'))
    
    def test_get_data_time_series_recovered(self):
        self.assertTrue(self.request.get_data_time_series('recovered'))

    def test_get_data_time_series_deaths(self):
        self.assertTrue(self.request.get_data_time_series('deaths'))

    def test_get_data_daily_reports(self):
        self.assertTrue(self.request.get_data_daily_reports())

    def setUp(self):
        self.app = app.test_client()
        self.request = Request()