from flask import Flask, render_template, request, redirect, url_for, flash, session
from config import Config
from models import db, User
from routes.settings_routes import settings_bp

app = Flask(__name__, static_folder='static')
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)

# Create the database tables if they don't exist
with app.app_context():
    db.create_all()

# Register blueprints
app.register_blueprint(settings_bp)

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('settings.settings'))
    return render_template('login-template.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        session['username'] = username
        flash('Login successful!', 'success')
        return redirect(url_for('settings.settings'))

    flash('Invalid credentials. Please try again.', 'danger')
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
