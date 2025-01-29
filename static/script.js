document.getElementById("askButton").addEventListener("click", function () {
    const query = document.getElementById("query").value;

    if (query.trim() === "") {
        return;
    }

    // Display the user's message in the chat box
    appendMessage(query, 'user');

    // Clear the textarea
    document.getElementById("query").value = '';

    // Send the query to the backend
    fetch('http://127.0.0.1:5000/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: query })
    })
        .then(response => response.json())
        .then(data => {
            // Display the AI's response in the chat box
            appendMessage(data.response, 'ai');
        })
        .catch(error => {
            console.error('Error:', error);
        });
});

// Function to append messages to the chat box
function appendMessage(message, sender) {
    const chatBox = document.getElementById("chat-box");

    const messageElement = document.createElement("div");
    messageElement.classList.add("message");
    messageElement.classList.add(sender === 'user' ? "user-message" : "ai-message");
    messageElement.innerText = message;

    chatBox.appendChild(messageElement);

    // Scroll to the latest message
    chatBox.scrollTop = chatBox.scrollHeight;
}
