import pytest
from app import create_app
from app.database import init_db, db_session
from app.models import User
from werkzeug.security import generate_password_hash


@pytest.fixture(scope="module")
def test_client():
    # Create the Flask application for testing
    flask_app = create_app()

    # Configure the app to use a test database
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    flask_app.config["TESTING"] = True

    # Initialize the test database
    with flask_app.app_context():
        init_db()
        setup_test_data()

    # Create a test client for making HTTP requests
    testing_client = flask_app.test_client()

    yield testing_client

    # Cleanup the database session
    with flask_app.app_context():
        db_session.remove()


def setup_test_data():
    test_user = User(
        first_name="Test",
        family_name="User",
        email_address="testuser@example.com",
        password=generate_password_hash("correct_password"),  # Correctly hashed
    )
    db_session.add(test_user)
    db_session.commit()


def test_login_failure(test_client):
    response = test_client.post(
        "/",
        data={
            "email_address": "wronguser@example.com",
            "password": "wrong_password",
        },
    )

    assert response.status_code == 200
    assert b"Invalid email address." in response.data


def test_profile_delete(test_client):
    test_client.post(
        "/",
        data={
            "email_address": "testuser@example.com",
            "password": "correct_password",
        },
    )

    response = test_client.post("/profile/", data={"_method": "DELETE"})

    assert response.status_code == 302
    assert b"Sign Up" in test_client.get("/").data
