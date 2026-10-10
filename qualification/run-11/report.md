# Run 11: description rewrite, cross-model and approved-ticket checks

Date: 10 October 2026. Candidate: the unreleased changes after 0.1.2 (third-person description that excludes approved-ticket implementation, a single word-cap recipe, appetite terminology, plugin keywords). Source hashes, cases, criteria and budget were recorded in `protocol.json` before any case ran. Each case ran once; there were no retries.

## Result

| Case | Model | Pass | Failed criteria |
|---|---|---|---|
| Capped assessment ×3 | Opus 5.5 | 3/3 | — |
| Capped assessment ×3 | Sonnet 5.5 | 2/3 | `sonnet-assess-3`: skill selected, references not read |
| Capped assessment ×3 | Haiku 5.5 | 0/3 | `haiku-assess-1`: no allocation for the conditional build; `haiku-assess-2`, `-3`: skill not selected, no allocation |
| Approved-ticket guard | Opus, Sonnet, Haiku 5.5 | 3/3 | — |
| Approved-copy guard (explicit) | Opus 5.5 | 1/1 | — |
| Capped assessment | Codex (native default) | 1/1 | — |
| Approved-ticket guard | Codex (native default) | 1/1 | — |

All 15 processes exited 0 within the time limit. Every answer stayed under 180 words (range 105–168). Reported list cost totalled about US$1.17.

**Opus** reproduced run 10: all three selected the skill, read `discovery.md` and `outputs.md`, and fit learning plus a conditional build inside ten days.

**Sonnet** selected the skill every time. One sample answered from `SKILL.md` alone without reading the references. Its answer still met the word cap and the appetite rule.

**Haiku** selected the skill once in three. When it did, it followed the five-part shape but left the conditional build without an allocation (the run 9 failure). The two unselected samples answered with bulleted hypotheses and pass bars that did not fit the ten-day window.

**Approved-ticket guard:** no model invoked the skill or read its references. Each made the minimal `formatTotal` change, `node --test` passed and the test file was unchanged. No answer added a product critique.

## Interpretation and limits

The description change did not cause over-triggering on an approved ticket for any model tested. Opus behaviour on the capped assessment is unchanged from run 10.

The Haiku result cannot be attributed to the new description. No earlier run tested Haiku, so there is no baseline for the old description. A paired run with old and new descriptions on Haiku is needed before concluding whether the rewrite lowered selection.

Three samples per model on one synthetic scenario, and one sample per guard, do not establish rates. Scoring was not blinded. The CLI flagged `claude-haiku-5-5` as an unrecognised model name but served it; `modelUsage` confirms the model. Claude ticket guards had no shell, so they could not run the test themselves; the harness ran it afterwards. Codex used its native model and the skill through the `~/.agents/skills` symlink to this checkout.

See `protocol.json`, `observations.json` (extracted by `extract.py`), `evaluation.json`, per-case event streams, prompts, stderr, execution records, fixture outputs and `fixture/`.
