import pytest
from app.database import init_db, db_session
from app.models import User


@pytest.fixture(scope="module")
def setup_database():
    # Initialize the database schema for testing
    init_db()
    yield db_session
    db_session.remove()


def test_user_creation(setup_database):
    # Create a new user
    user = User(
        first_name="Test",
        family_name="User",
        email_address="testuser@example.com",
        password="hashed_password",
    )
    db_session.add(user)
    db_session.commit()

    # Verify the user was created
    retrieved_user = (
        db_session.query(User).filter_by(email_address="testuser@example.com").first()
    )
    assert retrieved_user is not None
    assert retrieved_user.first_name == "Test"
    assert retrieved_user.family_name == "User"


def test_session_creation(setup_database):
    # Create a new user and a session
    user = User(
        first_name="Session",
        family_name="Tester",
        email_address="sessiontester@example.com",
        password="hashed_password",
    )
    db_session.add(user)
    db_session.commit()