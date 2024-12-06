from flask import Blueprint, render_template, session, redirect, flash
from app.utils.youtube_api import search_youtube_videos
from app.database import db_session
from sqlalchemy import func
from app.models import Exercise, SessionExercise, Session
import datetime

improv_bp = Blueprint('improvement', __name__)


@improv_bp.route('/', methods=['GET'])
def improv():
    try:
        # Get the logged-in user's ID
        user_id = session.get("user_id")
        if not user_id:
            flash("Please log in to access improvement suggestions.", "warning")
            return redirect('/login')  # Redirect to login if no user is logged in

        # Define the date range for the past week
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=7)

        # Query session IDs for the user within the date range
        session_ids = db_session.query(Session.session_id).filter(
            Session.date.between(start_date, end_date),
            Session.user_id == user_id
        ).all()
        # Extract session IDs into a list
        session_ids = [s[0] for s in session_ids]  # Unpacking the tuples

        if not session_ids:
            flash("No sessions found for the past week.", "info")
            return render_template('improvement.html', videos=[], exercise_name=None)

        # Query the most logged exercise in these sessions
        most_logged_exercise = db_session.query(
            Exercise.exercise_name, func.count(SessionExercise.exercise_id).label("count")
            ).join(SessionExercise, Exercise.exercise_id == SessionExercise.exercise_id
            ).filter(
                SessionExercise.session_id.in_(session_ids)
            ).group_by(
                Exercise.exercise_name
            ).order_by(
                func.count(SessionExercise.exercise_id).desc()
            ).first()

        # If no exercises are found, provide a default suggestion
        exercise_name = most_logged_exercise[0] if most_logged_exercise else None

        # Fetch YouTube videos related to the most logged exercise
        videos = search_youtube_videos(exercise_name) if exercise_name else []
        videos = videos[:4]  # Ensure only 4 videos are displayed

        # Pass videos and exercise name to the template
        return render_template('improvement.html', videos=videos, exercise_name=exercise_name)

    except Exception as e:
        # Log and handle errors gracefully
        print(f"Error in improvement route: {e}")
        flash("An error occurred while fetching improvement suggestions.", "danger")
        return redirect('/sessions')

    finally:
        # Ensure database session is closed properly
        db_session.close()
