# Run 12: Haiku 5.5 old/new description comparison

Date: 10 October 2026. Question: did the run 11 description rewrite lower Haiku 5.5's automatic skill selection? Two arms were built and staged before any case ran: **baseline**, 0.1.2 as committed at `cbcccba`, and **candidate**, the working tree tested in run 11. Each arm ran the run 11 capped-assessment prompt three times, interleaved. Hashes, cases and criteria are in `protocol.json`. There were no retries.

## Result

| Arm | Skill selected | Under 180 words | Appetite fits ten days | Full pass |
|---|---|---|---|---|
| Baseline (old description) | 0/3 | 3/3 | 1/3 | 0/3 |
| Candidate (new description) | 0/3 | 2/3 | 1/3 | 0/3 |

Every session's init event listed `product-sense:product-sense` as available, so selection failures are Haiku declining the skill, not a loading fault. All six processes exited 0; reported list cost was about US$0.37.

Without the skill, both arms gave the same generic shape: bulleted H1–H3 hypotheses, a numbered day plan and a pass bar. They labelled hypotheses and avoided a build-first verdict. Four of six gave a conditional build no allocation inside the ten days, or set pass bars of several weeks that cannot fit the window.

## Interpretation

The rewrite did not cause Haiku's low selection. Haiku selected the skill 0/3 with the old description here, and 1/6 with the new description across runs 11 and 12. Haiku 5.5 rarely selects this skill automatically for this prompt under either wording.

For Haiku users, the skill's guidance reaches the answer reliably only through explicit invocation (`/product-sense:product-sense`). Run 11's single selected Haiku sample still missed the conditional-build allocation, so explicit invocation alone may not meet the appetite rule on Haiku either; that is untested.

## Limits

Three samples per arm on one synthetic prompt cannot detect small differences. Scoring was not blinded. Only automatic selection was tested; explicit Haiku invocation was not.
