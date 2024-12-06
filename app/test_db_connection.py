from sqlalchemy.sql import text
from database import db_session


def test_db_connection():
    try:
        # Wrap raw SQL query in text()
        result = db_session.execute(text("SELECT 1")).scalar()
        if result == 1:
            print("Database connection successful!")
        else:
            print("Unexpected result:", result)
    except Exception as e:
        print(f"Database connection test failed: {e}")
    finally:
        db_session.close()


if __name__ == "__main__":
    test_db_connection()
