import pytest
from app.database import init_db, db_session
from app.models import User, Session, SavedVideo

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
        password="hashed_password"
    )
    db_session.add(user)
    db_session.commit()

    # Verify the user was created
    retrieved_user = db_session.query(User).filter_by(email_address="testuser@example.com").first()
    assert retrieved_user is not None
    assert retrieved_user.first_name == "Test"
    assert retrieved_user.family_name == "User"


def test_session_creation(setup_database):
    # Create a new user and a session
    user = User(
        first_name="Session",
        family_name="Tester",
        email_address="sessiontester@example.com",
        password="hashed_password"
    )
    db_session.add(user)
    db_session.commit()

    session = Session(
        user_id=user.user_id,
        session_name="Test Session",
        date="2023-12-08",
        duration=60.0
    )
    db_session.add(session)
    db_session.commit()

    # Verify the session was created and linked to the user
    retrieved_session = db_session.query(Session).filter_by(session_name="Test Session").first()
    assert retrieved_session is not None
    assert retrieved_session.user_id == user.user_id


def test_cascade_delete_user(setup_database):
    # Create a user and a related session and video
    user = User(
        first_name="Cascade",
        family_name="Delete",
        email_address="cascade@example.com",
        password="hashed_password"
    )
    db_session.add(user)
    db_session.commit()

    session = Session(
        user_id=user.user_id,
        session_name="Cascade Session",
        date="2023-12-08",
        duration=45.0
    )
    db_session.add(session)

    video = SavedVideo(
        user_id=user.user_id,
        video_id="12345",
        title="Test Video",
        url="http://example.com/video",
        thumbnail="http://example.com/thumbnail.jpg"
    )
    db_session.add(video)
    db_session.commit()

    # Delete the user
    db_session.delete(user)
    db_session.commit()

    # Verify related data is also deleted
    assert db_session.query(Session).filter_by(session_name="Cascade Session").first() is None
    assert db_session.query(SavedVideo).filter_by(video_id="12345").first() is None


def test_saved_video_creation(setup_database):
    # Create a user and a saved video
    user = User(
        first_name="Video",
        family_name="Saver",
        email_address="videosaver@example.com",
        password="hashed_password"
    )
    db_session.add(user)
    db_session.commit()

    video = SavedVideo(
        user_id=user.user_id,
        video_id="67890",
        title="Example Video",
        url="http://example.com/examplevideo",
        thumbnail="http://example.com/examplethumbnail.jpg"
    )
    db_session.add(video)
    db_session.commit()

    # Verify the video was saved
    retrieved_video = db_session.query(SavedVideo).filter_by(video_id="67890").first()
    assert retrieved_video is not None
    assert retrieved_video.title == "Example Video"
