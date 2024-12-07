from flask import Blueprint, render_template, jsonify, session, request, redirect, flash
from app.utils.youtube_api import search_youtube_videos
from app.database import db_session
from sqlalchemy import func
from app.models import Exercise, SessionExercise, Session, SavedVideo
import datetime

improv_bp = Blueprint("improvement", __name__)


@improv_bp.route("/", methods=["GET", "POST"])
def improv():
    try:
        # Get the logged-in user's ID
        user_id = session.get("user_id")
        if not user_id:
            flash("Please log in to access improvement suggestions.", "warning")
            return redirect("/login")  # Redirect to login if no user is logged in

        if request.method == "POST":
            data = request.get_json()
            print(f"Raw POST data: {data}")  # See the data from the POST request

            # Extract video data (Handle None values and trim extra whitespace)
            video_id = str(data.get('video_id', '')).strip()
            title = str(data.get('title', '')).strip()
            url = str(data.get('url', '')).strip()
            thumbnail = str(data.get('thumbnail', '')).strip()

            if not video_id:
                print(f"❌ Video ID is missing or invalid. Received: {video_id}")
                return jsonify(success=False, message="Video ID is missing.")

            print(f"✅ Received video data - ID: {video_id}, Title: {title}, URL: {url}, Thumbnail: {thumbnail}")

            # Check if the video is already saved
            existing_video = db_session.query(SavedVideo).filter_by(
                user_id=user_id, video_id=video_id
            ).first()

            if existing_video:
                return jsonify(success=False, message="Video already saved.")

            # Save the video in the database
            new_video = SavedVideo(
                user_id=user_id,
                video_id=video_id,
                title=title,
                url=url,
                thumbnail=thumbnail
            )
            db_session.add(new_video)
            db_session.commit()

            return jsonify(success=True, message="Video saved successfully!")

        # Define the date range for the past week
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=7)

        # Query session IDs for the user within the date range
        session_ids = (
            db_session.query(Session.session_id)
            .filter(
                Session.date.between(start_date, end_date), Session.user_id == user_id
            )
            .all()
        )
        # Extract session IDs into a list
        session_ids = [s[0] for s in session_ids]  # Unpacking the tuples

        if not session_ids:
            flash("No sessions found for the past week.", "info")
            return render_template("improvement.html", videos=[], exercise_name=None)

        # Query the most logged exercise in these sessions
        most_logged_exercise = (
            db_session.query(
                Exercise.exercise_name,
                func.count(SessionExercise.exercise_id).label("count"),
            )
            .join(SessionExercise, Exercise.exercise_id == SessionExercise.exercise_id)
            .filter(SessionExercise.session_id.in_(session_ids))
            .group_by(Exercise.exercise_name)
            .order_by(func.count(SessionExercise.exercise_id).desc())
            .first()
        )

        # If no exercises are found, provide a default suggestion
        exercise_name = most_logged_exercise[0] if most_logged_exercise else None

        # Fetch YouTube videos related to the most logged exercise
        videos = search_youtube_videos(exercise_name) if exercise_name else []
        videos = videos[:4]  # Ensure only 4 videos are displayed
        # print("Video data being passed ",videos)

        # Fetch saved videos for the sidebar
        saved_videos = db_session.query(SavedVideo).filter_by(user_id=user_id).all()
        saved_video_list = [
            {'title': video.title, 'url': video.url, 'thumbnail': video.thumbnail}
            for video in saved_videos
        ]

        return render_template(
            "improvement.html",
            videos=videos,
            exercise_name=exercise_name,
            saved_videos=saved_video_list
        )

    except Exception as e:
        # Log and handle errors gracefully
        print(f"Error in improvement route: {e}")
        flash("An error occurred while fetching improvement suggestions.", "danger")
        return redirect("/sessions")

    finally:
        # Ensure database session is closed properly
        db_session.close()
