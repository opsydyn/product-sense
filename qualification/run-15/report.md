# Run 15: do the new verdict definitions turn park cases into investigations?

Date: 11 October 2026. Arms: **new** (trimmed skill, `63884f5`), **old** (before the trim, `43b5871`) and **none**. Nine new scenarios: six where existing evidence already decides against investing (park) and three where parking would be premature (investigate). 162 responder sessions and 194 grader sessions all completed, with no retries and no quota blocks. Reported list cost: responders US$7.91, graders US$3.36. The answer key was not human-reviewed; the owner deferred review.

Unlike runs 13 and 14, the grader never saw the key or the expected verdict. It classified each anonymised answer's **stated label** and its **recommended action**: stop now, research first, or invest. A seeded 20% subset was graded twice; action and label agreement were both **100%**.

## Result: no shift

| Park cases (36 answers per arm) | New | Old | None |
|---|---|---|---|
| Recommended stopping now | **15 (42%)** | 10 (28%) | 9 (25%) |
| Labelled "park" | 15 | 13 | 0 |
| Labelled "investigate" | 10 | 3 | 0 |
| Labelled "reshape" | 8 | 15 | 0 |
| Mean research days before deciding, when proposed | 6.7 | 7.0 | 8.5 |

The pre-registered rule returns **no_shift**. The trimmed skill stopped *more* often than the old one (14 points higher), not less. Its labels moved from "reshape" to "investigate", not away from "park".

There was **no overcorrection**: every arm deferred all 18 investigate-case decisions for evidence (100%), and none stopped or invested prematurely.

By model:

| Park-case stop rate | New | Old | None |
|---|---|---|---|
| Opus | 61% | 39% | 33% |
| Sonnet | 22% | 17% | 17% |

Sonnet selected the skill in only 44% (new) and 41% (old) of sessions. When Sonnet did not select it, none of 14 park answers stopped. When it did, 4 of 11 (new) and 3 of 11 (old) stopped. **The skill increases decisive stopping when it loads. Sonnet often doesn't load it.**

## What run 14's failure was

Run 14's Opus shortfall came from one park scenario labelled "investigate". Here, with labels and actions separated, the trimmed definitions make Claude *more* willing to stop. The run 14 failure was label noise on one scenario, as its report concluded.

## A wider finding: the key may be too strict on park

In every arm, most park-case answers proposed a short check before stopping, typically 1–2 weeks: 25 at 14 days and 17 at 7 days. Many are sensible. On the PDF case (p6), a trimmed-skill answer checks the six enterprise contracts for PDF commitments before the licence lapses, finishes before renewal and states its stop rule. On the bank case (p5), answers give the bank two weeks to put requirements in writing before dropping it. No arm stopped outright on p5 or p6.

The key defines park as "stop now". A defensible alternative is "stop unless a brief, deadline-safe check finds a blocker". Runs 13–15 suggest much of the measured park/investigate gap is this definitional line rather than poor judgment. Future keys should accept a short, bounded pre-stop check that cannot outlast a deadline, or score research length directly.

## Limits

- Key not human-reviewed. Synthetic scenarios.
- 36 park answers per arm detect differences of roughly 25 points; the 14-point new-versus-old gain is suggestive, not established.
- Sonnet's low selection mixes skill and no-skill behaviour in its skill arms.

See `protocol.json`, `answer-key.json`, `grader-prompt.md`, `harness.py`, `classified.json`, `analysis.json`, `responses/` and `grades/`.
