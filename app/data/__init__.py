import requests
import csv
import dateutil.parser
from datetime import datetime
from cachetools import cached, TTLCache
from app.utils import countrycodes, date as date_util
from app.helpers import sorted_history_date, formated_date

"""
Base URL for fetching data.
"""
base_url = "https://raw.githubusercontent.com/CSSEGISandData/2019-nCoV/master/csse_covid_19_data/csse_covid_19_time_series/"

@cached(cache=TTLCache(maxsize=1024, ttl=3600))
def get_data(category):
    """
    Retrieves the data for the provided type. The data is cached for 1 hour.
    """
    category = category.lower()

    # URL to request data from.
    url = base_url + "time_series_covid19_%s_global.csv" % category

    request = requests.get(url)
    text    = request.text
    # Parse the CSV.
    data = list(csv.DictReader(text.splitlines()))
    # The normalized locations.
    locations = []

    for item in data:
        # Filter out all the dates.
        history = dict(filter(lambda element: date_util.is_date(element[0]), item.items()))
        #sorted date history
        history = sorted_history_date(formated_date(history))
        # Country for this location.
        country = item['Country/Region']
        # Latest data insert value.
        latest = list(history.values())[-1];
        # Normalize the item and append to locations.
        locations.append({
            # General info.
            'country':  country,
            'country_code': countrycodes.country_code(country),
            'province': item['Province/State'],
            # History.
            'history': history,
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

"""
Get all the data for different categories (confirmed, death and recovered)
"""
def get_all_data():
    # data
    data = []
    # Get all the categories.
    confirmed = get_data('confirmed')
    deaths    = get_data('deaths')
    recovered = get_data('recovered')

    # Add confirmed
    for element in confirmed['locations']:
        data.append({
            'country':  element['country'],
            'country_code': element['country_code'],
            'province': element['province'],
            'total': {
                'confirmed': element['total']
            }
        })

    # Add death
    for country in data:
        for element in deaths['locations']:
            if element['country'] == country['country']:
                country['total']['death'] = element['total']

    # Add recovered
    for country in data:
        for element in recovered['locations']:
            if element['country'] == country['country']:
                country['total']['recovered'] = element['total']

    return {
        'data': data,
        'last_updated': dateutil.parser.parse(confirmed["last_updated"]),
        # Latest.
        'latest': {
            'confirmed': confirmed['total'],
            'deaths':    deaths['total'],
            'recovered': recovered['total'],
        }
    }

"""
Get the country name by code
"""
def get_country_name(country_code):
    data = get_data('confirmed')

    for element in data['locations']:
        if element['country_code'].lower() == country_code.lower() :
            return element['country']

    return None