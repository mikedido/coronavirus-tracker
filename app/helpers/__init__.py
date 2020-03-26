import dateutil.parser
from datetime import datetime

"""
Sorted data by date
"""
def sorted_history_date(data):

    return dict(sorted(data.items(), key = lambda x:datetime.strptime(x[0], '%m/%d/%Y')))

"""
Formated date in the history
"""
def formated_date(data):
    data_formated = {}

    for date in data :
        splited_date = date.split('/')
        date_formated = "{:02d}/{:02d}/{:2d}".format(int(splited_date[0]), int(splited_date[1]), int(splited_date[2]))
        data_formated[date_formated+"20"] = data[date]
    
    return data_formated

"""
Sorted data by date desc
"""
def sorted_data(data, reversed):
    data_tuple = data['locations']
    data_tuple = sorted(data_tuple, key=lambda k: k.get('total', 0), reverse=reversed)
    
    return {
        'data': data_tuple,
        'total': data['total']
    }