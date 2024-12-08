import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from config import Config
from models import init_db, add_user, get_user_by_username, check_password
from datetime import datetime
import pytz
import sqlite3

# from routes.user_routes import user_bp
from routes.settings_routes import settings_bp
from routes.weather_routes import weather_bp
from routes.pollution_routes import pollution_bp
from routes.traffic_routes import traffic_bp



app = Flask(__name__, static_folder='static')
app.instance_path = os.path.abspath('./instance')
app.config['db'] = os.path.join(app.instance_path, 'database.db')
app.config.from_object(Config)
os.makedirs(app.instance_path, exist_ok=True)

# Initialize extensions
init_db()

# Register blueprints
app.register_blueprint(weather_bp)
app.register_blueprint(settings_bp)
app.register_blueprint(traffic_bp)
app.register_blueprint(pollution_bp)

# Root route serving login-template.html
@app.route('/')
def home():
    return render_template('login-template.html')



@app.route('/homepage')
def homepage():
    username = session.get('username', 'Guest')
    location = session.get('location', 'UTC')

    timezone = 'America/Los_Angeles'
    current_time = datetime.now(pytz.timezone(timezone)).strftime('%I:%M:%S %p')

    avg_stats = None
    try:
        conn = sqlite3.connect('instance/database.db')
        cursor = conn.cursor()

        # Execute advanced query
        cursor.execute("""
            SELECT W.Location, 
                   AVG(W.Temperature) AS AvgTemperature, 
                   AVG(W.Humidity) AS AvgHumidity,
                   AVG(P.FineParticulateMatter) AS AvgFineParticulateMatter, 
                   AVG(P.OzoneLevel) AS AvgOzoneLevel
            FROM WeatherData W
            JOIN PollutionData P ON W.Location = P.Location
            WHERE W.Location = ?
            GROUP BY W.Location
        """, (location,))
        result = cursor.fetchone()
        if result:
            avg_stats = {
                'Location': result[0],
                'AvgTemperature': result[1],
                'AvgHumidity': result[2],
                'AvgFineParticulateMatter': result[3],
                'AvgOzoneLevel': result[4]
            }

    except sqlite3.Error as e:
        flash(f"Error fetching weather stats: {str(e)}", "danger")
        result = None
    finally:
        conn.close()

    return render_template(
        'homepage.html',
        username=username,
        location=location,
        current_time=current_time,
        avg_stats=avg_stats
    )

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = get_user_by_username(username)
    if user and check_password(username, password):
        flash('Login successful!', 'success')
        session['username'] = user[1]  # Username
        session['location'] = user[4]  # Location
        return redirect(url_for('homepage'))
    else:
        flash('Invalid username or password.', 'danger')
        return redirect(url_for('home'))


@app.route('/signup', methods=['POST'])
def signup():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm-password')
    location = request.form.get('location')

    if password != confirm_password:
        flash('Passwords do not match!', 'danger')
        return redirect(url_for('home'))

    # Check if username or email already exists
    if get_user_by_username(username):
        flash('Username is already taken!', 'danger')
        return redirect(url_for('home'))

    try:
        add_user(username, email, password, location)
        flash('Account created successfully! Please log in.', 'success')
    except sqlite3.Error as e:
        flash(f'Error creating account: {str(e)}', 'danger')

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)