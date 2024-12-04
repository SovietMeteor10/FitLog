import requests
from config import Config
from app.models import Exercise
from app import db

HEADERS = {
    "x-rapidapi-key": Config.RAPIDAPI_KEY,
    "x-rapidapi-host": "exercisedb.p.rapidapi.com",
}


def fetch_and_store_exercises():
    """
    Fetch exercises from ExerciseDB API and store them in the database.
    """
    response = requests.get(Config.EXERCISE_API_URL, headers=HEADERS)

    if response.status_code == 200:
        exercises = response.json()

        for exercise in exercises:
            existing_exercise = Exercise.query.filter_by(
                exercise_name=exercise["name"]
            ).first()
            if not existing_exercise:
                new_exercise = Exercise(
                    exercise_name=exercise["name"],
                    description=exercise.get("target", ""),
                    category=exercise.get("bodyPart", ""),
                    youtube_videos=None,  # Extend this with YouTube integration if needed
                )
                db.session.add(new_exercise)

        db.session.commit()
        print("Exercises successfully stored in the database.")
    else:
        print(f"Failed to fetch exercises. Status code: {response.status_code}")
