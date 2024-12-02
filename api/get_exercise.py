import requests
from app.config import Config

# Prepare headers with the API key
headers = {
    # Adjust based on API docs; might be "Token" instead of "Bearer"
    "Authorization": f"Token {Config.API_KEY}",
}


def fetch_exercises():
    try:
        # Make the API request
        response = requests.get(Config.API_URL, headers=headers)

        # Check the response status code
        if response.status_code == 200:
            # Parse the JSON data
            data = response.json()

            # Extract the "results" key
            exercises_data = data.get("results", [])

            exercises = []
            for exercise in exercises_data:
                exercises.append(
                    {
                        "name": exercise.get("name", "Unknown"),
                        "description": exercise.get(
                            "description", "No description available"
                        ),
                        "category": exercise.get("category", {}).get(
                            "name", "Uncategorized"
                        ),  # Nested dictionary
                        "muscle_group": exercise.get(
                            "muscles", []
                        ),  # List of muscle groups
                        "image": exercise.get("images", [{}])[0].get(
                            "image", None
                        ),  # List with potential images
                    }
                )

            return exercises
        else:
            # Handle non-200 responses
            return {"error": "Status code: {response.status_code}"}

    except requests.RequestException as e:
        # Handle network or other request exceptions
        return {"error": f"An error occurred: {str(e)}"}
