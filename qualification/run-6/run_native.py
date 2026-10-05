"""Run one predeclared Claude case once; requires an authenticated local CLI."""

import json
from pathlib import Path
import subprocess
import sys
import time


run = Path(__file__).resolve().parent
protocol = json.loads((run / "protocol.json").read_text())
if len(sys.argv) != 2 or sys.argv[1] not in {"explicit", "implicit"}:
    raise SystemExit("Usage: python3 qualification/run-6/run_native.py explicit|implicit")
case = sys.argv[1]
output = run / f"{case}-events.jsonl"
if output.exists():
    raise SystemExit("Case evidence exists; create a new protocol/run instead of retrying")
plugin = protocol["plugin"]
command = [
    "claude", "--print", "--output-format", "stream-json", "--verbose",
    "--no-session-persistence", "--restricted", "--strict-mcp-config", "--no-chrome",
    "--settings", json.dumps(protocol["runtime"]["settings"]),
    "--permission-mode", "dontAsk", "--permission-prompts", "none",
    "--tools", "Skill,Read,Glob,Grep", "--allowedTools", "Skill,Read,Glob,Grep",
    "--plugin-dir", plugin, "--add-dir", plugin,
    "--max-budget-usd", str(protocol["sample_budget"]["max_budget_usd_per_session"]),
    "--prompt-suggestions", "false",
]
started = time.time()
record = {"case": case, "command": command, "cwd": str(Path(protocol["stage"]) / case)}
with (run / f"{case}-prompt.txt").open() as prompt, output.open("w") as stdout, (run / f"{case}-stderr.txt").open("w") as stderr:
    try:
        result = subprocess.run(command, cwd=record["cwd"], stdin=prompt, stdout=stdout, stderr=stderr,
                                timeout=protocol["sample_budget"]["timeout_seconds_per_session"])
        record["exit_code"] = result.returncode
    except subprocess.TimeoutExpired:
        record["timeout"] = True
record["elapsed_seconds"] = round(time.time() - started, 3)
(run / f"{case}-execution.json").write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps({key: value for key, value in record.items() if key not in {"command", "cwd"}}))
