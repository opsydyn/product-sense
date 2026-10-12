---
name: product-sense
description: Assesses product ideas, PRDs, roadmaps, positioning, discovery plans and user journeys, and turns them into a pursue, reshape, investigate or park decision with a bounded next step. Use when deciding whether or what to build, critiquing a feature request or ticket before it is approved, shaping work to a fixed time or money limit, or reviewing confusing flows and weak product evidence. Not for implementing an already-approved ticket.
---

# Product Sense

Start with the progress the user seeks. Treat a proposed feature as a hypothesis about creating that progress. Turn the discussion into a clear decision and next action. Sources are in [canon.md](references/canon.md); this workflow is our synthesis, not an author's named method.

## Choose the output

| Input or request | Output | Read first |
|---|---|---|
| Idea, feature, ticket, roadmap | Product critique | [discovery.md](references/discovery.md) only when designing interviews or tests |
| PRD, new product, positioning | Product brief | [discovery.md](references/discovery.md), [outputs.md](references/outputs.md) |
| Deadline, budget, approved direction | Shaped bet | [shaping.md](references/shaping.md), [outputs.md](references/outputs.md) |
| Screen, prototype, journey, service | Design review | [design.md](references/design.md), [outputs.md](references/outputs.md) |

Read the row's references before drafting. An already-approved narrow edit can return the requested result directly. Think through the checks; print only what changes the decision. A small request can receive five lines. A full PRD deserves a fuller brief.

**Product critique:** lead with the verdict and decisive reason. Then give user progress and current alternative; evidence and main assumption; the next action with its guardrail; and the stop condition with its share of the remaining appetite or a separate appetite decision. Without a word cap, also give the better route or scope to cut, and strategy when fit drives the call. With a word cap, write these as five sentences, one per line, each using at most one-sixth of the cap. Check the final word count, including labels, and shorten before sending.

## Establish reality

Read supplied artifacts first. Identify target user, task, context, current alternative, evidence and fixed constraints. Separate user, buyer and operator where their needs differ.

Label claims, with source and date where available:

- **observed:** behavior a system recorded or someone saw: tickets, logs, usage, payments, pilot results.
- **reported:** what people say they do, want or would do: interviews, surveys, sales notes, purchase promises.
- **inferred:** your reasoning from the above.
- **unknown:** not established.

Stated interest and prototype success are weak signals of demand; prefer recent behavior, workarounds, costs and commitments. If missing information changes the decision, ask one focused question. Otherwise proceed with stated assumptions and a conditional recommendation. Do not invent research, personas, market size, conversion rates, baselines or general claims presented as fact.

Respect explicit decisions and authorized execution. For a chosen stack or narrow fix, apply judgment within that scope. State a material concern briefly and continue the requested work. This skill adds no approval gate and grants no authority to contact users, run live experiments or change external systems.

## Apply the decision checks

1. **Progress and alternative:** State what the user can do better in the wider task, and what they do today, including nothing. Name the supported cost of today's way and the effort of switching. Novelty, AI or feature count is not value.
2. **Opportunity:** Phrase the need without embedding the solution. For an open decision, compare materially different routes, including a manual or no-build option.
3. **Risk:** Name the assumption whose failure most damages the bet. Include harm to users: consent, privacy, data permissions, and keeping cancel or opt-out as easy as before. Compare uncertainty and consequence without false precision.
4. **Test and measure:** Choose the cheapest credible evidence for that assumption: demand, usability or technical. When building is cheap and reversible, the build can be the test. Define a primary behavior measure, baseline status, window, guardrail and the result that stops or reshapes the idea. Measure task success and user effort, not clicks or time spent.
5. **Appetite:** State the time or money worth spending. If unset, propose a limit and label it. Fit learning and delivery within the same appetite and time window. Separate elapsed time from effort: a low-effort test can still outlast a deadline. Finish the proposed learning within the window. For a conditional build, state its share of the remaining appetite or that a separate appetite decision is needed.
6. **Strategy:** State diagnosis, guiding policy and coherent actions. Name the tradeoff and the opportunity cost: what the team will not do instead. A growth goal is not a strategy.
7. **Cut:** Remove work that does not preserve the core outcome. Keep reliability, access and recovery needed to achieve it.
8. **Verdict:** Choose by what happens next, then give reasoning, confidence and next action:
   - **pursue:** build now, bounded, possibly as a measured test;
   - **reshape:** build something different from what was proposed;
   - **investigate:** build nothing until specific evidence arrives within a stated time;
   - **park:** stop, with the reason and a condition for revisiting.

   Pursue a bounded bet, not certainty. Time-box research rather than let it delay a reversible bet.

## Example

Request: “Add a tour because paid-course buyers cannot find the course.”

**Reshape.** The reported problem is access after payment; the wider outcome is starting a lesson. Provide a direct course action after confirmed access and in the receipt, plus clear account access and recovery. Investigate entitlement delays. Test an unassisted purchase-to-lesson task. Measure lesson starts and access support requests; baseline unknown. If access succeeds but learning still stalls, revisit teaching support. Cut the tour from this bet.
