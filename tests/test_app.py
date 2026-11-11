"""Run with:  python -m unittest discover -s tests -v
No API key or internet needed: the Gemini call is replaced by a fake (mock) in these tests."""

import os
import re
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import coach
import data
import runner
from app import app

FAKE_KEY = "AIza-test-key-123"


def fake_response(status=200, text="Hello from Gemini"):
    r = MagicMock()
    r.status_code = status
    r.json.return_value = {"candidates": [{"content": {"parts": [{"text": text}]}}]}
    return r


class RunnerTests(unittest.TestCase):
    def test_stdout(self):
        r = runner.run_code('print("hi")')
        self.assertEqual(r["stdout"].strip(), "hi")
        self.assertEqual(r["exit_code"], 0)

    def test_runtime_error_and_line(self):
        r = runner.run_code("x = 1\nprint(y)")
        self.assertIn("NameError", r["stderr"])
        self.assertEqual(r["error_line"], 2)

    def test_timeout(self):
        with patch.object(runner, "TIMEOUT_SECONDS", 1):
            r = runner.run_code("while True:\n    pass")
        self.assertTrue(r["timed_out"])

    def test_api_key_hidden_from_student_code(self):
        with patch.dict(os.environ, {"GEMINI_API_KEY": FAKE_KEY}):
            r = runner.run_code("import os\nprint(os.environ.get('GEMINI_API_KEY'))")
        self.assertEqual(r["stdout"].strip(), "None")

    def test_validation(self):
        for bad in ["", "   ", None, 123, "x" * (runner.MAX_CODE_CHARS + 1)]:
            with self.assertRaises(ValueError):
                runner.run_code(bad)


class GeminiTests(unittest.TestCase):
    """coach.py with a fake Gemini."""

    def setUp(self):
        patcher = patch.dict(os.environ, {"GEMINI_API_KEY": FAKE_KEY})
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_missing_key(self):
        for value in ("", "your-api-key-here"):
            with patch.dict(os.environ, {"GEMINI_API_KEY": value}):
                with self.assertRaises(coach.CoachError) as cm:
                    coach.ask_gemini("hi")
                self.assertIn("GEMINI_API_KEY", str(cm.exception))

    def test_request_format(self):
        with patch("coach.requests.post", return_value=fake_response()) as post:
            reply = coach.ask_gemini("What is a loop?",
                                     [{"role": "user", "content": "hi"}, {"role": "assistant", "content": "hello"}])
        self.assertEqual(reply, "Hello from Gemini")
        url = post.call_args.args[0]
        body = post.call_args.kwargs["json"]
        self.assertNotIn(FAKE_KEY, url)                                   # key is not in the URL
        self.assertEqual(post.call_args.kwargs["headers"]["x-goog-api-key"], FAKE_KEY)
        self.assertIn("Python tutor", body["system_instruction"]["parts"][0]["text"])
        self.assertEqual([c["role"] for c in body["contents"]], ["user", "model", "user"])
        self.assertEqual(body["contents"][-1]["parts"][0]["text"], "What is a loop?")

    def test_http_errors_are_friendly(self):
        cases = {400: "GEMINI_API_KEY", 403: "GEMINI_API_KEY", 404: "GEMINI_MODEL", 429: "limit", 500: "500"}
        for status, word in cases.items():
            with patch("coach.requests.post", return_value=fake_response(status)):
                with self.assertRaises(coach.CoachError) as cm:
                    coach.ask_gemini("hi")
            self.assertIn(word, str(cm.exception))

    def test_network_problems(self):
        for error in (coach.requests.exceptions.Timeout(), coach.requests.exceptions.ConnectionError()):
            with patch("coach.requests.post", side_effect=error):
                with self.assertRaises(coach.CoachError):
                    coach.ask_gemini("hi")

    def test_empty_answer(self):
        bad = MagicMock(status_code=200)
        bad.json.return_value = {"promptFeedback": {"blockReason": "SAFETY"}}
        with patch("coach.requests.post", return_value=bad):
            with self.assertRaises(coach.CoachError):
                coach.ask_gemini("hi")

    def test_history_cleaning(self):
        h = [{"role": "user", "content": "a"}, {"role": "hacker", "content": "x"}, "junk", {"role": "user", "content": 5}]
        self.assertEqual(len(coach.clean_history(h)), 1)
        self.assertEqual(coach.clean_history("not a list"), [])


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_chat_api_with_fake_gemini(self):
        with patch.dict(os.environ, {"GEMINI_API_KEY": FAKE_KEY}), \
                patch("coach.requests.post", return_value=fake_response(text="A loop repeats code.")):
            r = self.client.post("/api/coach", json={"message": "what is a loop", "code": "", "history": []})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json()["reply"], "A loop repeats code.")
        self.assertNotIn(FAKE_KEY, r.get_data(as_text=True))

    def test_chat_api_without_key(self):
        with patch.dict(os.environ, {"GEMINI_API_KEY": ""}):
            r = self.client.post("/api/coach", json={"message": "hi"})
        self.assertEqual(r.status_code, 503)
        self.assertIn("GEMINI_API_KEY", r.get_json()["error"])

    def test_chat_validation(self):
        self.assertEqual(self.client.post("/api/coach", json={"message": "  "}).status_code, 400)
        self.assertEqual(self.client.post("/api/coach", json={"message": 5}).status_code, 400)
        self.assertEqual(self.client.post("/api/coach", json={"message": "x" * 2000}).status_code, 400)
        self.assertEqual(self.client.post("/api/coach", data="nope").status_code, 400)

    def test_explain_error_api(self):
        with patch.dict(os.environ, {"GEMINI_API_KEY": FAKE_KEY}), \
                patch("coach.requests.post", return_value=fake_response(text="y is not defined")) as post:
            r = self.client.post("/api/explain-error", json={
                "code": "x = 1\nprint(y)", "error": "NameError: name 'y' is not defined", "error_line": 2})
        self.assertEqual(r.status_code, 200)
        self.assertIn("NameError", post.call_args.kwargs["json"]["contents"][-1]["parts"][0]["text"])

    def test_explain_error_validation(self):
        self.assertEqual(self.client.post("/api/explain-error", json={"code": "x", "error": ""}).status_code, 400)
        self.assertEqual(self.client.post("/api/explain-error", json={"code": "", "error": "e"}).status_code, 400)

    def test_run_api(self):
        r = self.client.post("/api/run", json={"code": "print(2+2)"})
        self.assertEqual(r.get_json()["stdout"].strip(), "4")
        self.assertEqual(self.client.post("/api/run", json={"code": ""}).status_code, 400)


class PageTests(unittest.TestCase):
    PAGES = ["/", "/topics", "/syllabus", "/chatbot", "/playground", "/resources", "/examples"]

    def setUp(self):
        self.client = app.test_client()

    def get(self, url):
        return self.client.get(url).get_data(as_text=True)

    def test_main_pages_load_with_same_navbar(self):
        for url in self.PAGES:
            r = self.client.get(url)
            self.assertEqual(r.status_code, 200, url)
            html = r.get_data(as_text=True)
            for link in ('href="/topics"', 'href="/syllabus"', 'href="/chatbot"', 'href="/playground"', 'href="/resources"', 'href="/examples"'):
                self.assertIn(link, html, f"{url} is missing navbar link {link}")

    def test_every_topic_page_loads_with_back_and_home(self):
        for slug in data.TOPICS:
            r = self.client.get(f"/topic/{slug}")
            self.assertEqual(r.status_code, 200, slug)
            html = r.get_data(as_text=True)
            self.assertIn("Back to Topics", html)
            self.assertIn("Home</a>", html)

    def test_404_page(self):
        r = self.client.get("/topic/nothing")
        self.assertEqual(r.status_code, 404)
        self.assertIn("Page not found", r.get_data(as_text=True))
        self.assertEqual(self.client.get("/no-such-page").status_code, 404)

    def test_every_internal_link_and_file_works(self):
        """Crawl: open every page, follow every internal link/script/stylesheet, expect 200."""
        urls = set(self.PAGES) | {f"/topic/{slug}" for slug in data.TOPICS}
        checked = set()
        for url in sorted(urls):
            for link in re.findall(r'(?:href|src|action)="(/[^"#]*)', self.get(url)):
                checked.add(link)
        for link in sorted(checked):
            self.assertEqual(self.client.get(link).status_code, 200, f"broken link: {link}")
        self.assertIn("/static/style.css", checked)
        self.assertIn("/topic/oop", checked)

    def test_external_links_are_https(self):
        for url in self.PAGES + ["/topic/apis"]:
            for link in re.findall(r'href="(http[^"]+)"', self.get(url)):
                self.assertTrue(link.startswith("https://"), link)

    def test_search(self):
        page = self.get("/topics?q=decorator")
        self.assertIn("Decorators", page)
        self.assertNotIn("Tuples &amp; Sets", page)
        self.assertIn("No topic found", self.get("/topics?q=zzzz"))
        self.assertIn("Please type a topic", self.get("/topics?q="))
        self.assertIn("Decorators", self.get("/topics"))   # no search = full syllabus
        oop = self.get("/topics?q=oop")
        self.assertIn("OOP: Classes", oop)
        self.assertNotIn("Loops (for", oop)                # "oop" must not match "loops"
        self.assertIn("Decorators", self.get("/topics?q=decor"))   # partial word works

    def test_error_solver(self):
        self.assertIn("Common cause", self.get("/examples?error=NameError: name 'x' is not defined"))
        self.assertIn("know this error", self.get("/examples?error=bananas"))

    def test_all_levels_present(self):
        self.assertEqual({t["level"] for t in data.TOPICS.values()}, set(data.LEVELS))
        for slug in ("oop", "dsa", "decorators", "apis", "automation"):
            self.assertIn(slug, data.TOPICS)

    def test_topic_data_is_complete(self):
        for slug, t in data.TOPICS.items():
            for field in ("title", "level", "summary", "notes", "code", "ref", "keywords"):
                self.assertTrue(t.get(field), f"{slug} is missing {field}")
            self.assertTrue(t["ref"].startswith("https://docs.python.org/3/"))
        for path in data.PATHS:
            for slug in path["topics"]:
                self.assertIn(slug, data.TOPICS)

    def test_video_data(self):
        for v in data.VIDEOS:
            self.assertRegex(v["url"], r"^https://(www\.youtube\.com|youtu\.be)/")
            self.assertIn(v["level"], data.LEVELS)
            for slug in v["topics"]:
                self.assertIn(slug, data.TOPICS)
        covered = {slug for v in data.VIDEOS for slug in v["topics"]}
        self.assertTrue({"oop", "dsa", "decorators", "apis", "automation"} <= covered)

    def test_topic_examples_run(self):
        """Every notes example must really run in the playground."""
        for slug, t in data.TOPICS.items():
            r = runner.run_code(t["code"])
            self.assertEqual(r["exit_code"], 0, f"{slug}: {r['stderr']}")

    def test_no_api_key_in_frontend_files(self):
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        for folder in ("templates", "static"):
            for name in os.listdir(os.path.join(root, folder)):
                with open(os.path.join(root, folder, name), encoding="utf-8") as f:
                    text = f.read()
                self.assertNotIn("GEMINI_API_KEY", text, name)
                self.assertNotIn("generativelanguage", text, name)
                self.assertIsNone(re.search(r"AIza[0-9A-Za-z_-]{10,}", text), name)


class SyllabusTests(unittest.TestCase):
    """The Academic Syllabus page: exact university wording, units, Hindi video links."""

    # The syllabus exactly as given (every line must appear on the page)
    WORDING = [
        "Unit I — Introduction & Basics", "Programming Cycle for Python", "Python IDE", "Interacting with Python Programs",
        "Elements of Python", "Type Conversion", "Expressions", "Assignment Statement", "Arithmetic Operators",
        "Operator Precedence", "Boolean Expression",
        "Unit II — Conditionals & Loops", "if-else", "nested-if", "elif", "expression evaluation", "float representation",
        "Purpose and working", "while loop", "for loop", "nested loops", "break and continue",
        "Unit III — Functions, Strings & Data Structures", "Parts and execution of a function",
        "keyword and default arguments", "scope rules", "Length", "concatenation", "repetition", "indexing and slicing",
        "Tuples", "unpacking sequences", "lists", "mutable sequences", "list comprehension", "sets", "dictionaries",
        "Higher Order Functions", "First-class functions and lambda expressions",
        "Unit IV — Algorithms, Files, Exceptions, Modules & OOP", "Sieve of Eratosthenes", "File I/O",
        "Input and output operations", "Exceptions and assertions", "Modules", "Introduction and importing modules",
        "Abstract Data Types", "ADTs and interfaces", "Classes", "Class definition and operations",
        "special methods (__init__, __str__, comparison and arithmetic methods)", "class examples", "inheritance and OOP",
        "Unit V — Iterators, Recursion, Searching & Sorting", "Iterators and Recursion", "Recursive Fibonacci",
        "Tower of Hanoi", "Searching", "Simple search", "estimating search time",
        "binary search and estimating binary search time", "Sorting and Merging", "Selection sort", "merge list",
        "merge sort", "higher-order sort",
    ]

    def setUp(self):
        self.client = app.test_client()
        self.html = self.client.get("/syllabus").get_data(as_text=True)

    def test_exact_wording_is_on_the_page(self):
        import html
        text = html.unescape(self.html)
        for phrase in self.WORDING:
            self.assertIn(phrase, text, phrase)

    def test_five_units_with_working_anchors(self):
        self.assertEqual(len(data.SYLLABUS), 5)
        for i in range(1, 6):
            self.assertIn(f'href="#unit-{i}"', self.html)   # unit navigation chip
            self.assertIn(f'id="unit-{i}"', self.html)      # the unit it jumps to
        self.assertIn('id="units"', self.html)               # target of the "All units" links

    def test_every_group_has_a_hindi_video_link(self):
        groups = [g for u in data.SYLLABUS for g in u["groups"]]
        self.assertEqual(self.html.count("Watch Video"), len(groups))
        for g in groups:
            self.assertIn(g["video"], data.SYLLABUS_VIDEOS, g["name"])
        for v in data.SYLLABUS_VIDEOS.values():
            self.assertRegex(v["url"], r"^https://www\.youtube\.com/(watch\?v=[\w-]{11}|playlist\?list=[\w-]+)$")

    def test_navbar_back_and_home(self):
        self.assertIn('class="active">Academic Syllabus', self.html)
        self.assertIn("Back to Home", self.html)


if __name__ == "__main__":
    unittest.main()
