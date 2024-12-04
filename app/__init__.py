from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import os

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_filename):
    """
    Factory function to create and configure the Flask application.
    """
    app = Flask(__name__)
    app.config.from_object(config_filename)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Register blueprints after extensions are initialized
    from api.routes import api_bp, profile_bp
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(profile_bp, url_prefix="/profile")

    # Fetch and store exercises on startup
    with app.app_context():
        try:
            from api.get_exercise import fetch_and_store_exercises  # Delayed import
            fetch_and_store_exercises()
            print("Exercises fetched and stored successfully.")
        except Exception as e:
            print(f"Error while fetching exercises: {e}")

    return app

