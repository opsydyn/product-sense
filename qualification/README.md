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

See [run-3/report.md](run-3/report.md) for desktop catalogue discovery and implicit selection in a fresh projectless desktop chat. Selection passed; the response exceeded its requested word limit, so complete task compliance did not pass.

See [run-4/report.md](run-4/report.md) for reproducible Claude packaging, strict manifest validation and native CLI session discovery. The account's weekly limit blocked model inference; explicit and implicit behaviour remain unqualified on Claude.

See [run-5/report.md](run-5/report.md) for five baseline candid-critique samples and an approved-copy regression. All declared criteria passed, so the run stopped before a candidate behavioural addition. Radical Candor was added as supporting-source attribution; no incremental behavioural benefit is claimed.

See [run-6/report.md](run-6/report.md) for the resumed Claude check on 5 October 2026 against version `0.1.1`. Package checks and native discovery passed; expired OAuth authentication blocked inference. The weekly-limit status could not be checked, and both behavioural cases remain unqualified.

See [run-7/report.md](run-7/report.md) for both native Claude cases after login was restored. Explicit invocation and exact copy passed. Automatic selection passed, but the implicit assessment failed reference loading, its 180-word cap and fitting the proposed work into ten-day availability. No runtime guidance was changed.

See [run-8/report.md](run-8/report.md) for the five-sample baseline/candidate comparison, package-location regression and first candidate failures.

See [run-9/report.md](run-9/report.md) for five capped assessments that passed length and references but retained two conditional-budget omissions.

See [run-10/report.md](run-10/report.md) for the final beta-candidate checks: five passing Claude assessments, a passing native Codex assessment, approved-copy guards on both hosts and thirteen package tests. Calendar scheduling, licence selection and actual publication remain separately qualified or pending.

See [run-11/report.md](run-11/report.md) for the description rewrite across Opus, Sonnet and Haiku 5.5, a new approved-ticket guard and Codex checks. Opus passed 3/3, Sonnet 2/3 (one skipped reference read) and Haiku 0/3 (selection 1/3, with conditional-build allocation missing). No model invoked the skill on an approved ticket. Haiku has no old-description baseline yet.

See [run-12/report.md](run-12/report.md) for a paired Haiku 5.5 comparison of the old and new descriptions. Neither selected the skill (0/3 each) although it was available in every session, so the rewrite did not cause Haiku's low selection. Haiku users should invoke the skill explicitly.

See [run-13/report.md](run-13/report.md) ([design](run-13/design.md)) for the first judgment-quality comparison against a no-skill control: ten scenarios whose right call varies, Opus and Sonnet, blind order-swapped grading. Neutral on Opus and inconclusive on Sonnet: the skill did not improve decisions or make Claude over-cautious, but it enforced length limits, halved invented figures and improved design reviews. Human calibration of the grader is pending.

See [run-14/report.md](run-14/report.md) for the trimmed skill against the committed skill and no skill on eight new scenarios, with regression checks. All regression checks passed and the targeted fixes worked (+22 to +25 points on targeted insights). The trim beat no skill in blind preference on both models, but it failed the pre-registered non-inferiority rule on Opus by 1.9 points, entirely from one scenario labelled investigate rather than park. The owner adopted the trim as a documented deviation from that rule.
