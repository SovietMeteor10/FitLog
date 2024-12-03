// JavaScript for the Stats Page - stats.js

document.addEventListener("DOMContentLoaded", function () {
    // Add event listeners for each recommended video to pin them
    const videoElements = document.querySelectorAll(".video-card");

    videoElements.forEach(video => {
        video.addEventListener("click", function () {
            const videoId = this.getAttribute("data-video-id");
            const videoTitle = this.querySelector("h3").innerText;

            pinVideo(videoId, videoTitle);
        });
    });
});

function pinVideo(videoId, videoTitle) {
    // Placeholder for backend logic to save pinned video
    // This could be a POST request to the backend API to save the video for the user

    // Example:
    /*
    fetch('/api/pin_video', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ videoId, videoTitle })
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            alert(`${videoTitle} has been pinned to your main page!`);
        } else {
            alert('An error occurred while pinning the video.');
        }
    })
    .catch(error => {
        alert('An error occurred while communicating with the server.');
    });
    */

    alert(`${videoTitle} has been pinned! (Simulating backend request)`);
}
