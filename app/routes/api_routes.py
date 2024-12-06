from flask import Blueprint, jsonify
from app.models import Exercise
from app.utils.fetch_exercise import fetch_and_store_exercises


api_bp = Blueprint('api', __name__)


@api_bp.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify([{"id": e.exercise_id, "name": e.exercise_name} for e in exercises])


@api_bp.route('/fetch_exercises', methods=['POST'])
def fetch_exercises():
    try:
        fetch_and_store_exercises()
        return jsonify({"message": "Exercises fetched successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
