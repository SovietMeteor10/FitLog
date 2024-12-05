from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    sessions = db.relationship('Session', backref='user', lazy=True)
    goal = db.Column(db.String(100), nullable=True)  # User's fitness goal
    
class Session(db.Model):
    __tablename__ = 'sessions'
    id = db.Column(db.Integer, primary_key=True)  # Ensure the primary key is defined
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', name='fk_sessions_users'),
        nullable=False
    )
    session_name = db.Column(db.String(120), nullable=False)
    date = db.Column(db.Date, nullable=False)

    session_exercises = db.relationship('SessionExercise', backref='session', lazy=True)

class Exercise(db.Model):
    __tablename__ = 'exercises'
    id = db.Column(db.Integer, primary_key=True)
    exercise_name = db.Column(db.String(120), unique=True, nullable=False)

    session_exercises = db.relationship('SessionExercise', backref='exercise', lazy=True)

class SessionExercise(db.Model):
    __tablename__ = 'sessions_exercises'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(
        db.Integer,
        db.ForeignKey('sessions.id', name='fk_sessions_exercises_sessions'),
        nullable=False
    )
    exercise_id = db.Column(
        db.Integer,
        db.ForeignKey('exercises.id', name='fk_sessions_exercises_exercises'),
        nullable=False
    )

class Set(db.Model):
    __tablename__ = 'sets'
    id = db.Column(db.Integer, primary_key=True)
    session_exercise_id = db.Column(
        db.Integer,
        db.ForeignKey('sessions_exercises.id', name='fk_sets_sessions_exercises'),
        nullable=False
    )
    set_number = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)  # Weight in kilograms
