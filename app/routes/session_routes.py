from flask import Blueprint, jsonify, render_template, request, session
from app.models import Session, Exercise, SessionExercise
from app.utils.youtube_api import search_youtube_videos
from app.utils.write_to_db import write_session_to_db
from app.database import db_session
from sqlalchemy import func, desc
import datetime
from app.routes.main_routes import login_required


session_bp = Blueprint('sessions', __name__)


# List Sessions
@session_bp.route('/', methods=['GET', 'POST'])
@login_required
def handle_sessions():
    if request.method == 'POST':
        if 'delete' in request.form:
            # Handle session deletion
            session_id = request.form.get('session_id')
            session_to_delete = Session.query.get(session_id)
            db_session.delete(session_to_delete)
            db_session.commit()
        else:
            session_data = {
                'Name': request.form.get('session_name'),
                'Date': datetime.datetime.strptime(
                    request.form.get('date'),
                    '%Y-%m-%d'
                ),
                'Duration': request.form.get('duration'),
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
            {"id": s.session_id, "date": s.date, "session_name": s.session_name, "duration": s.duration}
            for s in sessions
            if s.user_id == session.get("user_id")
        ]
        return render_template('sessions.html', sessions=session_data)
    except Exception as e:
        print(f"Error fetching sessions: {str(e)}")
        return "An error occurred while fetching sessions", 500


@session_bp.route('/<int:session_id>', methods=['GET'])
@login_required
def get_session_details(session_id):
    fetched_session = Session.query.get(session_id)
    if fetched_session and fetched_session.user_id == session.get("user_id"):
        session_data = {
            "id": fetched_session.session_id,
            "name": fetched_session.session_name,
            "date": fetched_session.date.strftime('%Y-%m-%d'),
            "duration": fetched_session.duration,
            "exercises": []
        }
        for session_exercise in fetched_session.session_exercises:
            exercise_data = {
                "name": session_exercise.exercise.exercise_name,
                "sets": []
            }
            for set in session_exercise.sets:
                exercise_data["sets"].append({
                    "reps": set.reps,
                    "weight": set.weight
                })
            session_data["exercises"].append(exercise_data)
        return jsonify(session_data)
    return jsonify({"error": "Session not found"}), 404


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
        db_session.query(Exercise.name, func.count(Exercise.id).label("count"))
        .join(SessionExercise, SessionExercise.exercise_id == Exercise.id)
        .join(Session, Session.id == SessionExercise.session_id)
        .filter(Session.user_id == user_id)  # Filter by user
        .group_by(Exercise.name)
        .order_by(desc("count"))
        .first()
    )

    if not exercises:
        return jsonify({"error": "No exercises found for this user"}), 404

    most_logged_category = exercises[0]  # Most logged exercise category
    videos = search_youtube_videos(most_logged_category)

    return jsonify({"category": most_logged_category, "videos": videos})
