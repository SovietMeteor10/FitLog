import pytest
from app.database import init_db, db_session
from app.utils.forms import LoginForm, SignupForm
from app.utils.config import Config


@pytest.fixture(scope="module")
def setup_test_database():
    # Initialize the database schema for testing
    init_db()
    yield db_session
    db_session.remove()


def test_init_db(setup_test_database):
    # Verify that the database initializes correctly
    # Check if the session can query metadata without errors
    try:
        db_session.execute("SELECT 1")
        assert True
    except Exception as e:
        pytest.fail(f"Database initialization failed: {e}")


def test_login_form():
    # Test the LoginForm with valid input
    form = LoginForm(email="test@example.com", password="securepassword")
    assert form.validate() == True

    # Test the LoginForm with invalid input (missing password)
    form = LoginForm(email="test@example.com", password="")
    assert form.validate() == False


def test_signup_form():
    # Test the SignupForm with valid input
    form = SignupForm(
        first_name="John",
        family_name="Doe",
        email="john.doe@example.com",
        password="securepassword",
        confirm_password="securepassword"
    )
    assert form.validate() == True

    # Test the SignupForm with mismatched passwords
    form = SignupForm(
        first_name="John",
        family_name="Doe",
        email="john.doe@example.com",
        password="securepassword",
        confirm_password="wrongpassword"
    )
    assert form.validate() == False

    # Test the SignupForm with invalid email
    form = SignupForm(
        first_name="John",
        family_name="Doe",
        email="not-an-email",
        password="securepassword",
        confirm_password="securepassword"
    )
    assert form.validate() == False


def test_config_class():
    # Test that the Config class correctly loads environment variables
    config = Config()

    # Assert default values are correctly assigned
    assert config.SECRET_KEY == "your_default_secret_key"
    assert config.SQLALCHEMY_DATABASE_URI == "sqlite:///fitness_app.db"

    # Mock environment variables and verify overrides
    import os
    os.environ["SECRET_KEY"] = "new_secret_key"
    os.environ["DATABASE_URL"] = "postgresql://testdb"

    new_config = Config()
    assert new_config.SECRET_KEY == "new_secret_key"
    assert new_config.SQLALCHEMY_DATABASE_URI == "postgresql://testdb"
