import requests
from app.models import Exercise
from app.database import db_session


EXERCISE_API_URL = "https://exercisedb-api.vercel.app/api/v1/exercises"
MAX_EXERCISES = 1000  # Limit the number of exercises to fetch


def fetch_exercises_from_api():
    """
    Fetch exercises from the ExerciseDB API with pagination.
    """
    all_exercises = []
    seen_exercises = set()  # Track unique exercise names to avoid duplicates
    next_page = EXERCISE_API_URL

    while next_page and len(all_exercises) < MAX_EXERCISES:
        try:
            response = requests.get(next_page)
            response.raise_for_status()
            api_data = response.json()

            # Get exercises and the next page
            exercises = api_data.get("data", {}).get("exercises", [])
            next_page = api_data.get("data", {}).get("nextPage")

            for exercise in exercises:
                exercise_name = exercise.get("name")
                if exercise_name and exercise_name not in seen_exercises:
                    seen_exercises.add(exercise_name)
                    all_exercises.append({
                        "name": exercise_name,
                        "instructions": exercise.get("instructions", []),
                        "targetMuscles": exercise.get("targetMuscles"),
                        "bodyParts": exercise.get("bodyParts"),
                    })

            print(f"Fetched {len(all_exercises)} exercises so far...")
        except requests.exceptions.RequestException as e:
            print(f"Error during API request: {e}")
            break

    return all_exercises[:MAX_EXERCISES]  # Return limited exercises


def store_exercises_in_db(exercises):
    """
    Store exercises in the database, avoiding duplicates.
    """
    new_exercises = 0
    updated_exercises = 0
    skipped_exercises = 0

    try:
        for exercise in exercises:
            exercise_name = exercise.get("name")
            target_muscles = exercise.get("targetMuscles", [])
            body_parts = exercise.get("bodyParts", [])

            # Prioritize target muscles for category; fallback to body parts
            if target_muscles:
                category = ", ".join(target_muscles)
            elif body_parts:
                category = ", ".join(body_parts)
            else:
                category = "Uncategorized"

            description = " ".join(exercise.get("instructions", []))  # Combine steps into one description

            # Check for duplicates in the database
            existing_exercise = db_session.query(Exercise).filter_by(exercise_name=exercise_name).first()
            if not existing_exercise:
                new_exercise = Exercise(
                    exercise_name=exercise_name,
                    description=description,
                    category=category
                )
                db_session.add(new_exercise)
                new_exercises += 1
            else:
                if not existing_exercise.category or existing_exercise.category != category:
                    existing_exercise.category = category
                    updated_exercises += 1
                else:
                    skipped_exercises += 1

        db_session.commit()
        print(f"Successfully added {new_exercises} new exercises to the database.")
        print(f"Updated {updated_exercises} exercises with new categories.")
        print(f"Skipped {skipped_exercises} duplicate exercises.")
    except Exception as e:
        db_session.rollback()
        print(f"Error storing exercises in the database: {e}")


def fetch_and_store_exercises():
    """
    Fetch exercises from the API and store them in the database.
    """
    print("Fetching exercises from ExerciseDB API...")
    exercises = fetch_exercises_from_api()
    print(f"Total unique exercises fetched: {len(exercises)}")

    if exercises:
        print("Storing exercises in the database...")
        store_exercises_in_db(exercises)
