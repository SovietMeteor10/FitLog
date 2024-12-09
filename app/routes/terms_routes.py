from flask import Blueprint, render_template
from app.routes.main_routes import login_required


terms_bp = Blueprint('terms', __name__)


@terms_bp.route('/', methods=['GET', 'POST'])
#@login_required
def profile():
    return render_template('terms.html')
