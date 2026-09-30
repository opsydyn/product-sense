# Product Sense qualification

This directory contains synthetic skill evaluations, separate from the skill's runtime instructions. Results qualify only the cases and conditions recorded in each run.

## Repeat a run

1. Create a new run directory. Record the skill commit, source hashes, task prompts, criteria, sample budget and stopping rule before dispatching responders.
2. Run each task once per arm in a fresh-context subagent. Give controls the task without Product Sense metadata or instructions. Give candidates the task plus the skill name, description and entrypoint path; allow them to select the skill and read relevant references. Do not give responders the rubric, assessment, other responses or previous conversation.
3. Permit only reading selected instructions and saving each response to its own JSON file. Use synthetic tasks; perform no external contacts, experiments, installations or product changes.
4. Save case, arm, selected_skill, actual read_files and the exact final response. Wait for each responder to finish before reviewing its output.
5. Manually evaluate each criterion with supporting evidence. Check requested word limits, response completeness and unchanged source hashes. Preserve failures.
6. Report observed results and limits. Metadata supplied in a test is separate from native discovery. A single sample does not establish repeatability or causal benefit. Test revisions in a new run with controls; do not rewrite the skill during an evaluation.

See [run-1/report.md](run-1/report.md) for the first result, [protocol.json](run-1/protocol.json) for its inputs and [evaluation.json](run-1/evaluation.json) for criterion-level scoring.

See [run-2/report.md](run-2/report.md) for native CLI discovery, an explicitly invoked approved fix, and a native metadata failure and repair. Run 2 uses one ephemeral read-only CLI model session rather than metadata supplied to a subagent.
