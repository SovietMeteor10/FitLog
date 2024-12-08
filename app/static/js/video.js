// Wait until the page content is fully loaded
document.addEventListener('DOMContentLoaded', function () {
    loadSavedVideos(); // Load saved videos on page load
});

/**
 * Function to save a video to the saved video list.
 * @param {HTMLElement} button - The button that triggered the save action.
 */
function saveVideo(button) {
    const videoId = button.getAttribute('data-video-id');
    const title = button.getAttribute('data-title');
    const url = button.getAttribute('data-url');
    const thumbnail = button.getAttribute('data-thumbnail');

    console.log("Button data attributes for save:", {
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
            action: 'save_video', // ✅ Action for saving the video
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
            loadSavedVideos(); // ✅ Reload saved videos on success
        } else {
            alert('Failed to save video: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error while saving video:', error);
        alert('An error occurred while saving the video.');
    });
}

/**
 * Function to remove a video from the saved video list.
 * @param {HTMLElement} button - The button that triggered the remove action.
 */
function removeVideo(button) {
    const videoId = button.getAttribute('data-video-id');

    console.log("Removing video with ID:", videoId);

    fetch('/improvement', {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json' 
        },
        body: JSON.stringify({
            action: 'remove_video', // ✅ Action for removing the video
            video_id: videoId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Video removed successfully!');
            loadSavedVideos(); // ✅ Reload saved videos on success
        } else {
            alert('Failed to remove video: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error while removing video:', error);
        alert('An error occurred while removing the video.');
    });
}

/**
 * Function to load saved videos and update the sidebar.
 */
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
    .catch(error => console.error('Error while loading saved videos:', error));
}
