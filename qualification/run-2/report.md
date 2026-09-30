# Native discovery and explicit approved-fix qualification

Date: 30 September 2026. Baseline commit: `3b54222`. Native CLI: `0.159.2`. User configuration selected `gpt-6.1-sol` with high reasoning effort; the model identifier was not independently reported in the execution events.

## Result

Product Sense is installed as a user skill through `/Users/alancurrie/.agents/skills/product-sense`, a symlink to this checkout. Native `skills/list` returned exactly one enabled Product Sense entry with user scope and the canonical checkout path.

One fresh ephemeral CLI session explicitly invoked `$product-sense` on an already-approved button-copy change. Its only model command read `SKILL.md`, `references/shaping.md`, `references/outputs.md` and `references/design.md`, completing with exit code 0. The final answer was exactly:

```text
Start lesson
```

There was no research, redesign, new permission gate or product mutation. The session used a read-only sandbox and approvals set to never, and finished successfully in 16.63 seconds. It included a brief initial skill-use commentary before the instruction read; the final answer itself contained only the requested replacement copy.

## Metadata failure and repair

The behavior passed, but native stderr exposed a packaging defect missed by the earlier YAML syntax checks: `policy.products` included `api`, which this native loader rejects. It ignored the entire `agents/openai.yaml` file. The initial scanner returned the instruction skill without its UI interface, despite reporting no skill-list errors.

After preserving the model-run evidence and verifying its original source hashes, the parent removed only the unsupported `api` entry. A model-free re-scan then returned the display name, UI description, default invocation prompt and both canonical icon paths, with no matching load errors or invalid-metadata warning. The skill body, references and icon asset stayed unchanged. No second model run was performed after this metadata-only repair.

This distinguishes syntax validity from native schema acceptance: a successful skill-list entry alone did not establish that the UI metadata loaded.

## Evidence and reproduction

- [Protocol and criteria](protocol.json): declared task, one-model-run budget, 180-second timeout, CLI configuration and source hashes.
- [Native discovery before repair](native-discovery.json) and [after repair](native-discovery-after-repair.json): filtered native responses with Product Sense metadata.
- [Native scanner helper](native_discovery.py): `python3 qualification/run-2/native_discovery.py --output /private/tmp/product-sense-discovery.json`. It requires permission to initialise Codex's normal local state database. The default output replaces the initial evidence, so use a new output path for subsequent checks.
- [Execution](execution.json), [events](events.jsonl), [stderr](cli.stderr.txt) and [final answer](final.txt): exact command, model actions, warnings and response.
- [Pre-repair source verification](pre-repair-verification.json), [metadata failure](metadata-failure.json), [evaluation](evaluation.json) and [post-repair hashes](post-repair-source-hashes.json): criterion results and the one changed source file.

The prompt supplied the skill name, without its description, body or path. The native command inherited normal user configuration and skill discovery. To repeat the behavior test, use the recorded argv in `execution.json` with `prompt.txt` on stdin and new evidence output paths; this starts another model run.

The first model-free scanner attempt could not start because the outer workspace sandbox prevented SQLite state initialisation under the user's Codex directory. A filesystem escalation allowed the scanner to start. This was a host permission issue, and consumed no model run. The behavioral log also includes a missing `computer-use` MCP executable and state-database lookup fallback warnings. Neither blocked the source read or final answer; those unrelated host settings were left unchanged.

## Limits and next action

This establishes native CLI discovery, actual instruction reading and one successful explicitly invoked narrow fix. It does not establish repeatability, implicit selection in ordinary tasks, native UI appearance or visibility in the currently open desktop chat. The metadata repair was verified through the native scanner; its changed metadata was not subjected to another model run.

Keep the current product guidance. The remaining useful check is a normal product request in a fresh desktop chat to observe implicit selection. Source wording changes are not justified by the current evidence.
