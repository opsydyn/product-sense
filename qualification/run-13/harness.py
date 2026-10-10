"""Run 13 harness: responders, blind grading, calibration and analysis.

Subcommands:
  cases                       write cases.json (fixed, shuffled order)
  respond NAME [--dry-run]    run one responder session once
  extract                     write observations.json from responder event streams
  pairs                       write pairs.json with A/B assignment for both orders
  grade GRADING [--dry-run]   run one grader session once (GRADING = PAIR-o1|PAIR-o2)
  calibration                 write the blind human-calibration sheet
  analyze                     write analysis.json and print the decision
"""

import json
from pathlib import Path
import random
import re
import shutil
import subprocess
import sys
import time

run = Path(__file__).resolve().parent
protocol = json.loads((run / "protocol.json").read_text())
key = {s["id"]: s for s in json.loads((run / "answer-key.json").read_text())["scenarios"]}
MODELS = {"opus": "claude-opus-5-5", "sonnet": "claude-sonnet-5-5"}
ARMS = ("skill", "control")
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
    cases = [{"name": f"{sid}-{short}-{arm}-{i}", "scenario": sid, "model": model, "model_short": short,
              "arm": arm, "sample": i}
             for sid in key for short, model in MODELS.items() for arm in ARMS for i in range(1, SAMPLES + 1)]
    random.Random(13).shuffle(cases)
    save("cases.json", cases)
    print(len(cases), "cases")


def execute(command, prompt_text, events, cwd, record_path, dry_run):
    record = {"command": command, "cwd": str(cwd)}
    if dry_run:
        print(json.dumps(record, indent=2))
        print("--- prompt ---\n" + prompt_text)
        return
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
    record_path.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({"case": record_path.stem, **{k: v for k, v in record.items() if k not in {"command", "cwd"}}}))


def respond(name, dry_run):
    case = {c["name"]: c for c in load("cases.json")}[name]
    stage = Path(protocol["stage"])
    cwd = stage / "cwd" / name
    command = BASE + ["--model", case["model"], "--tools", protocol["responder_tools"],
                      "--allowedTools", protocol["responder_tools"]]
    if case["arm"] == "skill":
        plugin = str(stage / "candidate")
        command += ["--plugin-dir", plugin, "--add-dir", plugin]
    if not dry_run:
        if cwd.exists():
            raise SystemExit("Stage already exists; do not overwrite or retry")
        cwd.mkdir(parents=True)
    prompt_text = (run / "scenarios" / f"{case['scenario']}.txt").read_text()
    execute(command, prompt_text, run / "responses" / f"{name}.jsonl", cwd,
            run / "responses" / f"{name}.execution.json", dry_run)


def parse_stream(path):
    skills, reads, available, final, cost, model, error = [], [], None, "", None, None, None
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
            model = list(event.get("modelUsage", {}))
    return {"skill_available": available, "skills_invoked": skills, "reads": reads, "final": final,
            "word_count": len(final.split()), "reported_list_cost_usd": cost, "model": model, "is_error": error}


def extract():
    out = {}
    for case in load("cases.json"):
        events = run / "responses" / f"{case['name']}.jsonl"
        if events.exists():
            record = {**case, **parse_stream(events)}
            record["skill_word_after_anonymising"] = bool(re.search(r"\bskill", anonymise(record["final"]), re.I))
            out[case["name"]] = record
    save("observations.json", out)
    for name, r in sorted(out.items()):
        print(f"{name:34} avail={r['skill_available']!s:5} skills={len(r['skills_invoked'])} "
              f"reads={len(r['reads'])} words={r['word_count']} err={r['is_error']}")


def write_pairs():
    rng = random.Random(1313)
    pairs = {}
    for sid in key:
        for short in MODELS:
            for i in range(1, SAMPLES + 1):
                pair = f"{sid}-{short}-{i}"
                skill_is_a = rng.random() < 0.5
                pairs[pair] = {"scenario": sid, "model_short": short, "sample": i,
                               "skill": f"{sid}-{short}-skill-{i}", "control": f"{sid}-{short}-control-{i}",
                               "o1": {"A": "skill" if skill_is_a else "control", "B": "control" if skill_is_a else "skill"},
                               "o2": {"A": "control" if skill_is_a else "skill", "B": "skill" if skill_is_a else "control"}}
    save("pairs.json", pairs)
    print(len(pairs), "pairs")


def anonymise(text):
    return "\n".join(line for line in text.splitlines() if not IDENTIFYING.search(line)).strip()


def bullet(items):
    return "\n".join(f"{n}. {item}" for n, item in enumerate(items, 1))


def grader_prompt(pair, order, observations):
    k = key[pair["scenario"]]
    fills = {
        "scenario_prompt": (run / "scenarios" / f"{pair['scenario']}.txt").read_text().strip(),
        "expected": ", ".join(k["expected"]),
        "acceptable_partial": json.dumps(k["acceptable_partial"]) if k["acceptable_partial"] else "none",
        "decisive_insights": bullet(k["decisive_insights"]),
        "traps": bullet(k["traps"]),
        "answer_a": anonymise(observations[pair[pair[order]["A"]]]["final"]),
        "answer_b": anonymise(observations[pair[pair[order]["B"]]]["final"]),
    }
    text = (run / "grader-prompt.md").read_text()
    for name, value in fills.items():
        text = text.replace("{{" + name + "}}", value)
    return text


def grade(grading, dry_run, observations=None):
    pair_id, order = grading.rsplit("-", 1)
    pair = load("pairs.json")[pair_id]
    observations = observations or load("observations.json")
    command = BASE + ["--model", protocol["grader"]["model"], "--tools", ""]
    stage = Path(protocol["stage"])
    cwd = stage / "grader"
    cwd.mkdir(parents=True, exist_ok=True)
    execute(command, grader_prompt(pair, order, observations), run / "grades" / f"{grading}.jsonl", cwd,
            run / "grades" / f"{grading}.execution.json", dry_run)


def parse_grade(grading):
    final = parse_stream(run / "grades" / f"{grading}.jsonl")["final"]
    match = re.search(r"\{.*\}", final, re.S)
    try:
        return json.loads(match.group(0)) if match else None
    except json.JSONDecodeError:
        return None


def calibration():
    pairs, observations = load("pairs.json"), load("observations.json")
    chosen = sorted(random.Random(131313).sample(sorted(pairs), 10))
    sheet = ["# Run 13 human calibration\n",
             "For each pair, read the question and key, then fill `calibration-human.json`: each answer's verdict "
             "(pursue, reshape, investigate, park, design review or unclear) and which answer shows better judgment "
             "(A, B or tie). Grade before looking at any model grades.\n"]
    blank = {}
    for n, pair_id in enumerate(chosen, 1):
        pair = pairs[pair_id]
        prompt = grader_prompt(pair, "o1", observations)
        body = prompt.split("## Question", 1)[1].split("## Output", 1)[0]
        sheet.append(f"\n---\n\n## Pair {n}: `{pair_id}`\n\n### Question{body}")
        blank[pair_id] = {"A_verdict": "", "B_verdict": "", "preference": ""}
    (run / "calibration-sheet.md").write_text("\n".join(sheet))
    if not (run / "calibration-human.json").exists():
        save("calibration-human.json", blank)
    print("calibration pairs:", ", ".join(chosen))


def mean(values):
    values = list(values)
    return round(sum(values) / len(values), 3) if values else None


def analyze():
    pairs, observations = load("pairs.json"), load("observations.json")
    per_answer, preferences, failures = {}, {}, []
    for pair_id, pair in pairs.items():
        votes = []
        for order in ("o1", "o2"):
            path = run / "grades" / f"{pair_id}-{order}.jsonl"
            grade_data = parse_grade(f"{pair_id}-{order}") if path.exists() else None
            if grade_data is None:
                failures.append(f"{pair_id}-{order}")
                continue
            for slot in ("A", "B"):
                arm = pair[order][slot]
                per_answer.setdefault(pair[arm], []).append(grade_data[slot])
            pref = grade_data.get("preference")
            votes.append(pair[order][pref] if pref in ("A", "B") else "tie")
        if votes:
            preferences[pair_id] = votes[0] if len(votes) == 2 and votes[0] == votes[1] else (
                "tie" if len(votes) == 2 else votes[0])
    pursue = {sid for sid, k in key.items() if k["expected"] == ["pursue"]}
    groups = {}
    for name, grades in per_answer.items():
        obs = observations[name]
        g = groups.setdefault(f"{obs['model_short']}-{obs['arm']}", {"verdict": [], "insights": [], "traps": [],
                                                                      "fabricated": [], "pursue_miss": 0.0,
                                                                      "verdicts": {}, "selected": [],
                                                                      "verdict_selected": []})
        score = mean(x["verdict_score"] for x in grades)
        if obs["scenario"] != "s09-direct-debit":
            g["verdict"].append(score)
            if obs["arm"] == "skill" and obs["skills_invoked"]:
                g["verdict_selected"].append(score)
        if obs["scenario"] in pursue:
            g["pursue_miss"] += 1 - score
        g["insights"].append(mean(mean(x["insights_hit"]) for x in grades))
        g["traps"].append(mean(mean(x["traps_fallen"]) for x in grades))
        g["fabricated"].append(mean(len(x["fabricated_figures"]) for x in grades))
        for x in grades:
            g["verdicts"][x["verdict"]] = g["verdicts"].get(x["verdict"], 0) + 1 / len(grades)
        g["selected"].append(bool(obs["skills_invoked"]))
    summary = {name: {"n": len(g["insights"]), "verdict_accuracy": mean(g["verdict"]),
                      "verdict_accuracy_when_selected": mean(g["verdict_selected"]),
                      "insight_hit_rate": mean(g["insights"]), "trap_rate": mean(g["traps"]),
                      "fabricated_per_answer": mean(g["fabricated"]), "pursue_misses": round(g["pursue_miss"], 2),
                      "verdict_distribution": {k: round(v, 2) for k, v in sorted(g["verdicts"].items())},
                      "selection_rate": mean(g["selected"])} for name, g in sorted(groups.items())}
    win = {}
    for short in MODELS:
        votes = [v for p, v in preferences.items() if pairs[p]["model_short"] == short]
        win[short] = mean(1 if v == "skill" else 0.5 if v == "tie" else 0 for v in votes)
    decision = {}
    for short in MODELS:
        s, c = summary.get(f"{short}-skill"), summary.get(f"{short}-control")
        if not s or not c:
            continue
        delta = round(s["verdict_accuracy"] - c["verdict_accuracy"], 3)
        harm = s["pursue_misses"] - c["pursue_misses"] >= 2 or win[short] < 0.40
        benefit = (delta >= 0.15 or win[short] >= 0.65) and s["trap_rate"] <= c["trap_rate"]
        neutral = abs(delta) <= 0.10 and 0.40 <= win[short] <= 0.60
        decision[short] = {"accuracy_delta": delta, "win_rate": win[short],
                           "rule": "harm" if harm else "benefit" if benefit else "neutral" if neutral else "inconclusive"}
    result = {"summary": summary, "win_rate": win, "pair_preferences": preferences, "decision": decision,
              "grading_failures": failures}
    human_path = run / "calibration-human.json"
    if human_path.exists():
        human = json.loads(human_path.read_text())
        rows = []
        for pair_id, h in human.items():
            if not h.get("preference"):
                continue
            g = parse_grade(f"{pair_id}-o1")
            if g:
                rows.append({"pair": pair_id,
                             "verdict_agree": (h["A_verdict"] == g["A"]["verdict"]) + (h["B_verdict"] == g["B"]["verdict"]),
                             "preference_agree": h["preference"] == g["preference"]})
        result["calibration"] = {"pairs": len(rows),
                                 "pairs_with_both_verdicts_agreeing": sum(r["verdict_agree"] == 2 for r in rows),
                                 "preference_agreement": sum(r["preference_agree"] for r in rows), "rows": rows}
    save("analysis.json", result)
    print(json.dumps({k: result[k] for k in ("summary", "win_rate", "decision", "grading_failures")}, indent=2))
    if "calibration" in result:
        print(json.dumps({k: v for k, v in result["calibration"].items() if k != "rows"}))


if __name__ == "__main__":
    command, *rest = sys.argv[1:]
    dry = "--dry-run" in rest
    rest = [r for r in rest if r != "--dry-run"]
    {"cases": write_cases, "extract": extract, "pairs": write_pairs, "calibration": calibration,
     "analyze": analyze}.get(command, lambda: None)()
    if command == "respond":
        respond(rest[0], dry)
    elif command == "grade":
        grade(rest[0], dry)
