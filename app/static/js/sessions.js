document.addEventListener("DOMContentLoaded", function () {
    const addSessionButton = document.getElementById("add-new-session");
    const newSessionPopup = document.getElementById("new-session-popup");
    const closePopupButton = document.getElementById("close-popup");
    const exercisesContainer = document.getElementById("exercises");
    let exerciseCount = 0;

    // Add New Session Pop-Up
    addSessionButton.addEventListener("click", () => {
        newSessionPopup.style.display = "flex";
        $('#add_exercise').click(); // Add initial exercise on pop-up open
    });

    // Close Pop-Up when clicking close button
    closePopupButton.addEventListener("click", () => {
        newSessionPopup.style.display = "none";
    });

    // Add exercise button handler
    $('#add_exercise').click(function () {
        $('#exercises').append(createExercise());
    });

    // Template for a new exercise
    function createExercise() {
        exerciseCount++;
        return `
            <div class="exercise" data-exercise="${exerciseCount}">
                <label for="exercise_${exerciseCount}">Exercise Name:</label>
                <input type="text" id="exercise_${exerciseCount}" name="exercise_${exerciseCount}" class="exercise-autocomplete" autocomplete="off" required>
                <ul class="autocomplete-results"></ul>

                <div class="sets">
                    <!-- Sets will be added here -->
                </div>

                <button type="button" class="form-button add_set">Add Set</button>
                <button type="button" class="form-button delete_exercise">Delete Exercise</button>
            </div>
        `;
    }

    // Template for a new set
    function createSet(exerciseId, setCount) {
        return `
            <div class="set">
                <label for="weight_${exerciseId}_${setCount}">Weight (kg):</label>
                <input type="number" step="0.5" id="weight_${exerciseId}_${setCount}"
                       name="weight_${exerciseId}_${setCount}" required>

                <label for="reps_${exerciseId}_${setCount}">Reps:</label>
                <input type="number" step="1" id="reps_${exerciseId}_${setCount}"
                       name="reps_${exerciseId}_${setCount}" required>
                <button type="button" class="form-button delete_set">Delete Set</button>
            </div>
        `;
    }

    // Add set button handler (using event delegation)
    $(document).on('click', '.add_set', function () {
        const exerciseDiv = $(this).closest('.exercise');
        const exerciseId = exerciseDiv.data('exercise');
        const setCount = exerciseDiv.find('.set').length + 1;
        exerciseDiv.find('.sets').append(createSet(exerciseId, setCount));
    });

    // Delete exercise button handler (using event delegation)
    $(document).on('click', '.delete_exercise', function () {
        $(this).closest('.exercise').remove();
    });

    // Delete set button handler (using event delegation)
    $(document).on('click', '.delete_set', function () {
        $(this).closest('.set').remove();
    });

    // Autocomplete functionality
    $(document).on('input', '.exercise-autocomplete', function () {
        const input = $(this);
        const query = input.val();
        const resultsList = input.siblings('.autocomplete-results');

        if (query.length > 1) {
            // Fetch suggestions from the server
            $.ajax({
                url: window.location.pathname,  // Sends request to the current route
                type: 'GET',
                data: { q: query },
                success: function (response) {
                    resultsList.empty();
                    response.forEach(exercise => {
                        const listItem = $('<li></li>').text(exercise.name).attr('data-id', exercise.id).addClass('autocomplete-item');
                        listItem.on('click', function () {
                            input.val($(this).text());
                            resultsList.empty(); // Clear suggestions
                        });
                        resultsList.append(listItem);
                    });
                },
                error: function () {
                    resultsList.empty();
                    resultsList.append('<li class="autocomplete-item">Error fetching suggestions</li>');
                }
            });
        } else {
            resultsList.empty(); // Clear suggestions for short queries
        }
    });

    // Hide suggestions when clicking outside
    $(document).on('click', function (e) {
        if (!$(e.target).closest('.exercise-autocomplete, .autocomplete-results').length) {
            $('.autocomplete-results').empty();
        }
    });
});



    /*// Submit session handler
    document.getElementById("new-session-form").addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent default form submission

        // Placeholder for backend logic to save session data
        // Send session data to backend API for storage here

        // Create new session entry for the table
        const sessionName = document.getElementById("session_name").value;
        const sessionDate = document.getElementById("date").value;
        const newRow = document.createElement("tr");

        // Add tooltip with exercise details
        let tooltip = `Session: ${sessionName}\nDate: ${sessionDate}\nExercises:\n`;
        document.querySelectorAll(".exercise").forEach(exercise => {
            const exerciseName = exercise.querySelector("input[type='text']").value;
            tooltip += `  - ${exerciseName}\n`;
            exercise.querySelectorAll(".set").forEach(set => {
                const weight = set.querySelector("input[name^='weight']").value;
                const reps = set.querySelector("input[name^='reps']").value;
                tooltip += `      Set: Weight: ${weight} kg, Reps: ${reps}\n`;
            });
        });

        newRow.innerHTML = `
            <td>${sessionDate}</td>
            <td title="${tooltip}">${sessionName}</td>
            <td>Duration Placeholder</td> <!-- Placeholder for duration -->
        `;
        sessionsList.appendChild(newRow);

        // Close the pop-up
        newSessionPopup.style.display = "none";
    });*/
