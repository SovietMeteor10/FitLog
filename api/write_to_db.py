import adbc_driver_postgresql.dbapi
from config import Config


def write_exercises_to_db(exercises):
    """
    Writes exercises fetched from the API to the database.
    """
    db_url = Config.DATABASE_URL
    conn = adbc_driver_postgresql.dbapi.connect(db_url)

    try:
        with conn:
            with conn.cursor() as cur:
                for exercise in exercises:
                    cur.execute(
                        """
                        INSERT INTO exercises (exercise_name, description, category, youtube_videos)
                        VALUES ($1, $2, $3, $4)
                        ON CONFLICT (exercise_name) DO NOTHING
                    """,
                        (
                            exercise["name"],
                            exercise["target"],
                            exercise["bodyPart"],
                            fetch_youtube_videos(exercise["name"]),
                        ),
                    )
    except Exception as e:
        print(f"Error writing exercises to DB: {e}")
    finally:
        conn.close()


def write_session_to_db(session):
    conn = adbc_driver_postgresql.dbapi.connect(Config.SQLALCHEMY_DATABASE_URI)
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO sessions (session_name, date) VALUES (%s, %s) RETURNING session_id",
                (session["Name"], session["Date"]),
            )
            session_id = cur.fetchone()[0]

            for exercise, sets in session["Exercises"].items():
                cur.execute(
                    "INSERT INTO exercises (exercise_name) VALUES (%s) ON CONFLICT DO NOTHING RETURNING exercise_id",
                    (exercise,),
                )
                exercise_id = cur.fetchone()[0]

                for set_data in sets:
                    weight, reps = set_data
                    cur.execute(
                        "INSERT INTO sets (session_exercise_id, set_number, weight, reps) VALUES (%s, %s, %s, %s)",
                        (session_id, len(sets), weight, reps),
                    )
            conn.commit()
    finally:
        conn.close()
