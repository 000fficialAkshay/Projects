// Function that takes the name of a cookie and returns its value
function getCookie(name) {
    // Start with no cookie value
    let cookieValue = null;
    // Check whether there are any cookies stored in the browser
    if (document.cookie && document.cookie !== '') {
        // Split all cookies into an array.
        // Cookies are separated by semicolons (;)
        const cookies = document.cookie.split(';');
        // Loop through each cookie
        for (let i = 0; i < cookies.length; i++) {
            // Remove any extra spaces from the beginning or end
            // of the current cookie
            const cookie = cookies[i].trim();
            // Check if the current cookie starts with "name="
            // For example, if name is "csrftoken", check for "csrftoken="
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                // Get everything after "name=" and decode it
                // to obtain the actual cookie value
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
                // Stop the loop because we found the cookie
                break;
            }
        }
    }
    // Return the cookie value.
    // If the cookie wasn't found, this returns null.
    return cookieValue;
}

document.addEventListener("DOMContentLoaded", function () {

    // =========================
    // DASHBOARD / DAILY TASKS
    // =========================

    const dailyTasks = document.querySelectorAll(".daily-task");
    dailyTasks.forEach(function (task) {
        const dailyTaskId = task.dataset.dailyTaskId;
        const savedSeconds = Number(task.dataset.actualSeconds);
        const completed = task.dataset.completed === "true";
        const timer = task.querySelector(".timer");
        // If the task is already completed, don't set up a timer for it
        if (completed) {
            return;
        }
        const startButton = task.querySelector(".start");
        const stopButton = task.querySelector(".stop");
        const completeButton = task.querySelector(".complete");
        let interval = null;
        let startTime = 0;
        let elapsedTime = savedSeconds * 1000;
        let isRunning = false;
        update();
        startButton.addEventListener("click", function () {
            if (!isRunning) {
                startTime = Date.now() - elapsedTime;
                interval = setInterval(update, 1000);
                isRunning = true;
            }
        });
        stopButton.addEventListener("click", function () {
            if (isRunning) {
                clearInterval(interval);
                elapsedTime = Date.now() - startTime;
                update();
                isRunning = false;
                const actualSeconds = Math.floor(elapsedTime / 1000);
                fetch(`/updateDailyTask/${dailyTaskId}/`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": getCookie("csrftoken")
                    },
                    body: JSON.stringify({
                        actual_seconds: actualSeconds
                    })
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                });
            }
        });

        completeButton.addEventListener("click", function () {
            if (isRunning) {
                alert("Please stop the timer before completing the task.");
                return;
            }
            const dailyTaskId = completeButton.dataset.dailyTaskId;
            fetch(`/completeDailyTask/${dailyTaskId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    completeButton.remove();
                    startButton.remove();
                    stopButton.remove();
                    task.remove();
                }
            });
        });

        function update() {
            if (isRunning) {
                elapsedTime = Date.now() - startTime;
            }
            let totalSeconds = Math.floor(elapsedTime / 1000);
            let hours = Math.floor(totalSeconds / 3600);
            let minutes = Math.floor((totalSeconds % 3600) / 60);
            let seconds = totalSeconds % 60;
            hours = String(hours).padStart(2, "0");
            minutes = String(minutes).padStart(2, "0");
            seconds = String(seconds).padStart(2, "0");
            timer.textContent = `${hours}:${minutes}:${seconds}`;
        }
    });

    // =========================
    // HISTORY / REVERT TASKS
    // =========================

    const completedTasks = document.querySelectorAll(".completed-task");
    completedTasks.forEach(function (task) {
        const revertButton = task.querySelector(".revert");
        const dailyTaskId = task.dataset.dailyTaskId;
        revertButton.addEventListener("click", function () {
            fetch(`/revertTask/${dailyTaskId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    task.remove();
                }
            });
        });
    });

    document.querySelectorAll(".complete-part").forEach(button => {
        button.addEventListener("click", () => {
            const partId = button.dataset.partId;

            fetch(`/complete-part/${partId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    button.remove();
                }
            });
        });
    });

    document.querySelectorAll(".revert-task").forEach(function (button) {
        button.addEventListener("click", function () {
            const dailyTaskId = button.dataset.id;
            fetch(`/revertTask/${dailyTaskId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    button.closest(".history-card").remove();
                }
            });
        });
    });

});