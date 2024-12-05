// Pre-load profile data if it exists
document.addEventListener('DOMContentLoaded', function() {
    fetch('/profile/get')
        .then(response => response.json())
        .then(data => {
            document.getElementById('first_name').value = data.first_name || '';
            document.getElementById('family_name').value = data.family_name || '';
            document.getElementById('age').value = data.age || '';
            document.getElementById('sex').value = data.sex || '';
            document.getElementById('height').value = data.height || '';
            document.getElementById('weight').value = data.weight || '';
            document.getElementById('bmi').value = data.bmi || '';
        })
        .catch(error => {
            console.error('Error loading profile data:', error);
        });
});

// Handle BMI calculation
document.getElementById('weight').addEventListener('input', calculateBMI);
document.getElementById('height').addEventListener('input', calculateBMI);

function calculateBMI() {
    const weight = parseFloat(document.getElementById('weight').value);
    const heightCm = parseFloat(document.getElementById('height').value);

    if (weight > 0 && heightCm > 0) {
        const heightMeters = heightCm / 100; // Convert height from cm to meters
        const bmi = weight / (heightMeters * heightMeters);
        document.getElementById('bmi').value = bmi.toFixed(2);
    }
}

// Handle form submission
document.getElementById('profile-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission

    const formData = new FormData(document.getElementById('profile-form'));

    fetch('/profile/complete', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            // Redirect to main page after successful submission
            window.location.href = '/main';
        } else {
            alert('Error: ' + result.message);
        }
    })
    .catch(error => {
        alert('An error occurred while submitting your profile: ' + error.message);
    });
});
