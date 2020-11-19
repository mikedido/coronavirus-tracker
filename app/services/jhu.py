"""
Johns Hopkins University Center for Systems Science and Engineering (JHU CSSE)
"""
from .request import Request
import dateutil.parser
from datetime import datetime, timedelta
from cachetools import cached, TTLCache
from app.helpers import sorted_history_date, formated_date, data_country_by_province
from app.utils import countrycodes, date as date_util


request = Request()

@cached(cache=TTLCache(maxsize=1024, ttl=3600))
def get_all_data_by_category(category):
    """
    Get all the data of all the countries by category. There is three category (confirmed | death | recovered)
    """
    data = request.get_data_time_series(category)
    # The normalized locations.
    locations = []

    for item in data:
        # Filter out all the dates.
        history = dict(filter(lambda element: date_util.is_date(element[0]), item.items()))
        # Sorted date history
        history = sorted_history_date(formated_date(history))
        # Country for this location.
        country = item['Country/Region']
        # Latest data insert value.
        latest = list(history.values())[-1];
        # Normalize the item and append to locations.
        locations.append({
            # General info.
            'country': country,
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


@cached(cache=TTLCache(maxsize=1024, ttl=3600))
def get_data_country_by_category_by_province(category, country_code):
    """
    Get all the data of a country by category. There is three category (confirmed | death | recovered)
    """
    data = request.get_data_time_series(category)
    # The normalized locations.
    locations = []

    for item in data:
        if country_code.upper() == countrycodes.country_code(item['Country/Region']):
            # Filter out all the dates.
            history = dict(filter(lambda element: date_util.is_date(element[0]), item.items()))
            # Sorted date history
            history = sorted_history_date(formated_date(history))
            # Country for this location.
            country = item['Country/Region']
            # Latest data insert value.
            latest = list(history.values())[-1];
            # Normalize the item and append to locations.
            locations.append({
                # General info.
                'country': country,
                'country_code': countrycodes.country_code(country),
                'province': item['Province/State'],
                # History.
                'history': history,
                # Latest statistic.
                'total': int(latest or 0),
            })
    
    #check if the country without province exist
    data_country_all_province = []

    # By country and province
    for country in locations:
        if country['country_code'] == country_code.upper() and country['province'] == '':
            return {
                'data': country['history'],
                'country': country['country'],
                'country_code': country['country_code'],
                'province': country['province'],
                'last_updated': ''
            }
    #otherwise regrouped all provinces of the country
    for country in locations:
        if country['country_code'] == country_code.upper():
            data_country_all_province.append(country['history'])
    
    return {
        'data': data_country_by_province(data_country_all_province),
        'country': country['country'],
        'country_code': country['country_code'],
        'province': '',
        'last_updated': ''
    }


@cached(cache=TTLCache(maxsize=1024, ttl=3600))
def get_all_data():
    """
    Get all the data information (death, confirmed, recovered,) of each country.
    """
    data = request.get_data_daily_reports()
    locations = []

    for item in data:
        locations.append({
            # General info.
            'country': item['Country_Region'],
            'country_code': countrycodes.country_code(item['Country_Region']),
            'province': item['Province_State'],
            'total' : {
                'confirmed' : item['Confirmed'],
                'deaths' : item['Deaths'],
                'recovered' : item['Recovered'],
                'active' : item['Active'],
                'Incident_Rate' : item['Incident_Rate'],
                'Case_Fatality_Ratio' : item['Case_Fatality_Ratio']
            }
        })

    return {
        'locations': locations,
        'last_updated': datetime.utcnow().isoformat() + 'Z'
    }


def get_data_country(country_code):
    """
    Get the data information (death, confirmed, recovered, ) of a country and theirs province.
    """
    data = request.get_data_daily_reports()

    locations = [
        {
            'country': '',
            'country_code': '',
            'population': get_population_by_county(country_code.upper()),
            'total' : {
                'confirmed' : '',
                'deaths' : '',
                'recovered' : '',
                'active' : '',
                'Incident_Rate' : '',
                'Case_Fatality_Ratio' : ''
            },
            'provinces': []
        }
    ]
    provinces = []

    for item in data:
        if countrycodes.country_code(item['Country_Region']) == country_code.upper() and item['Province_State'] == '':
            locations[0]['country'] = item['Country_Region']
            locations[0]['country_code'] = countrycodes.country_code(item['Country_Region'])
            locations[0]['total']['confirmed'] = item['Confirmed']
            locations[0]['total']['deaths'] = item['Deaths']
            locations[0]['total']['recovered'] = item['Recovered']
            locations[0]['total']['active'] = item['Active']
            locations[0]['total']['Incident_Rate'] = item['Incident_Rate']
            locations[0]['total']['Case_Fatality_Ratio'] = item['Case_Fatality_Ratio']
        # Add the provinces info to the country mother
        if countrycodes.country_code(item['Country_Region']) == country_code and item['Province_State'] != '':
            locations[0]['country'] = item['Country_Region']
            locations[0]['country_code'] = countrycodes.country_code(item['Country_Region'])
            provinces.append({
                'name': item['Province_State'],
                'administration': item['Admin2'],
                #'population': get_population_by_province(item['Province_State'], item['Admin2']),
                'total' : {
                    'confirmed' : item['Confirmed'],
                    'deaths' : item['Deaths'],
                    'recovered' : item['Recovered'],
                    'active' : item['Active'],
                    'Incident_Rate' : item['Incident_Rate'],
                    'Case_Fatality_Ratio' : item['Case_Fatality_Ratio']
                }
            })

    #add all the provinces
    locations[0]['provinces'] = provinces
    
    #check the global result of the country
    if locations[0]['total']['confirmed'] == '':
        locations[0]['total']['confirmed'] = sum(int(province['total']['confirmed']) for province in locations[0]['provinces'])
        locations[0]['total']['deaths'] = sum(int(province['total']['deaths']) for province in locations[0]['provinces'])
        locations[0]['total']['active'] = sum(int(province['total']['active']) for province in locations[0]['provinces'] if province['total']['active'] != '')
        locations[0]['total']['recovered'] = sum(int(province['total']['recovered']) for province in locations[0]['provinces'])
    
    #add population for provinces
    #ouverture du fichier
    data = request.get_data_info_country()
    for province in locations[0]['provinces']:
        province['population'] = get_population_by_province(data, province['name'], province['administration'])

    #result
    return {
        'locations': locations,
        'last_updated': datetime.utcnow().isoformat() + 'Z'
    }

@cached(cache=TTLCache(maxsize=1024, ttl=3600))
def get_all_data_grouped_by_country():
    """
    Get all the data information (death, confirmed, recovered,) grouped by country (Many country have many provinces).
    """
    data = request.get_data_daily_reports()
    
    locations = []
    country_added = {}
    index = 0
    total_confirmed = 0
    total_deaths = 0
    total_recovered = 0
    

    for item in data:
        # country/province exist
        country_code = countrycodes.country_code(item['Country_Region'])

        if not country_code in country_added or country_code == 'XX':
            locations.append({
                'country': item['Country_Region'],
                'country_code': country_code,
                'total' : {
                    'confirmed' : int(item['Confirmed']),
                    'deaths' : int(item['Deaths']),
                    'recovered' : int(item['Recovered']),
                    'active' : ('0' if item['Active'] == '' else int(item['Active']))
                }
            })
            country_added[country_code] = index
            index +=1
        else:
            locations[country_added[country_code]]['total']['confirmed'] += int(item['Confirmed'])
            locations[country_added[country_code]]['total']['recovered'] += int(item['Recovered'])
            locations[country_added[country_code]]['total']['active'] += (0 if item['Active'] == '' else int(item['Active']))
            locations[country_added[country_code]]['total']['deaths'] += int(item['Deaths'])

        total_confirmed += int(item['Confirmed'])
        total_deaths += int(item['Deaths'])
        total_recovered += int(item['Recovered'])


    return {
        'locations': locations,
        'latest': {
            'confirmed': total_confirmed,
            'deaths': total_deaths,
            'recovered': total_recovered,
            'active': total_confirmed - total_deaths - total_recovered,
        },
        'last_updated': datetime.utcnow().isoformat() + 'Z'
    }


def get_population_by_county(country_code):
    """
    Get the population of a country by country code
    """
    data = request.get_data_info_country()

    for item in data:
        if item['iso2'] == country_code.upper():
            return item['Population']

    return ''

def get_population_by_province(data, province_name, adminitration):
    """
    Get the population of a country by 
    """
    for item in data:
        if item['Province_State'] == province_name and item['Admin2']== adminitration:
            return item['Population']

    return ''