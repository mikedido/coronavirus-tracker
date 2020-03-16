from flask import Flask, render_template
from .data import get_data, get_new_data, get_sorted_data
from flask import jsonify, json

app = Flask(__name__)

@app.route('/')
def index():
    print(get_sorted_data(get_new_data('confirmed')))
    return render_template(
        'index.html', 
        confirmed=get_sorted_data(get_new_data('confirmed')),
        death=get_sorted_data(get_new_data('deaths')),
        recovered=get_sorted_data(get_new_data('recovered'))
    )

@app.route('/api/recovered')
def api_recovered():
    data = get_new_data('recovered')
    data_tuple = data['locations']
    return jsonify(sorted(data_tuple, key=lambda k: k.get('total', 0), reverse=True))

@app.route('/api/deaths')
def api_deaths():
    data = get_new_data('deaths')
    data_tuple = data['locations']
    return jsonify(sorted(data_tuple, key=lambda k: k.get('total', 0), reverse=True))

@app.route('/api/confirmed')
def api_confirmed():
    data = get_new_data('confirmed')
    data_tuple = data['locations']
    return jsonify(sorted(data_tuple, key=lambda k: k.get('total', 0), reverse=True))

#get the resume of all (detah)
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
        # Latest.
        'latest': {
            'confirmed': confirmed['total'],
            'deaths':    deaths['total'],
            'recovered': recovered['total'],
        }
    })
    
"""
@app.route('/all')
def all():
    # Get all the categories.
    confirmed = get_data('confirmed')
    deaths    = get_data('deaths')
    recovered = get_data('recovered')

    return jsonify({
        # Data.
        'confirmed': confirmed,
        'deaths':    deaths,
        'recovered': recovered,

        # Latest.
        'latest': {
            'confirmed': confirmed['latest'],
            'deaths':    deaths['latest'],
            'recovered': recovered['latest'],
        }
    })
"""

if __name__== "__main__":
    app.run() 
