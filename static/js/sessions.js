document.addEventListener("DOMContentLoaded", function () {
    const addSessionButton = document.getElementById("add-new-session");
    const newSessionPopup = document.getElementById("new-session-popup");
    const addExerciseButton = document.getElementById("add-exercise-button");
    const addExercisePopup = document.getElementById("add-exercise-popup");
    const exerciseType = document.getElementById("exercise-type");
    const weightBasedFields = document.getElementById("weight-based-fields");
    const cardioBasedFields = document.getElementById("cardio-based-fields");
    const exercisesList = document.getElementById("exercises-list");
    const enterExerciseButton = document.getElementById("enter-exercise");
    const submitSessionButton = document.getElementById("submit-session");

    // Add New Session Pop-Up
    addSessionButton.addEventListener("click", () => {
        newSessionPopup.style.display = "flex";
    });

    // Add Exercise Button in New Session Pop-Up
    addExerciseButton.addEventListener("click", () => {
        addExercisePopup.style.display = "flex";
    });

    // Close Pop-Up when clicking outside content
    document.addEventListener("click", (event) => {
        if (event.target === newSessionPopup) {
            newSessionPopup.style.display = "none";
        } else if (event.target === addExercisePopup) {
            addExercisePopup.style.display = "none";
        }
    });

    // Show different fields based on exercise type
    exerciseType.addEventListener("change", () => {
        if (exerciseType.value === "treadmill") {
            weightBasedFields.style.display = "none";
            cardioBasedFields.style.display = "block";
        } else {
            cardioBasedFields.style.display = "none";
            weightBasedFields.style.display = "block";
        }
    });

    // Enter Exercise and add to the list
    enterExerciseButton.addEventListener("click", () => {
        const selectedExercise = exerciseType.value;
        if (selectedExercise) {
            const exerciseElement = document.createElement("div");
            exerciseElement.textContent = selectedExercise;
            exercisesList.appendChild(exerciseElement);
            addExercisePopup.style.display = "none";
        }
    });

    // Submit Session Button
    submitSessionButton.addEventListener("click", () => {
        newSessionPopup.style.display = "none";
        // Placeholder for backend logic to save session
        // Navigate back to the sessions list, add new session to the table dynamically if needed
    });
});

