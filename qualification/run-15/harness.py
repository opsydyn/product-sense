"""Run 15 harness: park versus investigate, by stated label and recommended action.

Subcommands:
  cases                       write cases.json (shuffled)
  respond NAME [--dry-run]    run one responder session once
  extract                     write observations.json
  gradings                    write gradings.json (every answer once, plus a seeded 20% repeat subset)
  grade GRADING [--dry-run]   run one grader session once
  analyze                     write analysis.json and print the decision
"""

import json
from pathlib import Path
import random
import re
import subprocess
import sys
import time

run = Path(__file__).resolve().parent
protocol = json.loads((run / "protocol.json").read_text())
key = json.loads((run / "answer-key.json").read_text())["scenarios"]
MODELS = {"opus": "claude-opus-5-5", "sonnet": "claude-sonnet-5-5"}
ARMS = ("new", "old", "none")
SAMPLES = protocol["samples_per_scenario_per_arm_per_model"]
TIMEOUT = protocol["budget"]["timeout_seconds"]
BUDGET = str(protocol["budget"]["max_usd_per_session"])
BASE = ["claude", "--print", "--output-format", "stream-json", "--verbose",
        "--no-session-persistence", "--restricted", "--strict-mcp-config", "--no-chrome",
        "--settings", '{"disableAllHooks":true}', "--permission-mode", "dontAsk",
        "--permission-prompts", "none", "--max-budget-usd", BUDGET, "--prompt-suggestions", "false"]
IDENTIFYING = re.compile(r"product[- ]sense|SKILL\.md|references/\w+\.md", re.I)


def load(name):
    return json.loads((run / name).read_text())


def save(name, data):
    path = run / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def write_cases():
    cases = [{"name": f"{sid}-{short}-{arm}-{i}", "scenario": sid, "type": key[sid]["type"], "model": model,
              "model_short": short, "arm": arm, "sample": i}
             for sid in key for short, model in MODELS.items() for arm in ARMS for i in range(1, SAMPLES + 1)]
    random.Random(15).shuffle(cases)
    save("cases.json", cases)
    print(len(cases), "cases")


def execute(command, prompt_text, events, cwd, dry_run):
    record = {"command": command, "cwd": str(cwd)}
    if dry_run:
        print(json.dumps(record))
        return record
    if events.exists():
        raise SystemExit("Evidence already exists; do not overwrite or retry")
    events.parent.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    with events.open("w") as stdout, events.with_suffix(".stderr.txt").open("w") as stderr:
        try:
            process = subprocess.run(command, cwd=cwd, input=prompt_text, text=True, stdout=stdout, stderr=stderr,
                                     timeout=TIMEOUT)
            record["exit_code"] = process.returncode
        except subprocess.TimeoutExpired:
            record["timeout"] = True
    record["elapsed_seconds"] = round(time.monotonic() - started, 3)
    events.with_suffix(".execution.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({"name": events.stem, **{k: v for k, v in record.items() if k not in {"command", "cwd"}}}))
    return record


def respond(name, dry_run):
    case = {c["name"]: c for c in load("cases.json")}[name]
    stage = Path(protocol["stage"])
    cwd = stage / "cwd" / name
    command = BASE + ["--model", case["model"], "--tools", protocol["responder_tools"],
                      "--allowedTools", protocol["responder_tools"]]
    if case["arm"] != "none":
        plugin = str(stage / case["arm"])
        command += ["--plugin-dir", plugin, "--add-dir", plugin]
    if not dry_run:
        if cwd.exists():
            raise SystemExit("Stage already exists; do not overwrite or retry")
        cwd.mkdir(parents=True)
    execute(command, (run / "scenarios" / f"{case['scenario']}.txt").read_text(),
            run / "responses" / f"{name}.jsonl", cwd, dry_run)


def parse_stream(path):
    skills, reads, available, final, cost, error = [], [], None, "", None, None
    for line in path.read_text().splitlines():
        event = json.loads(line)
        if event.get("type") == "system" and event.get("subtype") == "init":
            available = any("product-sense" in s for s in event.get("skills", []) + event.get("slash_commands", []))
        elif event.get("type") == "assistant":
            for block in event["message"]["content"]:
                if block.get("type") == "tool_use" and block["name"] == "Skill":
                    skills.append(block["input"].get("skill"))
                if block.get("type") == "tool_use" and block["name"] == "Read":
                    reads.append(block["input"].get("file_path"))
        elif event.get("type") == "result":
            final, cost, error = event.get("result", ""), event.get("total_cost_usd"), event.get("is_error")
    return {"skill_available": available, "skills_invoked": skills, "reads": reads, "final": final,
            "word_count": len(final.split()), "reported_list_cost_usd": cost, "is_error": error}


def anonymise(text):
    return "\n".join(line for line in text.splitlines() if not IDENTIFYING.search(line)).strip()


def extract():
    out = {}
    for case in load("cases.json"):
        events = run / "responses" / f"{case['name']}.jsonl"
        if events.exists():
            out[case["name"]] = {**case, **parse_stream(events)}
    save("observations.json", out)
    print(len(out), "observations")


def write_gradings():
    names = [c["name"] for c in load("cases.json")]
    repeat = sorted(random.Random(1515).sample(sorted(names), round(len(names) * 0.2)))
    save("gradings.json", {"first": names, "repeat": repeat})
    print(len(names), "first gradings,", len(repeat), "repeats")


def grade(grading, dry_run):
    name, round_ = grading.rsplit("-g", 1)
    obs = load("observations.json")[name]
    text = (run / "grader-prompt.md").read_text()
    text = text.replace("{{scenario_prompt}}", (run / "scenarios" / f"{obs['scenario']}.txt").read_text().strip())
    text = text.replace("{{answer}}", anonymise(obs["final"]))
    if dry_run:
        print(text)
        return
    cwd = Path(protocol["stage"]) / "grader"
    cwd.mkdir(parents=True, exist_ok=True)
    execute(BASE + ["--model", protocol["grader"]["model"], "--tools", ""], text,
            run / "grades" / f"{grading}.jsonl", cwd, dry_run)


def parse_grade(grading):
    path = run / "grades" / f"{grading}.jsonl"
    if not path.exists():
        return None
    final = parse_stream(path)["final"]
    match = re.search(r"\{.*\}", final, re.S)
    try:
        return json.loads(match.group(0)) if match else None
    except json.JSONDecodeError:
        return None


def mean(values):
    values = list(values)
    return round(sum(values) / len(values), 3) if values else None


def analyze():
    observations, plan = load("observations.json"), load("gradings.json")
    grades, failures = {}, []
    for name in plan["first"]:
        g = parse_grade(f"{name}-g1")
        if g is None:
            failures.append(f"{name}-g1")
        else:
            grades[name] = g
    agreement = []
    for name in plan["repeat"]:
        g2 = parse_grade(f"{name}-g2")
        if g2 is None:
            failures.append(f"{name}-g2")
        elif name in grades:
            agreement.append({"name": name, "action": grades[name]["action"] == g2["action"],
                              "label": grades[name]["stated_label"] == g2["stated_label"]})
    rows = []
    for name, g in grades.items():
        o = observations[name]
        rows.append({"name": name, "scenario": o["scenario"], "type": o["type"], "arm": o["arm"],
                     "model": o["model_short"], "selected": bool(o["skills_invoked"]), "label": g["stated_label"],
                     "action": g["action"], "research_days": g.get("research_days_before_decision"),
                     "correct": g["action"] == key[o["scenario"]]["correct_action"]})
    save("classified.json", rows)

    def rates(subset):
        park = [r for r in subset if r["type"] == "park"]
        inv = [r for r in subset if r["type"] == "investigate"]
        days = [r["research_days"] for r in park if isinstance(r["research_days"], (int, float))]
        return {"park_n": len(park), "park_stop_rate": mean(r["action"] == "stop" for r in park),
                "park_label_rate": mean(r["label"] == "park" for r in park),
                "park_actions": {a: sum(r["action"] == a for r in park) for a in ("stop", "research_first", "invest")},
                "park_labels": {l: sum(r["label"] == l for r in park) for l in ("park", "investigate", "reshape", "pursue", "none")},
                "park_mean_research_days": mean(days),
                "investigate_n": len(inv), "investigate_research_first_rate": mean(r["action"] == "research_first" for r in inv),
                "investigate_actions": {a: sum(r["action"] == a for r in inv) for a in ("stop", "research_first", "invest")},
                "selection_rate": mean(r["selected"] for r in subset)}

    by_arm = {arm: rates([r for r in rows if r["arm"] == arm]) for arm in ARMS}
    by_arm_model = {f"{m}-{arm}": rates([r for r in rows if r["arm"] == arm and r["model"] == m])
                    for m in MODELS for arm in ARMS}
    by_scenario = {sid: {arm: [r["action"][:5] for r in rows if r["scenario"] == sid and r["arm"] == arm]
                         for arm in ARMS} for sid in key}
    new, old = by_arm["new"], by_arm["old"]
    stop_gap = round(old["park_stop_rate"] - new["park_stop_rate"], 3)
    label_gap = round(old["park_label_rate"] - new["park_label_rate"], 3)
    rule = "substantive_shift" if stop_gap >= 0.20 else "label_only" if label_gap >= 0.20 else "no_shift"
    agree = mean(a["action"] for a in agreement)
    result = {"by_arm": by_arm, "by_arm_model": by_arm_model, "by_scenario_actions": by_scenario,
              "decision": {"rule": rule, "old_minus_new_stop_rate": stop_gap, "old_minus_new_park_label_rate": label_gap,
                           "overcorrection": round(old["investigate_research_first_rate"] - new["investigate_research_first_rate"], 3) >= 0.20,
                           "grader_action_agreement": agree, "grader_label_agreement": mean(a["label"] for a in agreement),
                           "grader_reliable": agree is not None and agree >= 0.85},
              "grading_failures": failures}
    save("analysis.json", result)
    print(json.dumps({"by_arm": by_arm, "decision": result["decision"], "failures": failures}, indent=2))


if __name__ == "__main__":
    command, *rest = sys.argv[1:]
    dry = "--dry-run" in rest
    rest = [r for r in rest if r != "--dry-run"]
    {"cases": write_cases, "extract": extract, "gradings": write_gradings, "analyze": analyze}.get(command, lambda: None)()
    if command == "respond":
        respond(rest[0], dry)
    elif command == "grade":
        grade(rest[0], dry)
