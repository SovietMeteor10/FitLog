from flask import Blueprint, request, jsonify
from app import db  # , bcrypt, jwt  # Now you can safely import these
from app.models import User
from .get_exercise import fetch_exercises
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity, jwt_required

auth_blueprint = Blueprint("auth", __name__)
api_bp = Blueprint("api", __name__)


@auth_blueprint.route("/register", methods=["POST"])
def register():
    data = request.get_json()
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


@auth_blueprint.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify({"access_token": access_token}), 200

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
