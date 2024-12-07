document.addEventListener('DOMContentLoaded', function () {
    loadSavedVideos(); // Load saved videos on page load
});

function saveVideo(button) {
    const videoId = button.getAttribute('data-video-id');
    const title = button.getAttribute('data-title');
    const url = button.getAttribute('data-url');
    const thumbnail = button.getAttribute('data-thumbnail');

    console.log("Button data attributes:", {
        video_id: videoId,
        title: title,
        url: url,
        thumbnail: thumbnail
    });

    fetch('/improvement', {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json' 
        },
        body: JSON.stringify({
            video_id: videoId,
            title: title,
            url: url,
            thumbnail: thumbnail
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Video saved successfully!');
            loadSavedVideos();
        } else {
            alert('Failed to save video: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while saving the video.');
    });
}




function loadSavedVideos() {
    fetch('/improvement')
    .then(response => response.text())
    .then(html => {
        // Create a temporary container to parse the HTML response
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        
        // Extract the saved videos section
        const savedVideos = doc.querySelectorAll('.saved-videos .video-box');

        // Clear the current saved videos section
        const savedVideosContainer = document.querySelector('.saved-videos');
        savedVideosContainer.innerHTML = '<h3>Saved Videos</h3>';
        
        // Append the extracted saved videos to the saved videos section
        savedVideos.forEach(video => {
            savedVideosContainer.appendChild(video);
        });
    })
    .catch(error => console.error('Error loading saved videos:', error));
}
