from flask import Blueprint, render_template
from app.routes.main_routes import login_required


improv_bp = Blueprint('improvement', __name__)


@improv_bp.route('/', methods=['GET'])
@login_required
def improv():
    # Pass the logged in user to the index template
    return render_template('improvement.html')
