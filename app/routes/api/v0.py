from app import app
import dateutil.parser
from flask import jsonify
from flask import Blueprint
from app.helpers import data_country_by_province
from app.services import get_data, get_all_data, regrouped_by_country
"""
Version 0 of the API
"""

version0 = Blueprint('v0', __name__, url_prefix='/v0')

@version0.route('/recovered')
def api_recovered():
    """
    Get the recovered by country
    """
    data = get_data('recovered')

    return jsonify(sorted(data['locations'], key=lambda k: k.get('total', 0), reverse=True))


@version0.route('/deaths')
def api_deaths():
    """
    Get the deaths by country
    """
    data = get_data('deaths')

    return jsonify(sorted(data['locations'], key=lambda k: k.get('total', 0), reverse=True))


@version0.route('/confirmed')
def api_confirmed():
    """
    get the confirmed by country
    """
    data = get_data('confirmed')

    return jsonify(sorted(data['locations'], key=lambda k: k.get('total', 0), reverse=True))


@version0.route('/<string:category>/<country_code>/', defaults={'province_name': ''})
@version0.route('/<string:category>/<country_code>/<province_name>')
def api_confirmed_country(category, country_code, province_name):
    """
    Get all the historic confirmed, deaths or recovered by country and/or provinces
    """
    if category.lower() not in ('confirmed', 'deaths', 'recovered'):
        return ''

    data = get_data(category)
    data_country_all_province = []

    # By country and province
    for country in data['locations']:
        if country['country_code'] == country_code.upper() and country['province'].lower() == province_name.lower():
            return jsonify({
                'data': country['history'],
                'last_updated': dateutil.parser.parse(data['last_updated'])
            })

    # By country, so we must regrouped province
    for country in data['locations']:
        if country['country_code'] == country_code.upper():
            data_country_all_province.append(country['history'])

    return {
        'data': data_country_by_province(data_country_all_province),
        'last_updated': ''
    }

@version0.route('/all')
def api_all():
    """
    Get all the detah, confirmed, recovered
    """
    return jsonify(get_all_data())


@version0.route('/all/regrouped')
def api_all_regrouped_by_country():
    """
    Get all the detah, confirmed, recovered
    """
    return jsonify(regrouped_by_country(get_all_data()))
