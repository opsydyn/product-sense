"""Run 14 harness: trimmed-skill regression checks and three-arm judgment comparison.

Subcommands:
  cases                       write cases.json (judgment cases shuffled, then regression cases)
  respond NAME [--dry-run]    run one responder session once
  extract                     write observations.json from responder event streams
  pairs                       write pairs.json (new vs old, new vs none) with A/B for both orders
  grade GRADING [--dry-run]   run one grader session once (GRADING = PAIR-o1|PAIR-o2)
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
answer_key = json.loads((run / "answer-key.json").read_text())
key = {s["id"]: s for s in answer_key["scenarios"]}
MODELS = {"opus": "claude-opus-5-5", "sonnet": "claude-sonnet-5-5"}
ARMS = ("new", "old", "none")
COMPARISONS = (("new", "old"), ("new", "none"))
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
    judgment = [{"name": f"{sid}-{short}-{arm}-{i}", "part": "judgment", "scenario": sid, "model": model,
                 "model_short": short, "arm": arm, "sample": i, "prompt": f"scenarios/{sid}.txt",
                 "tools": protocol["responder_tools"]}
                for sid in key for short, model in MODELS.items() for arm in ARMS for i in range(1, SAMPLES + 1)]
    random.Random(14).shuffle(judgment)
    regression = []
    for short in MODELS:
        for i in (1, 2, 3):
            regression.append({"name": f"reg-assess-{short}-{i}", "part": "regression", "kind": "capped assessment",
                               "model": MODELS[short], "model_short": short, "arm": "new",
                               "prompt": "assess-prompt.txt", "tools": "Skill,Read,Glob,Grep"})
        regression.append({"name": f"reg-ticket-{short}", "part": "regression", "kind": "approved-ticket guard",
                           "model": MODELS[short], "model_short": short, "arm": "new", "prompt": "ticket-prompt.txt",
                           "tools": "Skill,Read,Glob,Grep,Edit", "fixture": True})
    regression.append({"name": "reg-copy-opus", "part": "regression", "kind": "explicit approved-copy guard",
                       "model": MODELS["opus"], "model_short": "opus", "arm": "new", "prompt": "copy-guard-prompt.txt",
                       "tools": "Skill,Read,Glob,Grep"})
    regression.append({"name": "reg-codex-assess", "part": "regression", "kind": "capped assessment", "codex": True,
                       "model": "codex native default", "model_short": "codex", "arm": "new",
                       "prompt": "assess-prompt.txt"})
    save("cases.json", judgment + regression)
    print(len(judgment), "judgment cases,", len(regression), "regression cases")


def execute(command, prompt_text, events, cwd, record_path, dry_run):
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
    return record


def respond(name, dry_run):
    case = {c["name"]: c for c in load("cases.json")}[name]
    stage = Path(protocol["stage"])
    cwd = stage / "cwd" / name
    events = run / "responses" / f"{name}.jsonl"
    if case.get("codex"):
        command = ["codex", "-a", "never", "exec", "--ephemeral", "--sandbox", "read-only", "--skip-git-repo-check",
                   "--json", "--output-last-message", str(run / "responses" / f"{name}.final.txt"), "--cd", str(cwd), "-"]
    else:
        command = BASE + ["--model", case["model"], "--tools", case["tools"], "--allowedTools", case["tools"]]
        if case["arm"] != "none":
            plugin = str(stage / case["arm"])
            command += ["--plugin-dir", plugin, "--add-dir", plugin]
    if not dry_run:
        if cwd.exists():
            raise SystemExit("Stage already exists; do not overwrite or retry")
        if case.get("fixture"):
            shutil.copytree(run / "fixture", cwd)
        else:
            cwd.mkdir(parents=True)
    record = execute(command, (run / case["prompt"]).read_text(), events, cwd,
                     run / "responses" / f"{name}.execution.json", dry_run)
    if dry_run:
        return
    if case.get("fixture"):
        for path in ("src/format.js", "test/format.test.js"):
            shutil.copyfile(cwd / path, run / "responses" / f"{name}-{path.replace('/', '-')}")
        test = subprocess.run(["node", "--test"], cwd=cwd, capture_output=True, text=True)
        record["node_test_exit_code"] = test.returncode
        (run / "responses" / f"{name}-node-test.txt").write_text(test.stdout + test.stderr)
    (run / "responses" / f"{name}.execution.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({"case": name, **{k: v for k, v in record.items() if k not in {"command", "cwd"}}}))


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
        elif event.get("type") == "item.completed" and event["item"].get("type") == "command_execution":
            if ".agents/skills/product-sense/" in event["item"]["command"]:
                reads.append(event["item"]["command"])
    return {"skill_available": available, "skills_invoked": skills, "reads": reads, "final": final,
            "word_count": len(final.split()), "reported_list_cost_usd": cost, "model_used": model, "is_error": error}


def anonymise(text):
    return "\n".join(line for line in text.splitlines() if not IDENTIFYING.search(line)).strip()


def extract():
    out = {}
    fixture_test = (run / "fixture/test/format.test.js").read_bytes()
    for case in load("cases.json"):
        events = run / "responses" / f"{case['name']}.jsonl"
        if not events.exists():
            continue
        record = {**case, **parse_stream(events)}
        if case.get("codex"):
            final_path = run / "responses" / f"{case['name']}.final.txt"
            record["final"] = final_path.read_text() if final_path.exists() else ""
            record["word_count"] = len(record["final"].split())
            record["skills_invoked"] = ["product-sense"] if any("SKILL.md" in r for r in record["reads"]) else []
        if case.get("fixture"):
            execution = load(f"responses/{case['name']}.execution.json")
            record["node_test_pass"] = execution.get("node_test_exit_code") == 0
            record["test_unchanged"] = (run / "responses" / f"{case['name']}-test-format.test.js").read_bytes() == fixture_test
        record["skill_word_after_anonymising"] = bool(re.search(r"\bskill", anonymise(record["final"]), re.I))
        out[case["name"]] = record
    save("observations.json", out)
    for name, r in sorted(out.items()):
        print(f"{name:36} avail={r['skill_available']!s:5} skills={len(r['skills_invoked'])} reads={len(r['reads'])} "
              f"words={r['word_count']} err={r['is_error']}")


def write_pairs():
    rng = random.Random(1414)
    pairs = {}
    for first, second in COMPARISONS:
        for sid in key:
            for short in MODELS:
                for i in range(1, SAMPLES + 1):
                    first_is_a = rng.random() < 0.5
                    a, b = (first, second) if first_is_a else (second, first)
                    pairs[f"{first}-vs-{second}-{sid}-{short}-{i}"] = {
                        "comparison": f"{first}-vs-{second}", "scenario": sid, "model_short": short, "sample": i,
                        first: f"{sid}-{short}-{first}-{i}", second: f"{sid}-{short}-{second}-{i}",
                        "o1": {"A": a, "B": b}, "o2": {"A": b, "B": a}}
    save("pairs.json", pairs)
    print(len(pairs), "pairs")


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


def grade(grading, dry_run):
    pair_id, order = grading.rsplit("-", 1)
    pair = load("pairs.json")[pair_id]
    cwd = Path(protocol["stage"]) / "grader"
    cwd.mkdir(parents=True, exist_ok=True)
    command = BASE + ["--model", protocol["grader"]["model"], "--tools", ""]
    prompt_text = grader_prompt(pair, order, load("observations.json"))
    if dry_run:
        print(prompt_text)
        return
    record = execute(command, prompt_text, run / "grades" / f"{grading}.jsonl", cwd,
                     run / "grades" / f"{grading}.execution.json", dry_run)
    (run / "grades" / f"{grading}.execution.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({"grading": grading, **{k: v for k, v in record.items() if k not in {"command", "cwd"}}}))


def parse_grade(grading):
    final = parse_stream(run / "grades" / f"{grading}.jsonl")["final"]
    match = re.search(r"\{.*\}", final, re.S)
    try:
        return json.loads(match.group(0)) if match else None
    except json.JSONDecodeError:
        return None


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
                per_answer.setdefault(pair[pair[order][slot]], []).append(grade_data[slot])
            pref = grade_data.get("preference")
            votes.append(pair[order][pref] if pref in ("A", "B") else "tie")
        if votes:
            preferences[pair_id] = votes[0] if len(votes) == 1 or votes[0] == votes[1] else "tie"
    targeted = {(sid, i) for sid, i in answer_key["targeted_insights"]["items"]}
    pursue = {sid for sid, k in key.items() if k["expected"] == ["pursue"]}
    design = {sid for sid, k in key.items() if k["expected"] == ["design review"]}
    groups = {}
    for name, grades in per_answer.items():
        obs = observations[name]
        g = groups.setdefault(f"{obs['model_short']}-{obs['arm']}", {"verdict": [], "insights": [], "targeted": [],
                                                                      "traps": [], "fabricated": [], "pursue_miss": 0.0,
                                                                      "verdicts": {}, "selected": [], "over_cap": []})
        if obs["scenario"] not in design:
            g["verdict"].append(mean(x["verdict_score"] for x in grades))
        if obs["scenario"] in pursue:
            g["pursue_miss"] += 1 - mean(x["verdict_score"] for x in grades)
        g["insights"].append(mean(mean(x["insights_hit"]) for x in grades))
        for sid, i in targeted:
            if sid == obs["scenario"]:
                g["targeted"].append(mean(x["insights_hit"][i] for x in grades))
        g["traps"].append(mean(mean(x["traps_fallen"]) for x in grades))
        g["fabricated"].append(mean(len(x["fabricated_figures"]) for x in grades))
        for x in grades:
            g["verdicts"][x["verdict"]] = g["verdicts"].get(x["verdict"], 0) + 1 / len(grades)
        g["selected"].append(bool(obs["skills_invoked"]))
        g["over_cap"].append(obs["word_count"] > 250)
    summary = {name: {"n": len(g["insights"]), "verdict_accuracy": mean(g["verdict"]),
                      "insight_hit_rate": mean(g["insights"]), "targeted_insight_hit_rate": mean(g["targeted"]),
                      "trap_rate": mean(g["traps"]), "fabricated_per_answer": mean(g["fabricated"]),
                      "pursue_misses": round(g["pursue_miss"], 2), "over_cap": sum(g["over_cap"]),
                      "selection_rate": mean(g["selected"]),
                      "verdict_distribution": {k: round(v, 2) for k, v in sorted(g["verdicts"].items())}}
               for name, g in sorted(groups.items())}
    win = {}
    for first, second in COMPARISONS:
        for short in MODELS:
            votes = [v for p, v in preferences.items()
                     if pairs[p]["comparison"] == f"{first}-vs-{second}" and pairs[p]["model_short"] == short]
            win[f"{first}-vs-{second}-{short}"] = mean(1 if v == first else 0.5 if v == "tie" else 0 for v in votes)
    decision = {}
    for short in MODELS:
        new, old, none = (summary.get(f"{short}-{arm}") for arm in ARMS)
        if not (new and old and none):
            continue
        d_old = round(new["verdict_accuracy"] - old["verdict_accuracy"], 3)
        d_none = round(new["verdict_accuracy"] - none["verdict_accuracy"], 3)
        w_old, w_none = win[f"new-vs-old-{short}"], win[f"new-vs-none-{short}"]
        harm = new["pursue_misses"] - none["pursue_misses"] >= 2 or w_none < 0.40
        benefit = (d_none >= 0.15 or w_none >= 0.65) and new["trap_rate"] <= none["trap_rate"]
        neutral = abs(d_none) <= 0.10 and 0.40 <= w_none <= 0.60
        decision[short] = {
            "trim_non_inferior": d_old >= -0.10 and w_old >= 0.40,
            "new_minus_old_accuracy": d_old, "win_rate_new_vs_old": w_old,
            "targeted_insight_gain_vs_old": round(new["targeted_insight_hit_rate"] - old["targeted_insight_hit_rate"], 3),
            "new_minus_none_accuracy": d_none, "win_rate_new_vs_none": w_none,
            "vs_none_rule": "harm" if harm else "benefit" if benefit else "neutral" if neutral else "inconclusive"}
    pooled = {arm: mean(summary[f"{s}-{arm}"]["targeted_insight_hit_rate"] for s in MODELS if f"{s}-{arm}" in summary)
              for arm in ARMS}
    result = {"summary": summary, "win_rate": win, "pair_preferences": preferences, "decision": decision,
              "targeted_insight_hit_rate_pooled": pooled,
              "fixes_effective": pooled["new"] is not None and pooled["old"] is not None
              and pooled["new"] - pooled["old"] >= 0.15,
              "grading_failures": failures}
    save("analysis.json", result)
    print(json.dumps({k: result[k] for k in ("decision", "targeted_insight_hit_rate_pooled", "fixes_effective",
                                             "grading_failures")}, indent=2))


if __name__ == "__main__":
    command, *rest = sys.argv[1:]
    dry = "--dry-run" in rest
    rest = [r for r in rest if r != "--dry-run"]
    {"cases": write_cases, "extract": extract, "pairs": write_pairs, "analyze": analyze}.get(command, lambda: None)()
    if command == "respond":
        respond(rest[0], dry)
    elif command == "grade":
        grade(rest[0], dry)
