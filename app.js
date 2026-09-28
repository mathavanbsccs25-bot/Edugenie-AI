const result = document.getElementById("result");
const statusEl = document.getElementById("status");

document.querySelectorAll(".tab").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach(b => b.classList.remove("active"));
    document.querySelectorAll(".panel").forEach(p => p.classList.remove("active"));
    btn.classList.add("active");
    document.getElementById(btn.dataset.tab).classList.add("active");
  });
});

async function api(path, body) {
  result.textContent = "Thinking…";
  const response = await fetch(path, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(body)
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.detail || "Request failed.");
  return data;
}

function showText(text) {
  result.textContent = text;
  window.scrollTo({top: document.body.scrollHeight, behavior: "smooth"});
}

async function askQuestion() {
  try {
    const data = await api("/ask", {
      question: value("ask-question"),
      context: value("ask-context")
    });
    showText(data.result);
  } catch (e) { showError(e); }
}

async function explainTopic() {
  try {
    const data = await api("/explain", {text: value("explain-topic")});
    showText(data.result);
  } catch (e) { showError(e); }
}

async function summarize() {
  try {
    const data = await api("/summarize", {text: value("summary-text")});
    showText(data.result);
  } catch (e) { showError(e); }
}

async function learningPath() {
  try {
    const data = await api("/learn/recommendations", {
      topic: value("learn-topic"),
      level: value("learn-level")
    });
    showText(data.result);
  } catch (e) { showError(e); }
}

async function makeQuiz() {
  try {
    const data = await api("/quiz", {text: value("quiz-content")});
    renderQuiz(data.quiz);
  } catch (e) { showError(e); }
}

function renderQuiz(quiz) {
  const container = document.getElementById("quiz-output");
  container.innerHTML = "";
  quiz.forEach((q, index) => {
    const box = document.createElement("div");
    box.className = "quiz-question";
    const title = document.createElement("strong");
    title.textContent = `${index + 1}. ${q.question}`;
    box.appendChild(title);

    q.options.forEach(option => {
      const btn = document.createElement("button");
      btn.className = "quiz-option";
      btn.textContent = option;
      btn.onclick = () => {
        box.querySelectorAll(".quiz-option").forEach(b => b.disabled = true);
        if (option === q.correct_answer) {
          btn.classList.add("correct");
          feedback.textContent = "Correct!";
        } else {
          btn.classList.add("wrong");
          feedback.textContent = `Not quite. Correct answer: ${q.correct_answer}`;
        }
        explanation.textContent = q.explanation || "";
      };
      box.appendChild(btn);
    });

    const feedback = document.createElement("div");
    feedback.className = "feedback";
    const explanation = document.createElement("div");
    explanation.className = "feedback";
    box.appendChild(feedback);
    box.appendChild(explanation);
    container.appendChild(box);
  });

  result.textContent = "Quiz generated below. Select an option for instant feedback.";
  container.scrollIntoView({behavior: "smooth", block: "start"});
}

function value(id) {
  return document.getElementById(id).value.trim();
}

function showError(error) {
  result.textContent = `Error: ${error.message}`;
  result.classList.add("error");
}

async function copyResult() {
  await navigator.clipboard.writeText(result.textContent);
}

fetch("/health")
  .then(r => r.json())
  .then(data => {
    statusEl.textContent = data.gemini_configured
      ? "Gemini API configured"
      : "Gemini API key missing";
    statusEl.style.color = data.gemini_configured ? "#067647" : "#b42318";
  })
  .catch(() => statusEl.textContent = "API unavailable");
