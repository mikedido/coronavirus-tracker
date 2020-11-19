import unittest
from app import app
from app.services.jhu import get_all_data, get_data_country

class TestJhu(unittest.TestCase):

    def test_get_all_data(self):
        self.assertEqual(len(get_all_data().keys()), 2)
        self.assertEqual(len(get_all_data()['locations'][0].keys()), 4)
        self.assertEqual(len(get_all_data()['locations'][0]['total'].keys()), 6)

    def test_get_data_country(self):
        self.assertEqual(len(get_data_country('fr').keys()), 2)
        self.assertEqual(len(get_data_country('fr')['locations'][0].keys()), 5)
        self.assertEqual(len(get_data_country('fr')['locations'][0]['total'].keys()), 6)

    def setUp(self):
        self.app = app.test_client()
