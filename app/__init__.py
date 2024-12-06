from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_login import LoginManager

# Initialize Flask extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
login_manager = LoginManager()
login_manager.login_view = "main.login"
login_manager.login_message = "Please log in to access this page."


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")  # Load app configuration

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    login_manager.init_app(app)

    # User loader function for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User  

        return User.query.get(int(user_id))

    # Register blueprints
    from app.routes import register_blueprints  # Delay import

    register_blueprints(app)

    # Fetch exercises from API after app context is ready
    with app.app_context():
        try:
            from app.utils.fetch_exercise import (
                fetch_and_store_exercises,
            )  # Delay import
            from app.database import SessionLocal

            db_session = SessionLocal()
            fetch_and_store_exercises()
            db_session.close()
        except Exception as e:
            print(f"Error fetching exercises: {e}")

    return app
