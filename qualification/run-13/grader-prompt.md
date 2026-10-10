You are grading two anonymous answers to the same product-management question. Grade only against the key below. Do not reward length, formatting, confidence or terminology. An answer that reaches the expected verdict for a different reason earns the verdict credit but not the insight credit.

## Question

{{scenario_prompt}}

## Key

Expected verdict: {{expected}}
Acceptable partial verdicts and their conditions: {{acceptable_partial}}
Decisive insights:
{{decisive_insights}}
Traps:
{{traps}}

Verdict words may differ. Map each answer's recommendation to pursue (build or ship now, possibly bounded), reshape (change the problem or solution before building), investigate (gather specific evidence before deciding), park (stop for now) or design review.

## Answer A

{{answer_a}}

## Answer B

{{answer_b}}

## Output

Return only this JSON:

{
  "A": {
    "verdict": "pursue|reshape|investigate|park|design review|unclear",
    "verdict_score": 0 | 0.5 | 1,
    "insights_hit": [true|false, ...one per decisive insight, in key order],
    "traps_fallen": [true|false, ...one per trap, in key order],
    "fabricated_figures": ["any number or fact stated as true that the question does not supply"],
    "actionability": 1-5
  },
  "B": { ...same fields... },
  "preference": "A|B|tie",
  "preference_reason": "one sentence naming the decisive difference in judgment"
}
