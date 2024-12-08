import sqlite3
from flask import Blueprint, render_template, request

weather_bp = Blueprint('weather', __name__)

def get_db_connection():
    """
    Establish a connection to the SQLite database.
    Returns a connection object.
    """
    connection = sqlite3.connect('instance/database.db')  # Replace with your database file name
    connection.row_factory = sqlite3.Row  # To access rows like dictionaries
    return connection

@weather_bp.route('/weather-data')
def weather_data():
    # Establish database connection
    conn = get_db_connection()

    # Query all unique locations
    locations_query = 'SELECT DISTINCT location FROM WeatherData ORDER BY location'
    locations = [row['location'] for row in conn.execute(locations_query).fetchall()]

    # Get selected location from query parameter
    selected_location = request.args.get('location', 'all')

    # Build query based on location filter
    if selected_location and selected_location != 'all':
        query = 'SELECT * FROM WeatherData WHERE location = ? ORDER BY timestamp'
        weather_records = conn.execute(query, (selected_location,)).fetchall()
    else:
        query = 'SELECT * FROM WeatherData ORDER BY timestamp'
        weather_records = conn.execute(query).fetchall()

    # Close the database connection
    conn.close()

    # Render the template with data
    return render_template('weather-data.html', 
                           weather_records=weather_records, 
                           locations=locations,
                           selected_location=selected_location)
