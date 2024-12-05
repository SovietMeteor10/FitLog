document.getElementById("login-form").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent the form from submitting normally

    const formData = {
        email: document.getElementById("email").value,
        password: document.getElementById("password").value
    };

    fetch("/auth/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json().then(data => ({ status: response.status, body: data })))
    .then(result => {
        if (result.status === 200) {
            // Redirect based on backend response
            window.location.href = result.body.redirect;
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

