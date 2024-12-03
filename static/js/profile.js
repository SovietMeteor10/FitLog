document.getElementById('weight').addEventListener('input', calculateBMI);
document.getElementById('height').addEventListener('input', calculateBMI);

function calculateBMI() {
    const weight = parseFloat(document.getElementById('weight').value);
    const heightFeet = parseFloat(document.getElementById('height').value);

    if (weight > 0 && heightFeet > 0) {
        const heightMeters = heightFeet * 0.3048; // Convert height from feet to meters
        const bmi = weight / (heightMeters * heightMeters);
        document.getElementById('bmi').value = bmi.toFixed(2);
    }
}
