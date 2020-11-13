import csv
import requests
from datetime import datetime, timedelta

"""
Base URL for fetching data.
"""
DATA_TIME_SERIES_BASE_URL = "https://raw.githubusercontent.com/CSSEGISandData/2019-nCoV/master/csse_covid_19_data/csse_covid_19_time_series/"
INFO_COUNTRY_URL = "https://raw.githubusercontent.com/CSSEGISandData/2019-nCoV/master/csse_covid_19_data/UID_ISO_FIPS_LookUp_Table.csv"
DATA_DAILY_REPORTS_BASE_URL = "https://raw.githubusercontent.com/CSSEGISandData/2019-nCoV/master/csse_covid_19_data/csse_covid_19_daily_reports/"

class Request:
    """
    Class Request to JHU CSV files
    """
    def __init__(self):
        self.date = (datetime.now() - timedelta(days=1)).strftime('%m-%d-%Y')

    def get_data_time_series(self, category):
        """
        Get all the data by category confirmed | deaths | recovered
        """
        category = category.lower()
        return self.get_request(DATA_TIME_SERIES_BASE_URL + "time_series_covid19_%s_global.csv" % category)
        
    def get_data_info_country(self):
        """
        Get all the countries informations
        """
        return self.get_request(INFO_COUNTRY_URL)

    def get_data_daily_reports(self):
        """
        Get all the confirmed | deaths | recovered daily by country 
        """
        return self.get_request(DATA_DAILY_REPORTS_BASE_URL + self.date + '.csv')


    def get_request(self, url):
        """
        """
        request = requests.get(url)
        text = request.text

        return list(csv.DictReader(text.splitlines()))