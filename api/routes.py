"""
from flask import Blueprint, request, jsonify, render_template
from app import db  # , bcrypt, jwt  # Now you can safely import these
from app.models import User
from .get_exercise import fetch_exercises
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity, jwt_required
import os

auth_blueprint = Blueprint("auth", __name__)
api_bp = Blueprint("api", __name__)


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
        access_token = create_access_token(identity=user.id)

        # Check if the user's profile is complete
        if hasattr(user, 'profile_complete') and user.profile_complete:
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

"
@auth_blueprint.route("/test", methods=["GET"])
def test_template():
    print("Current working directory:", os.getcwd())  # Current directory
    print("Templates folder contains:", os.listdir("templates"))  # List contents of templates folder
    return render_template("test_template.html")
"""
from flask import Blueprint, render_template

# Define the blueprint
auth_blueprint = Blueprint("auth", __name__)

# Define a simple signup route
@auth_blueprint.route("/signup", methods=["GET"])
def signup():
    print("Signup route accessed through blueprint")
    return render_template("signup.html")
