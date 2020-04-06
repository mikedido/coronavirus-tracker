import unittest
from app import app
from app import helpers


class TestHelpers(unittest.TestCase):

    def test_sorted_history_date(self):
        data = {
            '01/06/2020': 0,
            '01/01/2020': 1,
            '01/16/2020': 67,
            '01/13/2020': 6,
            '01/09/2020': 8,
            '01/22/2020': 78
        }
        expected_data = {
            '01/01/2020': 1,
            '01/06/2020': 0,
            '01/09/2020': 8,
            '01/13/2020': 6,
            '01/16/2020': 67,
            '01/22/2020': 78
        }

        self.assertEqual(helpers.sorted_history_date(data), expected_data)

    def test_formated_date(self):
        data = {
            '1/6/20': 0,
            '1/1/20': 1,
            '11/16/20': 67
        }
        expected_data = {
            '01/06/2020': 0,
            '01/01/2020': 1,
            '11/16/2020': 67
        }
        self.assertEqual(helpers.formated_date(data), expected_data)

    def test_sorted_data(self):
        pass

    def test_data_country_by_province(self):
        pass

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass
