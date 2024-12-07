import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'c78bae2d28d74ff2950ee6775b745571346f49acc8b83134')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
