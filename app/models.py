from flask_sqlalchemy import SQLAlchemy

# Import db from app
from app import db


class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # Relationships
    sessions = db.relationship("Session", backref="user", lazy=True)


class Exercise(db.Model):
    __tablename__ = "exercises"

    exercise_id = db.Column(db.Integer, primary_key=True)
    exercise_name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(80), nullable=True)
    youtube_videos = db.Column(db.JSON, nullable=True)


class Session(db.Model):
    __tablename__ = "sessions"

    session_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    session_name = db.Column(db.String(80), nullable=False)
    date = db.Column(db.Date, nullable=False)

    # Relationships
    sets = db.relationship("Set", backref="session", lazy=True)


class Set(db.Model):
    __tablename__ = "sets"

    set_id = db.Column(db.Integer, primary_key=True)
    session_exercise_id = db.Column(
        db.Integer, db.ForeignKey("sessions.session_id"), nullable=False
    )
    set_number = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Numeric(5, 2), nullable=False)
    reps = db.Column(db.Integer, nullable=False)
