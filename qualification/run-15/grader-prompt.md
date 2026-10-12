Classify one answer to a product-management question. Do not judge whether it is right. Report only what it recommends.

## Question

{{scenario_prompt}}

## Answer

{{answer}}

## Definitions

- stated_label: the verdict word the answer itself uses for its recommendation (pursue, reshape, investigate, park), or "none" if it uses none of these words as its verdict.
- action: what the answer recommends doing about the proposal now.
  - "stop": it decides now to stop, decline, freeze, retire, not renew or not start the proposed investment. Remaining work only carries out that decision, such as notice, migration help or a revisit condition.
  - "research_first": it defers the stop-or-invest decision until more evidence is gathered (a study, analysis, interviews, a test or fixing measurement), however short.
  - "invest": it commits now to building, continuing or funding the proposed investment, in full or reduced form.
- research_days_before_decision: calendar days of evidence-gathering the answer proposes before the decision, 0 if it decides now, null if unclear.

## Output

Return only this JSON:

{"stated_label": "pursue|reshape|investigate|park|none", "action": "stop|research_first|invest", "research_days_before_decision": number or null, "evidence": "a short quote from the answer that shows the action"}
