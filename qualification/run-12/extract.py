"""Extract objective observations from retained event streams; judgement criteria are scored separately."""

import json
from pathlib import Path

run = Path(__file__).resolve().parent
protocol = json.loads((run / "protocol.json").read_text())
skill_root = "/skills/product-sense/"
out = {}
for case in protocol["claude_cases"] + protocol["codex_cases"]:
    name = case["name"]
    execution = json.loads((run / f"{name}-execution.json").read_text())
    skills, reads, final, model, cost = [], [], "", None, None
    for line in (run / f"{name}-events.jsonl").read_text().splitlines():
        event = json.loads(line)
        if name.startswith("codex-"):
            item = event.get("item", {})
            if event["type"] == "item.completed" and item.get("type") == "command_execution":
                if ".agents/skills/product-sense/" in item["command"]:
                    reads.append(item["command"])
        elif event["type"] == "assistant":
            for block in event["message"]["content"]:
                if block.get("type") == "tool_use" and block["name"] == "Skill":
                    skills.append(block["input"].get("skill"))
                if block.get("type") == "tool_use" and block["name"] == "Read":
                    reads.append(block["input"].get("file_path"))
        elif event["type"] == "result":
            final, cost = event.get("result", ""), event.get("total_cost_usd")
            model = list(event.get("modelUsage", {}))
    if name.startswith("codex-"):
        skill_root = ".agents/skills/product-sense/"
        final = (run / f"{name}-final.txt").read_text() if (run / f"{name}-final.txt").exists() else ""
        skills = ["product-sense"] if any("product-sense/SKILL.md" in r for r in reads) else []
    record = {
        "kind": case["kind"],
        "exit_code": execution.get("exit_code"),
        "timeout": execution.get("timeout", False),
        "model": model or case.get("model", "native default"),
        "skills_invoked": skills,
        "product_sense_reads": [r for r in reads if skill_root in str(r)],
        "word_count": len(final.split()),
        "reported_list_cost_usd": cost,
        "final": final,
    }
    if case.get("fixture"):
        record["node_test_pass"] = execution.get("node_test_exit_code") == 0
        record["test_unchanged"] = (run / f"{name}-test-format.test.js").read_bytes() == fixture_test
        record["format_js"] = (run / f"{name}-src-format.js").read_text()
    out[name] = record
(run / "observations.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
for name, r in out.items():
    print(f"{name:18} exit={r['exit_code']} skills={r['skills_invoked']} reads={len(r['product_sense_reads'])} "
          f"words={r['word_count']} cost={r['reported_list_cost_usd']}"
          + (f" test_pass={r['node_test_pass']} test_unchanged={r['test_unchanged']}" if "node_test_pass" in r else ""))
