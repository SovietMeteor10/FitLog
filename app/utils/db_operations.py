from app import db
from app.models import Session, Exercise, SessionExercise, Set


def write_session_to_db(session_data, user_id=1):
    try:
        # 1. Add the session
        session = Session(user_id=user_id, session_name=session_data['Name'], date=session_data['Date'])
        db.session.add(session)
        db.session.commit()

        # 2. Process each exercise
        for exercise_name, sets in session_data['Exercises'].items():
            # Insert or get exercise
            exercise = Exercise.query.filter_by(exercise_name=exercise_name).first()
            if not exercise:
                exercise = Exercise(exercise_name=exercise_name)
                db.session.add(exercise)
                db.session.commit()

            # Create session-exercise link
            session_exercise = SessionExercise(session_id=session.id, exercise_id=exercise.id)
            db.session.add(session_exercise)
            db.session.commit()

            # 3. Add sets for the exercise
            for set_number, (weight, reps) in enumerate(sets, 1):
                exercise_set = Set(
                    session_exercise_id=session_exercise.id,
                    set_number=set_number,
                    reps=reps,
                    weight=weight
                )
                db.session.add(exercise_set)

        # Commit all changes
        db.session.commit()

    except Exception as e:
        db.session.rollback()  # Rollback in case of an error
        raise e
