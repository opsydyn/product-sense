# Run 4: Claude package and native discovery

## Result

The skills-only Claude package builds reproducibly and passes strict native manifest validation with no warnings. Model-free inventory reports one skill, with no agents, hooks, MCP or LSP servers. Native Claude session initialisation lists `product-sense:product-sense` from the staged `product-sense@inline` plugin, version `0.1.0`.

Behaviour qualification is blocked. The explicit case returned HTTP 429 before any model inference: “You've hit your weekly limit · resets Oct 3 at 8pm (Europe/London)”. The CLI exited 1, reported `is_error: true`, zero model tokens and US$0 cost. Its result subtype was nevertheless `success`; that field is not a passing task result.

The implicit case was not attempted after this account-wide quota block. Explicit skill invocation, implicit selection, reference use and the 180-word requirement remain untested on Claude. The earlier Codex word-limit failure remains in run 3; this run neither repairs nor overturns it.

## Package evidence

- Python 3.14.4 standard-library builder; all seven integration tests pass. The initial six tests first failed because the builder did not exist; the additional manifest-parent regression first failed on both symlink paths.
- Manifest author is Alan P Currie, the recorded author of the existing repository commits; version is a local candidate, not a published release.
- ZIP contains exactly seven regular files: manifest, entrypoint and five references. Canonical skill/reference bytes are unchanged.
- Tests cover exact archive payload, stale-output removal, byte-identical rebuilds, missing entrypoint/reference failure and rejected reference and manifest-parent symlinks.
- Archive SHA-256: `8203e40312ae143359f2fdb43574ba2e866928111f0657cb0f2014644d58ca82`.
- Staged files extracted from the ZIP match its inventory, and both staged payload and repository source remain unchanged after the attempted native case.

The auxiliary skill-creator `quick_validate.py` helper could not run: PyYAML is absent from the active, bundled and system Python interpreters. No dependency was installed for this unchanged entrypoint. This is separate from the passing package tests, native manifest validation and catalogue discovery.

## Independent review

A fresh read-only reviewer reproduced one Important defect: a symlink in `packaging/` or `packaging/claude/` bypassed the builder's final-file check and imported an external manifest. A regression test reproduced both failures, then passed after checking every path component from the source root. Existing outputs remain unchanged on rejection. The full seven-test suite passes and the corrected builder emits the same archive bytes and hash.

No Critical or Minor findings were reported. The reviewer did not judge model behaviour, other hosts, publication or global installation because those lacked evidence or were outside scope. It did not independently verify the historical RED chronology; initial failures were observed in the implementer's tool outputs, with the chronology recorded here rather than retained as a raw transcript. The review and fix do not qualify any blocked behaviour.

## Native conditions

Claude Code 2.1.259 on the local macOS host selected its default `claude-sonnet-5`. The model was not overridden. Each predeclared case had a US$1 cap and 180-second timeout; there was one attempt and no retry.

The session used `--restricted`, explicit hook disabling, `--strict-mcp-config`, no Chrome integration and no session persistence. Its observed tools were exactly Glob, Grep, Read and Skill, with no MCP servers. Native built-in skills were also present. User settings contained hooks and were ignored for this restricted session; no global configuration was changed. The snapshot proves these observed conditions, not complete isolation from every host default or managed policy.

The plugin was loaded session-only from a disposable, symlink-free directory extracted from the built archive. Nothing was installed globally, submitted or published. Discovery on this CLI does not establish behaviour or acceptance on Claude chat, Cowork or OpenAI plugin surfaces.

## Next bounded check

After Claude inference access returns, create a new run with the same two prompts and current package hashes. Verify explicit native invocation and ordinary implicit selection, including the 180-word cap. Preserve this blocked attempt. No skill instruction change is supported by this run.

See `protocol.json`, `native-inventory.txt`, `validation.txt`, `explicit-events.jsonl`, `explicit-execution.json`, `evaluation.json`, `archive-inventory.json` and `source-verification.json` for evidence.
