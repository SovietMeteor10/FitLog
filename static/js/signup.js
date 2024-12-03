document.getElementById("signup-form").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent the form from submitting normally

    // Collect form data
    const formData = {
        username: document.getElementById("name").value,
        email: document.getElementById("email").value,
        password: document.getElementById("password").value
    };

    // Send data to backend for registration
    fetch("/auth/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json().then(data => ({ status: response.status, body: data })))
    .then(result => {
        if (result.status === 201) {
            // Successful registration, redirect to profile completion page
            window.location.href = "/profile";
        } else {
            // Handle error message
            const messageElement = document.getElementById("message");
            messageElement.textContent = "Error: " + result.body.message;
            messageElement.className = "message error";
            messageElement.style.display = "block";
        }
    })
    .catch(error => {
        const messageElement = document.getElementById("message");
        messageElement.textContent = "An error occurred while processing your request.";
        messageElement.className = "message error";
        messageElement.style.display = "block";
    });
});
