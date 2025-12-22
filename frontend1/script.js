/* ================= ELEMENTS ================= */
const chatToggle = document.getElementById("chat-toggle");
const chatWidget = document.getElementById("chat-widget");
const chatClose = document.getElementById("chat-close");

const form = document.getElementById("chat-form");
const input = document.getElementById("user-input");
const chatBody = document.getElementById("chat-body");

/* ================= CONFIG ================= */
const API_URL = "http://localhost:8000/chat";

/* ================= UI HELPERS ================= */
function addMessage(text, sender) {
  const div = document.createElement("div");
  div.className = sender === "user" ? "user-message" : "bot-message";
  div.textContent = text;
  chatBody.appendChild(div);
  chatBody.scrollTop = chatBody.scrollHeight;
}

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

/* ================= CHATBOT TOGGLE ================= */
chatToggle.addEventListener("click", () => {
  chatWidget.classList.remove("hidden");
  chatToggle.style.display = "none";
  input.focus();
});

chatClose.addEventListener("click", () => {
  chatWidget.classList.add("hidden");
  chatToggle.style.display = "flex";
});

/* ================= FORM SUBMIT ================= */
form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const message = input.value.trim();
  if (!message) return;

  addMessage(message, "user");
  input.value = "";
  showTyping();

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_message: message,
        session_id: "demo",
        model: "claude" // or "titan"
      })
    });

    const data = await response.json();
    removeTyping();
    addMessage(data.response || "No response from backend", "bot");

  } catch (error) {
    removeTyping();
    addMessage("❌ Backend error. Please try again.", "bot");
    console.error(error);
  }
});
