from flask import Blueprint

from app.routes.main_routes import main_bp
from app.routes.session_routes import session_bp
from app.routes.api_routes import api_bp

def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(session_bp, url_prefix="/sessions")
    app.register_blueprint(api_bp, url_prefix="/api")
