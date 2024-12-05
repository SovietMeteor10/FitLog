from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_login import LoginManager

# Initialize Flask extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()
login_manager = LoginManager()  # Use snake_case for consistency
login_manager.login_view = "main.login"  # Redirect here if not authenticated
login_manager.login_message = "Please log in to access this page."  # Default login message

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")  # Load app configuration

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # User loader function for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User  # Import User model
        return User.query.get(int(user_id))  # Fetch user by ID

    # Register blueprints
    from app.routes import register_blueprints
    register_blueprints(app)

    return app
