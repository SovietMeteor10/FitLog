import requests
from app.models import Exercise
from app import db
from app.config import Config

EXERCISE_API_URL = "https://exercisedb.p.rapidapi.com/exercises"
HEADERS = {
    "X-RapidAPI-Key": Config.RAPIDAPI_KEY,
    "X-RapidAPI-Host": "exercisedb.p.rapidapi.com",
}

def fetch_and_store_exercises():
    try:
        response = requests.get(EXERCISE_API_URL, headers=HEADERS)
        response.raise_for_status()
        exercises = response.json()

        for exercise in exercises:
            # Avoid duplicates by checking if the exercise already exists
            existing_exercise = Exercise.query.filter_by(exercise_name=exercise['name']).first()
            if not existing_exercise:
                new_exercise = Exercise(
                    exercise_name=exercise['name']
                )
                db.session.add(new_exercise)

        db.session.commit()
        print("Exercises successfully fetched and stored!")
    except Exception as e:
        db.session.rollback()
        print(f"Error fetching/storing exercises: {e}")