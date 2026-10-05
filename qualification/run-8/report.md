# Run 8: release-gap baseline and first candidate

Date: 5 October 2026. Five fresh native Claude samples per arm used the unchanged run-7 product question. The baseline was the frozen `0.1.1` archive; the first `0.1.2` candidate added explicit reference loading, a five-line quick-output recipe and a shared learning/delivery appetite. No rubric or prior answers were supplied to responders.

The baseline word counts were 213, 222, 213, 214 and 224: zero of five met the 180-word cap. None loaded the selected references. The first candidate loaded discovery and output references in all five cases, but its word counts were 194, 189, 165, 197 and 185: only one of five met the cap. Reference routing improved; the output-shape correction was insufficient.

Both arms proposed two-week or longer learning without clearly reconciling elapsed time with the ten-day availability. Some candidate effort allocations fit ten engineer-days, and several separately budgeted a later build. That is a partial improvement, but elapsed time and effort remained ambiguous. We do not treat every manual two-week test as proof of excess engineering effort.

One native Codex candidate assessment read the entrypoint, discovery and outputs, produced 160 words, proposed a two-day discovery limit and made a later build a separate budget decision. One exact-copy guard on each host returned exactly `Start lesson`. Source hashes remained unchanged while model samples ran. All processes completed successfully; that does not establish full task compliance.

Package-location regression tests first reproduced three failures: the default builder generated a nested skill inside the source; an explicitly nested output was accepted; and a destination could replace its own source folder. The corrected builder rejects overlapping output and defaults to an external temporary directory. Two additional Codex-distribution tests first failed because that format was absent. All twelve package tests passed after implementation.

The previous generated Claude folder matched its old archive and was moved to the disposable run stage, preserving it while removing the nested entrypoint. The repository now contains one `SKILL.md`. Native Codex discovery returned one canonical match with UI metadata and no matching errors both before and after; total skills fell from 18 to 17. The fresh desktop picker was not inspected, so its refresh is not claimed.

This is five repetitions of one synthetic scenario per Claude arm and two single-sample Codex checks. Both use native defaults and other built-in or installed guidance may influence results. There is no no-skill control, blind independent scorer, other-surface qualification or causal product-value claim. The first candidate was not accepted as the final release guidance. Run 9 evaluates a more concrete five-sentence contract and distinguishes elapsed time from effort.

See `protocol.json`, `evaluation.json`, both archive inventories, all raw event streams and final responses, native discovery snapshots, and retained package RED outputs for evidence.
