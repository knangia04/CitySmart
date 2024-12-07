from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from models import db, User
from routes.user_routes import user_bp

app = Flask(__name__, static_folder='static')
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)

# Register blueprints
app.register_blueprint(user_bp)

# Root route serving login-template.html
@app.route('/')
def home():
    return render_template('login-template.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Check if the user exists
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        flash('Login successful!', 'success')
        return redirect(url_for('home'))
    else:
        flash('Invalid username or password', 'danger')
        return redirect(url_for('home'))
    

# Route to handle signup
@app.route('/signup', methods=['POST'])
def signup():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm-password')

    # Validate passwords match
    if password != confirm_password:
        flash('Passwords do not match!', 'danger')
        return redirect(url_for('home'))

    # Check if email or username already exists
    if User.query.filter_by(email=email).first():
        flash('Email is already registered!', 'danger')
        return redirect(url_for('home'))
    if User.query.filter_by(username=username).first():
        flash('Username is already taken!', 'danger')
        return redirect(url_for('home'))

    # Create a new user
    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    flash('Account created successfully! Please log in.', 'success')
    return redirect(url_for('home'))


# Run the application
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Initialize the database tables
    app.run(debug=True)
