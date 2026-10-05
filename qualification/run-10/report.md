# Run 10: final beta-candidate qualification

Date: 5 October 2026. Version 0.1.2, frozen canonical-source hashes in `protocol.json`. This final candidate adds an explicit remaining allocation or separate budget decision to the quick-assessment decision gate. Baseline and earlier candidate failures remain in runs 7, 8 and 9.

## Result

All five native Claude product-assessment samples passed the declared checks: automatic skill selection, discovery/output reference loading, the 180-word cap, supplied evidence and hypothesis treatment, a bounded next action and stop condition, and an explicit effort allocation within ten engineer-days or separate later budget. Word counts were **151, 147, 163, 144 and 139**.

One fresh native Codex assessment read the entrypoint and relevant references, returned **126 words**, allocated two learning days plus eight manual-pilot days, and made app development a separate decision. One explicit approved-copy guard on each host returned exactly `Start lesson`. All eight processes exited 0; no contacts, live experiments or product mutations were observed. The responder conditions and original prompts are retained in full.

An independent read-only reviewer confirmed all five Claude word counts, successful native reference reads and effort allocations. One answer leaves the elapsed schedule ambiguous by referring to two weekly cycles while allocating three learning engineer-days plus seven build days. The prompt specified ten days of engineer availability, not a calendar deadline; the reviewer found no established material appetite violation. We retain the ambiguity rather than claiming a proven calendar schedule.

## Package and discovery checks

All **13** package integration tests pass. The external-output default, source-overlap guards, Codex payload and licence inclusion each have retained failing regression output followed by passing checks. Strict Claude manifest validation passed without errors or warnings. Both ZIPs contain exact canonical instruction/reference bytes; their inventories and hashes are in `package-verification.json`. Root `LICENSE` is copied unchanged into both formats when supplied; no licence grant was chosen or assumed during this run.

The generated Claude copy was moved outside the installed source tree after its old payload was verified. Only the canonical `SKILL.md` remains inside the checkout. Native Codex discovery found one canonical entry with UI metadata and no matching errors; its total catalogue dropped from 18 to 17. The fresh desktop picker was not inspected, so picker refresh is not claimed.

Canonical instruction/reference and manifest hashes remained unchanged during final model evaluation. The packaging helper was subsequently extended to include an owner-supplied licence, without changing this unlicensed candidate payload. The final archives were compared with the tested hashes after rebuilding.

## Independent review

A fresh read-only code review found no Critical or Important issues. One Minor licence-packaging omission was fixed: a supplied root licence had been excluded from both archive allowlists. The new regression first failed for both formats and then passed. The reviewer independently ran the prior twelve-test suite; the implementer verified the final thirteen-test suite. No second full code review is claimed. Release-document pointers were updated to this final run.

## Limits and release decision

Claude Code 2.1.289 used its default `claude-opus-5-5`, with Read/Skill/Glob/Grep tools only, no MCP servers, restricted settings and hook disabling. Native Codex used normal host configuration, ephemeral read-only sessions and approvals set to never; its exact model identifier was not independently reported in the event stream. Other native or installed guidance can influence these observations.

Five repetitions of one Claude scenario and two single-sample Codex cases support an **internal beta candidate**. They do not establish universal model compliance, a verified calendar schedule, other-surface support, marketplace acceptance or real-user product value. Parent scoring was not blinded; the independent reviewer checked selected criteria, not every interpretation. There were no automatic retries. Each Claude session had a US$1 cap and each process a 180-second timeout; reported list-price cost is recorded separately from actual subscription billing.

Licence selection and the publication destination remain owner decisions. Installation documentation, examples, release notes and both ZIP formats are prepared locally. This is not a published release. After licence selection, rebuild both ZIPs, verify the exact licence and canonical bytes, and complete the chosen distribution/review flow.

See `protocol.json`, `evaluation.json`, raw event streams, execution records, final responses, `source-verification.json`, `package-tests.txt`, `validation.txt`, `package-verification.json` and the retained licence-package RED output.
