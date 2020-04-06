import unittest
from app import app
from app import services


class TestHelpers(unittest.TestCase):

    def test_get_data_keys_number(self):
        self.assertEqual(len(services.get_data('confirmed').keys()), 3)
        self.assertEqual(len(services.get_data('confirmed')['locations'][0].keys()), 5)

    def test_get_data_keys_name(self):
        expect_key = {'locations', 'total', 'last_updated'}
        expect_location_keys = {'country', 'country_code', 'province', 'history', 'total'}

        self.assertEqual(services.get_data('confirmed').keys(), expect_key)
        self.assertEqual(services.get_data('confirmed')['locations'][0].keys(), expect_location_keys)

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass
