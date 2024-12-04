from flask import Blueprint, request, jsonify, render_template
from app import db
from app.models import User, Exercise
from api.get_exercise import fetch_and_store_exercises
from api.write_to_db import write_session_to_db
from flask_jwt_extended import get_jwt_identity, jwt_required

auth_blueprint = Blueprint("auth", __name__)
api_bp = Blueprint("api", __name__)
profile_bp = Blueprint("profile", __name__)


# ---------- AUTH ROUTES ----------
@auth_blueprint.route("/register", methods=["POST"])
def register():
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


@auth_blueprint.route("/signup", methods=["GET"])
def signup():
    return render_template("signup.html")


@auth_blueprint.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        # Redirect based on profile completion
        redirect_url = (
            "/main" if getattr(user, "profile_complete", False) else "/profile"
        )
        return jsonify({"redirect": redirect_url}), 200

    return jsonify({"message": "Invalid email or password"}), 401


@auth_blueprint.route("/logout", methods=["POST"])
def logout():
    return jsonify({"message": "Logged out successfully"}), 200


# ---------- API ROUTES ----------
@api_bp.route("/exercises", methods=["GET"])
def get_exercises():
    """
    Fetches exercises from the database to populate the dropdown menu.
    """
    exercises = Exercise.query.all()
    return jsonify([exercise.exercise_name for exercise in exercises])


@api_bp.route("/fetch_exercises", methods=["POST"])
def fetch_and_store():
    """
    Fetches exercises from the external API and stores them in the database.
    This should be called only during setup or when refreshing data.
    """
    try:
        fetch_and_store_exercises()
        return jsonify({"message": "Exercises fetched "
                                   "and stored successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/session", methods=["POST"])
def create_session():
    """
    Creates a user session and writes it to the database.
    """
    session_data = request.get_json()
    write_session_to_db(
        session_data, user_id=1
    )  # Replace user_id=1 with dynamic user retrieval
    return jsonify({"message": "Session created successfully"})


# ---------- PROFILE ROUTES ----------
@profile_bp.route("/get", methods=["GET"])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if user:
        profile_data = {
            "first_name": user.first_name,
            "family_name": user.family_name,
            "age": user.age,
            "sex": user.sex,
            "height": user.height,
            "weight": user.weight,
            "bmi": user.bmi,
        }
        return jsonify(profile_data), 200
    return jsonify({"error": "User not found"}), 404
