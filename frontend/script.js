const form = document.getElementById("chat-form");
const input = document.getElementById("user-input");
const chatBody = document.getElementById("chat-body");

const API_URL = "http://localhost:8000/chat";

// Helper: add message to UI
function addMessage(text, sender) {
  const div = document.createElement("div");
  div.className = sender === "user" ? "user-message" : "bot-message";
  div.textContent = text;
  chatBody.appendChild(div);
  chatBody.scrollTop = chatBody.scrollHeight;
}

// Helper: typing indicator
function showTyping() {
  const div = document.createElement("div");
  div.className = "bot-message typing";
  div.id = "typing-indicator";
  div.textContent = "Typing...";
  chatBody.appendChild(div);
  chatBody.scrollTop = chatBody.scrollHeight;
}

function removeTyping() {
  const typing = document.getElementById("typing-indicator");
  if (typing) typing.remove();
}

// THIS IS THE IMPORTANT PART
form.addEventListener("submit", async (e) => {
  e.preventDefault(); // prevents page reload

  const message = input.value.trim();
  if (!message) return;

  // Show user message
  addMessage(message, "user");
  input.value = "";

  // Show typing
  showTyping();

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_message: message,
        session_id: "demo",
        model: "claude"  // or "titan"
      })
    });

    const data = await response.json();
    removeTyping();
    addMessage(data.response || "No response", "bot");

  } catch (error) {
    removeTyping();
    addMessage("❌ Backend error", "bot");
    console.error(error);
  }
});
