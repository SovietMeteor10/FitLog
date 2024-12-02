# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_default_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///your_database.db'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'your_jwt_secret_key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_URL = "https://wger.de/api/v2/exercise/"
    API_KEY = os.getenv('API_KEY', '0e796d1f4ca0e764b163b0bff8011c96a37fb894')  # Use an environment variable for security
