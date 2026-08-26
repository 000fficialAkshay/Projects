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

document.querySelectorAll(".editButton").forEach(button => {
    button.addEventListener("click", () => {
        const postId = button.dataset.postId;
        const content = document.querySelector(`#content-${postId}`);
        const textarea = document.createElement("textarea");
        const currentContent = content.textContent.replace("Content: ", "");
        textarea.value = currentContent;
        content.replaceWith(textarea);
        const saveButton = document.createElement("button");
        saveButton.innerHTML = "Save";
        textarea.after(saveButton);
        saveButton.addEventListener("click", () => {
            fetch(`/edit/${postId}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: JSON.stringify({
                    content: textarea.value
                })
            })
            .then(response => response.json())
            .then(data => {
                content.textContent = `Content: ${textarea.value}`;
                textarea.replaceWith(content);
                saveButton.remove();
            });
        });
    });
});

document.querySelectorAll(".likeButton").forEach(button => {
    button.addEventListener("click", () => {
        const postId = button.dataset.postId;
        fetch(`/like/${postId}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")
            }
        })
        .then(response => response.json())
        .then(data => {
            const likes = document.querySelector(`#likes-${postId}`);
            likes.innerText = `Likes: ${data.likes}`;
            button.innerText = data.isLiked ? "Dislike" : "Like";
        });
    });
});