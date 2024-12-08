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

    console.log("🔥 [DEBUG] Initiating save video request with:", {
        video_id: videoId,
        title: title,
        url: url,
        thumbnail: thumbnail
    });

    fetch('/improvement/save_video', {
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
    .then(response => {
        console.log("📩 [DEBUG] Response received from server:", response);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log("📩 [DEBUG] Parsed JSON response:", data);
        if (data.success) {
            alert('Video saved successfully!');
            loadSavedVideos(); // Reload saved videos after saving
        } else {
            alert('Failed to save video: ' + data.message);
        }
    })
    .catch(error => {
        console.error("❌ [ERROR] Save video request failed:", error);
        alert('An error occurred while saving the video.');
    });
}

/**
 * Function to remove a video from the saved video list and update the sidebar.
 * @param {HTMLElement} button - The button that triggered the remove action.
 */
function removeVideo(button) {
    const videoId = button.getAttribute('data-video-id');

    console.log("🔥 [DEBUG] Initiating remove video request with:", { video_id: videoId });

    fetch('/improvement/remove_video', {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json' 
        },
        body: JSON.stringify({
            video_id: videoId
        })
    })
    .then(response => {
        console.log("📩 [DEBUG] Response received from server:", response);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log("📩 [DEBUG] Parsed JSON response:", data);
        if (data.success) {
            alert('Video removed successfully!');
            loadSavedVideos(); // Reload saved videos after removal
        } else {
            alert('Failed to remove video: ' + data.message);
        }
    })
    .catch(error => {
        console.error("❌ [ERROR] Remove video request failed:", error);
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
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const savedVideos = doc.querySelectorAll('.saved-videos .video-box');

        const savedVideosContainer = document.querySelector('.saved-videos');
        savedVideosContainer.innerHTML = '<h3>Saved Videos</h3>';

        savedVideos.forEach(video => {
            // Add a "Remove" button to each video box
            const removeButton = document.createElement('button');
            removeButton.textContent = 'Remove';
            removeButton.classList.add('remove-button');
            removeButton.setAttribute('data-video-id', video.getAttribute('data-video-id'));
            removeButton.onclick = function() {
                removeVideo(removeButton);
            };

            video.appendChild(removeButton);
            savedVideosContainer.appendChild(video);
        });
    })
    .catch(error => {
        console.error("❌ [ERROR] Error while loading saved videos:", error);
    });
}
