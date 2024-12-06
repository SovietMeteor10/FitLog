# Use the app factory pattern to create an instance of the Flask application

from app import create_app, db
from app.database import init_db

# Create an instance of the Flask application
app = create_app()

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    # Run the app in debug mode for development
    init_db()
    app.run(debug=True)