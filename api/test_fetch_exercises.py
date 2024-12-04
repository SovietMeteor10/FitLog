from api.get_exercise import fetch_exercises


def test_fetch_exercises_with_youtube():
    exercises = fetch_exercises()
    if "error" in exercises:
        print(f"Error: {exercises['error']}")
    else:
        for exercise in exercises[:3]:  # Display only the first 3 for brevity
            print(f"Name: {exercise['name']}")
            print(f"Description: {exercise['description']}")
            print(f"Category: {exercise['category']}")
            print(f"Target Muscle: {exercise['target']}")
            print(f"Equipment: {exercise['equipment']}")
            print(f"GIF URL: {exercise['gifUrl']}")
            print("YouTube Videos:")
            for video in exercise["youtube_videos"]:
                print(f"  - {video['title']} ({video['url']})")
            print("\n")


if __name__ == "__main__":
    test_fetch_exercises_with_youtube()
