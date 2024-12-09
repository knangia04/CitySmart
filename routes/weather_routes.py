from flask import Blueprint, render_template, request, flash
import sqlite3

weather_bp = Blueprint('weather', __name__)

@weather_bp.route('/weather-data')
def weather_data():
    try:
        conn = sqlite3.connect('instance/database.db')
        cursor = conn.cursor()

        # Query all locations
        cursor.execute("SELECT DISTINCT location FROM WeatherData ORDER BY location")
        locations = [row[0] for row in cursor.fetchall()]

        # Get selected location from query parameter
        selected_location = request.args.get('location', 'all')

        # Build query based on location filter
        if selected_location and selected_location != 'all':
            cursor.execute("SELECT * FROM WeatherData WHERE location = ? ORDER BY timestamp", (selected_location,))
        else:
            cursor.execute("SELECT * FROM WeatherData ORDER BY timestamp")
        
        weather_records = cursor.fetchall()

    except sqlite3.Error as e:
        flash(f"Error fetching weather data: {str(e)}", "danger")
        weather_records = []
        locations = []
        selected_location = 'all'

    finally:
        conn.close()

    return render_template(
        'weather-data.html',
        weather_records=weather_records,
        locations=locations,
        selected_location=selected_location
    )
