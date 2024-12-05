document.addEventListener("DOMContentLoaded", function () {
    const addSessionButton = document.getElementById("add-new-session");
    const newSessionPopup = document.getElementById("new-session-popup");
    const addExerciseButton = document.getElementById("add-exercise-button");
    const exerciseType = document.getElementById("exercise-type");
    const weightBasedFields = document.getElementById("weight-based-fields");
    const cardioBasedFields = document.getElementById("cardio-based-fields");
    const exercisesList = document.getElementById("exercise-items");
    const submitSessionButton = document.getElementById("submit-session");
    const exerciseDropdown = document.getElementById("exercise-type");

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

    // Fetch exercises from the backend API and populate the dropdown
    async function populateExerciseDropdown() {
        try {
            const response = await fetch("/get_exercises"); // Call the API route
            const fetchedExercises = await response.json();

            // Clear loading placeholder and populate exercises
            exerciseDropdown.innerHTML = "<option value=''>Select...</option>";
            fetchedExercises.forEach((exercise) => {
                const option = document.createElement("option");
                option.value = exercise.id; // Use the exercise ID
                option.textContent = exercise.name; // Use the exercise name
                exerciseDropdown.appendChild(option);
            });
        } catch (error) {
            console.error("Error fetching exercises:", error);
            exerciseDropdown.innerHTML = "<option value=''>Error loading exercises</option>";
        }
    }

    // Call the populate function on page load
    populateExerciseDropdown();

    // Add Exercise Button
    addExerciseButton.addEventListener("click", () => {
        const type = exerciseType.value;
        const selectedExerciseText = exerciseDropdown.options[exerciseDropdown.selectedIndex].text;

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

        // Add exercise details
        exerciseData.name = selectedExerciseText;

        exercises.push(exerciseData);
        updateExercisesList();
    });

    // Update Exercises List
    function updateExercisesList() {
        exercisesList.innerHTML = "";

        exercises.forEach((exercise, index) => {
            const listItem = document.createElement("li");
            listItem.textContent = `${exercise.name} (${exercise.type})`;

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
        if (exercises.length === 0) {
            alert("Please add at least one exercise to the session.");
            return;
        }

        // Gather session data
        const sessionData = {
            date: document.getElementById("session-date").value,
            duration: {
                hours: document.getElementById("session-duration-hours").value,
                minutes: document.getElementById("session-duration-minutes").value,
            },
            name: document.getElementById("session-name").value,
            exercises: exercises,
        };

        // Placeholder for submitting session to backend
        console.log("Submitting session:", sessionData);

        // Clear the popup and reset the form
        exercises = [];
        updateExercisesList();
        newSessionPopup.style.display = "none";
        alert("Session submitted successfully.");
    });
});
