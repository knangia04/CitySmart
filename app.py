# import sqlite3
# from flask import Flask, render_template, request, redirect, url_for, flash, session
# from datetime import datetime
# import pytz

# app = Flask(__name__, static_folder='static')
# app.secret_key = 'your_secret_key'

# # Helper function to connect to the SQLite database
# def get_db_connection():
#     """
#     Establish a connection to the SQLite database.
#     Returns a connection object.
#     """
#     connection = sqlite3.connect('instance/database.db')  # Replace with your database file name
#     connection.row_factory = sqlite3.Row  # Access rows like dictionaries
#     return connection

# @app.route('/')
# def home():
#     return render_template('login-template.html')

# @app.route('/homepage')
# def homepage():
#     username = session.get('username', 'Guest')
#     location = session.get('location', 'UTC')

#     timezone = 'America/Los_Angeles'
#     current_time = datetime.now(pytz.timezone(timezone)).strftime('%I:%M:%S %p')

#     result = None  # Initialize result to handle errors
#     try:
#         # Establish database connection
#         conn = get_db_connection()
#         cursor = conn.cursor()

#         # Start transaction
#         cursor.execute("BEGIN TRANSACTION;")

#         # Query to get average weather stats
#         query = """
#             SELECT W.Location, 
#                    AVG(W.Temperature) AS AvgTemperature, 
#                    AVG(W.Humidity) AS AvgHumidity,
#                    AVG(P.FineParticulateMatter) AS AvgFineParticulateMatter, 
#                    AVG(P.OzoneLevel) AS AvgOzoneLevel
#             FROM WeatherData W
#             JOIN PollutionData P ON W.Location = P.Location
#             WHERE W.Location = ?
#             GROUP BY W.Location
#         """
#         cursor.execute(query, (location,))
#         result = cursor.fetchone()

#         # Commit transaction
#         conn.commit()

#     except Exception as e:
#         # Rollback in case of error
#         if conn:
#             conn.rollback()
#         flash(f"Error fetching weather stats: {str(e)}", "danger")
#     finally:
#         # Ensure connection is closed
#         if conn:
#             conn.close()

#     return render_template(
#         'homepage.html',
#         username=username,
#         location=location,
#         current_time=current_time,
#         avg_stats=result
#     )

# @app.route('/login', methods=['POST'])
# def login():
#     username = request.form.get('username')
#     password = request.form.get('password')

#     conn = get_db_connection()
#     cursor = conn.cursor()

#     try:
#         # Query the database for the user
#         cursor.execute("SELECT * FROM User WHERE username = ?", (username,))
#         user = cursor.fetchone()

#         if user and user['password'] == password:
#             flash('Login successful!', 'success')
#             session['username'] = user['username']
#             session['location'] = user['location']
#             return redirect(url_for('homepage'))
#         else:
#             flash('Invalid username or password', 'danger')
#     except Exception as e:
#         flash(f"Error during login: {str(e)}", 'danger')
#     finally:
#         conn.close()

#     return redirect(url_for('home'))

# @app.route('/signup', methods=['POST'])
# def signup():
#     email = request.form.get('email')
#     username = request.form.get('username')
#     password = request.form.get('password')
#     confirm_password = request.form.get('confirm-password')
#     location = request.form.get('location')

#     if password != confirm_password:
#         flash('Passwords do not match!', 'danger')
#         return redirect(url_for('home'))

#     conn = get_db_connection()
#     cursor = conn.cursor()

#     try:
#         # Check if email or username already exists
#         cursor.execute("SELECT * FROM User WHERE email = ?", (email,))
#         if cursor.fetchone():
#             flash('Email is already registered!', 'danger')
#             return redirect(url_for('home'))

#         cursor.execute("SELECT * FROM User WHERE username = ?", (username,))
#         if cursor.fetchone():
#             flash('Username is already taken!', 'danger')
#             return redirect(url_for('home'))

#         # Insert new user into the database
#         cursor.execute(
#             "INSERT INTO User (email, username, password, location) VALUES (?, ?, ?, ?)",
#             (email, username, password, location)
#         )
#         conn.commit()
#         flash('Account created successfully! Please log in.', 'success')
#     except Exception as e:
#         conn.rollback()
#         flash(f"Error during signup: {str(e)}", 'danger')
#     finally:
#         conn.close()

#     return redirect(url_for('home'))

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, flash, session
from config import Config
from models import db, User
from routes.user_routes import user_bp
from routes.settings_routes import settings_bp
import pandas as pd
from sqlalchemy.sql import text

from routes.weather_routes import weather_bp  # Import the weather blueprint
from routes.pollution_routes import pollution_bp
from routes.traffic_routes import traffic_bp

from datetime import datetime
import pytz
import weather_api

app = Flask(__name__, static_folder='static')
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)

# Register blueprints
app.register_blueprint(user_bp)
app.register_blueprint(weather_bp)  # Register the weather blueprint
app.register_blueprint(settings_bp)
app.register_blueprint(traffic_bp)
app.register_blueprint(pollution_bp)

# Root route serving login-template.html
@app.route('/')
def home():
    return render_template('login-template.html')


# Other routes (login, signup, etc.)
@app.route('/homepage')
def homepage():
    username = session.get('username', 'Guest')
    location = session.get('location', 'UTC')

    timezone = 'America/Los_Angeles'
    current_time = datetime.now(pytz.timezone(timezone)).strftime('%I:%M:%S %p')

    try:
        # Start transaction
        db.session.begin()
        
        query = text("""
            SELECT W.Location, 
                   AVG(W.Temperature) AS AvgTemperature, 
                   AVG(W.Humidity) AS AvgHumidity,
                   AVG(P.FineParticulateMatter) AS AvgFineParticulateMatter, 
                   AVG(P.OzoneLevel) AS AvgOzoneLevel
            FROM WeatherData W
            JOIN PollutionData P ON W.Location = P.Location
            WHERE W.Location = :location
            GROUP BY W.Location
        """)
        
        result = db.session.execute(query, {'location': location}).first()

        # Commit the transaction if successful
        db.session.commit()

    except Exception as e:
        # Rollback in case of an error
        db.session.rollback()
        flash(f"Error fetching weather stats: {str(e)}", "danger")
        result = None  # Handle error gracefully

    # Fetch current weather information
    curr_temp, curr_condition, curr_humidity, curr_wind = weather_api.getCurrWeather(location)

    return render_template(
        'homepage.html', 
        username=username, 
        location=location, 
        current_time=current_time, 
        avg_stats=result,
        curr_temp=curr_temp,
        curr_condition=curr_condition,
        curr_humidity=curr_humidity,
        curr_windspeed = curr_wind
    )
# def homepage():
#     username = session.get('username', 'Guest')
#     location = session.get('location', 'UTC')

#     timezone = 'America/Los_Angeles'
#     current_time = datetime.now(pytz.timezone(timezone)).strftime('%I:%M:%S %p')

#     try:
#         # Start transaction
#         db.session.begin()
        
#         query = text("""
#             SELECT W.Location, 
#                    AVG(W.Temperature) AS AvgTemperature, 
#                    AVG(W.Humidity) AS AvgHumidity,
#                    AVG(P.FineParticulateMatter) AS AvgFineParticulateMatter, 
#                    AVG(P.OzoneLevel) AS AvgOzoneLevel
#             FROM WeatherData W
#             JOIN PollutionData P ON W.Location = P.Location
#             WHERE W.Location = :location
#             GROUP BY W.Location
#         """)
        
#         result = db.session.execute(query, {'location': location}).first()

#         # Commit the transaction if successful
#         db.session.commit()

#     except Exception as e:
#         # Rollback in case of an error
#         db.session.rollback()
#         flash(f"Error fetching weather stats: {str(e)}", "danger")
#         result = None  # Handle error gracefully
#     curr_weather_info = weather_api.getCurrWeather(location)

#     return render_template(
#         'homepage.html', 
#         username=username, 
#         location=location, 
#         current_time=current_time, 
#         avg_stats=result
#     )

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        flash('Login successful!', 'success')
        session['username'] = user.username
        session['location'] = user.location
        return redirect(url_for('homepage'))
    else:
        flash('Invalid username or password', 'danger')
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

    if User.query.filter_by(email=email).first():
        flash('Email is already registered!', 'danger')
        return redirect(url_for('home'))
    if User.query.filter_by(username=username).first():
        flash('Username is already taken!', 'danger')
        return redirect(url_for('home'))

    # Create a new user
    new_user = User(username=username, email=email, password = password, location=location)

    db.session.add(new_user)
    db.session.commit()

    flash('Account created successfully! Please log in.', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
