# Run 6: resumed Claude behaviour qualification

Date: 5 October 2026. Source baseline: `4d7bf4d`. This resumes the two native cases from run 4 against the current `0.1.1` package. The earlier weekly-limit failure is preserved.

## Result

Behaviour qualification remains blocked, now by authentication. The explicit case returned `authentication_failed`: “Failed to authenticate: OAuth session expired and could not be refreshed”. Claude exited 1 before inference, with `is_error: true`, zero model tokens and US$0 reported cost. The result subtype was nevertheless `success`; that field does not establish task success.

The implicit case was not attempted after the account authentication failure, as required by the predeclared stopping rule. Explicit skill invocation, implicit selection, reference use and the 180-word requirement remain untested on Claude. This attempt could not establish whether the weekly limit has reset. The previous Codex word-limit failure remains recorded in run 3.

## Verified conditions

- All seven package integration tests passed. Strict native manifest validation passed with zero errors and warnings.
- Native Claude Code `2.1.289` initialisation lists the staged `product-sense@inline` plugin, version `0.1.1`, and the `product-sense:product-sense` skill.
- The CLI selected its current default `claude-opus-5-5`; no model override was supplied. This differs from the default recorded in run 4, and there was no inference with either model in these attempts.
- Observed tools were exactly Glob, Grep, Read and Skill, with no MCP servers. Restricted mode, hook disabling, no Chrome integration and no session persistence were requested. Native built-in plugins and skills were also present; these conditions do not establish complete host isolation.
- The single attempted case had a US$1 cap, 180-second timeout and no retry. It ended after approximately one second.
- Canonical source hashes and the archive hash remained unchanged. The staged regular-file payload still matches the archive, with no staged symlinks.
- Archive SHA-256: `57f81de3448af72c329993ae8aa5938ffb0eb1b544ca6ebc6e1798daf7d5843a`.

The plugin was loaded for this disposable CLI session only. No skill instructions, global installation or account settings were changed. Package and catalogue checks do not qualify model behaviour, other Claude surfaces or incremental product value.

## Next bounded check

Restore the local Claude subscription login with `claude auth login`. After authentication returns, create a new run with the same two prompts and current hashes, then attempt explicit invocation and ordinary implicit selection once each. Preserve both blocked runs. No skill instruction change is supported by this attempt.

See `protocol.json`, `explicit-events.jsonl`, `explicit-execution.json`, `evaluation.json`, `archive-inventory.json` and `source-verification.json` for the evidence.
