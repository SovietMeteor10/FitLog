from flask import Blueprint, render_template


improv_bp = Blueprint('improvement', __name__)

@improv_bp.route('/', methods=['GET'])
def improv():
    # Pass the logged in user to the index template
    return render_template('improvement.html')
