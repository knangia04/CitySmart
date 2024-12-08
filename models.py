from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class NotificationPreferences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    weather_enabled = db.Column(db.Boolean, default=False)
    pollution_enabled = db.Column(db.Boolean, default=False)
    traffic_enabled = db.Column(db.Boolean, default=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    notification_preferences = db.relationship('NotificationPreferences', backref='user', uselist=False, lazy=True)
