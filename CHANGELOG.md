# Changelog

## Unreleased

- Rewrite the skill description in the third person: state what the skill produces, and exclude implementing already-approved tickets so it does not load for routine engineering work.
- Keep the capped five-sentence recipe only in `SKILL.md`; `outputs.md` now points to it.
- Use "appetite" consistently for the time or money limit and "time window" for elapsed time.
- Add plugin keywords; spell "judgment" consistently.

Run 11 checked these changes: Opus 3/3 and Codex passed the capped assessment, and no model invoked the skill on an approved ticket. Sonnet passed 2/3 and Haiku 0/3. Run 12 found Haiku 5.5 also ignored the skill with the old description (0/3), so the rewrite did not cause it; Haiku users should invoke the skill explicitly.

## 0.1.2 — beta candidate, 5 October 2026

- Load selected references before assessments; preserve direct completion of approved narrow edits.
- Use a five-sentence recipe and a per-sentence budget for quick capped assessments.
- Distinguish elapsed time from effort; fit learning and delivery into the agreed appetite and window, with later investment a separate decision.
- Build outside the installed source tree and reject paths that could overwrite source.
- Provide a Codex install bundle alongside the Claude Code plugin, from identical instructions and references.
- Add installation instructions, examples, release preparation guidance and retained qualification evidence.

The first candidate still exceeded the word cap in four of five Claude samples. Those failures remain in run 8, with two later scope omissions retained in run 9. The final run 10 passed five Claude assessments, a Codex assessment and exact-copy guards on both hosts; one elapsed-schedule ambiguity remains. No public publication is claimed.

## 0.1.1 — 2 October 2026

Add Radical Candor attribution. Retain runtime guidance after five pressure samples and an approved-copy guard passed; no incremental benefit was demonstrated.

## 0.1.0 — 30 September 2026

Package the shared skill for Claude Code with reproducible builds and manifest checks. Verify Codex discovery and explicit invocation; retain a desktop word-cap failure and Claude's initial quota-blocked attempt.
