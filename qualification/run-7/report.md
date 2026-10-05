# Run 7: Claude behaviour after restored login

Date: 5 October 2026. Source baseline: `4d7bf4d`, package `0.1.1`. The two prompts and criteria are unchanged from runs 4 and 6. Both earlier blocked attempts are preserved.

## Result

Inference access is restored. Explicit native invocation passed all four declared criteria. The ordinary product assessment selected Product Sense without its name in the prompt, but passed only three of six criteria. Overall: one complete case passed, one failed; seven criteria passed and three failed.

| Criterion | Explicit approved-copy case | Implicit product-assessment case |
|---|---|---|
| Native catalogue discovery | Pass | Pass |
| Native invocation / automatic selection | Pass | Pass |
| Exact requested copy | Pass: `Start lesson` | Not applicable |
| Relevant reference use | Not required in this case | Fail: no reference contents loaded |
| Evidence and scope, bounded action and stop condition | Not applicable | Fail: sound evidence treatment and a stop gate, but proposed work exceeds the stated availability |
| Maximum 180 words | Not applicable | Fail: 204 words |
| No writes or external actions | Pass | Pass |

The implicit response correctly treated three stated expressions of interest as weak evidence, labelled the central assumption as a hypothesis, compared the current email/message workflow, and proposed a manual test with a stop/change condition. However, its learning plan runs through day 8, followed by a proposed small ten-day build. It does not reconcile that further work with one engineer available for ten days. This is why the combined evidence-and-scope criterion failed.

Both event streams show one `Skill` invocation and native injection of the staged entrypoint. Neither shows a Read, Glob or Grep call, or injected reference contents. For the implicit assessment, the entrypoint routes to `discovery.md` and `outputs.md`; those were not loaded. This fails the predeclared reference-use criterion even though parts of the assessment are sensible.

The implicit final contains 204 whitespace-delimited words, 24 above its maximum. Its skill invocation arguments retained the word limit and ten-day constraint, so those requirements were not lost during task forwarding. The earlier Codex word-limit failure in run 3 remains; this run does not repair it.

## Native conditions and integrity

- Claude Code `2.1.289` used its current default `claude-opus-5-5`, without a model override.
- Each fresh-context CLI session listed `product-sense:product-sense` from the staged `product-sense@inline` plugin, version `0.1.1`.
- Observed tools were exactly Glob, Grep, Read and Skill, with no MCP servers. Restricted mode, disabled hooks, no Chrome integration and no session persistence were requested. Native built-ins remained present; these conditions do not establish complete host isolation.
- Both processes exited 0 with `is_error: false` and no permission denials. Process success does not establish full task compliance.
- Explicit execution took 5.465 seconds; implicit execution took 15.978 seconds. Each remained within its 180-second timeout and US$1 cap, with no retry.
- The CLI reported US$0.1119936 total list-price cost. This is not proof of an actual subscription charge.
- Strict native manifest validation passed with zero errors and warnings. The unchanged package's seven integration tests passed in run 6; they were not rerun here.
- Source and archive hashes remained unchanged, and the staged regular-file payload still matches the archive with no staged symlinks.
- Archive SHA-256: `57f81de3448af72c329993ae8aa5938ffb0eb1b544ca6ebc6e1798daf7d5843a`.

No runtime guidance or global configuration was changed. The plugin was loaded for these disposable sessions only. Qualification documentation is separate from the tested payload.

## Interpretation and next step

The outstanding native attempts are complete: discovery, explicit invocation and ordinary implicit selection now have positive CLI evidence. Full implicit task compliance failed. These are one-sample observations, with no control arm, blind independent scorer or repeatability claim. They do not establish behaviour on claude.ai, Cowork or OpenAI surfaces, or incremental product value.

If behavioural changes are pursued, target the observed omissions: apply the requested output cap, fit all proposed work into the fixed appetite, and load the selected references. Compare any revised guidance with the unchanged baseline in a separate bounded run. Preserve these failures and avoid adding broad rules unsupported by them.

See `protocol.json`, both `*-events.jsonl` streams, `*-execution.json` records, `*-final.txt` responses, `evaluation.json`, `validation.txt`, `archive-inventory.json` and `source-verification.json` for the evidence.
