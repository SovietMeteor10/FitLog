from flask import Blueprint, request, jsonify, redirect, render_template, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, Exercise
from app.database import db_session
from werkzeug.security import generate_password_hash, check_password_hash

main_bp = Blueprint('main', __name__)

@main_bp.route('/index')
def index():
    # Pass the logged in user to the index template
    return render_template('index.html', user = current_user)

# ---------- AUTH ROUTES ----------
#Login route
@main_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_address = request.form['email_address']
        password = request.form['password']
        error = None
        user = User.query.filter_by(email_address=email_address).first()
        if user is None:
            error = 'Invalid email address.'
        elif not check_password_hash(user.password, password): #Make this secure
            error = 'Invalid password.'

        if error is None:
            session.clear()
            session['user_id'] = user.user_id
            return redirect(url_for('main.index'))

        flash(error)

    return render_template('login.html')

@main_bp.route('/logout')
@login_required  # Only logged-in users can access this route
def logout():
    logout_user()  # Log the user out
    flash("You have been logged out.", "info")
    return redirect(url_for('main.login'))

@main_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        family_name = request.form['family_name']
        email_address = request.form['email_address']
        password = generate_password_hash(request.form['password'], method='pbkdf2')

        u = User(first_name, family_name, email_address, password)

        db_session.add(u)
        db_session.commit()
        return redirect(url_for('main.login'))

    return render_template('signup.html')