lucide.createIcons();

const socket = new WebSocket("ws://localhost:8000/ws/chat/");
const chatDiv = document.getElementById("chat");
const msgInput = document.getElementById("msgBox");
const sendBtn = document.getElementById("sendBtn");

let botTypingElement = null;
let isBotTyping = false;

function formatTimestamp() {
  const now = new Date();
  return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function appendMessage(role, content) {
  const container = document.createElement("div");
  container.className = `message ${role}`;

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = content;

  const timestamp = document.createElement("div");
  timestamp.className = "timestamp";
  timestamp.innerText = formatTimestamp();

  container.appendChild(bubble);
  container.appendChild(timestamp);
  chatDiv.appendChild(container);
  chatDiv.scrollTop = chatDiv.scrollHeight;

  return bubble;
}

function showTypingIndicator() {
  if (botTypingElement) return;

  botTypingElement = document.createElement("div");
  botTypingElement.className = "message bot typing";
  botTypingElement.innerText = "Typing...";
  chatDiv.appendChild(botTypingElement);
  chatDiv.scrollTop = chatDiv.scrollHeight;
}

function removeTypingIndicator() {
  if (botTypingElement) {
    chatDiv.removeChild(botTypingElement);
    botTypingElement = null;
  }
}

async function simulateTyping(content) {
  isBotTyping = true;
  sendBtn.disabled = true;
  msgInput.disabled = true;

  removeTypingIndicator();

  const bubble = appendMessage("bot", "");

  for (let i = 0; i < content.length; i++) {
    await new Promise((res) => setTimeout(res, 20));
    bubble.textContent += content[i];
    chatDiv.scrollTop = chatDiv.scrollHeight;
  }

  isBotTyping = false;
  sendBtn.disabled = false;
  msgInput.disabled = false;
  msgInput.focus();
}

let botMessageBuffer = ""; // buffer to collect partials
let botMessageTimeout = null; // debounce to detect end of stream

socket.onmessage = (event) => {
  const data = JSON.parse(event.data);
  const role = data.role;
  const content = data.content;

  if (role === "bot" || role === "assistant" || role === "Chatbot") {
    // Buffer incoming chunks
    if (!botTypingElement) showTypingIndicator();
    botMessageBuffer += content;

    // Reset debounce timeout
    if (botMessageTimeout) clearTimeout(botMessageTimeout);

    // Wait 500ms after last chunk to consider it complete
    botMessageTimeout = setTimeout(() => {
      removeTypingIndicator();
      simulateTyping(botMessageBuffer.trim());
      botMessageBuffer = ""; // reset buffer
    }, 500);
  } else {
    appendMessage(role, content); // user or others
  }
};


function sendMessage() {
  const message = msgInput.value.trim();
  if (!message || isBotTyping) return;

  appendMessage("user", message);
  socket.send(JSON.stringify({ message }));
  msgInput.value = "";
}

msgInput.addEventListener("keypress", function (e) {
  if (e.key === "Enter") sendMessage();
});

sendBtn.addEventListener("click", sendMessage);
