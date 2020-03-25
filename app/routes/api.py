from flask import Flask, render_template, redirect, url_for
from app.data import get_data, get_country_name, get_all_data
from flask import jsonify, json
import dateutil.parser
from app import app

"""
Get the recovered by country
"""
@app.route('/api/recovered')
def api_recovered():
    data = get_data('recovered')

    return jsonify(sorted(data['locations'], key=lambda k: k.get('total', 0), reverse=True))

"""
Get the deaths by country
"""
@app.route('/api/deaths')
def api_deaths():
    data = get_data('deaths')

    return jsonify(sorted(data['locations'], key=lambda k: k.get('total', 0), reverse=True))

"""
get the confirmed by country
"""
@app.route('/api/confirmed')
def api_confirmed():
    data = get_data('confirmed')

    return jsonify(sorted(data['locations'], key=lambda k: k.get('total', 0), reverse=True))

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
    
    return jsonify(get_all_data())