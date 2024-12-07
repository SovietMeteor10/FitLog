import requests


YOUTUBE_API_KEY = "AIzaSyB0DWNypHqqZoKOuNzuLDo39Tm22zJzMg8"
YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/search"


def search_youtube_videos(query):
    try:
        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "maxResults": 4,
            "key": YOUTUBE_API_KEY,
        }
        response = requests.get(YOUTUBE_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        videos = [
            {
                "id": item["id"]["videoId"],
                "title": item["snippet"]["title"],
                "thumbnail": item["snippet"]["thumbnails"]["high"]["url"],
                "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
            }
            for item in data.get("items", [])
        ]
        return videos
    except Exception as e:
        print(f"Error fetching YouTube videos: {e}")
        return []
