from flask import Flask, render_template, request, redirect, url_for, flash, session
from config import Config
from models import db, User
from routes.user_routes import user_bp

from weather_routes import weather_bp  # Import the weather blueprint

from datetime import datetime
import pytz


app = Flask(__name__, static_folder='static')
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)

# Register blueprints
app.register_blueprint(user_bp)
app.register_blueprint(weather_bp)  # Register the weather blueprint

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

    return render_template('homepage.html', username=username, location=location, current_time=current_time)




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


# Run the application
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Initialize the database tables
    app.run(debug=True)

# from flask import Flask, render_template, request, redirect, url_for, flash
# from config import Config
# from models import db, User
# from routes.user_routes import user_bp
# from sqlalchemy.sql import text

# app = Flask(__name__, static_folder='static')
# app.config.from_object(Config)

# # Initialize extensions
# db.init_app(app)

# # Register blueprints
# app.register_blueprint(user_bp)

# # Root route serving login-template.html
# @app.route('/')
# def home():
#     return render_template('login-template.html')


# @app.route('/login', methods=['POST'])
# def login():
#     username = request.form.get('username')
#     password = request.form.get('password')

#     # Check if the user exists
#     user = User.query.filter_by(username=username).first()
#     if user and user.password == password:
#         flash('Login successful!', 'success')
#         return redirect(url_for('home'))
#     else:
#         flash('Invalid username or password', 'danger')
#         return redirect(url_for('home'))
    

# # Route to handle signup
# @app.route('/signup', methods=['POST'])
# def signup():
#     email = request.form.get('email')
#     username = request.form.get('username')
#     password = request.form.get('password')
#     confirm_password = request.form.get('confirm-password')

#     # Validate passwords match
#     if password != confirm_password:
#         flash('Passwords do not match!', 'danger')
#         return redirect(url_for('home'))

#     # Check if email or username already exists
#     if User.query.filter_by(email=email).first():
#         flash('Email is already registered!', 'danger')
#         return redirect(url_for('home'))
#     if User.query.filter_by(username=username).first():
#         flash('Username is already taken!', 'danger')
#         return redirect(url_for('home'))

#     # Create a new user
#     new_user = User(username=username, email=email)
#     new_user.set_password(password)
#     db.session.add(new_user)
#     db.session.commit()

#     flash('Account created successfully! Please log in.', 'success')
#     return redirect(url_for('home'))


# # Route to display WeatherData table
# @app.route('/weather-data')
# def weather_data():
#     # Query the WeatherData table using text()
#     query = text('SELECT * FROM WeatherData')
#     weather_records = db.session.execute(query).fetchall()

#     # Render the data on a template
#     return render_template('weather-data.html', weather_records=weather_records)
# # def weather_data():
# #     # Query the WeatherData table
# #     weather_records = db.session.execute('SELECT * FROM WeatherData').fetchall()

# #     # Render the data on a template
# #     return render_template('weather-data.html', weather_records=weather_records)


# # Run the application
# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()  # Initialize the database tables
#     app.run(debug=True)

# from flask import Flask, render_template, request, redirect, url_for, flash
# from config import Config
# from models import db, User
# from routes.user_routes import user_bp

# app = Flask(__name__, static_folder='static')
# app.config.from_object(Config)

# # Initialize extensions
# db.init_app(app)

# # Register blueprints
# app.register_blueprint(user_bp)

# # Root route serving login-template.html
# @app.route('/')
# def home():
#     return render_template('login-template.html')


# @app.route('/login', methods=['POST'])
# def login():
#     username = request.form.get('username')
#     password = request.form.get('password')

#     # Check if the user exists
#     user = User.query.filter_by(username=username).first()
#     if user and user.password == password:
#         flash('Login successful!', 'success')
#         return redirect(url_for('home'))
#     else:
#         flash('Invalid username or password', 'danger')
#         return redirect(url_for('home'))
    

# # Route to handle signup
# @app.route('/signup', methods=['POST'])
# def signup():
#     email = request.form.get('email')
#     username = request.form.get('username')
#     password = request.form.get('password')
#     confirm_password = request.form.get('confirm-password')

#     # Validate passwords match
#     if password != confirm_password:
#         flash('Passwords do not match!', 'danger')
#         return redirect(url_for('home'))

#     # Check if email or username already exists
#     if User.query.filter_by(email=email).first():
#         flash('Email is already registered!', 'danger')
#         return redirect(url_for('home'))
#     if User.query.filter_by(username=username).first():
#         flash('Username is already taken!', 'danger')
#         return redirect(url_for('home'))

#     # Create a new user
#     new_user = User(username=username, email=email)
#     new_user.set_password(password)
#     db.session.add(new_user)
#     db.session.commit()

#     flash('Account created successfully! Please log in.', 'success')
#     return redirect(url_for('home'))


# # Run the application
# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()  # Initialize the database tables
#     app.run(debug=True)
