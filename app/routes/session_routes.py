from flask import Blueprint, jsonify, render_template, request
from app.models import Session, Exercise, SessionExercise, User
from app import db
from app.utils.youtube_api import search_youtube_videos

session_bp = Blueprint('session', __name__)

# List Sessions
@session_bp.route('/')
def list_sessions():
    """
    List all sessions stored in the database.
    """
    sessions = Session.query.all()
    session_data = [
        {"id": session.id, "date": session.date, "name": session.name}
        for session in sessions
    ]
    return render_template('sessions.html', sessions=session_data)

# Add New Session
@session_bp.route('/submit_session', methods=['POST'])
def submit_session():
    """
    Handle the submission of a new session with exercises.
    """
    data = request.get_json()

    # Validate incoming data
    if not data or "date" not in data or "name" not in data or "exercises" not in data:
        return jsonify({"error": "Invalid session data"}), 400

    try:
        # Create a new session
        new_session = Session(
            name=data["name"],
            date=data["date"],
            duration_hours=data["duration"]["hours"],
            duration_minutes=data["duration"]["minutes"],
        )
        db.session.add(new_session)
        db.session.commit()  # Commit to get the session ID

        # Add exercises to the session
        for exercise_data in data["exercises"]:
            # Check if the exercise already exists
            exercise = Exercise.query.filter_by(name=exercise_data["type"]).first()
            if not exercise:
                # Create a new exercise if it doesn't exist
                exercise = Exercise(name=exercise_data["type"])
                db.session.add(exercise)
                db.session.commit()  # Commit to get the exercise ID

            # Create a SessionExercise entry
            session_exercise = SessionExercise(
                session_id=new_session.id,
                exercise_id=exercise.id,
                sets=exercise_data.get("sets", None),
                reps=exercise_data.get("reps", None),
                weight=exercise_data.get("weight", None),
                distance=exercise_data.get("distance", None),
                time_spent=exercise_data.get("timeSpent", None),
            )
            db.session.add(session_exercise)

        # Commit all changes
        db.session.commit()

        return jsonify({"message": "Session submitted successfully"}), 201

    except Exception as e:
        db.session.rollback()  # Rollback on error
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

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


@session_bp.route("/recommend_videos_by_goal", methods=["GET"])
def recommend_videos_by_goal():
    """
    Recommend YouTube videos based on user's fitness goal.
    """
    user_id = request.args.get("user_id")  # Use session or token to identify user
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    # Fetch the user's goal
    user = User.query.get(user_id)
    if not user or not user.goal:
        return jsonify({"error": "User goal not found"}), 404

    videos = search_youtube_videos(user.goal)
    return jsonify({"goal": user.goal, "videos": videos})
