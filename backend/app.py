from flask import Flask
from config import Config
from models import db
from routes.user_routes import user_bp

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)

# Register blueprints
app.register_blueprint(user_bp)

@app.route('/')
def home():
    return 

# Run the application
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Initialize the database tables
    app.run(debug=True)
