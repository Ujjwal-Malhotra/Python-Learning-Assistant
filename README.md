# Python Learning Assistant (Flask + Gemini)

A simple college mini-project for learning Python: syllabus with searchable notes, an AI chatbot,
a code playground, YouTube resources and common-error help.
Built with only **HTML, CSS, Python Flask and the Gemini API**. No database, no JavaScript framework.

## Pages and navigation
Every page shares one navbar (`templates/base.html`): **Home - Topics - Academic Syllabus - Chatbot - Playground - Resources - Examples**.
Inner pages also have a **← Back** link and a **Home** link. Browser Back/Forward work because every page is a normal link.

```
Home  (/)                  intro, cards to every section, learning paths, search box
 ├─ Topics  (/topics)      Beginner / Intermediate / Advanced syllabus + search (?q=)
 │    └─ Notes (/topic/<name>)   notes, example, official docs link, related videos
 ├─ Academic Syllabus (/syllabus)   university syllabus, Units I-V, Hindi video per topic
 ├─ Chatbot  (/chatbot)    Gemini Python tutor
 ├─ Playground (/playground)   write + run code; "Explain error" asks Gemini
 ├─ Resources (/resources)     YouTube videos by level + free reading
 └─ Examples (/examples)       code examples + error solver
```

## Project structure
```
app.py                 Flask routes: 7 pages + 3 small JSON APIs
data.py                All content as lists/dictionaries (topics, videos, paths, examples, errors)
coach.py               Gemini code: builds the request, calls the API, friendly error messages
runner.py              Runs the playground code with subprocess (timeout + limits)
templates/base.html    Shared layout: navbar, back/home bar, footer
templates/*.html       One short template per page (home, topics, topic, syllabus, chatbot, playground, resources, examples, 404)
static/style.css       One stylesheet, responsive
static/app.js          Small JS: chatbot page and playground page
tests/test_app.py      33 automated tests
.env.example  .gitignore  requirements.txt
```

## Setup
1. Install Python 3.9 or newer.
2. Create a virtual environment and install packages:
   ```bash
   python -m venv venv
   venv\Scripts\activate            # Windows   (macOS/Linux: source venv/bin/activate)
   pip install -r requirements.txt
   ```
3. Get a free Gemini API key: https://aistudio.google.com/apikey
4. Copy `.env.example` to `.env` and put your key in it: `GEMINI_API_KEY=AIza...`
5. Run `python app.py` and open http://127.0.0.1:5000

Without a key, every page works except the AI parts (Chatbot and Explain error), which show
*"GEMINI_API_KEY is missing"*.

If the chatbot says **"model not found"**, Google has renamed its models. Pick a current Flash model from
https://ai.google.dev/gemini-api/docs/models and set `GEMINI_MODEL=...` in `.env` (default: `gemini-3.5-flash-lite`).

## How it works
- **Academic Syllabus:** `SYLLABUS` in `data.py` is a list of units, each with groups of topics (the university wording) and a video key. `SYLLABUS_VIDEOS` holds the 4 Hindi videos, reused across related topics. The `/syllabus` route just passes both to `syllabus.html`.
- **Content in `data.py`:** dictionaries are easy to read and edit, so no database is needed. Add one entry to add a topic or video.
- **Search:** `/topics?q=word` keeps topics where a word in the title or keywords starts with the search text.
- **Shared layout:** `base.html` holds the navbar once. Each page `{% extends %}` it, so links are never duplicated.
- **Chatbot:** `app.js` sends the question to `/api/coach`. `coach.py` reads `GEMINI_API_KEY` from `.env`, sends it to Gemini in a request header together with a system prompt ("friendly Python tutor, hints first") and the last 20 messages, and returns the text. The key never reaches the browser.
- **Errors:** missing key, wrong key, no internet, quota and unknown model each give a clear message (`CoachError`).
- **Playground:** code is saved to a temp file and run with `subprocess` and a timeout. The key is not passed to the student's code.
- **Safety:** all text is shown with `textContent` (no HTML injection); `.env` is in `.gitignore`.
