document.addEventListener("DOMContentLoaded", function () {
  const responseBox = document.getElementById("response");
  const chatForm = document.getElementById("chatForm");
  const chatInput = document.getElementById("chatInput");
  const chatOutput = document.getElementById("chatOutput");
  const scoreDisplay = document.getElementById("scoreDisplay");

  document.getElementById("uploadForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const formData = new FormData();
    formData.append("resume", document.getElementById("resume").files[0]);
    formData.append("jd", document.getElementById("jd").files[0]);
    formData.append("prompt", document.getElementById("prompt").files[0]);
    formData.append("session_id", "default");

    responseBox.textContent = "Rating in progress...";
    chatOutput.innerHTML = "";

    try {
      const res = await fetch("/evaluate", {
        method: "POST",
        body: formData,
      });

      const result = await res.json();

      scoreDisplay.textContent = "Score: " + result.score;
      const cleanedReason = result.reason.replace(/Score:\s*\d+/gi, "").trim();
      responseBox.textContent = cleanedReason;
      addMessage(cleanedReason, false);
      chatForm.style.display = "flex";
    } catch (err) {
      responseBox.textContent = "Error: " + err.message;
    }
  });

  chatForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const msg = chatInput.value.trim();
    if (!msg) return;

    addMessage(msg, true);
    chatInput.value = "";

    const formData = new FormData();
    formData.append("user_input", msg);
    formData.append("session_id", "default");

    try {
      const res = await fetch("/chat", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      addMessage(data.response, false);
    } catch (err) {
      addMessage("Error: " + err.message, false);
    }
  });

  function addMessage(text, isUser) {
    const chatOutput = document.getElementById("chatOutput");
    const parts = isUser ? [text] : text.split(/\n+|\* /);

    parts.forEach((part) => {
      const clean = part.trim();
      if (!clean) return;

      const messageDiv = document.createElement("div");
      messageDiv.className = "message " + (isUser ? "user-message" : "ai-message");
      messageDiv.textContent = isUser ? clean : (clean.startsWith("•") ? clean : "• " + clean);

      chatOutput.appendChild(messageDiv);
    });

    chatOutput.scrollTop = chatOutput.scrollHeight;
  }
});

document.addEventListener("mousemove", function (e) {
  const light = document.getElementById("spotlight");
  if (light) {
    light.style.left = e.clientX + "px";
    light.style.top = e.clientY + "px";
  }
});
