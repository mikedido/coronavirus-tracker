from app import app
from app.utils import checker
from flask import jsonify, Blueprint
from app.services.jhu import get_all_data, get_all_data_by_category, get_data_country, get_all_data_grouped_by_country, get_data_country_by_category_by_province

version1 = Blueprint('v1', __name__, url_prefix='/v1')


@version1.route('/all')
def v1_api_all():
    """
    Get all the deaths, confirmed, recovered
    """
    return jsonify(get_all_data())


@version1.route('/all/grouped')
def v1_api_all_grouped():
    """
    Get all the deaths, confirmed, recovered grouped by country (for the country with many provinces like France, Canada)
    """
    return jsonify(get_all_data_grouped_by_country())


@version1.route('/recovered')
def v1_api_recovered():
    """
    Get all recovered by country
    """
    data = get_all_data_by_category('recovered')

    return jsonify(sorted(data['locations'], key=lambda k: k.get('total', 0), reverse=True))


@version1.route('/deaths')
def v1_api_deaths():
    """
    Get all deaths by country
    """
    data = get_all_data_by_category('deaths')

    return jsonify(sorted(data['locations'], key=lambda k: k.get('total', 0), reverse=True))


@version1.route('/confirmed')
def v1_api_confirmed():
    """
    get all confirmed by country
    """
    data = get_all_data_by_category('confirmed')

    return jsonify(sorted(data['locations'], key=lambda k: k.get('total', 0), reverse=True))


@version1.route('/<string:category>/<country_code>')
def v1_api_category_country(category, country_code):
    """
    Get all the historic confirmed, deaths or recovered by country and/or provinces
    """
    # Check the country code format
    if (not checker.country_code_format(country_code)):
        return ''

    if category.lower() not in ('confirmed', 'deaths', 'recovered'):
        return ''

    return get_data_country_by_category_by_province(category, country_code)


@version1.route('/country/<country_code>')
def v1_api_data_country(country_code):
    """
    Get all the country information about confirmed, deaths, recovered and also by provences
    """
    # Check the country code format
    if (not checker.country_code_format(country_code)):
        return ''

    return jsonify(get_data_country(country_code))
