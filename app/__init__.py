from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app(config_filename=None):
    app = Flask(__name__)

    app.config.from_pyfile(config_filename)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Register Blueprints
    from api.routes import api_bp  # Import the Blueprint

    app.register_blueprint(api_bp, url_prefix="/api")

    return app
