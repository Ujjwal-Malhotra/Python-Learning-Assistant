"""runner.py - runs the learner's Python code in a separate process.

IMPORTANT: this is NOT a secure sandbox.
The default "local" runner only adds safety nets (timeout, memory/CPU/file-size
limits on Linux/macOS, empty environment, temporary folder). The code still runs
as the same OS user and can use the network and read files that user can read.
For anything public, set RUNNER=docker (see README) or use a real sandbox service.
"""

import os
import re
import signal
import subprocess
import sys
import tempfile
import uuid

TIMEOUT_SECONDS = int(os.environ.get("RUN_TIMEOUT", "5"))
MAX_CODE_CHARS = 10_000
MAX_OUTPUT_CHARS = 10_000
MEMORY_LIMIT_MB = 256
RUNNER = os.environ.get("RUNNER", "local").lower()  # "local" or "docker"


def _limit_resources():
    """Runs in the child process before the code starts (Linux/macOS only)."""
    import resource

    limits = [
        (resource.RLIMIT_CPU, TIMEOUT_SECONDS + 1),             # CPU seconds
        (resource.RLIMIT_AS, MEMORY_LIMIT_MB * 1024 * 1024),    # memory
        (resource.RLIMIT_FSIZE, 1024 * 1024),                   # max file size 1 MB
        (resource.RLIMIT_NOFILE, 64),                           # open files
        (resource.RLIMIT_CORE, 0),                              # no core dumps
    ]
    for name, value in limits:
        try:
            resource.setrlimit(name, (value, value))
        except (ValueError, OSError):
            pass  # some systems (e.g. macOS) refuse certain limits; carry on


def validate_code(code):
    """Return an error message if the code is not acceptable, else None."""
    if not isinstance(code, str):
        return "Code must be text."
    if not code.strip():
        return "Please write some code first."
    if len(code) > MAX_CODE_CHARS:
        return f"Code is too long (maximum {MAX_CODE_CHARS} characters)."
    if "\x00" in code:
        return "Code contains invalid characters."
    return None


def _read_capped(path):
    """Read at most MAX_OUTPUT_CHARS from a file. Returns (text, was_cut)."""
    with open(path, "rb") as f:
        data = f.read(MAX_OUTPUT_CHARS * 4 + 1)
    text = data.decode("utf-8", errors="replace")
    if len(text) > MAX_OUTPUT_CHARS:
        return text[:MAX_OUTPUT_CHARS] + "\n... (output cut off)", True
    return text, False


def _command(tmp, container_name):
    if RUNNER == "docker":
        return [
            "docker", "run", "--rm", "--name", container_name,
            "--network", "none",            # no network
            "--memory", "128m", "--cpus", "0.5", "--pids-limit", "64",
            "--read-only", "--cap-drop", "ALL",
            "--security-opt", "no-new-privileges",
            "--user", "65534:65534",
            "-v", f"{tmp}:/work:ro", "-w", "/work",
            "python:3.12-slim", "python", "-I", "main.py",
        ]
    # -I isolated mode, -S no site-packages (learner code can't import Flask etc.)
    return [sys.executable, "-I", "-S", "-X", "utf8", "main.py"]


def run_code(code):
    """Run code and return a dict:
    stdout, stderr, exit_code, timed_out, error_line (int or None)."""
    problem = validate_code(code)
    if problem:
        raise ValueError(problem)

    container_name = "pla-" + uuid.uuid4().hex[:12]
    timed_out = False

    with tempfile.TemporaryDirectory(prefix="pla_") as tmp:
        with open(os.path.join(tmp, "main.py"), "w", encoding="utf-8") as f:
            f.write(code)
        out_path = os.path.join(tmp, ".stdout")
        err_path = os.path.join(tmp, ".stderr")

        # Environment is nearly empty on purpose: API keys etc. are NOT passed on.
        env = {"PYTHONDONTWRITEBYTECODE": "1"}
        if os.name == "nt":
            env["SYSTEMROOT"] = os.environ.get("SYSTEMROOT", "")

        posix = os.name == "posix"
        try:
            with open(out_path, "wb") as out, open(err_path, "wb") as err:
                proc = subprocess.Popen(
                    _command(tmp, container_name),
                    cwd=tmp, env=env,
                    stdin=subprocess.DEVNULL, stdout=out, stderr=err,
                    preexec_fn=_limit_resources if (posix and RUNNER == "local") else None,
                    start_new_session=posix,
                )
                try:
                    proc.wait(timeout=TIMEOUT_SECONDS)
                except subprocess.TimeoutExpired:
                    timed_out = True
                    if RUNNER == "docker":
                        subprocess.run(["docker", "kill", container_name],
                                       capture_output=True, timeout=10)
                    if posix:
                        try:
                            os.killpg(proc.pid, signal.SIGKILL)
                        except ProcessLookupError:
                            pass
                    proc.kill()
                    proc.wait()
        except FileNotFoundError:
            raise RuntimeError("Docker runner selected but 'docker' was not found."
                               if RUNNER == "docker" else "Could not start Python.")

        stdout, cut1 = _read_capped(out_path)
        stderr, cut2 = _read_capped(err_path)

        # Hide the temp folder path from tracebacks
        for path in {tmp, os.path.realpath(tmp)}:
            stderr = stderr.replace(path + os.sep, "").replace(path + "/", "")

    exit_code = proc.returncode
    if timed_out:
        stderr += f"\nTimeoutError: your code ran for more than {TIMEOUT_SECONDS} seconds and was stopped. Is there an infinite loop?"
    elif exit_code is not None and exit_code < 0:
        stderr += f"\nYour program was stopped by the system (signal {-exit_code}). It may have used too much CPU, memory or output."
    elif "EOFError" in stderr and "input" in stderr:
        stderr += "\nNote: input() is not supported in this playground (no keyboard input is available). Use fixed values instead."

    stderr = stderr.lstrip("\n")
    lines = re.findall(r'File "main\.py", line (\d+)', stderr)
    return {
        "stdout": stdout,
        "stderr": stderr,
        "exit_code": exit_code,
        "timed_out": timed_out,
        "error_line": int(lines[-1]) if lines else None,
    }
