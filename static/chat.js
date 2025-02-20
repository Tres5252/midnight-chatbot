document.addEventListener("DOMContentLoaded", function () {
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");

    userInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            const message = userInput.value;
            if (message.trim() !== "") {
                appendMessage("You", message);
                fetchAIResponse(message);
                userInput.value = "";
            }
        }
    });

    function appendMessage(sender, text) {
        const messageElement = document.createElement("p");
        messageElement.classList.add(sender === "You" ? "user-text" : "midnight-text");
        messageElement.textContent = sender + ": " + text;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function fetchAIResponse(message) {
        fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ user_input: message }),
        })
        .then(response => response.json())
        .then(data => {
            appendMessage("Midnight", data.response);
        })
        .catch(error => {
            console.error("Error:", error);
            appendMessage("Midnight", "Something is wrong... Try again.");
        });
    }
});

