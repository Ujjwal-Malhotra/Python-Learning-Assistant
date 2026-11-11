// playground.js - small, dependency-free front-end logic for the playground page.
// (The tutor answers come from the Flask server, which calls the Gemini API. The API key never reaches this file.)
// Output is always inserted with textContent (never innerHTML) so it cannot inject HTML.

const codeBox = document.getElementById("code");
const output = document.getElementById("output");
const runBtn = document.getElementById("run-btn");
const explainBtn = document.getElementById("explain-btn");
const chat = document.getElementById("chat");
const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");
const chatSend = document.getElementById("chat-send");

let history = [];        // chat history [{role, content}]
let lastError = null;    // {error, error_line} from the last failed run

// ---- helpers ----
async function postJSON(url, body) {
    try {
        const res = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body),
        });
        const data = await res.json().catch(() => ({}));
        if (!res.ok) return { ok: false, error: data.error || "Something went wrong. Please try again." };
        return { ok: true, data: data };
    } catch (e) {
        return { ok: false, error: "Could not reach the server. Is it running?" };
    }
}

function addMessage(who, text) {
    const div = document.createElement("div");
    div.className = "msg " + who;
    div.textContent = text;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
    return div;
}

// ---- editor: Tab key inserts 4 spaces, Ctrl+Enter runs ----
codeBox.addEventListener("keydown", (e) => {
    if (e.key === "Tab") {
        e.preventDefault();
        const s = codeBox.selectionStart;
        codeBox.setRangeText("    ", s, codeBox.selectionEnd, "end");
    } else if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
        e.preventDefault();
        runCode();
    }
});

// ---- run code ----
async function runCode() {
    runBtn.disabled = true;
    explainBtn.disabled = true;
    lastError = null;
    output.className = "terminal";
    output.textContent = "Running...";

    const result = await postJSON("/api/run", { code: codeBox.value });
    runBtn.disabled = false;

    if (!result.ok) {
        output.className = "terminal err";
        output.textContent = result.error;
        return;
    }
    const r = result.data;
    output.textContent = "";
    if (r.stdout) output.appendChild(document.createTextNode(r.stdout));
    if (r.stderr) {
        const span = document.createElement("span");
        span.className = "err";
        span.textContent = (r.stdout && !r.stdout.endsWith("\n") ? "\n" : "") + r.stderr;
        output.appendChild(span);
        lastError = { error: r.stderr, error_line: r.error_line };
        explainBtn.disabled = false;
    }
    if (!r.stdout && !r.stderr) output.textContent = "(program finished with no output)";
}

// ---- explain error ----
async function explainError() {
    if (!lastError) return;
    explainBtn.disabled = true;
    const waiting = addMessage("coach", "Looking at your error...");
    const result = await postJSON("/api/explain-error", {
        code: codeBox.value,
        error: lastError.error,
        error_line: lastError.error_line,
    });
    waiting.textContent = result.ok ? result.data.reply : "⚠ " + result.error;
    if (!result.ok) waiting.classList.add("problem");
    explainBtn.disabled = false;
}

// ---- chat with the AI tutor ----
async function sendChat(e) {
    e.preventDefault();
    const text = chatInput.value.trim();
    if (!text) return;
    chatInput.value = "";
    chatSend.disabled = true;
    addMessage("user", text);
    const waiting = addMessage("coach", "Thinking...");

    const result = await postJSON("/api/coach", {
        message: text, code: codeBox.value, history: history,
    });
    if (result.ok) {
        waiting.textContent = result.data.reply;
        history.push({ role: "user", content: text });
        history.push({ role: "assistant", content: result.data.reply });
        history = history.slice(-20);
    } else {
        waiting.textContent = "⚠ " + result.error;
        waiting.classList.add("problem");
    }
    chatSend.disabled = false;
    chatInput.focus();
}

runBtn.addEventListener("click", runCode);
explainBtn.addEventListener("click", explainError);
chatForm.addEventListener("submit", sendChat);
