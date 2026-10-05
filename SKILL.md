---
name: product-sense
description: Use when assessing product ideas, feature requests, PRDs, Jira tickets, roadmaps, positioning, discovery plans or user journeys; when deciding whether or what to build; or when reviewing confusing flows, weak product evidence and scope under a fixed budget.
---

# Product Sense

Start with the progress the user seeks. Treat a proposed feature as a hypothesis about creating that progress. Turn the discussion into a clear decision and next action.

Use four pillars: Sierra for user capability, Norman for understandable design, Torres for discovery, and Rumelt for strategy. Apply supporting books only where they help the decision. See [canon.md](references/canon.md) for sources. This workflow is our synthesis, not an author's named method.

## Choose the output

| Input or request | Output | Read |
|---|---|---|
| Idea, feature, ticket, roadmap | Product critique | [discovery.md](references/discovery.md) |
| PRD, new product, positioning | Product brief | [discovery.md](references/discovery.md) |
| Deadline, budget, approved direction | Shaped bet | [shaping.md](references/shaping.md) |
| Screen, prototype, journey, service | Design review | [design.md](references/design.md) |

For an assessment, first load the reference in the selected row and [outputs.md](references/outputs.md), then draft the answer. An already-approved narrow edit can return the requested result directly. Think through relevant checks; print only what changes the decision. A small request can receive five lines. A full PRD deserves a fuller brief.

For a quick assessment with a word cap, write five sentences, one per line: verdict; user progress/current alternative; evidence/main assumption; bounded next action; decision/stop condition with the remaining allocation or a separate budget decision. Each sentence has one job. Budget at most one-sixth of the requested words per sentence, leaving the remainder as margin. Check the final word count, including labels, and shorten before sending.

## Establish reality

Read supplied artifacts first. Identify target user, task, context, current alternative, evidence and fixed constraints. Separate user, buyer and operator where their needs differ. Mark claims as **observed**, **reported**, **inferred** or **unknown**, with source and date where available. Treat compliments and purchase promises as weak signals; seek recent behavior, workarounds, costs and commitments.

If missing information changes the decision, ask one focused question. Otherwise proceed with stated assumptions and a conditional recommendation. Do not invent research, personas, market size, conversion rates or baselines. Draft personas as behavior-based hypotheses, not demographic stereotypes.

Respect explicit decisions and authorized execution. For a chosen stack or narrow fix, apply judgment within that scope. State a material concern briefly and continue the requested work. This skill adds no approval gate and grants no authority to contact users, run live experiments or change external systems.

## Apply the decision checks

1. **Progress:** State what the user can do better in the wider task. Name first useful success and capability that grows with use. Product engagement alone is insufficient.
2. **Reality:** Describe today's approach, including doing nothing. Identify the supported cost or failure.
3. **Switch:** Identify push toward change, pull of the new way, anxiety and habit. Include migration and learning effort.
4. **Opportunity:** Phrase the need without embedding the solution. For an open decision, compare materially different routes, including a manual or no-build option.
5. **Positioning:** Identify the real alternative, distinct capability, resulting value and best-fit customer. Mark unverified advantage as a hypothesis.
6. **Outcome:** Link user behavior to business value. Define a primary measure, baseline status, time window and relevant guardrail. Label proposed targets.
7. **Risk:** Identify the assumption whose failure most damages the bet. Compare uncertainty and consequence without false precision.
8. **Test:** Choose the cheapest credible evidence for that assumption. State what would change the decision, including a result that stops or reshapes the idea. Distinguish demand, usability and technical tests.
9. **Appetite:** State the time or money worth spending. If unset, propose a limit and label it. Allocate learning and delivery within the same total budget and available window. Separate elapsed time from effort: a low-effort test can still outlast a deadline. Finish the proposed learning within the window. For a conditional build, write its allocation from the remaining budget or state that a separate budget decision is needed.
10. **Strategy:** State diagnosis, guiding policy and coherent actions. Name the tradeoff; a growth goal is not a strategy.
11. **Cut:** Remove work that does not preserve the core outcome. Keep reliability, access and recovery needed to achieve it.
12. **Verdict:** Lead with **pursue**, **reshape**, **investigate** or **park**, reasoning, confidence and next action. Pursue a bounded bet, not certainty. Park with a reason and condition for revisiting.

For flows, also compare expected and actual behavior, cues, feedback, memory burden, likely errors, recovery and mental model. Make the outcome visible across the whole journey.

## Common mistakes

| Mistake | Correction |
|---|---|
| AI, novelty or feature count treated as value | Name user progress and compare a simpler route |
| Prototype success treated as demand | State the tested assumption and remaining unknowns |
| Metrics reward clicks or time spent alone | Measure task success and user effort |
| Every book becomes a workshop | Use only lenses affecting this call |
| Research becomes endless delay | Time-box learning and make a reversible bet |
| Education covers confusing design | Fix access and cues; teach the domain where needed |

## Example

Request: “Add a tour because paid-course buyers cannot find the course.”

**Reshape.** The reported problem is access after payment; the wider outcome is starting a lesson. Provide a direct course action after confirmed access and in the receipt, plus clear account access and recovery. Investigate entitlement delays. Test an unassisted purchase-to-lesson task. Measure lesson starts and access support requests; baseline unknown. If access succeeds but learning still stalls, revisit teaching support. Cut the tour from this bet.
