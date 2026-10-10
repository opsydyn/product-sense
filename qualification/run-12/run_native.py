"""Execute each predeclared native case once, preserving failures."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

run = Path(__file__).resolve().parent
protocol = json.loads((run / "protocol.json").read_text())
name = sys.argv[1]
cases = {case["name"]: case for case in protocol["claude_cases"] + protocol["codex_cases"]}
if name not in cases:
    raise SystemExit("Unknown predeclared case")
case = cases[name]
events = run / f"{name}-events.jsonl"
if events.exists():
    raise SystemExit("Evidence already exists; do not overwrite or retry")
stage = Path(protocol["stage"])
cwd = stage / name
if cwd.exists():
    raise SystemExit("Stage already exists; do not overwrite or retry")
if case.get("fixture"):
    shutil.copytree(run / "fixture", cwd)
else:
    cwd.mkdir()
shutil.copyfile(run / case["prompt"], run / f"{name}-prompt.txt")
if name.startswith("codex-"):
    command = ["codex", "-a", "never", "exec", "--ephemeral", "--sandbox", case["sandbox"],
               "--skip-git-repo-check", "--json", "--output-last-message", str(run / f"{name}-final.txt"),
               "--cd", str(cwd), "-"]
else:
    plugin = str(stage / case["arm"])
    command = ["claude", "--print", "--output-format", "stream-json", "--verbose", "--model", case["model"],
               "--no-session-persistence", "--restricted", "--strict-mcp-config", "--no-chrome",
               "--settings", '{"disableAllHooks":true}', "--permission-mode", "dontAsk",
               "--permission-prompts", "none", "--tools", case["tools"],
               "--allowedTools", case["tools"], "--plugin-dir", plugin, "--add-dir", plugin,
               "--max-budget-usd", str(protocol["budget"]["max_usd_per_claude_session"]),
               "--prompt-suggestions", "false"]
started = time.monotonic()
record = {"case": name, "command": command, "cwd": str(cwd)}
with (run / f"{name}-prompt.txt").open() as prompt, events.open("w") as stdout, (run / f"{name}-stderr.txt").open("w") as stderr:
    try:
        process = subprocess.run(command, cwd=cwd, stdin=prompt, stdout=stdout, stderr=stderr,
                                 timeout=protocol["budget"]["timeout_seconds"])
        record["exit_code"] = process.returncode
    except subprocess.TimeoutExpired:
        record["timeout"] = True
record["elapsed_seconds"] = round(time.monotonic() - started, 3)
if case.get("fixture"):
    for path in ("src/format.js", "test/format.test.js"):
        shutil.copyfile(cwd / path, run / f"{name}-{path.replace('/', '-')}")
    test = subprocess.run(["node", "--test"], cwd=cwd, capture_output=True, text=True)
    record["node_test_exit_code"] = test.returncode
    (run / f"{name}-node-test.txt").write_text(test.stdout + test.stderr)
(run / f"{name}-execution.json").write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps({k: v for k, v in record.items() if k not in {"command", "cwd"}}))
