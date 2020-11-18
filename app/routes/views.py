import requests
from app import app
from app.helpers import sorted_data
from app.services import get_country_name
from flask import render_template, redirect, url_for, json
from app.services.jhu import get_data_country, get_all_data_grouped_by_country


@app.route('/')
def index():
    """
    The principal route of the website
    """
    data = get_all_data_grouped_by_country()
    return render_template(
        'dashboard.html',
        data=sorted(data['locations'], key=lambda entry: entry['total'].get('confirmed', 0), reverse=True),
        total_confirmed=data['latest']['confirmed'],
        total_deaths=data['latest']['deaths'],
        total_recovered=data['latest']['recovered'],
        total_active=data['latest']['active']
    )

@app.route('/<country_code>/')
def country_stats(country_code):
    """
    The dashboard charts (deaths, confirmed, recovered) of country country
    """
    # Get the country name
    country_name = get_country_name(country_code)
    if country_name is not None:
        # Get country info
        country_info = get_data_country(country_code)
        print(country_info['locations'][0]['total'])
        return render_template('country.html', country_code=country_code, country_name=country_name, country_info=country_info['locations'][0])
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(error):
    """
    Not exisiting route
    """
    return redirect(url_for('index'))
