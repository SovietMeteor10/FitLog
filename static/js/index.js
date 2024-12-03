document.addEventListener("DOMContentLoaded", function () {
    // Load pinned videos from the backend when the main page loads
    loadPinnedVideos();
});

function loadPinnedVideos() {
    // Placeholder for backend logic to load pinned videos
    // This could be a GET request to the backend API to retrieve the user's pinned videos

    // Example:
    /*
    fetch('/api/get_pinned_videos')
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            updatePinnedVideos(result.videos);
        } else {
            console.error('Error loading pinned videos');
        }
    })
    .catch(error => {
        console.error('Error communicating with server:', error);
    });
    */

    // Simulating backend data for demonstration purposes
    const pinnedVideos = [
        { id: 'video1', title: 'Sample Video 1' },
        { id: 'video2', title: 'Sample Video 2' }
    ];
    updatePinnedVideos(pinnedVideos);
}

function updatePinnedVideos(pinnedVideos) {
    const video1Container = document.getElementById("video-1");
    const video2Container = document.getElementById("video-2");

    // Clear existing content
    video1Container.innerHTML = '';
    video2Container.innerHTML = '';

    if (pinnedVideos.length > 0) {
        // Populate video-1 and video-2 with pinned video details from the backend
        const firstVideo = pinnedVideos[0];
        video1Container.innerHTML = `<p>${firstVideo.title}</p>`;

        if (pinnedVideos.length > 1) {
            const secondVideo = pinnedVideos[1];
            video2Container.innerHTML = `<p>${secondVideo.title}</p>`;
        }
    } else {
        // If no pinned videos, display placeholder
        video1Container.innerHTML = '<p>No video pinned</p>';
        video2Container.innerHTML = '<p>No video pinned</p>';
    }
}

