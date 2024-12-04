from flask import Flask, render_template, redirect, request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from api.routes import api_bp, profile_bp
from api.write_to_db import write_session_to_db
from app.models import Exercise
import datetime

# Initialize the app and extensions
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Register Blueprints
app.register_blueprint(api_bp, url_prefix="/api")
app.register_blueprint(profile_bp, url_prefix="/profile")

# Frontend Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/stats")
def stats():
    return render_template("stats.html")

@app.route("/sessions")
def sessions():
    return render_template("sessions.html")


@app.route("/addsession", methods=["GET", "POST"])
def add_session():
    if request.method == "POST":
        # Process the session data
        session_data = {
            "Name": request.form.get("session_name"),
            "Date": request.form.get("date"),
            "Exercises": {}
        }

        # Process exercises and sets
        exercise_inputs = [k for k in request.form.keys() if k.startswith("exercise_")]
        for exercise_input in exercise_inputs:
            exercise_id = exercise_input.split("_")[1]
            exercise_name = request.form.get(f"exercise_{exercise_id}")
            session_data["Exercises"][exercise_name] = []

            set_count = 1
            while True:
                weight = request.form.get(f"weight_{exercise_id}_{set_count}")
                reps = request.form.get(f"reps_{exercise_id}_{set_count}")
                if not weight or not reps:
                    break

                session_data["Exercises"][exercise_name].append((float(weight), int(reps)))
                set_count += 1

        # Save session to the database
        write_session_to_db(session_data)
        return "Session saved successfully!"

    # Fetch exercises from the database for the dropdown
    exercises = Exercise.query.all()
    return render_template("add_session.html", exercises=exercises)


if __name__ == "__main__":
    app.run(debug=True)
