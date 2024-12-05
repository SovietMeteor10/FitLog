from flask import Blueprint, request, jsonify, redirect, render_template, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import LoginForm, SignupForm
from app.models import User, Exercise
from app import db

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
        email = request.form.get("email")
        password = request.form.get("password")

        # Authenticate the user
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Logged in successfully",success=True)
            # Redirect to the index page on successful login
            return redirect(url_for('main.index'))

        # If login fails, re-render login page with error message
        flash ("Invalid email or password",error=True)
        return render_template('login.html', error="Invalid email or password")

    # Render login page for GET requests
    return render_template('login.html')


@main_bp.route('/logout')
@login_required  # Only logged-in users can access this route
def logout():
    logout_user()  # Log the user out
    flash("You have been logged out.", "info")
    return redirect(url_for('main.login'))

@main_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("signup.html")  # Create a simple register.html file with a form

    data = request.get_json() if request.is_json else request.form
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 400

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@main_bp.route('/stats')
def stats():
    stats_data = {
        "recent_stats": [
            {"date": "2024-12-01", "calories": 300},
            {"date": "2024-12-02", "calories": 250},
        ],
        "recommended_videos": ["Video 1", "Video 2", "Video 3", "Video 4"],
    }
    return render_template('stats.html', stats=stats_data, recommended_videos=stats_data["recommended_videos"])
