from flask import Blueprint, render_template
from sqlalchemy.sql import text
from models import db
from flask import Blueprint, render_template, request
weather_bp = Blueprint('weather', __name__)

@weather_bp.route('/weather-data')
def weather_data():
    # Query all locations first
    locations_query = text('SELECT DISTINCT location FROM WeatherData ORDER BY location')
    locations = [loc[0] for loc in db.session.execute(locations_query).fetchall()]
    
    # Get selected location from query parameter
    selected_location = request.args.get('location', 'all')
    
    # Build query based on location filter
    if selected_location and selected_location != 'all':
        query = text('SELECT * FROM WeatherData WHERE location = :location ORDER BY timestamp')
        weather_records = db.session.execute(query, {'location': selected_location}).fetchall()
    else:
        query = text('SELECT * FROM WeatherData ORDER BY timestamp')
        weather_records = db.session.execute(query).fetchall()

    return render_template('weather-data.html', 
                         weather_records=weather_records, 
                         locations=locations,
                         selected_location=selected_location)