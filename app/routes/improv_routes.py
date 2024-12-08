from flask import Blueprint, render_template, jsonify, session, request, redirect, flash
from app.utils.youtube_api import search_youtube_videos
from app.database import db_session
from sqlalchemy import func
from app.models import Exercise, SessionExercise, CachedVideo, Session, SavedVideo
import datetime

improv_bp = Blueprint("improvement", __name__)

@improv_bp.route("/", methods=["GET"])
def improv():
    try:
        # Get the logged-in user's ID
        user_id = session.get("user_id")
        if not user_id:
            print(f"🔥 [DEBUG] User not logged in!")
            flash("Please log in to access improvement suggestions.", "warning")
            return redirect("/login")  # Redirect to login if no user is logged in

        # Define the date range for the past week
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=7)

        # Check if we already have cached videos for this user
        video_data = []  # Initialize video data
        exercise_name = None  # Initialize exercise name
        cached_videos = db_session.query(CachedVideo).filter(
            CachedVideo.user_id == user_id,
            CachedVideo.updated_at >= start_date
        ).first()

        if cached_videos:
            print(f"✅ [DEBUG] Using cached videos for user {user_id}")
            video_data = cached_videos.video_data  # Use the cached video data
            exercise_name = cached_videos.exercise_name  # Get the exercise name from the cache
        else:
            print(f"🆕 [DEBUG] No cached videos for user {user_id}. Querying YouTube API...")

            session_ids = (
                db_session.query(Session.session_id)
                .filter(
                    Session.date.between(start_date, end_date),
                    Session.user_id == user_id
                )
                .all()
            )

            session_ids = [s[0] for s in session_ids]  # Extract session IDs

            if not session_ids:
                flash("No sessions found for the past week.", "info")
                return render_template("improvement.html", videos=[], exercise_name=None)

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

            exercise_name = most_logged_exercise[0] if most_logged_exercise else None

            if exercise_name:
                try:
                    video_data = search_youtube_videos(exercise_name)
                    video_data = video_data[:4]  # Limit to 4 videos

                    new_cache = CachedVideo(
                        user_id=user_id,
                        exercise_name=exercise_name,
                        video_data=video_data
                    )
                    db_session.add(new_cache)
                    db_session.commit()
                    print(f"✅ [DEBUG] Cached new videos for user {user_id}")
                except Exception as e:
                    print(f"❌ [ERROR] Error fetching YouTube videos: {e}")
                    video_data = []

        saved_videos = db_session.query(SavedVideo).filter_by(user_id=user_id).all()
        saved_video_list = [
            {'title': video.title, 'url': video.url, 'thumbnail': video.thumbnail, 'video_id': video.video_id}
            for video in saved_videos
        ]

        return render_template(
            "improvement.html",
            videos=video_data,
            exercise_name=exercise_name,
            saved_videos=saved_video_list
        )

    except Exception as e:
        print(f"❌ [ERROR] Error in improvement route: {e}")
        flash("An error occurred while fetching improvement suggestions.", "danger")
        return redirect("/sessions")

    finally:
        db_session.close()


@improv_bp.route("/save_video", methods=["POST"])
def save_video():
    try:
        user_id = session.get("user_id")
        if not user_id:
            print(f"🔥 [DEBUG] User not logged in!")
            return jsonify(success=False, message="User not logged in."), 401

        data = request.get_json()
        print(f"🔥 [DEBUG] Raw POST data: {data}")

        video_id = str(data.get('video_id', '')).strip()
        title = str(data.get('title', '')).strip()
        url = str(data.get('url', '')).strip()
        thumbnail = str(data.get('thumbnail', '')).strip()

        if not video_id or not title or not url or not thumbnail:
            print(f"❌ [ERROR] Video data is missing or incomplete: {data}")
            return jsonify(success=False, message="Video data is missing or incomplete.")

        existing_video = db_session.query(SavedVideo).filter_by(user_id=user_id, video_id=video_id).first()

        if existing_video:
            print(f"⚠️ [DEBUG] Video already saved: {video_id}")
            return jsonify(success=False, message="Video already saved.")

        new_video = SavedVideo(user_id=user_id, video_id=video_id, title=title, url=url, thumbnail=thumbnail)
        db_session.add(new_video)
        db_session.commit()
        print(f"✅ [DEBUG] Video saved successfully: {video_id}")
        return jsonify(success=True, message="Video saved successfully!")

    except Exception as e:
        print(f"❌ [ERROR] Exception while saving video: {e}")
        return jsonify(success=False, message="An error occurred while saving the video."), 500

    finally:
        db_session.close()


@improv_bp.route("/remove_video", methods=["POST"])
def remove_video():
    try:
        user_id = session.get("user_id")
        if not user_id:
            print(f"🔥 [DEBUG] User not logged in!")
            return jsonify(success=False, message="User not logged in."), 401

        data = request.get_json()
        print(f"🔥 [DEBUG] Raw POST data: {data}")

        video_id = str(data.get('video_id', '')).strip()

        if not video_id:
            print(f"❌ [ERROR] Video ID is missing from request: {data}")
            return jsonify(success=False, message="Video ID is missing.")

        video_to_delete = db_session.query(SavedVideo).filter_by(user_id=user_id, video_id=video_id).first()

        if video_to_delete:
            db_session.delete(video_to_delete)
            db_session.commit()
            print(f"✅ [DEBUG] Video removed successfully: {video_id}")
            return jsonify(success=True, message="Video removed successfully!")
        else:
            print(f"❌ [ERROR] Video not found for removal: {video_id}")
            return jsonify(success=False, message="Video not found for removal.")

    except Exception as e:
        print(f"❌ [ERROR] Exception while removing video: {e}")
        return jsonify(success=False, message="An error occurred while removing the video."), 500

    finally:
        db_session.close()
