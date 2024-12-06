from flask import Blueprint, jsonify, render_template, request, session
from app.models import Session, Exercise, SessionExercise
from app import db
from app.utils.youtube_api import search_youtube_videos
from app.utils.write_to_db import write_session_to_db
from app.database import db_session
import datetime


session_bp = Blueprint('sessions', __name__)


# List Sessions
@session_bp.route('/', methods=['GET', 'POST'])
def handle_sessions():
    if request.method == 'POST':
        session_data = {
            'Name': request.form.get('session_name'),
            'Date': datetime.datetime.strptime(
                request.form.get('date'),
                '%Y-%m-%d'
            ),
            'Exercises': {}
        }
        exercise_inputs = [k for k in request.form.keys()
                           if k.startswith('exercise_')]
        for exercise_input in exercise_inputs:
            exercise_id = exercise_input.split('_')[1]
            exercise_name = request.form.get(f'exercise_{exercise_id}')
            session_data['Exercises'][exercise_name] = []
            set_count = 1
            while True:
                weight = request.form.get(f'weight_{exercise_id}_{set_count}')
                reps = request.form.get(f'reps_{exercise_id}_{set_count}')
                if not weight or not reps:
                    break
                session_data['Exercises'][exercise_name].append((
                    float(weight), int(reps)
                ))
                set_count += 1
        write_session_to_db(session_data, user_id=session.get("user_id"))

    elif request.method == 'GET' and 'q' in request.args:
        # Handle the exercise search functionality
        query = request.args.get('q', '').lower()
        if not query:
            return jsonify([])

        results = (
            db_session.query(Exercise)
            .filter(Exercise.exercise_name.ilike(f"%{query}%"))
            .limit(10)
            .all()
        )
        return jsonify([{"id": e.exercise_id, "name": e.exercise_name} for e in results])

    try:
        sessions = Session.query.all()
        session_data = [
            {"date": s.date, "session_name": s.session_name}
            for s in sessions
            if s.user_id == session.get("user_id")
        ]
        return render_template('sessions.html', sessions=session_data)
    except Exception as e:
        print(f"Error fetching sessions: {str(e)}")
        return "An error occurred while fetching sessions", 500


# Retrieve Exercises
@session_bp.route('/get_exercises', methods=['GET'])
def get_exercises():
    """
    Retrieve all exercises for populating dropdowns.
    """
    exercises = Exercise.query.all()
    exercise_list = [{"id": exercise.id, "name": exercise.name} for exercise in exercises]
    return jsonify(exercise_list)


# Recommend YouTube videos
@session_bp.route("/recommend_videos", methods=["GET"])
def recommend_videos():
    """
    Recommend YouTube videos based on user's most logged exercise category.
    """
    user_id = request.args.get("user_id")  # Use session or token to identify user
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    # Aggregate user's most logged exercises
    exercises = (
        db.session.query(Exercise.name, db.func.count(Exercise.id).label("count"))
        .join(SessionExercise, SessionExercise.exercise_id == Exercise.id)
        .join(Session, Session.id == SessionExercise.session_id)
        .filter(Session.user_id == user_id)  # Filter by user
        .group_by(Exercise.name)
        .order_by(db.desc("count"))
        .first()
    )

    if not exercises:
        return jsonify({"error": "No exercises found for this user"}), 404

    most_logged_category = exercises[0]  # Most logged exercise category
    videos = search_youtube_videos(most_logged_category)

    return jsonify({"category": most_logged_category, "videos": videos})
