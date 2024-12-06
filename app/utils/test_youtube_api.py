from youtube_api import search_youtube_videos

def test_search_youtube_videos():
    try:
        # Test with a sample query
        query = "bench press exercise"
        videos = search_youtube_videos(query)
        
        # Print results for verification
        print(f"Search results for '{query}':")
        for video in videos:
            print(f"Title: {video['title']}")
            print(f"URL: {video['url']}")
            print(f"Thumbnail: {video['thumbnail']}")
            print("-" * 40)
    except Exception as e:
        print(f"Error during test: {e}")

if __name__ == "__main__":
    test_search_youtube_videos()
