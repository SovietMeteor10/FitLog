document.addEventListener("DOMContentLoaded", function () {
    const addSessionButton = document.getElementById("add-new-session");
    const newSessionPopup = document.getElementById("new-session-popup");
    const addExerciseButton = document.getElementById("add-exercise-button");
    const exerciseType = document.getElementById("exercise-type");
    const weightBasedFields = document.getElementById("weight-based-fields");
    const cardioBasedFields = document.getElementById("cardio-based-fields");
    const exercisesList = document.getElementById("exercise-items");
    const submitSessionButton = document.getElementById("submit-session");

    let exercises = [];

    // Add New Session Pop-Up
    addSessionButton.addEventListener("click", () => {
        newSessionPopup.style.display = "flex";
    });

    // Close Pop-Up when clicking outside content
    document.addEventListener("click", (event) => {
        if (event.target === newSessionPopup) {
            newSessionPopup.style.display = "none";
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

    // Add Exercise Button
    addExerciseButton.addEventListener("click", () => {
        const type = exerciseType.value;

        if (!type) {
            alert("Please select an exercise type.");
            return;
        }

        let exerciseData = { type };

        if (type === "treadmill") {
            exerciseData.distance = document.getElementById("distance").value;
            exerciseData.timeSpent = document.getElementById("time-spent").value;
        } else {
            exerciseData.sets = document.getElementById("sets").value;
            exerciseData.reps = document.getElementById("reps").value;
            exerciseData.weight = document.getElementById("weight").value;
        }

        exercises.push(exerciseData);
        updateExercisesList();
    });

    // Update Exercises List
    function updateExercisesList() {
        exercisesList.innerHTML = "";

        exercises.forEach((exercise, index) => {
            const listItem = document.createElement("li");
            listItem.textContent = `${exercise.type}`;
            const editButton = document.createElement("button");
            editButton.textContent = "Edit";
            editButton.className = "edit-button";
            editButton.addEventListener("click", () => {
                // Add logic to edit exercise
            });
            const deleteButton = document.createElement("button");
            deleteButton.textContent = "Delete";
            deleteButton.className = "delete-button";
            deleteButton.addEventListener("click", () => {
                exercises.splice(index, 1);
                updateExercisesList();
            });
            listItem.appendChild(editButton);
            listItem.appendChild(deleteButton);
            exercisesList.appendChild(listItem);
        });
    }

    // Submit New Session
    submitSessionButton.addEventListener("click", () => {
        // Placeholder for submitting session to backend
        newSessionPopup.style.display = "none";
        alert("Session submitted successfully.");
    });
});

