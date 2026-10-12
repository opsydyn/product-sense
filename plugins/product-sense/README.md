# Product Sense

Turn an ambiguous product request into a defensible decision and a bounded next step.

Product Sense is a skill for product managers, designers and engineers. Give Claude a product idea, feature request, ticket, PRD, roadmap item or user flow, and it returns a clear verdict (**pursue**, **reshape**, **investigate** or **park**) with the reasoning, the main assumption, the cheapest credible test, a stop condition, and a time or money limit for the next step. For screens and journeys it returns a design review that ranks blockers before polish.

It separates what was observed from what was reported or inferred, does not invent research or figures, and checks for harm to users such as consent, privacy and easy cancellation. It respects decisions you have already made: ask it to implement an approved change and it stays out of the way.

## Use it

Ask an ordinary product question and Claude selects the skill, or invoke it directly with `/product-sense:product-sense`. Smaller models select it less reliably, so invoke it explicitly there.

Example requests:

- "Quick assessment, at most 180 words: three club organisers say they would use an AI weekly summary. Today they use email. One engineer has ten days. Should we build?"
- "We have five days and an approved direction. Shape this workflow improvement into a bounded bet with exclusions and a stop condition."
- "Review this password reset flow and say what to fix first in one sprint."

## What it does and does not do

The plugin contains one skill: written instructions and five reference documents that Claude reads. It runs no code, hooks or servers, makes no network requests, collects no data and sends nothing anywhere. It does not contact users, run experiments or change external systems; it only advises.

## Evidence and limits

Synthetic evaluations in Claude Code found that the skill makes Claude keep to requested word limits, invent fewer figures, review flows more completely and stop unpromising work more decisively. It did not consistently change which verdict Claude reaches. Results come from synthetic scenarios scored by a model grader, mostly in Claude Code; behaviour on other surfaces is less tested. The full evaluation record is in the [source repository](https://github.com/opsydyn/product-sense).

## Licence

MIT. See [LICENSE](LICENSE).
