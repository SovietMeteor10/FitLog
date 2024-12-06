import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "your_default_secret_key")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL",
                                             "sqlite:///fitness_app.db")
    SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_size": 10,
    "max_overflow": 20,
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    EXERCISE_API_URL = "https://exercisedb.p.rapidapi.com/exercises"
    RAPIDAPI_KEY = os.environ.get(
        "RAPIDAPI_KEY", "80bf475784mshb3508101d4c1216p1d2f3ajsne4411c275351"
    )
