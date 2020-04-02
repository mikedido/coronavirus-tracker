from app.services import get_data, get_all_data, regrouped_by_country
from flask import jsonify
import dateutil.parser
from app import app


@app.route('/api/recovered')
def api_recovered():
    """
    Get the recovered by country
    """
    data = get_data('recovered')

    return jsonify(sorted(data['locations'], key=lambda k: k.get('total', 0), reverse=True))


@app.route('/api/deaths')
def api_deaths():
    """
    Get the deaths by country
    """
    data = get_data('deaths')

    return jsonify(sorted(data['locations'], key=lambda k: k.get('total', 0), reverse=True))


@app.route('/api/confirmed')
def api_confirmed():
    """
    get the confirmed by country
    """
    data = get_data('confirmed')

    return jsonify(sorted(data['locations'], key=lambda k: k.get('total', 0), reverse=True))


@app.route('/api/recovered/<country_code>/', defaults={'province_name': ''})
@app.route('/api/recovered/<country_code>/<province_name>')
def api_recovered_country(country_code, province_name):
    """
    Get all the historic recovered by country
    """
    data = get_data('recovered')

    for country in data['locations']:

        if country['country_code'] == country_code.upper() and country['province'] == province_name:
            return jsonify({
                'data': country['history'],
                'last_updated': dateutil.parser.parse(data['last_updated'])
            })
    else:
        return jsonify({
            'data': '',
            'last_updated': ''
        })


@app.route('/api/deaths/<country_code>/', defaults={'province_name': ''})
@app.route('/api/deaths/<country_code>/<province_name>')
def api_deaths_country(country_code, province_name):
    """
    Get all the historic deaths by country
    """
    data = get_data('deaths')

    for country in data['locations']:
        if country['country_code'] == country_code.upper() and country['province'] == province_name:

            return jsonify({
                'data': country['history'],
                'last_updated': dateutil.parser.parse(data['last_updated'])
            })
    else:
        return jsonify({
            'data': '',
            'last_updated': ''
        })


@app.route('/api/confirmed/<country_code>/', defaults={'province_name': ''})
@app.route('/api/confirmed/<country_code>/<province_name>')
def api_confirmed_country(country_code, province_name):
    """
    Get all the historic confirmed by country
    """
    data = get_data('confirmed')

    for country in data['locations']:

        if country['country_code'] == country_code.upper() and country['province'].lower() == province_name.lower():

            return jsonify({
                'data': country['history'],
                'last_updated': dateutil.parser.parse(data['last_updated'])
            })
    else:
        return jsonify({
            'data': '',
            'last_updated': ''
        })


@app.route('/api/all')
def api_all():
    """
    Get all the detah, confirmed, recovered
    """
    return jsonify(get_all_data())


@app.route('/api/all/regrouped')
def api_all_regrouped_by_country():
    """
    Get all the detah, confirmed, recovered
    """
    return jsonify(regrouped_by_country(get_all_data()))
