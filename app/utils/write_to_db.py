from app.database import db_session
from app.models import Session, Exercise, SessionExercise, Set

def write_session_to_db(session_data, user_id=1):
    new_session = Session(
        user_id=user_id,
        session_name=session_data['Name'],
        date=session_data['Date']
    )
    db_session.add(new_session)
    db_session.commit()
    db_session.refresh(new_session)  # Get the generated session_id

    # Process each exercise
    for exercise_name in session_data['Exercises']:
        # Insert or get exercise
        exercise = db_session.query(Exercise).filter_by(exercise_name=exercise_name).first()
        if not exercise:
            exercise = Exercise(exercise_name=exercise_name)
            db_session.add(exercise)
            db_session.commit()
            db_session.refresh(exercise)  # Get the generated exercise_id

        # Create session-exercise link
        session_exercise = SessionExercise(
            session_id=new_session.session_id,
            exercise_id=exercise.exercise_id
        )
        db_session.add(session_exercise)
        db_session.commit()
        db_session.refresh(session_exercise)  # Get the generated session_exercise_id

        # Insert sets
        for set_number, (weight, reps) in enumerate(
                session_data['Exercises'][exercise_name], 1
        ):
            new_set = Set(
                session_exercise_id=session_exercise.session_exercise_id,
                set_number=set_number,
                reps=reps,
                weight=weight
            )
            db_session.add(new_set)
            db_session.commit()




