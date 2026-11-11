// app.js - small vanilla JS for the two interactive pages (Chatbot and Playground).
// The browser only talks to our Flask server. The Gemini API key stays on the server.
// Text is always inserted with textContent (never innerHTML), so it cannot inject HTML.

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

// ---------- Chatbot page ----------
function startChat() {
    const chat = document.getElementById("chat");
    const form = document.getElementById("chat-form");
    const input = document.getElementById("chat-input");
    const send = document.getElementById("chat-send");
    let history = [];   // [{role: "user" | "assistant", content: text}] sent with every question

    function addMessage(who, text) {
        const div = document.createElement("div");
        div.className = "msg " + who;
        div.textContent = text;
        chat.appendChild(div);
        chat.scrollTop = chat.scrollHeight;
        return div;
    }

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const text = input.value.trim();
        if (!text) return;
        input.value = "";
        send.disabled = true;
        addMessage("user", text);
        const waiting = addMessage("coach", "Thinking...");

        const result = await postJSON("/api/coach", { message: text, history: history });
        if (result.ok) {
            waiting.textContent = result.data.reply;
            history.push({ role: "user", content: text }, { role: "assistant", content: result.data.reply });
            history = history.slice(-20);
        } else {
            waiting.textContent = "⚠ " + result.error;
            waiting.classList.add("problem");
        }
        send.disabled = false;
        input.focus();
    });
}

// ---------- Playground page ----------
function startPlayground() {
    const codeBox = document.getElementById("code");
    const output = document.getElementById("output");
    const explain = document.getElementById("explain");
    const runBtn = document.getElementById("run-btn");
    const explainBtn = document.getElementById("explain-btn");
    let lastError = null;   // {error, error_line} from the last failed run

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
        output.textContent = r.stdout;
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

    async function explainError() {
        explainBtn.disabled = true;
        explain.className = "explain";
        explain.textContent = "Looking at your error...";
        const result = await postJSON("/api/explain-error", {
            code: codeBox.value, error: lastError.error, error_line: lastError.error_line,
        });
        explain.textContent = result.ok ? result.data.reply : "⚠ " + result.error;
        if (!result.ok) explain.className = "explain problem";
        explainBtn.disabled = false;
    }

    // Tab key inserts 4 spaces, Ctrl+Enter runs
    codeBox.addEventListener("keydown", (e) => {
        if (e.key === "Tab") {
            e.preventDefault();
            codeBox.setRangeText("    ", codeBox.selectionStart, codeBox.selectionEnd, "end");
        } else if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
            e.preventDefault();
            runCode();
        }
    });
    runBtn.addEventListener("click", runCode);
    explainBtn.addEventListener("click", explainError);
}

if (document.getElementById("chat")) startChat();
if (document.getElementById("code")) startPlayground();
