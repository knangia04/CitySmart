from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    location = db.Column(db.String(50), nullable=False)

    # Relationship with NotificationPreferences
    notification_preferences = db.relationship('NotificationPreferences', 
                                               backref='user', 
                                               lazy=True, 
                                               cascade='all, delete-orphan')

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

class NotificationPreferences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    weather_enabled = db.Column(db.Boolean, default=False)
    pollution_enabled = db.Column(db.Boolean, default=False)
    traffic_enabled = db.Column(db.Boolean, default=False)