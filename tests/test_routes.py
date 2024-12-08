import pytest
from app import create_app
from app.database import init_db, db_session
from app.models import User, SavedVideo


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
    # Add a test user to the database
    test_user = User(
        first_name="Test",
        family_name="User",
        email_address="testuser@example.com",
        password="hashed_password",  # Use the hashed version of the password
    )
    db_session.add(test_user)
    db_session.commit()


def test_login_success(test_client):
    # Simulate a POST request to the login route with valid credentials
    response = test_client.post("/", data={
        "email_address": "testuser@example.com",
        "password": "hashed_password",
    })

    # Assert the login was successful and the user is redirected
    assert response.status_code == 302
    assert b"Login successful!" in response.data


def test_login_failure(test_client):
    # Simulate a POST request to the login route with invalid credentials
    response = test_client.post("/", data={
        "email_address": "wronguser@example.com",
        "password": "wrong_password",
    })

    # Assert the login failed and the user receives an error message
    assert response.status_code == 200
    assert b"Invalid email address." in response.data


def test_logout(test_client):
    # Simulate logging in first
    test_client.post("/", data={
        "email_address": "testuser@example.com",
        "password": "hashed_password",
    })

    # Simulate a GET request to the logout route
    response = test_client.get("/logout")

    # Assert the logout was successful and the user is redirected
    assert response.status_code == 302
    assert b"Please log in to access this page." in test_client.get("/").data


def test_profile_update(test_client):
    # Simulate logging in first
    test_client.post("/", data={
        "email_address": "testuser@example.com",
        "password": "hashed_password",
    })

    # Simulate a POST request to update the profile
    response = test_client.post("/profile", data={
        "first_name": "Updated",
        "family_name": "User",
        "age": 30,
        "sex": "male",
        "height": 180,
        "weight": 75.5,
        "gym_goal": "build_muscle",
    })

    # Assert the profile update was successful
    assert response.status_code == 200
    assert b"Updated" in response.data


def test_profile_delete(test_client):
    # Simulate logging in first
    test_client.post("/", data={
        "email_address": "testuser@example.com",
        "password": "hashed_password",
    })

    # Simulate a DELETE request to remove the profile
    response = test_client.post("/profile", data={"_method": "DELETE"})

    # Assert the profile deletion was successful and the user is redirected
    assert response.status_code == 302
    assert b"Sign Up" in test_client.get("/").data


def test_save_video(test_client):
    # Simulate logging in first
    test_client.post("/", data={
        "email_address": "testuser@example.com",
        "password": "hashed_password",
    })

    # Simulate saving a video
    response = test_client.post("/improvement", json={
        "action": "save_video",
        "video_id": "1234",
        "title": "Test Video",
        "url": "http://example.com/video",
        "thumbnail": "http://example.com/thumbnail.jpg",
    })

    # Assert the video was saved successfully
    assert response.status_code == 200
    assert b"Video saved successfully!" in response.data


def test_remove_video(test_client):
    # Simulate logging in first
    test_client.post("/", data={
        "email_address": "testuser@example.com",
        "password": "hashed_password",
    })

    # Simulate removing a video
    response = test_client.post("/improvement", json={
        "action": "remove_video",
        "video_id": "1234",
    })

    # Assert the video was removed successfully
    assert response.status_code == 200
    assert b"Video removed successfully!" in response.data


def test_terms_page(test_client):
    # Simulate a GET request to the terms page
    response = test_client.get("/terms")

    # Assert the terms page loads successfully
    assert response.status_code == 200
    assert b"Terms and Conditions" in response.data
