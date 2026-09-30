# Claude Package Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans to implement this approved plan in this session. Steps use checkbox syntax for tracking.

**Goal:** Build a distributable Claude plugin from the existing Product Sense source and record native host checks.

**Architecture:** Keep root `SKILL.md` and `references/` canonical. A standard-library Python builder copies them into Claude's plugin layout and creates a reproducible ZIP; host metadata stays outside the skill source.

**Tech Stack:** Python 3 standard library; Claude Code 2.1.259.

**Spec:** The user-approved proposal: shared source, Claude manifest and distributable package, native discovery, explicit invocation and implicit selection including the 180-word case. Publication, global installation and MCP/UI extensions are outside this change.

## Global Constraints

- Preserve canonical instructions byte for byte and existing Codex metadata.
- Package only the manifest, entrypoint and Markdown references; no qualification records, credentials, hooks, tools or symlinks.
- Run at most two fresh Claude model sessions, each capped at US$1; read-only tools, no configured MCP servers, no automatic model retry.
- Keep exact responses and failures; results apply only to this host and these samples.

## Review Focus

- Missing or changed references must not silently create an incomplete package.
- Rebuilding must remove stale generated files and produce identical ZIP bytes.
- Symlinks must not import files from outside the canonical source.
- Manifest validation is separate from native discovery and invocation.
- Native tool events must establish the loaded skill; response quality alone does not prove selection.

### Task 1: Reproducible package

**Files:** `packaging/claude/plugin.json`, `scripts/build_claude.py`, `tests/test_claude_package.py`, `.gitignore`, `PACKAGING.md`.

**Interface:** `build(repo: Path, destination: Path) -> Path` returns the generated ZIP path. Default CLI destination is `dist/claude/`.

- [x] Write integration tests for exact canonical bytes, archive allowlist, stale-file removal, repeatable archives and rejected symlinks/missing sources; watch them fail before implementing the builder.
- [x] Implement the builder and manifest version `0.1.0`, author `Alan P Currie` as recorded in existing repository commits.
- [x] Run `python3 -m unittest discover -s tests -v` and `python3 scripts/build_claude.py`; strictly validate the generated manifest with Claude.

### Task 2: Native Claude qualification

**Files:** `qualification/run-4/`, `qualification/README.md`.

**Interface:** Generated plugin loaded session-only with `--plugin-dir`; responses recorded as stream JSON, stderr and extracted final text.

- [x] Record source/archive hashes, prompts, tools, criteria and stopping rule before either model session.
- [ ] Check model-free plugin validation/details, then run one explicit approved-copy invocation and one ordinary product assessment with a 180-word limit.
- [x] Evaluate catalogue, Skill invocation, reference reads, task compliance, word count and source integrity; report failures and host limits. Native behaviour was blocked before inference; unevaluated criteria are explicit.
- [x] Review the change and verify the fix. Commit the approved work after these checks.

## Execution record

Task 1: complete; six packaging tests RED → GREEN, build and strict native validation passed.

Task 2: native discovery passed; explicit attempt blocked by account-wide HTTP 429, before inference. Implicit case remains pending. No model retry or source edit was made during evaluation.

Final review: one Important manifest-parent symlink bypass reproduced and fixed with a RED → GREEN regression. Full suite: 7/7. No Critical or Minor findings. Corrected builder produces the same candidate archive hash. Auxiliary skill-creator validation remains unavailable because its PyYAML dependency is absent; native discovery and package validation are recorded separately.
