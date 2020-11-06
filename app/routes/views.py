from flask import render_template, redirect, url_for, json
from app import app
from app.services import get_data, get_country_name, get_all_data
from app.helpers import sorted_data
import requests


@app.route('/')
def index():
    """
    The principal route of the website
    """
    data = get_all_data()
    return render_template(
        'index.html',
        data=sorted(data['data'], key=lambda entry: entry['total'].get('confirmed', 0), reverse=True),
        total_confirmed=data['latest']['confirmed'],
        total_deaths=data['latest']['deaths'],
        total_recovered=data['latest']['recovered']
    )


@app.route('/<country_code>/', defaults={'province_name': ''})
@app.route('/<country_code>/<province_name>')
def country_stats(country_code, province_name):
    """
    The dashboard charts (deaths, confirmed, recovered) by country
    """
    # Get the country name
    country_name = get_country_name(country_code)
    if country_name is not None:
        return render_template('dashboard.html', country_code=country_code, country_name=country_name, province_name=province_name)
    return redirect(url_for('index'))


@app.route('/histo/<country_code>/', defaults={'province_name': ''})
@app.route('/histo/<country_code>/<province_name>')
def country_stats_histogramme(country_code, province_name):
    """
    The dashboard charts (deaths, confirmed, recovered) by country
    """
    # Get the country name
    country_name = get_country_name(country_code)
    if country_name is not None:
        return render_template('histogramme.html', country_code=country_code, country_name=country_name, province_name=province_name)
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(error):
    """
    Not exisiting route
    """
    return redirect(url_for('index'))
