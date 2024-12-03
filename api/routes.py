from flask import Blueprint, request, jsonify, render_template
from app import db  # , bcrypt, jwt  # Now you can safely import these
from app.models import User
from .get_exercise import fetch_exercises

# from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity, jwt_required


auth_blueprint = Blueprint("auth", __name__)
api_bp = Blueprint("api", __name__)

profile_bp = Blueprint("profile", __name__)


@auth_blueprint.route("/register", methods=["POST"])
def register():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

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

    # Find the user by email
    user = User.query.filter_by(email=email).first()

    # Check if user exists and if the password matches
    if user and user.check_password(password):
        #  access_token = create_access_token(identity=user.id)

        # Check if the user's profile is complete
        if hasattr(user, "profile_complete") and user.profile_complete:
            # If profile is complete, redirect to main page
            return jsonify({"redirect": "/main"}), 200
        else:
            # If profile is incomplete, redirect to profile completion page
            return jsonify({"redirect": "/profile"}), 200

    # If user is not found or password is incorrect, return an error
    return jsonify({"message": "Invalid email or password"}), 401


@auth_blueprint.route("/logout", methods=["POST"])
def logout():
    return jsonify({"message": "Logged out successfully"}), 200


@auth_blueprint.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({"message": f"Hello {current_user}"}), 200


@api_bp.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = fetch_exercises()
    return jsonify(exercises), 200


@profile_bp.route("/profile/get", methods=["GET"])
@jwt_required()
def get_profile():
    # Get the current user's ID from the JWT token
    user_id = get_jwt_identity()

    # Query the database for the user's profile information
    user = User.query.get(user_id)

    if user:
        # Create a dictionary with user profile details
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
    else:
        return jsonify({"error": "User not found"}), 404
