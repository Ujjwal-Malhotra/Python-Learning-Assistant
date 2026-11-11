"""coach.py - the Python tutor, powered by the Google Gemini API.

How it works (easy to explain in a viva):
  1. The browser sends the student's question to Flask (/api/coach).
  2. Flask calls ask_gemini() here. This file sends an HTTPS request to Gemini.
  3. The API key is read from the .env file on the SERVER. The browser never sees it.
  4. A "system prompt" tells Gemini to behave like a friendly beginner Python tutor.
"""

import os

import requests

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
DEFAULT_MODEL = "gemini-3.5-flash-lite"   # free-tier friendly; change with GEMINI_MODEL in .env
MAX_MESSAGE_CHARS = 1000
MAX_CODE_CHARS = 3000
MAX_HISTORY = 20   # last 20 chat messages are sent so Gemini remembers the conversation

SYSTEM_PROMPT = (
    "You are a friendly Python tutor for college students, including complete beginners "
    "(BTech, BCA, MBA and others). Rules:\n"
    "- Use simple English and short answers (under 150 words unless asked for more).\n"
    "- Explain concepts with one small, easy example.\n"
    "- When the student asks for the answer to an exercise, give a HINT first and ask them to try. "
    "Give the full solution only if they ask again.\n"
    "- Only answer questions about Python and programming. Politely refuse other topics.\n"
    "- Reply in plain text. Do not use Markdown symbols like ** or ```. Indent code with 4 spaces."
)


class CoachError(Exception):
    """Raised with a friendly message that is safe to show to the student."""


def get_api_key():
    key = os.getenv("GEMINI_API_KEY", "").strip()
    if not key or key == "your-api-key-here":
        raise CoachError("The tutor is not set up yet: GEMINI_API_KEY is missing. "
                         "Copy .env.example to .env, add your key, and restart the app.")
    return key


def clean_history(history):
    """Keep only well-formed {'role': 'user'|'assistant', 'content': text} items from the browser."""
    cleaned = []
    if isinstance(history, list):
        for item in history[-MAX_HISTORY:]:
            if isinstance(item, dict) and item.get("role") in ("user", "assistant") \
                    and isinstance(item.get("content"), str):
                cleaned.append({"role": item["role"], "content": item["content"][:MAX_MESSAGE_CHARS]})
    return cleaned


def ask_gemini(message, history=None):
    """Send the chat to Gemini and return its reply text. Raises CoachError on any problem."""
    key = get_api_key()

    # Gemini calls the tutor's side "model" instead of "assistant"
    contents = []
    for m in clean_history(history):
        role = "model" if m["role"] == "assistant" else "user"
        contents.append({"role": role, "parts": [{"text": m["content"]}]})
    contents.append({"role": "user", "parts": [{"text": message}]})

    body = {
        "system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "contents": contents,
    }
    url = API_URL.format(model=os.getenv("GEMINI_MODEL", DEFAULT_MODEL))

    try:
        # The key goes in a header (not in the URL), so it does not end up in logs
        response = requests.post(url, json=body, timeout=30,
                                 headers={"x-goog-api-key": key})
    except requests.exceptions.Timeout:
        raise CoachError("Gemini took too long to answer. Please try again.")
    except requests.exceptions.RequestException:
        raise CoachError("Could not reach Gemini. Check your internet connection.")

    # Turn common HTTP errors into friendly messages
    if response.status_code in (400, 401, 403):
        raise CoachError("Gemini rejected the request. Check that your GEMINI_API_KEY is correct.")
    if response.status_code == 404:
        raise CoachError("Gemini model not found. Set GEMINI_MODEL in .env to a current model name.")
    if response.status_code == 429:
        raise CoachError("Free Gemini limit reached for now. Please wait a minute and try again.")
    if response.status_code != 200:
        raise CoachError(f"Gemini is not available right now (error {response.status_code}).")

    try:
        return response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
    except (KeyError, IndexError, TypeError, ValueError):
        raise CoachError("Gemini did not return an answer. Try rephrasing your question.")


def explain_error(code, error_text, error_line=None):
    """Explain a Python error in simple words and give a hint (not the full fixed program)."""
    question = ("My Python program gave this error. In simple words: say what it means, "
                "where to look, and give a hint to fix it. Do not rewrite my whole program.\n\n"
                "My code:\n" + str(code)[:MAX_CODE_CHARS] + "\n\nError:\n" + str(error_text)[:1500])
    if error_line:
        question += f"\n\n(The error is on line {error_line}.)"
    return ask_gemini(question)
