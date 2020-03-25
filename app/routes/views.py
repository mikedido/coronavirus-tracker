from flask import Flask, render_template, redirect, url_for
from app import app
from app.data import get_data, get_new_data, get_sorted_data, get_country_name
from flask import jsonify, json
import dateutil.parser

"""
The principal route of the website
"""
@app.route('/')
def index():
    return render_template(
        'index.html', 
        confirmed=get_sorted_data(get_new_data('confirmed')),
        death=get_sorted_data(get_new_data('deaths')),
        recovered=get_sorted_data(get_new_data('recovered'))
    )

"""
The dashboard charts (deaths, confirmed, recovered) by country
"""
@app.route('/<country_code>')
def country_stats(country_code):
    #Get the country name
    country_name = get_country_name(country_code)
    if country_name != None:
        return render_template('dashboard.html', country_code=country_code,country_name=country_name)

    return redirect(url_for('index'))

"""
Not exisiting route
"""
@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for('index'))
