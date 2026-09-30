"""Capture Product Sense metadata through this host's native Codex scanner."""
import argparse
import json
import selectors
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUN = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--output", type=Path, default=RUN / "native-discovery.json")
arguments = parser.parse_args()
REQUESTS = [
    {"id": 1, "method": "initialize", "params": {"clientInfo": {"name": "product_sense_qualification", "version": "1"}}},
    {"method": "initialized", "params": {}},
    {"id": 2, "method": "skills/list", "params": {"cwds": [str(ROOT)], "forceReload": True}},
]

with open("/private/tmp/product-sense-native-discovery.stderr", "w") as stderr:
    process = subprocess.Popen(
        ["codex", "app-server", "--stdio"],
        cwd=ROOT, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=stderr, text=True, bufsize=1,
    )
    selector = selectors.DefaultSelector()
    selector.register(process.stdout, selectors.EVENT_READ)

    def send(message):
        process.stdin.write(json.dumps(message) + "\n")
        process.stdin.flush()

    def receive(request_id):
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline:
            if not selector.select(max(0, deadline - time.monotonic())):
                break
            line = process.stdout.readline()
            if not line:
                raise RuntimeError("app-server closed stdout")
            try:
                message = json.loads(line)
            except json.JSONDecodeError:
                continue
            if message.get("id") == request_id:
                if "error" in message:
                    raise RuntimeError(str(message["error"]))
                return message
        raise TimeoutError("native discovery response timed out")

    try:
        send(REQUESTS[0])
        initialised = receive(1)
        send(REQUESTS[1])
        send(REQUESTS[2])
        response = receive(2)
        entries = []
        for entry in response["result"]["data"]:
            entries.append({
                "cwd": entry["cwd"],
                "matches": [skill for skill in entry["skills"] if skill["name"] == "product-sense"],
                "matching_errors": [error for error in entry["errors"] if "product-sense" in error["path"]],
                "total_skills": len(entry["skills"]),
                "other_error_count": sum("product-sense" not in error["path"] for error in entry["errors"]),
            })
        evidence = {"transport": "stdio JSON-RPC", "requests": REQUESTS, "server": initialised["result"], "result": entries}
        arguments.output.write_text(json.dumps(evidence, indent=2) + "\n")
        print(json.dumps(entries, indent=2))
    finally:
        selector.close()
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
