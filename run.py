""""
from app import create_app

app = create_app()

if __name__ == "__main__":
     app.run(debug=True)


from flask import Flask, render_template
#import os

# Create Flask application instance
app = Flask(__name__, template_folder="templates")


# A simple signup route to test rendering the template
@app.route('/signup', methods=['GET'])
def signup():
     # Render the signup.html template
    return render_template('signup.html')

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/terms', methods=['GET'])
def terms():
    return render_template('terms.html')

@app.route('/main', methods=['GET'])
def main():
    return render_template('index.html')


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
"""
from flask import Flask, render_template, redirect, request
# from flask request
# from flask jsonify
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from api.routes import api_bp  # Keep the API blueprint here
from api.routes import profile_bp
from api.write_to_db import write_session_to_db
import datetime

# Initialize the app and extensions
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Register API Blueprint
app.register_blueprint(api_bp, url_prefix="/api")

# Register PROFILE Blueprint
app.register_blueprint(profile_bp)
# Frontend routes


@app.route("/signup", methods=["GET"])
def signup():
    return render_template("signup.html")


@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")


@app.route("/index", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/terms", methods=["GET"])
def terms():
    return render_template("terms.html")


# If you want to add profile completion:
@app.route("/profile", methods=["GET"])
def profile():
    return render_template("profile.html")


@app.route("/profile/complete", methods=["POST"])
def complete_profile():
    """ Extract data from form
    full_name = request.form.get('full_name')
    age = request.form.get('age')
    sex = request.form.get('sex')
    height = request.form.get('height')
    weight = request.form.get('weight')
    bmi = request.form.get('bmi')
    gym_goals = request.form.get('gym_goals')
    """
    # Handle the data (e.g., save to database)
    # Here you would add code to save the profile to your database

    return redirect("/index")


@app.route('/stats')
def stats():
    return render_template('stats.html')


@app.route('/sessions', methods=['GET'])
def sessions():
    return render_template('sessions.html')


@app.route('/addsession', methods=['GET', 'POST'])
def add_session():
    if request.method == 'POST':
        session_data = {
            'Name': request.form.get('session_name'),
            'Date': datetime.datetime.strptime(
                request.form.get('date'),
                '%Y-%m-%d'
            ),
            'Exercises': {}
        }

        # Process form data
        exercise_inputs = [k for k in request.form.keys()
                           if k.startswith('exercise_')]
        for exercise_input in exercise_inputs:
            exercise_id = exercise_input.split('_')[1]
            exercise_name = request.form.get(f'exercise_{exercise_id}')
            session_data['Exercises'][exercise_name] = []

            # Get all sets for this exercise
            set_count = 1
            while True:
                weight = request.form.get(f'weight_{exercise_id}_{set_count}')
                reps = request.form.get(f'reps_{exercise_id}_{set_count}')
                if not weight or not reps:
                    break

                session_data['Exercises'][exercise_name].append((
                    float(weight), int(reps)
                ))
                set_count += 1

        # Here you would typically save session_data to your database
        write_session_to_db(session_data)
        return 'session saved successfully!'

    return render_template('add_session.html')


if __name__ == "__main__":
    app.run(debug=True)
