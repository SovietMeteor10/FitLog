from sqlalchemy import Column, Integer, String
from sqlalchemy import Float, Boolean, Date, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
import datetime


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    email_address = Column(String)
    password = Column(String)
    age = Column(Integer)
    first_name = Column(String)
    family_name = Column(String)
    sex = Column(Boolean)
    height = Column(Integer)
    weight = Column(Float)
    gym_goal = Column(String)

    def __init__(self, first_name, family_name, email_address, password):
        self.first_name = first_name
        self.family_name = family_name
        self.email_address = email_address
        self.password = password

    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")


class Session(Base):
    __tablename__ = "sessions"

    session_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    session_name = Column(String)
    date = Column(Date)
    duration = Column(Float)

    def __init__(self, user_id, session_name, date, duration):
        self.user_id = user_id
        self.session_name = session_name
        self.date = date
        self.duration = duration

    user = relationship("User", back_populates="sessions")
    session_exercises = relationship("SessionExercise", back_populates="session", cascade="all, delete-orphan")


class Exercise(Base):
    __tablename__ = "exercises"

    exercise_id = Column(Integer, primary_key=True)
    exercise_name = Column(String)
    description = Column(Text)
    category = Column(String)

    session_exercises = relationship("SessionExercise", back_populates="exercise")


class SessionExercise(Base):
    __tablename__ = "sessions_exercises"

    session_exercise_id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("sessions.session_id"))
    exercise_id = Column(Integer, ForeignKey("exercises.exercise_id"))

    session = relationship("Session", back_populates="session_exercises")
    exercise = relationship("Exercise", back_populates="session_exercises")
    sets = relationship("Set", back_populates="session_exercise", cascade="all, delete-orphan")


class Set(Base):
    __tablename__ = "sets"

    set_id = Column(Integer, primary_key=True)
    session_exercise_id = Column(
        Integer, ForeignKey("sessions_exercises.session_exercise_id")
    )
    reps = Column(Integer)
    weight = Column(Float)
    set_number = Column(Integer)

    session_exercise = relationship("SessionExercise", back_populates="sets")


class SavedVideo(Base):
    __tablename__ = "saved_videos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    video_id = Column(String, nullable=False)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    thumbnail = Column(String, nullable=True)
    saved_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", backref="saved_videos")
