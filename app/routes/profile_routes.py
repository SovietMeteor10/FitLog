from flask import Blueprint, render_template
from app.routes.main_routes import login_required


profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('profile.html')
