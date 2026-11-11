import os

from dotenv import load_dotenv

load_dotenv()  # read the .env file first (GEMINI_API_KEY, optional settings)

from flask import Flask, abort, jsonify, render_template, request

import coach
import runner
from data import ERRORS, EXAMPLES, LEVELS, PATHS, SYLLABUS, SYLLABUS_VIDEOS, TOPICS, VIDEOS

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 64 * 1024  # reject huge requests (64 KB)

STARTER_CODE = "# Goal: print the squares of the numbers 1 to 5.\n# Write your own code below, then press Run.\n\n"


# ---------- Pages ----------

@app.route("/")
def home():
    return render_template("home.html", paths=PATHS, topics=TOPICS)


@app.route("/topics")
def topic_list():
    """Syllabus grouped by level. ?q=word filters it (search bar)."""
    shown, message = TOPICS, None
    query = request.args.get("q", "").strip().lower()[:50]
    if "q" in request.args and not query:
        message = "Please type a topic to search. Showing all topics."
    elif query:
        # match the start of any word, so "oop" finds OOP but not "loops"
        shown = {slug: t for slug, t in TOPICS.items()
                 if " " + query in " " + t["title"].lower() + " " + t["keywords"]}
        if not shown:
            message = f"No topic found for '{query}'. Try: loops, oop, decorators, dsa, api or files."
            shown = TOPICS
    groups = {level: {s: t for s, t in shown.items() if t["level"] == level} for level in LEVELS}
    return render_template("topics.html", groups=groups, query=query, message=message)


@app.route("/topic/<slug>")
def topic_notes(slug):
    topic = TOPICS.get(slug)
    if topic is None:
        abort(404)
    videos = [v for v in VIDEOS if slug in v["topics"]]
    return render_template("topic.html", t=topic, videos=videos)


@app.route("/syllabus")
def syllabus():
    return render_template("syllabus.html", syllabus=SYLLABUS, videos=SYLLABUS_VIDEOS)


@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")


@app.route("/playground")
def playground():
    return render_template("playground.html", starter=STARTER_CODE)


@app.route("/resources")
def resources():
    return render_template("resources.html", videos=VIDEOS, levels=LEVELS)


@app.route("/examples")
def examples():
    """Code examples + error solver (?error=text)."""
    error_name, error_msg = None, None
    text = request.args.get("error", "").strip().lower()[:200]
    if "error" in request.args and not text:
        error_msg = "Please enter an error name or message."
    elif text:
        error_name = next((name for name, e in ERRORS.items() if any(k in text for k in e["keywords"])), None)
        if error_name is None:
            error_msg = "Sorry, I don't know this error yet. Try NameError, SyntaxError, TypeError, IndexError or ZeroDivisionError."
    return render_template("examples.html", examples=EXAMPLES, errors=ERRORS,
                           error_name=error_name, error_msg=error_msg, error_text=text)


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


# ---------- JSON API (used by static/app.js) ----------

def read_json():
    """Return the JSON body as a dict, or None if it is invalid."""
    data = request.get_json(silent=True)
    return data if isinstance(data, dict) else None


def bad_request(message, status=400):
    return jsonify(error=message), status


@app.route("/api/coach", methods=["POST"])
def api_coach():
    data = read_json()
    message = data.get("message") if data else None
    if not isinstance(message, str) or not message.strip():
        return bad_request("Please type a question first.")
    if len(message) > coach.MAX_MESSAGE_CHARS:
        return bad_request(f"Message too long (maximum {coach.MAX_MESSAGE_CHARS} characters).")
    try:
        return jsonify(reply=coach.ask_gemini(message.strip(), data.get("history")))
    except coach.CoachError as e:
        return bad_request(str(e), 503)


@app.route("/api/run", methods=["POST"])
def api_run():
    data = read_json()
    if data is None:
        return bad_request("Send JSON like {\"code\": \"print(1)\"}.")
    try:
        return jsonify(runner.run_code(data.get("code")))
    except ValueError as e:
        return bad_request(str(e))
    except RuntimeError as e:
        return bad_request(str(e), 500)


@app.route("/api/explain-error", methods=["POST"])
def api_explain_error():
    data = read_json()
    if data is None:
        return bad_request("Invalid request.")
    code, error = data.get("code"), data.get("error")
    problem = runner.validate_code(code)
    if problem:
        return bad_request(problem)
    if not isinstance(error, str) or not error.strip():
        return bad_request("There is no error to explain. Run your code first.")
    line = data.get("error_line")
    line = line if isinstance(line, int) and not isinstance(line, bool) else None
    try:
        return jsonify(reply=coach.explain_error(code, error, line))
    except coach.CoachError as e:
        return bad_request(str(e), 503)


if __name__ == "__main__":
    # Debug mode is OFF by default: Flask's debugger lets visitors run code on your PC.
    # For local development only:  FLASK_DEBUG=1 python app.py
    app.run(host="127.0.0.1", port=5000, debug=os.environ.get("FLASK_DEBUG") == "1")
