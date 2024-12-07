from flask import Blueprint, render_template, session, request, redirect, url_for
from app.routes.main_routes import login_required
from app.models import User, SavedVideo
from app.database import db_session

profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/', methods=['GET', 'POST'])
@login_required
def profile():
    user = db_session.query(User).filter_by(user_id=session.get('user_id')).first()

    if request.method == 'POST':
        if request.form.get('_method') == 'DELETE':
            user = db_session.query(User).filter_by(user_id=session.get('user_id')).first()
            db_session.query(SavedVideo).filter_by(user_id=user.user_id).delete()
            db_session.delete(user)
            db_session.commit()
            return redirect(url_for('main.register'))

        user.first_name = request.form['first_name']
        session['user_first_name'] = user.first_name
        user.family_name = request.form['family_name']
        user.age = request.form['age']
        user.sex = request.form['sex'].lower() == 'true'
        user.height = request.form['height']
        user.weight = request.form['weight']
        user.gym_goal = request.form['gym_goal']

        db_session.commit()

        return render_template('profile.html', user=user)

    return render_template('profile.html', user=user)
