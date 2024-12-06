from app.routes.main_routes import main_bp
from app.routes.session_routes import session_bp
from app.routes.stats_routes import stats_bp


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(session_bp, url_prefix="/sessions")
    app.register_blueprint(stats_bp, url_prefix="/statistics")
