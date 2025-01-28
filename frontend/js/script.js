const chatMessages = document.getElementById('chat-messages');
const chatInput = document.getElementById('chat-input');
const sendButton = document.getElementById('send-button');
const chatbotContainer = document.querySelector('.chatbot-container');
const chatbotButton = document.querySelector('.chatbot-button');
const closeButton = document.querySelector('.close-button');

// Replace with your actual user ID (if needed)
const userId = "your_user_id";

// Show chatbot when the button is clicked
chatbotButton.addEventListener('click', () => {
    chatbotContainer.style.display = 'flex'; // Show chatbot
    chatbotButton.style.display = 'none'; // Hide the floating button
});

// Hide chatbot when the close button is clicked
closeButton.addEventListener('click', () => {
    chatbotContainer.style.display = 'none'; // Hide chatbot
    chatbotButton.style.display = 'flex'; // Show the floating button
});

function sendMessage() {
  const message = chatInput.value.trim();
  if (message) {
    fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: userId, message })
    })
    .then(response => response.json())
    .then(data => {
      appendMessage(message, 'user');
      appendMessage(data.response, 'bot');
      chatInput.value = ''; // Clear input field
    })
    .catch(error => console.error('Error sending message:', error));
  }
}

function appendMessage(message, role) {
  const messageElement = document.createElement("div");
  messageElement.className = "message " + (role === "user" ? "user-message" : "bot-message");
  messageElement.textContent = message;
  chatMessages.appendChild(messageElement);

  // Scroll to the bottom of the chat
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Add event listener for the send button
sendButton.addEventListener("click", sendMessage);

// Add event listener for pressing Enter in the input field
chatInput.addEventListener("keypress", (event) => {
  if (event.key === "Enter") {
    sendMessage();
  }
});
