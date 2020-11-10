from app.services.jhu import get_all_data, get_all_data_by_category, get_data_country, get_all_data_grouped_by_country
from flask import jsonify
from app import app
from flask import Blueprint

version1 = Blueprint('v1', __name__, url_prefix='/v1')

@app.route('/v1/all')
def v1_api_all():
    """
    Get all the deaths, confirmed, recovered
    """
    return jsonify(get_all_data())

@app.route('/v1/all/grouped')
def v1_api_all_grouped():
    """
    Get all the deaths, confirmed, recovered grouped by country (for the country with many provinces like France, Canada)
    """
    return jsonify(get_all_data_grouped_by_country())

@app.route('/v1/recovered')
def v1_api_recovered():
    """
    Get all recovered by country
    """
    data = get_all_data_by_category('recovered')

    return jsonify(sorted(data['locations'], key=lambda k: k.get('total', 0), reverse=True))


@app.route('/v1/deaths')
def v1_api_deaths():
    """
    Get all deaths by country
    """
    data = get_all_data_by_category('deaths')

    return jsonify(sorted(data['locations'], key=lambda k: k.get('total', 0), reverse=True))


@app.route('/v1/confirmed')
def v1_api_confirmed():
    """
    get all confirmed by country
    """
    data = get_all_data_by_category('confirmed')

    return jsonify(sorted(data['locations'], key=lambda k: k.get('total', 0), reverse=True))


@app.route('/v1/<string:category>/<country_code>/', defaults={'province_name': ''})
@app.route('/v1/<string:category>/<country_code>/<province_name>')
def v1_api_category_country(category, country_code, province_name):
    """
    Get all the historic confirmed, deaths or recovered by country and/or provinces
    """
    if category.lower() not in ('confirmed', 'deaths', 'recovered'):
        return ''

    data = get_all_data(category)
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

    return data_country_by_province(data_country_all_province, dateutil.parser.parse(data['last_updated']))


@app.route('/v1/country/<country_code>/', defaults={'province_name': ''})
@app.route('/v1/country/<country_code>/<province_name>')
def v1_api_data_country(country_code, province_name):
    
    return jsonify(get_data_country(country_code, province_name))