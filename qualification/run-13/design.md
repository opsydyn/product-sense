# Run 13 design: does Product Sense improve product judgment?

Status: **designed, not run.** Runs 1–12 mostly measured whether Claude followed the skill's own contract: loading the skill, reading references, the word cap and fitting the appetite. The one no-skill comparison (run 1) reached the same verdict as the skill on every case, and nearly every later assessment was the same easy scenario with the answer "investigate". This run asks whether the skill changes *which decision* Claude reaches, on cases where the right call varies and ordinary judgment can go wrong.

## Scenarios

| ID | Right call | What it tests |
|---|---|---|
| s01 CSV export | Pursue | Observed demand, cheap and reversible; research would cost about as much as building |
| s02 SMS reminders | Pursue | A comparison pilot already exists; consent and cost risks |
| s03 Enterprise deal | Park | Large, unsigned, off-strategy deal; opportunity cost |
| s04 Meal planner | Park | Sunk cost against observed non-use |
| s05 HR chatbot | Reshape | Solution-shaped request; the evidence points to buried forms |
| s06 Streaks | Reshape | Vanity metric versus the observed value driver |
| s07 Competitor copilot | Investigate | Competitor pressure without customer evidence; cheap evidence already in hand |
| s08 Correlation | Investigate | Causal claim from correlation; a forced step harms a segment |
| s09 Direct debit | Design review | Rank blockers; don't paper over faults with help text |
| s10 Pause subscription | Pursue | Cheap randomised test without a dark pattern |

Three of the ten are "pursue" cases. They check whether the skill makes Claude too cautious. Prompts are in `scenarios/`; the expected verdict, decisive insights and traps for each are in `answer-key.json`.

## Method

Each scenario runs three times with the skill and three times without it, on Opus 5.5 and Sonnet 5.5: 120 answers. A separate Opus grader, with no access to the skill, compares each skill answer against a control answer for the same scenario. It doesn't know which answer is which and grades each pair twice with the order swapped, using `grader-prompt.md`. It scores verdict accuracy, decisive insights, traps, invented figures and an overall preference. A human blind-grades 10 pairs to check the grader. Expected list cost is about US$20.

Decision rules, measures, power limits and the stopping rule are fixed in `protocol.json`. A large effect either way is detectable; a small one is not.

## Before running

1. **Done 10 October 2026: Alan P Currie approved `answer-key.json` as drafted.** Originally required because Claude wrote the key, will answer the scenarios and will grade them. Without independent review, the run would measure agreement with Claude's own views.
2. Record source and staged-plugin hashes in `protocol.json`.
3. Write the runner and grader harness and dry-run them without model calls.

These scenarios are a holdout set. Don't tune the skill against them; if this run leads to skill changes, confirm them on new scenarios.
