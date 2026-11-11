"""data.py - all the learning content, stored as plain Python lists and dictionaries.

Syllabus order follows the official Python Tutorial (https://docs.python.org/3/tutorial/).
To add a topic: add one entry to TOPICS. To add a video: add one entry to VIDEOS.
"""

LEVELS = ["Beginner", "Intermediate", "Advanced"]

DOCS = "https://docs.python.org/3/"

# ---------- Syllabus + notes (one dictionary per topic) ----------
# level    : Beginner / Intermediate / Advanced
# notes    : short bullet points
# code     : a small example (runs in the Playground)
# ref      : link to the official Python documentation
# keywords : extra words so the search bar finds the topic
TOPICS = {
    # ---------------- Beginner ----------------
    "intro": {
        "title": "Introduction & First Program", "level": "Beginner",
        "summary": "What Python is and how to run your first program.",
        "notes": [
            "Python is a simple, readable language used for web, data, automation and AI.",
            "print() shows output on the screen.",
            "A line starting with # is a comment. Python ignores it.",
            "Python uses indentation (spaces at the start of a line) instead of curly braces.",
        ],
        "code": '# My first program\nprint("Hello, World!")\nprint(2 + 3)',
        "ref": DOCS + "tutorial/introduction.html",
        "keywords": "hello world print comment start install first program basics",
    },
    "variables": {
        "title": "Variables & Data Types", "level": "Beginner",
        "summary": "Store numbers, text and True/False values.",
        "notes": [
            "A variable is a name that stores a value: age = 20.",
            "Common types: int (10), float (3.5), str ('hi'), bool (True/False).",
            "type(x) tells you the type. int(), float(), str() convert between types.",
            "Operators: + - * / // % **  (// is whole-number division, ** is power).",
        ],
        "code": 'age = 20\nprice = 99.5\nname = "Asha"\nprint(name, age, price)\nprint(type(age))\nprint(7 // 2, 7 % 2, 2 ** 3)',
        "ref": DOCS + "tutorial/introduction.html#using-python-as-a-calculator",
        "keywords": "variable variables int float str bool type operator number assign data types",
    },
    "strings": {
        "title": "Strings", "level": "Beginner",
        "summary": "Work with text: join, slice, search and change case.",
        "notes": [
            "Strings are text inside quotes: 'hello' or \"hello\".",
            "Index starts at 0: text[0] is the first letter. text[-1] is the last.",
            "Slicing: text[0:3] gives the first 3 characters.",
            "Useful methods: upper(), lower(), strip(), replace(), split(). f-strings: f'Hi {name}'.",
        ],
        "code": 'text = "python rocks"\nprint(text.upper())\nprint(text[0:6])\nprint(text.replace("rocks", "is fun"))\nname = "Asha"\nprint(f"Hello {name}!")',
        "ref": DOCS + "tutorial/introduction.html#text",
        "keywords": "string strings text slice upper lower split replace fstring format",
    },
    "io": {
        "title": "Input & Output", "level": "Beginner",
        "summary": "Take input from the user and format the output.",
        "notes": [
            "input() reads text typed by the user. It always returns a string.",
            "Convert it when you need a number: age = int(input()).",
            "f-strings make output easy: print(f'{name} is {age} years old').",
            "The Playground here does not support input(), so use fixed values to practise.",
        ],
        "code": 'name = "Asha"      # in a real program: name = input("Name: ")\nage = 20           # age = int(input("Age: "))\nprint(f"{name} is {age} years old")',
        "ref": DOCS + "tutorial/inputoutput.html",
        "keywords": "input output print format fstring user keyboard",
    },
    "conditions": {
        "title": "Conditions (if / elif / else)", "level": "Beginner",
        "summary": "Make decisions in your program.",
        "notes": [
            "if runs a block only when the condition is True. else runs otherwise.",
            "Use elif for more than two choices.",
            "Comparison: == != > < >= <=. Combine with and, or, not.",
            "= stores a value, == compares two values.",
        ],
        "code": 'marks = 72\nif marks >= 75:\n    print("Distinction")\nelif marks >= 40:\n    print("Pass")\nelse:\n    print("Fail")',
        "ref": DOCS + "tutorial/controlflow.html#if-statements",
        "keywords": "if else elif condition conditions decision compare boolean and or not",
    },
    "loops": {
        "title": "Loops (for / while)", "level": "Beginner",
        "summary": "Repeat a block of code.",
        "notes": [
            "for repeats over a sequence: for i in range(5) gives 0,1,2,3,4.",
            "while repeats as long as a condition is True. Change something inside, or it never stops!",
            "break stops the loop. continue skips to the next round.",
        ],
        "code": 'for i in range(1, 6):\n    print(i, "squared is", i * i)\n\ncount = 3\nwhile count > 0:\n    print(count)\n    count -= 1',
        "ref": DOCS + "tutorial/controlflow.html#for-statements",
        "keywords": "loop loops for while range break continue iteration repeat",
    },
    "functions": {
        "title": "Functions", "level": "Beginner",
        "summary": "Reusable blocks of code.",
        "notes": [
            "Define with def, run by calling its name with ().",
            "Parameters receive values. return sends a value back.",
            "Default values: def greet(name='friend').",
            "print shows a value; return gives it back so you can store it.",
        ],
        "code": 'def square(x):\n    return x * x\n\ndef greet(name="friend"):\n    return "Hello, " + name\n\nprint(square(5))\nprint(greet())\nprint(greet("Asha"))',
        "ref": DOCS + "tutorial/controlflow.html#defining-functions",
        "keywords": "function functions def return parameter argument lambda default reuse",
    },
    # ---------------- Intermediate ----------------
    "lists": {
        "title": "Lists", "level": "Intermediate",
        "summary": "Store many values in one variable.",
        "notes": [
            "A list keeps items in order: fruits = ['apple', 'banana'].",
            "Methods: append(), remove(), sort(), len(list). Indexes start at 0.",
            "Slicing works like strings: nums[1:3].",
            "Lists can be changed (mutable).",
        ],
        "code": 'fruits = ["apple", "banana"]\nfruits.append("mango")\nprint(fruits)\nprint(len(fruits), fruits[0])\nnums = [5, 2, 9]\nnums.sort()\nprint(nums)',
        "ref": DOCS + "tutorial/datastructures.html#more-on-lists",
        "keywords": "list lists array append sort index slicing items",
    },
    "tuples_sets": {
        "title": "Tuples & Sets", "level": "Intermediate",
        "summary": "Fixed collections and collections without duplicates.",
        "notes": [
            "A tuple is like a list that cannot be changed: point = (3, 4).",
            "A set stores unique values only: {1, 2, 2, 3} becomes {1, 2, 3}.",
            "Sets support union (|), intersection (&) and difference (-).",
        ],
        "code": 'point = (3, 4)\nprint(point[0])\nnums = [1, 2, 2, 3, 3]\nprint(set(nums))\nprint({1, 2, 3} & {2, 3, 4})',
        "ref": DOCS + "tutorial/datastructures.html#tuples-and-sequences",
        "keywords": "tuple tuples set sets unique duplicate immutable",
    },
    "dictionaries": {
        "title": "Dictionaries", "level": "Intermediate",
        "summary": "Store data as key-value pairs.",
        "notes": [
            "Look up by key, not by position: student['name'].",
            "get() returns None (no error) if the key is missing.",
            "Loop with .items() to get key and value together.",
        ],
        "code": 'student = {"name": "Asha", "marks": 82}\nprint(student["name"])\nstudent["city"] = "Agra"\nprint(student.get("age", "unknown"))\nfor key, value in student.items():\n    print(key, "->", value)',
        "ref": DOCS + "tutorial/datastructures.html#dictionaries",
        "keywords": "dictionary dictionaries dict key value json pairs map",
    },
    "comprehensions": {
        "title": "List Comprehensions", "level": "Intermediate",
        "summary": "Build a list in one short line.",
        "notes": [
            "Pattern: [expression for item in sequence if condition].",
            "It replaces a small for-loop that builds a list.",
            "Keep it short. If it is hard to read, use a normal loop.",
        ],
        "code": 'squares = [n * n for n in range(1, 6)]\nprint(squares)\nevens = [n for n in range(10) if n % 2 == 0]\nprint(evens)',
        "ref": DOCS + "tutorial/datastructures.html#list-comprehensions",
        "keywords": "comprehension comprehensions list shortcut one line",
    },
    "modules": {
        "title": "Modules & Packages", "level": "Intermediate",
        "summary": "Reuse code written by others.",
        "notes": [
            "A module is a .py file. import brings it into your program.",
            "Python has many built-in modules: math, random, datetime, json.",
            "from math import sqrt imports just one name.",
            "Third-party packages are installed with pip (pip install flask).",
        ],
        "code": 'import math\nimport random\nprint(math.sqrt(16))\nprint(math.pi)\nprint(random.randint(1, 6))',
        "ref": DOCS + "tutorial/modules.html",
        "keywords": "module modules import package pip math random library",
    },
    "files": {
        "title": "File Handling", "level": "Intermediate",
        "summary": "Read and write text files.",
        "notes": [
            "open(name, mode): 'r' read, 'w' write (erases old content), 'a' append.",
            "Use 'with open(...) as f:' so the file closes automatically.",
            "f.read() reads everything, f.write(text) writes text.",
        ],
        "code": 'with open("notes.txt", "w") as f:\n    f.write("Hello file!\\n")\n\nwith open("notes.txt") as f:\n    print(f.read())',
        "ref": DOCS + "tutorial/inputoutput.html#reading-and-writing-files",
        "keywords": "file files open read write append txt csv with",
    },
    "exceptions": {
        "title": "Errors & Exceptions", "level": "Intermediate",
        "summary": "Handle mistakes without crashing the program.",
        "notes": [
            "Put risky code in try. Handle the problem in except.",
            "Catch a specific error: except ZeroDivisionError.",
            "finally always runs. raise creates your own error.",
            "Read the LAST line of an error message first: it names the problem.",
        ],
        "code": 'try:\n    number = int("abc")\nexcept ValueError:\n    print("Please type a number")\nfinally:\n    print("Done")',
        "ref": DOCS + "tutorial/errors.html",
        "keywords": "error errors exception exceptions try except finally raise debug",
    },
    # ---------------- Advanced ----------------
    "oop": {
        "title": "OOP: Classes & Objects", "level": "Advanced",
        "summary": "Organise code with classes (blueprints) and objects.",
        "notes": [
            "A class is a blueprint. An object is one thing made from it.",
            "__init__ sets up the object's data. self means 'this object'.",
            "Methods are functions inside a class.",
            "Four pillars: encapsulation, inheritance, polymorphism, abstraction.",
        ],
        "code": 'class Student:\n    def __init__(self, name):\n        self.name = name\n\n    def greet(self):\n        print("Hi, I am", self.name)\n\ns = Student("Asha")\ns.greet()',
        "ref": DOCS + "tutorial/classes.html",
        "keywords": "oop object oriented class classes object init self method attribute encapsulation",
    },
    "inheritance": {
        "title": "OOP: Inheritance", "level": "Advanced",
        "summary": "Make a new class from an existing one.",
        "notes": [
            "class Child(Parent) gets everything the Parent has.",
            "The child can add new methods or override old ones.",
            "super() calls the parent's version of a method.",
        ],
        "code": 'class Animal:\n    def speak(self):\n        print("Some sound")\n\nclass Dog(Animal):\n    def speak(self):\n        print("Woof")\n\nfor pet in [Animal(), Dog()]:\n    pet.speak()',
        "ref": DOCS + "tutorial/classes.html#inheritance",
        "keywords": "inheritance super override polymorphism subclass parent child oop",
    },
    "generators": {
        "title": "Iterators & Generators", "level": "Advanced",
        "summary": "Produce values one at a time, saving memory.",
        "notes": [
            "A generator function uses yield instead of return.",
            "It remembers where it stopped and continues on the next request.",
            "Great for big data because values are not all stored in memory.",
        ],
        "code": 'def countdown(n):\n    while n > 0:\n        yield n\n        n -= 1\n\nfor x in countdown(3):\n    print(x)',
        "ref": DOCS + "tutorial/classes.html#generators",
        "keywords": "generator generators yield iterator iterators next lazy",
    },
    "decorators": {
        "title": "Decorators", "level": "Advanced",
        "summary": "Add extra behaviour to a function without changing it.",
        "notes": [
            "A decorator is a function that takes a function and returns a new one.",
            "Write @decorator above a function to apply it.",
            "Common uses: logging, timing, login checks (Flask uses @app.route).",
        ],
        "code": 'def shout(func):\n    def wrapper():\n        print("Before")\n        func()\n        print("After")\n    return wrapper\n\n@shout\ndef hello():\n    print("Hello")\n\nhello()',
        "ref": DOCS + "glossary.html#term-decorator",
        "keywords": "decorator decorators wrapper closure at flask route",
    },
    "dsa": {
        "title": "Data Structures & Algorithms", "level": "Advanced",
        "summary": "Stacks, queues, searching and sorting basics.",
        "notes": [
            "Stack = last in, first out (use list append/pop). Queue = first in, first out (use collections.deque).",
            "Binary search finds an item in a SORTED list by halving the range each time.",
            "Big-O describes how time grows with input size: O(1), O(n), O(log n), O(n^2).",
            "Practise sorting, recursion, linked lists, trees and graphs next.",
        ],
        "code": 'stack = []\nstack.append(1)\nstack.append(2)\nprint(stack.pop())\n\nfrom collections import deque\nqueue = deque([1, 2, 3])\nprint(queue.popleft())\n\nnums = [1, 3, 5, 7, 9]\nlow, high = 0, len(nums) - 1\nwhile low <= high:\n    mid = (low + high) // 2\n    if nums[mid] == 7:\n        print("found at", mid)\n        break\n    elif nums[mid] < 7:\n        low = mid + 1\n    else:\n        high = mid - 1',
        "ref": DOCS + "tutorial/datastructures.html#using-lists-as-stacks",
        "keywords": "dsa data structures algorithms stack queue binary search sorting big o recursion linked list tree graph",
    },
    "apis": {
        "title": "APIs & JSON", "level": "Advanced",
        "summary": "Talk to web services and read their data.",
        "notes": [
            "An API lets one program ask another program for data over the internet.",
            "Most web APIs reply in JSON, which looks like a Python dictionary.",
            "json.loads(text) turns JSON text into a dictionary.",
            "To call a real API you usually install the requests package: requests.get(url).json().",
        ],
        "code": 'import json\n\nreply = \'{"city": "Agra", "temp": 31}\'   # pretend this came from an API\ndata = json.loads(reply)\nprint(data["city"], data["temp"])\n\n# Real call (needs: pip install requests):\n# import requests\n# data = requests.get("https://example.com/api").json()',
        "ref": DOCS + "library/json.html",
        "keywords": "api apis json rest http requests web service get post",
    },
    "automation": {
        "title": "Automation with Python", "level": "Advanced",
        "summary": "Let Python do boring, repeated work for you.",
        "notes": [
            "Rename, move and organise files with the os and pathlib modules.",
            "Read and write CSV, Excel, PDF and text files.",
            "Scrape web pages, send emails and schedule tasks.",
            "Start small: automate one task you repeat every week.",
        ],
        "code": 'from pathlib import Path\n\nfor name in ["a.txt", "b.txt", "c.txt"]:\n    Path(name).write_text("sample")\n\nfor file in sorted(Path(".").glob("*.txt")):\n    print("Found:", file.name)',
        "ref": DOCS + "tutorial/stdlib.html#operating-system-interface",
        "keywords": "automation automate boring stuff os pathlib scripts scraping excel csv email schedule",
    },
}

# ---------- Learning paths ("For Everyone") ----------
PATHS = [
    {"who": "Complete beginner (any stream)",
     "plan": "Start from zero. Learn the basics step by step, then practise in the Playground.",
     "topics": ["intro", "variables", "conditions", "loops", "functions"]},
    {"who": "BTech / BCA (CS and IT)",
     "plan": "Strong basics first, then OOP and DSA for exams, labs and placements.",
     "topics": ["lists", "dictionaries", "oop", "dsa", "decorators"]},
    {"who": "MBA / Commerce / Non-CS",
     "plan": "Skip the heavy theory. Learn enough to analyse data and automate daily work.",
     "topics": ["files", "dictionaries", "apis", "automation"]},
    {"who": "Quick revision",
     "plan": "Know Python already? Use the search bar or jump to a topic.",
     "topics": ["comprehensions", "exceptions", "generators"]},
]

# ---------- YouTube learning (links checked from the creators' own pages / articles) ----------
YT = "https://www.youtube.com/"
VIDEOS = [
    {"title": "Learn Python - Full Course for Beginners", "by": "freeCodeCamp",
     "url": YT + "watch?v=rfscVS0vtbw", "level": "Beginner",
     "topics": ["intro", "variables", "strings", "conditions", "loops", "functions"]},
    {"title": "Python Full Course for Beginners", "by": "Programming with Mosh",
     "url": YT + "watch?v=_uQrJ0TkZlc", "level": "Beginner",
     "topics": ["intro", "variables", "conditions", "loops", "functions"]},
    {"title": "Python Tutorials (playlist)", "by": "Corey Schafer",
     "url": YT + "playlist?list=PL-osiE80TeTt2d9bfVyTiXJA-UTHn6WwU", "level": "Intermediate",
     "topics": ["lists", "dictionaries", "modules", "files", "exceptions", "comprehensions"]},
    {"title": "Python OOP Tutorials (playlist)", "by": "Corey Schafer",
     "url": YT + "playlist?list=PL-osiE80TeTsqhIuOqKhwlXsIBIdSeYtc", "level": "Advanced",
     "topics": ["oop", "inheritance"]},
    {"title": "Python Tutorial: Decorators", "by": "Corey Schafer",
     "url": YT + "watch?v=FsAPt_9Bf3U", "level": "Advanced",
     "topics": ["decorators"]},
    {"title": "Data Structures and Algorithms in Python - Full Course", "by": "freeCodeCamp (Aakash N S)",
     "url": "https://youtu.be/pkYVOmU3MgA", "level": "Advanced",
     "topics": ["dsa"]},
    {"title": "APIs for Beginners - How to use an API", "by": "freeCodeCamp",
     "url": YT + "watch?v=GZvSYJDk-us", "level": "Advanced",
     "topics": ["apis"]},
    {"title": "Automate the Boring Stuff with Python (first 15 lessons)", "by": "Al Sweigart",
     "url": YT + "watch?v=1F_OgqRuSdI&list=PL0-84-yl1fUnRuXGFe_F7qSH1LEnn9LkW", "level": "Advanced",
     "topics": ["automation", "files"]},
    {"title": "Flask Tutorials (playlist)", "by": "Corey Schafer",
     "url": YT + "playlist?list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH", "level": "Advanced",
     "topics": ["apis", "decorators"]},
]

# ---------- Code examples (home page) ----------
EXAMPLES = [
    {"title": "HELLO WORLD", "code": 'name = "Python"\nprint("Hello,", name)', "output": "Hello, Python"},
    {"title": "SUM OF A LIST", "code": 'numbers = [1, 2, 3, 4, 5]\ntotal = 0\nfor n in numbers:\n    total += n\nprint("Total:", total)', "output": "Total: 15"},
    {"title": "EVEN OR ODD", "code": 'num = 7\nif num % 2 == 0:\n    print("Even")\nelse:\n    print("Odd")', "output": "Odd"},
    {"title": "FUNCTION", "code": "def square(x):\n    return x * x\n\nprint(square(5))", "output": "25"},
    {"title": "CLASS AND OBJECT", "code": 'class Student:\n    def __init__(self, name):\n        self.name = name\n\n    def greet(self):\n        print("Hi, I am", self.name)\n\ns = Student("Asha")\ns.greet()', "output": "Hi, I am Asha"},
]

# ---------- Common errors (Error Solver on the home page) ----------
ERRORS = {
    "NameError": {
        "keywords": ["nameerror", "is not defined"],
        "meaning": "Python found a name (variable or function) that has not been defined.",
        "cause": "Using a variable before creating it, or a spelling mistake in its name.",
        "wrong": "print(age)", "fixed": "age = 20\nprint(age)",
    },
    "SyntaxError": {
        "keywords": ["syntaxerror", "invalid syntax", "expected ':'", "unterminated", "was never closed"],
        "meaning": "Your code breaks Python's grammar rules, so Python cannot read it.",
        "cause": "A missing colon, bracket or quote.",
        "wrong": "if 5 > 3\n    print('Yes')", "fixed": "if 5 > 3:\n    print('Yes')",
    },
    "TypeError": {
        "keywords": ["typeerror", "unsupported operand", "not callable", "can only concatenate", "indices must be integers"],
        "meaning": "An operation was used on a value of the wrong type.",
        "cause": "Adding a number to a string without converting it.",
        "wrong": 'print("Age: " + 20)', "fixed": 'print("Age: " + str(20))',
    },
    "IndexError": {
        "keywords": ["indexerror", "index out of range"],
        "meaning": "You tried to access a list position that does not exist.",
        "cause": "Using an index equal to or larger than the length of the list.",
        "wrong": "nums = [10, 20, 30]\nprint(nums[3])", "fixed": "nums = [10, 20, 30]\nprint(nums[2])",
    },
    "ZeroDivisionError": {
        "keywords": ["zerodivisionerror", "division by zero", "divide by zero", "modulo by zero"],
        "meaning": "You tried to divide a number by zero, which is not possible.",
        "cause": "The divisor (the number after /) is 0.",
        "wrong": "print(10 / 0)", "fixed": "b = 2\nif b != 0:\n    print(10 / b)",
    },
}

# ---------- Academic Syllabus (university syllabus, original wording) ----------
# Hindi videos (links checked from the creators' own descriptions / YouTube pages).
# One video can be reused by many topics: groups below refer to it by key.
SYLLABUS_VIDEOS = {
    "cwh_course": {"title": "Python Tutorial For Beginners in Hindi | Complete Python Course", "by": "CodeWithHarry",
                   "url": YT + "watch?v=UrsmFxEIp5k"},
    "cwh_2hr": {"title": "Python Tutorial in Hindi (2 hours)", "by": "CodeWithHarry",
                "url": YT + "watch?v=ihk_Xglr164"},
    "cwh_oop": {"title": "Python OOP playlist in Hindi", "by": "CodeWithHarry",
                "url": YT + "playlist?list=PLu0W_9lII9ahfRrhFcoB-4lpp9YaBmdCP"},
    "cd_dsa": {"title": "Data Structures and Algorithms with Python (Hindi)", "by": "Code & Debug",
               "url": YT + "playlist?list=PLhR2IpV1b2FwWwviBHRrR118YAaSlyhTU"},
}

# unit -> groups -> topics (subtopics written exactly as in the syllabus) + video key
SYLLABUS = [
    {"unit": "Unit I", "title": "Introduction & Basics", "groups": [
        {"name": "Introduction", "video": "cwh_2hr", "topics": [
            "Programming Cycle for Python", "Python IDE", "Interacting with Python Programs",
            "Elements of Python", "Type Conversion"]},
        {"name": "Basics", "video": "cwh_course", "topics": [
            "Expressions", "Assignment Statement", "Arithmetic Operators",
            "Operator Precedence", "Boolean Expression"]},
    ]},
    {"unit": "Unit II", "title": "Conditionals & Loops", "groups": [
        {"name": "Conditionals", "video": "cwh_course", "topics": [
            "if-else", "nested-if", "elif", "expression evaluation", "float representation"]},
        {"name": "Loops", "video": "cwh_2hr", "topics": [
            "Purpose and working", "while loop", "for loop", "nested loops", "break and continue"]},
    ]},
    {"unit": "Unit III", "title": "Functions, Strings & Data Structures", "groups": [
        {"name": "Functions", "video": "cwh_2hr", "topics": [
            "Parts and execution of a function", "keyword and default arguments", "scope rules"]},
        {"name": "Strings", "video": "cwh_course", "topics": [
            "Length", "concatenation", "repetition", "indexing and slicing"]},
        {"name": "Data Structures", "video": "cwh_course", "topics": [
            "Tuples", "unpacking sequences", "lists", "mutable sequences", "list comprehension",
            "sets", "dictionaries"]},
        {"name": "Higher Order Functions", "video": "cwh_course", "topics": [
            "First-class functions and lambda expressions"]},
    ]},
    {"unit": "Unit IV", "title": "Algorithms, Files, Exceptions, Modules & OOP", "groups": [
        {"name": "Sieve of Eratosthenes", "video": "cd_dsa", "topics": []},
        {"name": "File I/O", "video": "cwh_course", "topics": ["Input and output operations"]},
        {"name": "Exceptions and assertions", "video": "cwh_course", "topics": []},
        {"name": "Modules", "video": "cwh_course", "topics": ["Introduction and importing modules"]},
        {"name": "Abstract Data Types", "video": "cwh_oop", "topics": ["ADTs and interfaces"]},
        {"name": "Classes", "video": "cwh_oop", "topics": [
            "Class definition and operations",
            "special methods (__init__, __str__, comparison and arithmetic methods)",
            "class examples", "inheritance and OOP"]},
    ]},
    {"unit": "Unit V", "title": "Iterators, Recursion, Searching & Sorting", "groups": [
        {"name": "Iterators and Recursion", "video": "cwh_course", "topics": [
            "Recursive Fibonacci", "Tower of Hanoi"]},
        {"name": "Searching", "video": "cd_dsa", "topics": [
            "Simple search", "estimating search time", "binary search and estimating binary search time"]},
        {"name": "Sorting and Merging", "video": "cd_dsa", "topics": [
            "Selection sort", "merge list", "merge sort", "higher-order sort"]},
    ]},
]
