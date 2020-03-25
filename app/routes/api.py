from flask import Flask, render_template, redirect, url_for
from app import app
from app.data import get_data, get_new_data, get_sorted_data, get_country_name
from flask import jsonify, json
import dateutil.parser

"""
Get the recovered by country
"""
@app.route('/api/recovered')
def api_recovered():
    data = get_new_data('recovered')
    data_tuple = data['locations']
    return jsonify(sorted(data_tuple, key=lambda k: k.get('total', 0), reverse=True))

"""
Get the deaths by country
"""
@app.route('/api/deaths')
def api_deaths():
    data = get_new_data('deaths')
    data_tuple = data['locations']
    return jsonify(sorted(data_tuple, key=lambda k: k.get('total', 0), reverse=True))

"""
get the confirmed by country
"""
@app.route('/api/confirmed')
def api_confirmed():
    data = get_new_data('confirmed')
    data_tuple = data['locations']
    return jsonify(sorted(data_tuple, key=lambda k: k.get('total', 0), reverse=True))

"""
Get all the historic recovered by country
"""
@app.route('/api/recovered/<country_code>')
def api_recovered_country(country_code):
    data = get_data('recovered')
    for country in data['locations']:
        if country['country_code'] == country_code.upper():
            return jsonify({
                'data' : country['history'],
                'last_updated': dateutil.parser.parse(data['last_updated'])
            })
    else:
        return 'No found'

"""
Get all the historic deaths by country
"""
@app.route('/api/deaths/<country_code>')
def api_deaths_country(country_code):
    data = get_data('deaths')
    for country in data['locations']:
        if country['country_code'] == country_code.upper():
            return jsonify({
                'data' : country['history'],
                'last_updated': dateutil.parser.parse(data['last_updated'])
            })
    else:
        return 'No found'

"""
Get all the historic confirmed by country
"""
@app.route('/api/confirmed/<country_code>')
def api_confirmed_country(country_code):
    data = get_data('confirmed')
    for country in data['locations']:
        if country['country_code'] == country_code.upper():
            return jsonify({
                'data' : country['history'],
                'last_updated': dateutil.parser.parse(data['last_updated'])
            })
    else:
        return 'No found'

"""
Get all the detah, confirmed, recovered
"""
@app.route('/api/all')
def api_all():
    # data
    data = []

    # Get all the categories.
    confirmed = get_new_data('confirmed')
    deaths    = get_new_data('deaths')
    recovered = get_new_data('recovered')

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

    return jsonify({
        'data': data,
        'last_updated': dateutil.parser.parse(confirmed["last_updated"]),
        # Latest.
        'latest': {
            'confirmed': confirmed['total'],
            'deaths':    deaths['total'],
            'recovered': recovered['total'],
        }
    })