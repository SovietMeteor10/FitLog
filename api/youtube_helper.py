import requests
from urllib.parse import urlencode

YOUTUBE_API_BASE_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_API_KEY = (
    "AIzaSyB0DWNypHqqZoKOuNzuLDo39Tm22zJzMg8"  # Replace with your actual API key
)


def fetch_youtube_videos(query, max_results=5):
    """
    Fetches YouTube videos related to the given query.
    :param query: The search query (e.g., exercise name or category).
    :param max_results: Number of results to return.
    :return: A list of video details.
    """
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": max_results,
        "key": YOUTUBE_API_KEY,
    }

    try:
        response = requests.get(f"{YOUTUBE_API_BASE_URL}?{urlencode(params)}")
        if response.status_code == 200:
            data = response.json()
            videos = []
            for item in data.get("items", []):
                videos.append(
                    {
                        "title": item["snippet"]["title"],
                        "description": item["snippet"]["description"],
                        "videoId": item["id"]["videoId"],
                        "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                    }
                )
            return videos
        else:
            return {
                "error": f"Failed to fetch videos. Status code: {response.status_code}"
            }

    except requests.RequestException as e:
        return {"error": f"An error occurred: {str(e)}"}
