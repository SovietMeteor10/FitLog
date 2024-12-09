from flask import Flask
from app.database import db_session


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")  # Load app configuration

    # Register blueprints
    from app.routes import register_blueprints  # Delay import

    register_blueprints(app)

    # Fetch exercises from API after app context is ready
    with app.app_context():
        try:
            pass
            # fetch_and_store_exercises()
        except Exception as e:
            print(f"Error fetching exercises: {e}")

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app
