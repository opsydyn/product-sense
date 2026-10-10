# Run 13: does Product Sense improve product judgment?

Date: 10 October 2026. Skill at `cdfc428`; hashes, scenarios, key, grader prompt and decision rules were fixed in `protocol.json` and `answer-key.json` before any session ran. The key was approved by Alan P Currie without amendment. 120 responder sessions (10 scenarios × Opus/Sonnet 5.5 × skill/control × 3) and 120 blind order-swapped grader sessions all completed; no retries, no grading failures. Reported list cost about US$11.73 (responders 6.23, graders 5.50).

**Status: model-graded results complete; human calibration pending.** The pre-registered rule treats model grades as unreliable if the human reviewer agrees on verdicts in fewer than 8 of 10 calibration pairs (`calibration-sheet.md`, `calibration-human.json`).

## Pre-registered result

| Model | Verdict accuracy, control → skill | Blind win rate for skill | Rule |
|---|---|---|---|
| Opus 5.5 | 0.861 → 0.880 (+1.9) | 0.50 | **Neutral** |
| Sonnet 5.5 | 0.889 → 0.787 (−10.2) | 0.45 | **Inconclusive** (just outside neutral) |

Neither model meets the benefit rule. Neither meets the harm rule: no pursue scenario was missed by either arm, so there is **no caution bias**. On this set, Product Sense does not make Claude reach better product decisions.

The skill was available and selected in all 60 skill-arm sessions and absent from all 60 controls. Opus read references in 28/30 sessions; Sonnet in 16/30.

## Where the arms differed

| Measure | Opus control | Opus skill | Sonnet control | Sonnet skill |
|---|---|---|---|---|
| Answers over the 250-word cap | **30/30** | 7/30 | **30/30** | 2/30 |
| Mean words | 312 | 216 | 294 | 199 |
| Fabricated figures per answer | 1.37 | **0.47** | 0.65 | **0.32** |
| Decisive-insight hit rate | 0.89 | 0.88 | 0.85 | 0.78 |
| Trap rate | 0.05 | 0.00 | 0.00 | 0.02 |

By scenario:

- **Pursue cases (s01, s02, s10):** every answer in both arms chose pursue. Skill answers hit fewer decisive insights on s01 and s02, mostly the permission/totals guardrail and the consent detail. They were about 100 words shorter because they obeyed the cap; controls did not.
- **Design review (s09):** the clearest skill gain. Insight hit rate 1.0 for the skill on both models against 0.5 (Opus) and 0.33 (Sonnet) for controls, and the grader preferred the skill answer in all six pairs.
- **Sunk cost (s04):** Opus with the skill parked 6/6 (accuracy 1.0); Opus control reshaped or investigated (0.25). Sonnet arms were similar.
- **Enterprise deal (s03):** Opus with the skill parked 4/6; controls reshaped. Sonnet with the skill was labelled "investigate" 4/6 and scored 0, although its answers withheld engineering until a signed LOI, close to the key's acceptable reshape.
- **Correlation (s08):** both arms caught the selection effect (insights 1.0). Skill answers proposed an optional prompt with a randomised holdout and labelled it reshape, which the key scores 0.5; controls called it investigate (1.0).

Much of the accuracy difference sits on the boundary between reshape, investigate and park, where answers recommending nearly the same action receive different labels. That reflects key and label strictness as much as judgment.

One skill answer (s01, Sonnet, no reference read) labelled 41 support tickets as "reported, not observed" evidence. Support tickets are observed behaviour, so the evidence-label system can be misapplied when references are skipped.

## Interpretation

The skill's measurable value on this set is **discipline, not better decisions**: it makes Claude obey length limits, invent fewer figures and review flows more completely, and on Opus it parks sunk-cost work more decisively. It does not raise verdict accuracy, and on Sonnet it trades away some insight coverage for brevity.

Under the neutral rule, the protocol's next step is to consider trimming guidance that does not move results. Candidates, to be confirmed on new scenarios rather than these:

1. Keep the design reference and the evidence and no-invention rules; they show the clearest effects.
2. Let the verdict vocabulary describe the recommended action, not force one label; several score losses were label disputes.
3. Have Sonnet read the routed references reliably, or move what matters into `SKILL.md`; it skipped them in 14 of 30 sessions.

## Limits

- Three samples per cell detect only large effects. Scenarios are synthetic.
- Claude wrote the key, answered and graded. One human approved the key; calibration of the grader is pending.
- Anonymisation removed skill names, but skill answers have a recognisable style (bold verdict first, evidence labels), so the grader was not fully blind.
- Controls ignored the word cap, so insight coverage is confounded with length. The grader was told not to reward length.
- Claude Code CLI only.

See `protocol.json`, `answer-key.json`, `grader-prompt.md`, `harness.py`, `cases.json`, `pairs.json`, `responses/`, `grades/`, `observations.json` and `analysis.json`.
