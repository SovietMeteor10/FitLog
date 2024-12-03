import adbc_driver_postgresql.dbapi


def write_session_to_db(session, user_id=1):
    db_url = ("postgresql://"
              "postgres.fqqhfswbaqorcblltgxn:FitLogSSE2425"
              "@aws-0-eu-west-2.pooler.supabase.com:5432/postgres")
    conn = adbc_driver_postgresql.dbapi.connect(db_url)
    cur = conn.cursor()

    cur.execute('''
                INSERT INTO sessions (user_id, session_name, date)
                VALUES ($1, $2, $3)
                RETURNING session_id
            ''', (user_id, session['Name'], session['Date']))
    session_id = cur.fetchone()[0]

    # 2. Process each exercise
    for exercise_name in session['Exercises']:
        # Insert or get exercise
        cur.execute('''
                    INSERT INTO exercises (exercise_name)
                    VALUES ($1)
                    ON CONFLICT (exercise_name) DO UPDATE
                    SET exercise_name = EXCLUDED.exercise_name
                    RETURNING exercise_id
                ''', (exercise_name,))
        exercise_id = cur.fetchone()[0]

        # 3. Create session-exercise link
        cur.execute('''
                    INSERT INTO sessions_exercises (session_id, exercise_id)
                    VALUES ($1, $2)
                    RETURNING session_exercise_id
                ''', (session_id, exercise_id))
        session_exercise_id = cur.fetchone()[0]

        # 4. Insert sets
        for set_number, (weight, reps) in enumerate(
                session['Exercises'][exercise_name], 1
        ):
            cur.execute('''
                        INSERT INTO sets (session_exercise_id, set_number,
                         reps, weight)
                        VALUES ($1, $2, $3, $4)
                    ''', (session_exercise_id, set_number, reps, weight))

    conn.commit()
    cur.close()
