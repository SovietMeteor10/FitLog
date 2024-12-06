// Function to save a video into the "Saved Videos" section
function saveVideo(videoId, videoTitle, videoUrl) {
    const savedVideosContainer = document.querySelector('.saved-videos');
    const existingSlots = savedVideosContainer.querySelectorAll('.video-box');

    // Check if the limit of 10 saved videos is reached
    if (existingSlots.length >= 10) {
        alert("The maximum of 10 saved videos has been reached. Remove a video to save more.");
        return;
    }

    // Create a new video slot
    const videoSlot = document.createElement('div');
    videoSlot.className = 'video-box';

    // Create the video link
    const videoLink = document.createElement('a');
    videoLink.href = videoUrl;
    videoLink.target = '_blank';
    videoLink.innerText = videoTitle;

    // Create the remove button
    const removeButton = document.createElement('button');
    removeButton.className = 'remove-button';
    removeButton.innerText = 'Remove';
    removeButton.onclick = () => removeVideo(videoSlot);

    // Append the link and the button to the new slot
    videoSlot.appendChild(videoLink);
    videoSlot.appendChild(removeButton);

    // Add the new video slot to the saved videos container
    savedVideosContainer.appendChild(videoSlot);

    alert(`Video "${videoTitle}" has been saved!`);
}

// Function to remove a video from the "Saved Videos" section
function removeVideo(videoSlot) {
    videoSlot.remove();
    alert("Video has been removed.");
}
