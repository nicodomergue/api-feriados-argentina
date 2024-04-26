from flask import Flask, jsonify
from datetime import datetime
from get_feriados import *

app = Flask(__name__)


def group_dates_by_month(date_objects, year):
    grouped_dates = {}
#
    for date_obj in date_objects:
        date_str = date_obj['date']
        # Parse the date string into a datetime object
        date = datetime.strptime(date_str, '%d/%m/%Y')

        date_year = int(date.strftime('%Y'))

        if date_year != year:
            continue

        # Extract the month from the datetime object
        month_key = int(date.strftime('%m')) - 1
        # Group the dates by month
        if month_key not in grouped_dates:
            grouped_dates[month_key] = {}
        # grouped_dates[month_key].append(date_str)
        grouped_dates[month_key][date_str] = date_obj

    return grouped_dates


@app.route('/api/feriados/<int:year>', methods=['GET'])
def get_data(year):
    data = get_holidays_of_year(year)
    formatted_data = group_dates_by_month(data, year)
    return jsonify(formatted_data)


if __name__ == '__main__':
    app.run(debug=True)
