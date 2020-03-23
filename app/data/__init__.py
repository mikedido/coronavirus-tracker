import requests
import csv
from datetime import datetime
#from cachetools import cached, TTLCache
from app.utils import countrycodes, date as date_util
import re

"""
Base URL for fetching data.
"""
base_url = 'https://raw.githubusercontent.com/CSSEGISandData/2019-nCoV/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-%s.csv';

#@cached(cache=TTLCache(maxsize=1024, ttl=3600))
def get_data(category):
    """
    Retrieves the data for the provided type. The data is cached for 1 hour.
    """
    
    # Adhere to category naming standard.
    category = category.lower().capitalize();

    # Request the data
    request = requests.get(base_url % category)
    text    = request.text

    # Parse the CSV.
    data = list(csv.DictReader(text.splitlines()))

    # The normalized locations.
    locations = []

    #add country
    add_country = []

    for item in data:
        # Filter out all the dates.
        history = dict(filter(lambda element: date_util.is_date(element[0]), item.items()))
        #sorted date history
        history = sorted_history_date(history)

        # Country for this location.
        country = item['Country/Region']

        # Latest data insert value.
        latest = list(history.values())[-1];

        # Normalize the item and append to locations.
        if not country in add_country:
            add_country.append(country)

            locations.append({
                # General info.
                'country':  country,
                'country_code': countrycodes.country_code(country),
                'province': item['Province/State'],

                # Coordinates.
                'coordinates': {
                    'lat':  item['Lat'],
                    'long': item['Long'],
                },

                # History.
                'history': history,

                # Latest statistic.
                'latest': int(latest or 0),
            })

    # Latest total.
    latest = sum(map(lambda location: location['latest'], locations))

    # Return the final data.
    return {
        'locations': locations,
        'latest': latest,
        'last_updated': datetime.utcnow().isoformat() + 'Z',
        'source': 'https://github.com/ExpDev07/coronavirus-tracker-api',
    }

def get_sorted_data(data):
    data_tuple = data['locations']
    data_tuple = sorted(data_tuple, key=lambda k: k.get('total', 0), reverse=True)
    return {
        'data': data_tuple,
        'total': data['total']
    }

def get_new_data(category):
    """
    Retrieves the data for the provided type. The data is cached for 1 hour.
    """
    
    # Adhere to category naming standard.
    category = category.lower().capitalize();

    # Request the data
    request = requests.get(base_url % category)
    text    = request.text

    # Parse the CSV.
    data = list(csv.DictReader(text.splitlines()))

    # The normalized locations.
    locations = []

    #add country
    add_country = []

    for item in data:
        # Filter out all the dates.
        history = dict(filter(lambda element: date_util.is_date(element[0]), item.items()))

        # Country for this location.
        country = item['Country/Region']

        # Latest data insert value.
        latest = list(history.values())[-1];

        # Normalize the item and append to locations.
        if not country in add_country:
            add_country.append(country)

            locations.append({
                # General info.
                'country':  country,
                'country_code': countrycodes.country_code(country),
                'province': item['Province/State'],

                # Latest statistic.
                'total': int(latest or 0),
            })

    # Latest total.
    total = sum(map(lambda location: location['total'], locations))

    # Return the final data.
    return {
        'locations': locations,
        'total': total,
        'last_updated': datetime.utcnow().isoformat() + 'Z'
    }

def get_all_data():
    """
    Retrieves the data for the provided type. The data is cached for 1 hour.
    """
    #all category
    categories = ['', '', '']
    
    # Adhere to category naming standard.
    category = category.lower().capitalize();

    # Request the data
    request = requests.get(base_url % category)
    text    = request.text

    # Parse the CSV.
    data = list(csv.DictReader(text.splitlines()))

    # The normalized locations.
    locations = []

    #add country
    add_country = []

    for item in data:
        # Filter out all the dates.
        history = dict(filter(lambda element: date_util.is_date(element[0]), item.items()))

        # Country for this location.
        country = item['Country/Region']

        # Latest data insert value.
        latest = list(history.values())[-1];

        # Normalize the item and append to locations.
        if not country in add_country:
            add_country.append(country)

            locations.append({
                # General info.
                'country':  country,
                'country_code': countrycodes.country_code(country),
                'province': item['Province/State'],

                # Coordinates.
                'coordinates': {
                    'lat':  item['Lat'],
                    'long': item['Long'],
                },

                # History.
                'history': history,

                # Latest statistic.
                'latest': int(latest or 0),
            })

    # Latest total.
    latest = sum(map(lambda location: location['latest'], locations))

    # Return the final data.
    return {
        'locations': locations,
        'latest': latest,
        'last_updated': datetime.utcnow().isoformat() + 'Z',
        'source': 'https://github.com/ExpDev07/coronavirus-tracker-api',
    }

"""
Sorted data by date
"""
def sorted_history_date(data):
    data = formated_date(data)
    return dict(sorted(data.items(), key = lambda x:datetime.strptime(x[0], '%m/%d/%Y')))

"""
Formated date in the history
"""
def formated_date(data):
    new_data = {}
    for date in data :
        value = data[date]
        #first regex for days
        result = date.split('/')
        date = "{:02d}/{:02d}/{:2d}".format(int(result[0]), int(result[1]), int(result[2]))
        new_data[date+"20"] = value
    
    return new_data

"""
Get the country name by code
"""
def get_country_name(country_code):
    data = get_new_data('confirmed')

    for element in data['locations']:
        if element['country_code'].lower() == country_code.lower() :
            return element['country']

    return None