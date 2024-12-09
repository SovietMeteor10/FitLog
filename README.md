# FitLog

## **Overview**
FitLog is a fitness tracking application designed to help users monitor their workout sessions, visualize progress, and set fitness goals. The app features user authentication, profile management, exercise statistics visualization, and integration with external APIs for additional fitness resources.

---

## **Features**
- **User Authentication**: Secure login, signup, and logout functionality.
- **Profile Management**: Update personal details, gym goals, and physical attributes.
- **Workout Session Tracking**: Log and manage workout sessions with associated exercises.
- **Statistics Dashboard**:
  - Line graph of workout durations.
  - Heatmap of weekly workout frequency.
  - Radial graph showing exercise category distribution.
- **Video Suggestions**: Integrated YouTube API to provide exercise-related video recommendations.
- **Saved Videos**: Save and manage video resources for easy access.

---

## **Getting Started**

### **1. Prerequisites**
- Python 3.10 or later
- PostgreSQL database
- A valid RapidAPI key (for exercise data)

### **2. Installation**

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/FitLog.git
   cd FitLog
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Create a `.env` file in the root directory and add the following:
     ```env
     SECRET_KEY=your_secret_key
     DATABASE_URL=your_database_url
     RAPIDAPI_KEY=your_rapidapi_key
     ```

5. Initialize the database:
   ```bash
   python -m app.database init_db
   ```

6. Run the application:
   ```bash
   python wsgi.py
   ```

### **3. Accessing the Application**
The app will be available at `http://127.0.0.1:5000`.

---

## **Project Structure**

```
FitLog/
├── app/
│   ├── __init__.py          # App initialization and blueprint registration
│   ├── routes/              # Route handlers
│   │   ├── main_routes.py
│   │   ├── profile_routes.py
│   │   ├── improv_routes.py
│   │   ├── stats_routes.py
│   │   └── terms_routes.py
│   ├── utils/               # Utility modules
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── database.py
│   │   └── forms.py
│   ├── models.py            # SQLAlchemy ORM models
├── tests/                   # Test suite
│   ├── test_routes.py       # Unit tests for route handlers
│   ├── test_models.py       # Unit tests for models
│   └── test_db_connection.py # Verifies database connectivity
├── requirements.txt         # Python dependencies
├── pytest.ini               # Pytest configuration
├── wsgi.py                  # WSGI entry point
├── README.md                # Project documentation
└── .env.example             # Example environment variables
```

---

## **Technologies Used**
- **Backend**: Flask, Flask-WTF, Flask-JWT-Extended
- **Database**: PostgreSQL, SQLAlchemy
- **Visualization**: Plotly, Pandas
- **APIs**: YouTube API, ExerciseDB API

---

## **Testing**

### **Unit Tests**
- The project uses `pytest` for testing.
- Tests are located in the `tests/` directory.

### **Run Tests**
1. Ensure dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the test suite:
   ```bash
   pytest
   ```

### **Pytest Configuration**
- The `pytest.ini` file in the root directory includes configurations for running tests:
  ```ini
  [pytest]
  testpaths = tests
  addopts = --disable-warnings
  ```
- This ensures tests are discovered in the `tests/` directory and warnings are suppressed for cleaner output.

---

## **Contributing**
We welcome contributions! To contribute:
1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes and push:
   ```bash
   git commit -m "Add feature description"
   git push origin feature-name
   ```
4. Submit a pull request.

---

## **License**
This project is licensed under the MIT License. See `LICENSE` for more information.

---

## **Contact**
For questions or support, reach out to [your-email@example.com].
