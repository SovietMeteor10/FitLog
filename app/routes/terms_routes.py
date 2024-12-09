from flask import Blueprint, render_template

terms_bp = Blueprint('terms', __name__)


@terms_bp.route('/', methods=['GET', 'POST'])
#@login_required
#Fixed it now
def profile():
    return render_template('terms.html')
