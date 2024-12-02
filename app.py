"""from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Initialize extensions (will be initialized in the create_app function)
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_filename=None):
    app = Flask(__name__)

    # If you have a config.py, load it
    if config_filename:
        app.config.from_pyfile(config_filename)
    else:
        # Provide the database URI directly here if no config file is used
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SECRET_KEY'] = 'your_default_secret_key'
        app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
    
    # Initialize other extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    return app"""

# Test code

from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(debug=True)
