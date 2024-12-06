from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    SelectField,
    IntegerField,
    DateField,
)
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class SignupForm(FlaskForm):
    first_name = StringField(
        "First Name", validators=[DataRequired(), Length(min=2, max=50)]
    )
    family_name = StringField(
        "Family Name", validators=[DataRequired(), Length(min=2, max=50)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6),
            EqualTo("confirm_password", message="Passwords must match"),
        ],
    )
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Sign Up")


class ProfileForm(FlaskForm):
    age = IntegerField("Age", validators=[DataRequired()])
    sex = SelectField(
        "Sex",
        choices=[("male", "Male"), ("female", "Female"), ("other", "Other")],
        validators=[DataRequired()],
    )
    height = IntegerField("Height (cm)", validators=[DataRequired()])
    weight = IntegerField("Weight (kg)", validators=[DataRequired()])
    gym_goals = SelectField(
        "Gym Goals",
        choices=[
            ("build_muscle", "Build Muscle"),
            ("lose_weight", "Lose Weight"),
            ("maintain_physique", "Maintain Physique"),
            ("improve_stamina", "Improve Stamina"),
        ],
        validators=[Optional()],
    )
    submit = SubmitField("Save Profile")


class AddSessionForm(FlaskForm):
    session_name = StringField("Session Name", validators=[DataRequired()])
    date = DateField("Date", validators=[DataRequired()])
    exercise_1 = StringField("Exercise", validators=[DataRequired()])
    submit = SubmitField("Add Session")
