# Product Sense: first bounded qualification

Date: 30 September 2026. Skill baseline: `f628527`. The skill and its references were unchanged throughout this run.

## Result

The candidate passed six of six synthetic cases and all 23 rubric criteria. The control passed five cases and 22 criteria. Both arms respected the requested word limits in their final responses.

| Case | Control | Candidate | Candidate selected Product Sense |
|---|---|---|---|
| Evidence-poor planning-app idea | Pass | Pass | Yes |
| Constrained repair-status PRD | Pass | Pass | Yes |
| Static course-payment screen transcription | Pass | Pass | Yes |
| One-week invoice-assistant discovery plan | Fail | Pass | Yes |
| Approved narrow button-copy change | Pass | Pass | No |
| Unrelated TypeScript identifier rename | Pass | Pass | No |

The control discovery plan proposed positive and stop/narrow gates but omitted an explicit inconclusive outcome for inadequate recruitment or evidence. The candidate deferred investment when recruitment or evidence was insufficient. Its six-hour schedule also kept the decision within the stated research budget.

For the mixed PRD/deadline request, the candidate produced the requested decision brief while preserving the approved stack and promised accessible status page and agent updates. It read discovery, shaping and output guidance. The discovery request produced a usable plan despite lacking a dedicated row in the entrypoint's output table. These samples did not reproduce the routing ambiguity raised during source assessment.

The candidate idea and PRD responses made proposed decision thresholds and operational limits explicit. Controls were already strong on evidence and scope, so these differences do not establish that Product Sense improves task performance.

## Method and evidence

Twelve fresh-context subagents answered six identical task prompts in two arms: ordinary judgment without Product Sense, and optional Product Sense metadata with access to the entrypoint and relevant references. The parent manually reviewed all final responses against the criteria declared before dispatch. The inherited session model was used; its exact identifier was not independently recorded or pinned.

The [protocol](protocol.json) records the source hashes, prompts, criteria, budget and stopping rule. Requested word limits are copied from the prompts for mechanical checking. [Raw responses](raw/) preserve each final answer and responder-reported selection and reads. [Evaluation](evaluation.json) records each criterion, result and supporting evidence. Word counts use whitespace splitting; the final responses, rather than files observed before an agent finished, were scored.

Basic structural checks found valid YAML frontmatter and UI metadata, valid description lengths, the default skill mention, existing icon assets and resolving local Markdown links. The bundled Python validator remains unavailable because its PyYAML dependency is missing; equivalent targeted YAML checks used Ruby. Source hashes match the baseline protocol.

## Limits and decision

This is a synthetic single-sample qualification. It does not establish repeatability, native installation/discovery, real-user outcomes or causal superiority over ordinary model judgment. Rich task prompts and shared runtime instructions may explain much of the success. The static design case is a text transcription rather than a rendered screenshot and resembles the course-access example already in the skill.

The approved-fix candidate declined optional skill activation. It demonstrated proportional response and selection boundaries, but did not exercise the skill's scope-preservation instruction after loading it. The unrelated rename likewise declined activation correctly. Selection and read lists are responder-reported, rather than native skill-loader telemetry.

Retain the current skill unchanged. No source-assessment concern reproduced as a candidate failure in this small run. The next bounded work should verify native discovery and an explicitly invoked, already-approved narrow fix, then use repeated samples if wording changes are justified. Installation or skill revision was not performed during this qualification.
