"""Execute each predeclared native case once, preserving failures."""

import json
from pathlib import Path
import subprocess
import sys
import time

run = Path(__file__).resolve().parent
protocol = json.loads((run / "protocol.json").read_text())
name = sys.argv[1]
cases = {case["name"]: case for case in protocol["claude_cases"]}
if name not in {*cases, "codex-implicit", "codex-guard"}:
    raise SystemExit("Unknown predeclared case")
events = run / f"{name}-events.jsonl"
if events.exists():
    raise SystemExit("Evidence already exists; do not overwrite or retry")
cwd = Path(protocol["stage"]) / name
if name.startswith("codex-"):
    command = ["codex", "-a", "never", "exec", "--ephemeral", "--sandbox", "read-only",
               "--skip-git-repo-check", "--json", "--output-last-message", str(run / f"{name}-final.txt"),
               "--cd", str(cwd), "-"]
else:
    plugin = str(Path(protocol["stage"]) / cases[name]["arm"])
    command = ["claude", "--print", "--output-format", "stream-json", "--verbose",
               "--no-session-persistence", "--restricted", "--strict-mcp-config", "--no-chrome",
               "--settings", '{"disableAllHooks":true}', "--permission-mode", "dontAsk",
               "--permission-prompts", "none", "--tools", "Skill,Read,Glob,Grep",
               "--allowedTools", "Skill,Read,Glob,Grep", "--plugin-dir", plugin, "--add-dir", plugin,
               "--max-budget-usd", "1", "--prompt-suggestions", "false"]
started = time.monotonic()
record = {"case": name, "command": command, "cwd": str(cwd)}
with (run / f"{name}-prompt.txt").open() as prompt, events.open("w") as stdout, (run / f"{name}-stderr.txt").open("w") as stderr:
    try:
        process = subprocess.run(command, cwd=cwd, stdin=prompt, stdout=stdout, stderr=stderr, timeout=180)
        record["exit_code"] = process.returncode
    except subprocess.TimeoutExpired:
        record["timeout"] = True
record["elapsed_seconds"] = round(time.monotonic() - started, 3)
(run / f"{name}-execution.json").write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps({k: v for k, v in record.items() if k not in {"command", "cwd"}}))
