"""
from flask import Flask
from config import Config  # Import the Config class
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__, template_folder="templates")

    # Load configuration from the Config class
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Register Blueprints
    from api.routes import api_bp
    from api.routes import auth_blueprint  # Import the auth blueprint

    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(auth_blueprint, url_prefix="/auth")  # Register the auth blueprint

    return app
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from config import Config

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__, template_folder="templates")

    # Load configuration from the Config class
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Register Blueprints
    from api.routes import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    print("Blueprints registered successfully")

    return app
