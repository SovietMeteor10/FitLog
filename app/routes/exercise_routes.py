from flask import Blueprint, jsonify
from app.models import Exercise


exercise_bp = Blueprint('exercise', __name__)


@exercise_bp.route('/get_exercises', methods=['GET'])
def get_exercises():
    try:
        exercises = Exercise.query.all()
        exercise_list = [{"id": ex.id, "name": ex.exercise_name} for ex in exercises]
        return jsonify(exercise_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
