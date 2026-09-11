const chatEl = document.getElementById("chat");
const chipsEl = document.getElementById("chips");
const form = document.getElementById("composer");
const input = document.getElementById("input");

const SUGGESTIONS = [
  "How do I spot a phishing email?",
  "Is public Wi-Fi safe?",
  "What is ransomware?",
  "What should I do after a data breach?",
  "How do I set up MFA?",
];

function addBubble(text, who) {
  const div = document.createElement("div");
  div.className = `msg ${who}`;
  // allow the `code` styling for tip markers, keep everything else text
  div.textContent = text;
  div.innerHTML = div.innerHTML.replace(/`([^`]+)`/g, "<code>$1</code>");
  chatEl.appendChild(div);
  chatEl.scrollTop = chatEl.scrollHeight;
}

function addTyping() {
  const wrap = document.createElement("div");
  wrap.className = "msg bot typing-wrap";
  wrap.innerHTML = '<div class="typing"><span></span><span></span><span></span></div>';
  chatEl.appendChild(wrap);
  chatEl.scrollTop = chatEl.scrollHeight;
  return wrap;
}

async function send(message) {
  addBubble(message, "user");
  const typing = addTyping();
  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });
    const data = await res.json();
    typing.remove();
    addBubble(data.reply, "bot");
  } catch {
    typing.remove();
    addBubble("Connection problem — is the server still running?", "bot");
  }
}

SUGGESTIONS.forEach((s) => {
  const b = document.createElement("button");
  b.className = "chip";
  b.textContent = s;
  b.addEventListener("click", () => send(s));
  chipsEl.appendChild(b);
});

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const value = input.value.trim();
  if (!value) return;
  input.value = "";
  send(value);
});

addBubble(
  "Hi! I'm Sentinel 🛡 Ask me anything about staying secure online — phishing, " +
  "passwords, MFA, ransomware, breaches. You can also run `check password: your-password`.",
  "bot"
);
