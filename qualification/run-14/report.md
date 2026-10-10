# Run 14: trimmed skill against the committed skill and no skill

Date: 10 October 2026. Arms: **new** (trimmed `SKILL.md`, wording approved by the owner), **old** (skill at `43b5871`) and **none** (no plugin). Scenarios, key, grader prompt, hashes and decision rules were fixed in `protocol.json` before any session ran. The answer key was **not human-reviewed**; the owner deferred review.

154 responder sessions and 192 grader sessions completed. 123 gradings first hit the account's weekly limit (HTTP 429, no model output) at about 19:25 BST, just before the 20:00 reset. Those blocked records are kept in `grades/blocked-quota/`. After the reset, the same 123 gradings were run once each with the same prompt and settings, as the protocol's resume plan specified. `analysis-interim.json` holds the pre-block result from 69 gradings. Reported list cost: responders US$7.98, graders US$8.10.

## Regression checks: all passed

| Check | Result |
|---|---|
| Capped assessment, Opus ×3 | Pass: 151, 119, 164 words; learning and build fit ten days or a separate build decision |
| Capped assessment, Sonnet ×3 | Pass: 116, 138, 131 words; same |
| Capped assessment, Codex | Pass: 126 words; read `SKILL.md` and `discovery.md` |
| Approved-ticket guard, Opus and Sonnet | Pass: skill not invoked, `node --test` passed, test unchanged |
| Approved-copy guard, Opus | Pass: exactly `Start lesson` |

No capped assessment read a reference, as the trimmed routing intends. All seven assessments raised consent for members' messages, which run 10's answers did not.

## Pre-registered decision

| Rule | Opus | Sonnet |
|---|---|---|
| Trim non-inferior to old (accuracy ≥ −10 points and win rate ≥ 0.40) | **Fail**: −11.9 points; win rate 0.625 | Pass: 0.0 points; win rate 0.667 |
| New against none | Benefit: 0.0 points; win rate 0.854 | Benefit: 0.0 points; win rate 0.688 |

Fixes effective (targeted insights pooled, new at least 15 points above old): **pass**, at 0.945 for new against 0.709 for old and 0.861 for none.

The adoption rule requires non-inferiority on both models, so **the trim is not adopted under the pre-registered rule.**

## Why Opus failed the rule

The whole Opus accuracy gap comes from one scenario, t04 (team chat). Expected verdict: park.

| Arm | Verdicts | Score |
|---|---|---|
| None | investigate ×3 | 0.00 |
| Old | park ×2, investigate ×1 | 0.83 |
| New | investigate ×3 | 0.00 |

The answers recommend substantively the same plan:
- don't fund the quarter;
- spend two weeks comparing chat users with non-users and interviewing both;
- fix only the worst bugs;
- otherwise freeze or retire chat with notice.

The old answers framed this as "expect to cut chat back or retire it", which the grader mapped to park. The new answers called it "Investigate first", which is consistent with the new verdict definition: investigate means build nothing until specific evidence arrives. Every other scenario scored equal or higher for new on Opus. One scenario carries a seventh of the verdict accuracy, so three samples moving label decide the rule.

This repeats run 13's finding: verdict accuracy here is sensitive to labels on the park/investigate/reshape boundary even when the recommended actions match.

## Other measures

| Measure | Opus none | Opus old | Opus new | Sonnet none | Sonnet old | Sonnet new |
|---|---|---|---|---|---|---|
| Decisive-insight hit rate | 0.83 | 0.85 | **0.95** | 0.79 | 0.76 | **0.87** |
| Targeted-insight hit rate | 0.83 | 0.75 | **0.97** | 0.89 | 0.67 | **0.92** |
| Trap rate | 0.03 | 0.04 | **0.00** | 0.03 | 0.08 | **0.01** |
| Fabricated figures per answer | 1.13 | 0.17 | 0.28 | 0.81 | 0.29 | 0.67 |
| Over the 250-word cap (of 24) | 24 | 8 | 4 | 24 | 8 | 11 |
| Skill selected | — | 24/24 | 24/24 | — | 16/24 | 15/24 |

No arm missed a pursue scenario. The trimmed skill invented more figures than the old one on both models, though fewer than no skill. On Sonnet the skill was not selected in about a third of sessions in both skill arms, including 0/3 for new on t01 and t07. Sonnet scores for the skill arms therefore mix skill and no-skill behaviour.

## Interpretation

The fixes worked. Targeted insights rose by 22 points (Opus) and 25 points (Sonnet) over the old skill, overall insight coverage and trap avoidance improved, and the grader preferred trimmed answers over old ones on both models. The trimmed skill also beat no skill in blind preference on both models, which run 13's skill did not.

The pre-registered rule still fails on Opus by 1.9 points. That failure comes from one scenario's label, not a different recommendation. Adopting the trim anyway would be a documented deviation from the rule and is the owner's decision.

## Decision

On 10 October 2026 the owner adopted the trim as a documented deviation from the pre-registered adoption rule, for the reasons above. The deviation is recorded in `protocol.json`. Future runs should confirm the verdict definitions do not systematically turn park cases into investigate.

## Limits

- Answer key not human-reviewed; run 13 grader calibration also pending.
- Three samples per cell; one scenario can move accuracy by 14 points.
- Grading not fully blind, because skill answers have a recognisable style.
- Sonnet's partial skill selection dilutes the Sonnet skill arms.
- 123 gradings ran after a quota pause with identical inputs.
