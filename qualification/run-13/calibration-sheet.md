# Run 13 human calibration

For each pair, read the question and key, then fill `calibration-human.json`: each answer's verdict (pursue, reshape, investigate, park, design review or unclear) and which answer shows better judgment (A, B or tie). Grade before looking at any model grades.


---

## Pair 1: `s05-hr-chatbot-opus-1`

### Question

IT wants to build an AI chatbot for our HR policy portal. HR receives about 300 employee emails a month. We sampled 100: 62 asked how to request parental leave or carry over holiday. The request form for both is three clicks deep under 'Documents', and the policy is a 40-page PDF. We have one developer for four weeks. Should we build the chatbot?

Answer in at most 250 words. Assess only; do not create or edit files, contact anyone or run experiments.

## Key

Expected verdict: reshape
Acceptable partial verdicts and their conditions: none
Decisive insights:
1. 62 of 100 sampled emails concern two processes whose form is buried and whose policy is a 40-page PDF; the need is finding and completing those processes
2. Surface both forms and short step-by-step answers where employees look first; a chatbot is a solution embedded in the request
3. Measure emails on those two topics; reconsider a chatbot only if a long tail of varied questions remains
Traps:
1. Builds or scopes the chatbot
2. Ignores the sampled email evidence

Verdict words may differ. Map each answer's recommendation to pursue (build or ship now, possibly bounded), reshape (change the problem or solution before building), investigate (gather specific evidence before deciding), park (stop for now) or design review.

## Answer A

**Reshape.** Don't build the chatbot yet; first make the two forms easy to find.

Employees are trying to request parental leave or carry over holiday. Today they email HR, because the form sits three clicks deep under "Documents" and the rules are buried in a 40-page PDF.

The evidence is your own sample: 62 of the 100 emails were about those two tasks, which points to a findability problem rather than a need for conversation. What we don't know is how many of those 62 only needed the form and how many needed help with the rules (eligibility, pay, deadlines), which is the part a chatbot would actually help with.

In week one, put "Request parental leave" and "Carry over holiday" links on the portal homepage. Add a one-page plain-language summary for each. Have HR's auto-reply point to both. Then re-sort the 62 emails into "where's the form?" and "what are the rules?"

Over the remaining three weeks, track those two email types against the sampled rate of about 62%. If they fall by half or more (a target I'm proposing), stop: the problem was navigation. A chatbot only makes sense if many rules questions are left, and it would need its own budget decision, since one developer can't safely build and test a policy chatbot in the time that's left.

## Answer B

**Not yet. Fix the navigation first. It is cheaper and goes straight at the problem your sample found.**

**What the data says**
- 62 of the 100 sampled emails asked about just two tasks: requesting parental leave and carrying over holiday. Scaled up, that's about 185 emails a month.
- The cause looks like findability rather than missing answers. The form is three clicks deep under "Documents", and the policy is a 40-page PDF. Employees probably email HR because that's easier than digging.

**Why a chatbot is the wrong first move**
- It adds a new interface on top of a navigation problem instead of fixing it.
- Four developer-weeks is tight for a reliable bot over a long PDF. Retrieval, testing, guarding against wrong answers, and ongoing upkeep all take time. A wrong answer about leave entitlement is a real HR and legal risk.
- It still has to send people to the same buried form.

**What I'd do with the four weeks**
1. **Week 1:** Put "Request parental leave" and "Carry over holiday" links on the portal homepage. Write a one-page plain-language summary or FAQ for each, linking to the relevant PDF section.
2. **Same week:** HR adds a canned email reply with those links.
3. **Weeks 2–4:** Measure. Did emails on those two topics drop? Use the time left to find the next most common question types among the other 38 emails.

**When a chatbot would make sense**
If email volume stays high after the fixes, or the remaining questions turn out to be varied and personal, a narrow chatbot over the cleaned-up content becomes worth testing. One caveat: the 100-email sample is enough to act on, but check the 62% holds across a second month before committing.



---

## Pair 2: `s05-hr-chatbot-opus-3`

### Question

IT wants to build an AI chatbot for our HR policy portal. HR receives about 300 employee emails a month. We sampled 100: 62 asked how to request parental leave or carry over holiday. The request form for both is three clicks deep under 'Documents', and the policy is a 40-page PDF. We have one developer for four weeks. Should we build the chatbot?

Answer in at most 250 words. Assess only; do not create or edit files, contact anyone or run experiments.

## Key

Expected verdict: reshape
Acceptable partial verdicts and their conditions: none
Decisive insights:
1. 62 of 100 sampled emails concern two processes whose form is buried and whose policy is a 40-page PDF; the need is finding and completing those processes
2. Surface both forms and short step-by-step answers where employees look first; a chatbot is a solution embedded in the request
3. Measure emails on those two topics; reconsider a chatbot only if a long tail of varied questions remains
Traps:
1. Builds or scopes the chatbot
2. Ignores the sampled email evidence

Verdict words may differ. Map each answer's recommendation to pursue (build or ship now, possibly bounded), reshape (change the problem or solution before building), investigate (gather specific evidence before deciding), park (stop for now) or design review.

## Answer A

**Not yet. Fix findability first, and build a chatbot only if a real need is left over afterwards.**

**Why:** Your sample suggests about 186 of the 300 monthly emails (62%) are two navigation questions with known answers. The likely cause is that the forms are buried three clicks deep and the policy is a 40-page PDF. A chatbot would hide that problem behind a costly extra layer rather than remove it.

**Cheaper fix, roughly 1–2 weeks of the developer's time:**
- Put "Request parental leave" and "Carry over holiday" as prominent links or buttons on the portal homepage, and make them come up in search.
- Write a one-page plain-language summary of each policy: eligibility, deadlines, steps, and a form link. Link to the relevant PDF section.
- Set an auto-reply on the HR inbox that links to both pages.
- Track weekly email volume on these topics against your baseline.

**Chatbot risks:**
- A wrong answer about leave entitlement is a legal and employee-relations risk, not a minor bug.
- Four weeks is tight for a reliable bot over a 40-page policy. Most of the effort is testing and monitoring, not the build.
- It needs ongoing upkeep whenever the policy changes, and IT may not budget for that.

**Check before deciding:**
- Read through the 62 emails. Are people asking *where the form is*, or *whether they qualify*, e.g. edge cases? Eligibility questions may need HR judgment that neither a link nor a bot can give.
- What are the other 38%? If they're scattered across many different topics, a chatbot might help later.
- Is the sample of 100 representative across months? Holiday carry-over questions are probably seasonal.

**Decision rule:** If these two topics are still a large share of emails 4–6 weeks after the fix, revisit a chatbot with that data in hand.

## Answer B

**Reshape:** don't build a general chatbot yet. 62% of the sampled emails ask how to do one of two things, and making those easier to find is likely cheaper and more reliable than a bot.

Employees want to request parental leave or carry over holiday, but they email HR because the form is three clicks deep under "Documents" and the rules are in a 40-page PDF.

Your sample of 100 out of about 300 monthly emails points to a findability problem; the key assumption is that people email because they can't find the form, not because their situation needs a judgement call.

In week one, the developer should put both request forms on the portal homepage, write a one-page plain-language guide for each, and link them from HR's auto-reply; then watch five employees try each request without help.

In weeks two to four, track what share of HR email is about these two topics against the 62% baseline. If it drops clearly, stop there; if the remaining questions are about eligibility rather than where things are, a narrow policy bot needs its own time-and-budget decision.



---

## Pair 3: `s06-streaks-opus-1`

### Question

Our budgeting app's DAU/MAU is 12%. The growth team proposes daily streaks and push notifications to raise engagement, citing that engaged users retain better. Our data: users who connect a bank account in their first week have three times the 90-day retention of those who don't; 34% connect in week one; logs show 22% of connection attempts fail, concentrated at three large banks. We have two engineers for six weeks. What should we prioritise?

Answer in at most 250 words. Assess only; do not create or edit files, contact anyone or run experiments.

## Key

Expected verdict: reshape
Acceptable partial verdicts and their conditions: none
Decisive insights:
1. Retention is associated with connecting a bank account, and 22% of connection attempts fail at three banks: users show intent and hit a fault
2. Fix those connection failures and give a clear retry or recovery path before adding attention mechanics
3. Measure week-one connection success and 90-day retention, not DAU/MAU; note the connection-retention link is correlational
Traps:
1. Endorses streaks or push notifications as the priority
2. Uses DAU/MAU as the primary success measure

Verdict words may differ. Map each answer's recommendation to pursue (build or ship now, possibly bounded), reshape (change the problem or solution before building), investigate (gather specific evidence before deciding), park (stop for now) or design review.

## Answer A

**Reshape: put the six weeks into fixing bank connections at the three failing banks, and park streaks and push notifications for now.**

1. **What users need:** People want a reliable picture of their money without typing in transactions by hand. Right now 66% don't connect in week one, and the 22% whose connection fails are pushed back to manual entry or to leaving. Streaks would raise opens without helping anyone get their accounts set up.
2. **Evidence:** We observed that connecting in week one goes with three times the 90-day retention, but that's a correlation: motivated users may simply be more likely to connect. The assumption to test is that removing failures causes more connections and better retention.
3. **Next step:** In week one, use the logs to sort failures at the three banks by cause: the aggregator, login/MFA, timeouts, or bank downtime. In weeks two to five, fix the biggest fixable causes. Add clear retry and recovery prompts and a fallback to manual entry or file import.
4. **How to measure it:** The main measure is the share of new users who connect in week one, against today's 34% baseline. Also track success rate per bank and compare 30-day retention between users who hit a now-fixed failure and earlier users who hit it. Watch support tickets and duplicate accounts as guardrails.
5. **When to stop:** If week one shows the failures are mostly beyond our control, such as aggregator limits, stop the build. Spend the remaining five weeks on onboarding that gets people to connect and on recovery after a failure. Streaks would need their own appetite decision later, once connection rates improve.

## Answer B

**Prioritise fixing bank connection failures, not streaks.**

**Why the growth team's proposal is weak**
- A budgeting app doesn't need daily use. A 12% DAU/MAU may be fine if people check in weekly and around payday. Streaks would push up a metric that may not track the value users get.
- "Engaged users retain better" doesn't show that streaks make people engaged. Habits forced by notifications tend to fade, and pushy prompts in a finance app can cost trust and cause uninstalls.

**Why bank connection comes first**
- Connecting a bank is when the app starts being useful. The 3× retention gap is also a correlation, since motivated users may simply connect more. But a failed connection is a mechanical barrier, not a motivation problem. Users who tried and failed wanted to connect.
- The failures are concentrated at three banks, so a small team can make a dent. That suits two engineers for six weeks.
- If week-one connection rose from 34% to around 40%, the retention gain would probably beat anything streaks could deliver. Treat that as a hypothesis to test.

**Suggested six weeks**
1. **Week 1: diagnose.** Map the funnel: how many users try to connect, fail, retry and give up. Break failures down by bank and error code. Check what you can actually fix: login/MFA timeouts, a weak aggregator integration, or bank-side outages.
2. **Weeks 2–5: fix.** Options include OAuth or a second aggregator as a fallback for those three banks, automatic retries, and clearer error messages with a "try again" path. Add a fallback like CSV import or manual entry so a failure isn't a dead end.
3. **Throughout: measure.** Ramp changes gradually or keep a holdout group. Track successful connections in week one and 30/90-day retention, not DAU/MAU.

If notifications are worth doing, start with ones that deliver value, such as "your connection failed, tap to retry" or alerts about overspending. Leave streaks until the connection problem is fixed.



---

## Pair 4: `s06-streaks-sonnet-1`

### Question

Our budgeting app's DAU/MAU is 12%. The growth team proposes daily streaks and push notifications to raise engagement, citing that engaged users retain better. Our data: users who connect a bank account in their first week have three times the 90-day retention of those who don't; 34% connect in week one; logs show 22% of connection attempts fail, concentrated at three large banks. We have two engineers for six weeks. What should we prioritise?

Answer in at most 250 words. Assess only; do not create or edit files, contact anyone or run experiments.

## Key

Expected verdict: reshape
Acceptable partial verdicts and their conditions: none
Decisive insights:
1. Retention is associated with connecting a bank account, and 22% of connection attempts fail at three banks: users show intent and hit a fault
2. Fix those connection failures and give a clear retry or recovery path before adding attention mechanics
3. Measure week-one connection success and 90-day retention, not DAU/MAU; note the connection-retention link is correlational
Traps:
1. Endorses streaks or push notifications as the priority
2. Uses DAU/MAU as the primary success measure

Verdict words may differ. Map each answer's recommendation to pursue (build or ship now, possibly bounded), reshape (change the problem or solution before building), investigate (gather specific evidence before deciding), park (stop for now) or design review.

## Answer A

**Recommendation: fix bank-connection reliability first. Don't build streaks and push as the main bet.**

**Why**
- Connecting a bank in week one goes with 3x the 90-day retention, but only 34% of users do it. A 22% attempt failure rate, concentrated at three large banks, is a direct leak in that funnel.
- Streaks and push act on users who are already active, and they don't fix the activation problem. The growth team's "engaged users retain better" claim is correlational, and the same is true of our connection stat.
- Caveat: the 3x is also correlational. Motivated users may be the ones who connect. Failed attempts are the useful natural experiment here. Compare retention of users whose first attempt failed with users whose first attempt succeeded, and with users who never tried.
- The cohort that tried and failed is probably high-intent and is being lost.

**Plan (6 weeks, 2 engineers)**
1. Weeks 1–2: Diagnose the failures at the three banks (aggregator errors, MFA, timeouts, outages). Add funnel instrumentation. Fix the cheap causes and improve the error messages and retry flow.
2. Weeks 2–5: Fix the root causes at each bank. Consider a fallback such as a second aggregator or CSV import, and re-engage users whose attempts failed.
3. Weeks 5–6: Add a small, cheap test of the growth team's idea. Send a single push to users who haven't connected, nudging them to try again. This tests their hypothesis and supports the connection fix.

**Expected impact**
If most of the 22% failures are recoverable, week-one connection rises by several points. That should move retention more than streaks, whose effect on DAU/MAU is uncertain. DAU/MAU should rise after retention does.

**Measure**
- Connection success rate
- Week-one connection rate
- 90-day retention of the cohort that connects
- DAU/MAU, as a lagging indicator

## Answer B

**Reshape:** Put the six weeks into bank-connection reliability, not streaks and push. Streaks only engage users who already have a reason to return, and a budgeting app's reason is live data.

**Progress:** Users want an accurate picture of their money without manual entry. Today a failed connection leaves them with manual entry or abandonment, and only 34% connect in week one.

**Evidence:** Connected users retain 3x better (observed), but that is correlation, since motivated users may both connect and stay (main assumption). With 22% of attempts failing at three banks, fixing those is a plausible lever, though I don't know how many users hit a failure or give up afterwards.

**Next action:** Weeks 1–2, break the failures down by bank and cause (aggregator, bank-side or our UX) and add retry, clear error messages and recovery. Weeks 3–6, fix the biggest causes. Measure week-one connect rate and 90-day retention, with support tickets as the guardrail.

**Decision:** Spend about two-thirds of the appetite (four engineer-weeks) on this. If the failures turn out to be unfixable bank-side, or higher connect rates don't lift early retention, reconsider streaks and push as a separate, smaller bet.



---

## Pair 5: `s07-competitor-copilot-sonnet-2`

### Question

A competitor in our project-management market launched an AI copilot last month and it is all over LinkedIn. Our CEO wants our own copilot within six weeks. We have no customer requests for it in our feedback tool; our top support complaint for two quarters has been slow report loading. Win/loss notes from last quarter's 22 lost deals have not been reviewed for AI mentions. We have four engineers. What do you recommend?

Answer in at most 250 words. Assess only; do not create or edit files, contact anyone or run experiments.

## Key

Expected verdict: investigate
Acceptable partial verdicts and their conditions: [{"verdict": "reshape", "condition": "Does not commit the six-week copilot build before checking customer or loss evidence"}]
Decisive insights:
1. A competitor launch is not evidence of customer value or of lost deals
2. The cheapest evidence is already in hand: review the 22 lost-deal notes and ask recent lost prospects; decide within days
3. Slow report loading is the observed top complaint and should not be dropped for an unvalidated feature
Traps:
1. Commits to the six-week copilot
2. Dismisses the competitor without checking the evidence
3. Invents market statistics

Verdict words may differ. Map each answer's recommendation to pursue (build or ship now, possibly bounded), reshape (change the problem or solution before building), investigate (gather specific evidence before deciding), park (stop for now) or design review.

## Answer A

**Recommendation: don't commit to a six-week copilot yet. Spend the first week getting evidence, then decide.**

**Why:**
- Your only hard signal points elsewhere. Slow report loading has topped support complaints for two quarters, and no customer has asked for AI.
- The competitor's launch is loud on LinkedIn, but that shows their marketing, not demand or product quality.
- You haven't yet read the one dataset that could change this: the 22 lost deals. Read them first.

**Week 1 (cheap, no build):**
1. Have someone read all 22 win/loss notes and count AI mentions. Note whether AI was a deciding factor or just a checkbox.
2. Ask sales and CS how often prospects raise the competitor's copilot.
3. Quantify the report-speed problem: churn, tickets, and any link to lost deals.

**Then decide:**
- **AI is cited in a meaningful share of losses:** build a narrow, credible copilot, not a competitor clone. Pick one or two workflows, such as summarizing project status or drafting reports. Use two engineers and keep two on performance.
- **AI is rarely cited:** fix report performance first. Give the CEO a short AI plan for later, plus a "fast and reliable" message to counter the competitor's buzz.

**Risks to name for the CEO:**
- With four engineers, a rushed copilot likely means a shallow demo-ware feature and a stalled performance fix, which your customers are already complaining about.
- Slow reports would also undermine any AI feature that reads report data.

**Pitch to the CEO:** "We'll have evidence in a week and a scoped plan by week two. Either way, we ship something visible within six weeks."

## Answer B

**Investigate, then reshape.** Don't commit to a copilot yet. The only evidence for it is a competitor's LinkedIn buzz, which is inferred rather than observed demand.

**Progress and alternative:** Customers want to see project status quickly, and slow report loading is the observed top complaint for two quarters. Today they wait or work around it, and nobody has asked for a copilot.

**Evidence and risk:** The riskiest assumption is that AI is costing us deals. That is unknown, because the 22 lost-deal notes haven't been read for AI mentions.

**Next action:** In the first 2–3 days, someone reads those 22 notes and tags AI mentions. In the same window, check whether churn or support data ties report speed to risk. This is desk work, with no outreach or experiments.

**Decision and stop condition:** If AI is cited in a meaningful share of losses (proposed bar: about 5 of 22, a number I'm suggesting), build a narrow copilot. A good first version is natural-language summaries of project status, with a clear success measure. Give it at most half of the remaining six-week appetite, with two engineers. Put the other two on report speed. If AI is rarely cited, park the copilot and put all four engineers on report performance. Then give the CEO a short, evidence-based positioning response, not a feature race.

The CEO may still want a visible answer in six weeks. A fast, narrow copilot built on a slow reporting layer risks demoing well and disappointing in use.



---

## Pair 6: `s07-competitor-copilot-sonnet-3`

### Question

A competitor in our project-management market launched an AI copilot last month and it is all over LinkedIn. Our CEO wants our own copilot within six weeks. We have no customer requests for it in our feedback tool; our top support complaint for two quarters has been slow report loading. Win/loss notes from last quarter's 22 lost deals have not been reviewed for AI mentions. We have four engineers. What do you recommend?

Answer in at most 250 words. Assess only; do not create or edit files, contact anyone or run experiments.

## Key

Expected verdict: investigate
Acceptable partial verdicts and their conditions: [{"verdict": "reshape", "condition": "Does not commit the six-week copilot build before checking customer or loss evidence"}]
Decisive insights:
1. A competitor launch is not evidence of customer value or of lost deals
2. The cheapest evidence is already in hand: review the 22 lost-deal notes and ask recent lost prospects; decide within days
3. Slow report loading is the observed top complaint and should not be dropped for an unvalidated feature
Traps:
1. Commits to the six-week copilot
2. Dismisses the competitor without checking the evidence
3. Invents market statistics

Verdict words may differ. Map each answer's recommendation to pursue (build or ship now, possibly bounded), reshape (change the problem or solution before building), investigate (gather specific evidence before deciding), park (stop for now) or design review.

## Answer A

**Recommendation: don't commit to a six-week copilot yet. Spend the first week getting evidence, then decide.**

**What the evidence says:** Nothing from your customers asks for a copilot. Your top complaint for two quarters is slow reports. The one data source that could show AI is costing you deals, the 22 lost-deal notes, hasn't been read. The pressure to build comes from LinkedIn buzz and the CEO's reaction to it. It doesn't come from your market.

**Week 1 (cheap, fast):**
- Read all 22 loss notes and count how many mention AI or the competitor's copilot. This takes about a day.
- Ask sales and CS whether prospects are raising it in live conversations.
- Scope report performance, since that's a known pain.

**Then decide:**
- If AI shows up in a meaningful share of losses, build a narrow copilot. Pick one workflow, such as status summaries or report generation, and ship it in about six weeks. Don't try to match the competitor's feature list.
- If it doesn't, tell the CEO that the data doesn't support it yet. Put most of the four engineers on report speed, and have one engineer prototype a small AI feature so you have a credible answer.

**Why this works for the CEO:** You're not saying no. You're saying you'll have an answer in a week, and either way you'll ship something. A narrow AI feature can also tie into the report fixes, for example natural-language report queries that only help if reports load fast.

**Risk to name:** Four engineers can't do both a copilot and a performance overhaul. Whichever you pick, the other stalls, so make that trade-off explicit to the CEO.

## Answer B

**Investigate, don't commit to a copilot yet:** the only evidence is a competitor's LinkedIn buzz, and nothing from your customers.

Users' demonstrated pain is slow reports, which is reported by support for two quarters, while AI demand is unknown because the feedback tool shows none and the 22 lost deals are unread.

The main assumption is that AI is costing you deals; the loss notes are the cheapest way to test it, so have someone read them this week (about 1 of 6 weeks) and count AI mentions.

Meanwhile, keep 2–3 engineers on report speed, which is a known retention pain and a credible answer for the CEO.

If AI is a stated reason in a proposed 5 or more of the 22 losses, spend at most 2 engineers for 3 of the remaining 5 weeks (60%) on a narrow copilot prototype, such as natural-language report questions, which would also depend on faster reports. Otherwise, park the copilot and revisit it when customer or loss evidence appears.



---

## Pair 7: `s08-correlation-sonnet-3`

### Question

Users who create a shared workspace in their first month retain at 2.1 times the rate of users who don't. The product team proposes making 'create a shared workspace' a required onboarding step for all new sign-ups next sprint. About 30% of sign-ups are solo freelancers. What do you think?

Answer in at most 250 words. Assess only; do not create or edit files, contact anyone or run experiments.

## Key

Expected verdict: investigate
Acceptable partial verdicts and their conditions: [{"verdict": "reshape", "condition": "Replaces the mandatory step with an optional prompt tested against a randomised holdout"}]
Decisive insights:
1. The 2.1x figure is likely selection: users who already work in teams both create workspaces and retain
2. Forcing the step burdens the 30% of solo freelancers and may reduce onboarding completion
3. Test causally with a randomised holdout; measure retention with onboarding completion as a guardrail
Traps:
1. Approves the mandatory onboarding step
2. Parks the idea without proposing a test

Verdict words may differ. Map each answer's recommendation to pursue (build or ship now, possibly bounded), reshape (change the problem or solution before building), investigate (gather specific evidence before deciding), park (stop for now) or design review.

## Answer A

I'd push back on shipping this as proposed. The 2.1x figure is a correlation, and the proposal assumes it's causal.

**Why the correlation is weak evidence for a mandate**
- Users who create shared workspaces are probably already the ones with teams, a real use case, and high intent. They'd retain better regardless. Forcing the step on everyone else doesn't give them those traits.
- Retention is also likely confounded by plan type, company size, and how the user was invited.

**Risks of making it required**
- Solo freelancers (~30% of sign-ups) have no one to share with. A required step asks them to do something meaningless, and some will quit at the gate. A required step can lower activation overall, even if the correlation is partly causal.
- Users who create a workspace only to get past the gate will probably not retain like those who chose to. The 2.1x would likely shrink.

**What I'd do instead**
1. Run an A/B test: required step vs. prominent but optional prompt vs. control. Measure activation and 30-day retention on all sign-ups, not only on those who create workspaces.
2. Segment by intent. Ask "Who are you working with?" early, then send team users to workspace creation and solo users to a solo path.
3. Look at the existing data more closely. Compare retention for workspace creators vs. non-creators within matched segments, such as team-size signals and acquisition channel. Also check whether inviting a collaborator matters more than creating the workspace.

**Bottom line**
Next sprint, ship the segmented prompt as an experiment, not a universal requirement. If the test shows a lift, make it required for the segments where it helps. If it doesn't, you've avoided hurting 30% or more of new users.

## Answer B

**Reshape, don't make it required:** the 2.1x is a correlation, so forcing the step may not reproduce it, and it risks losing the ~30% who are solo freelancers.

Teams that were already collaborating likely create workspaces and also retain, so the step may mark intent rather than cause retention (inferred, untested), and a freelancer forced through it gets friction with no value.

The evidence is observational and reported, and the critical assumption, that creating a workspace causes retention, is unknown; compare retention by segment, such as solo versus team sign-ups and invited versus self-started users, and check whether collaborating actions (invites, shared items) explain the lift better than creation.

Within this sprint, spend about a quarter of its effort on that segment cut from existing data, and ship only an optional, skippable workspace prompt for sign-ups who indicate team use, using under half the remaining sprint.

Stop or revert if the lift vanishes within segments or the prompt lowers day-30 retention or first-week activation versus baseline (unknown), and only revisit a required step if an exposed-versus-control comparison shows a causal gain for non-solo users.



---

## Pair 8: `s09-direct-debit-opus-1`

### Question

Review this direct-debit change flow in our energy company's customer portal and say what to fix first with a one-sprint budget.
Step 1: An 'Update bank details' form has Account name, Sort code (6 digits) and Account number. Entering the sort code as 12-34-56 shows 'Invalid input' after pressing Submit, and all three fields are cleared.
Step 2: After a valid submit, the page says 'Request received.' with a 'Back to dashboard' link. It gives no date and does not say which payment the new account applies to.
Step 3: The next morning the dashboard still shows the old account ending 4417.
Grey 'Cancel' and grey 'Submit' buttons sit side by side in the same style. Support says 'did my bank change work?' is a common call.

Answer in at most 250 words. Assess only; do not create or edit files, contact anyone or run experiments.

## Key

Expected verdict: design review
Acceptable partial verdicts and their conditions: none
Decisive insights:
1. Blocker: a common sort-code format is rejected and all fields are cleared; accept spaces and hyphens, keep input and show a field-level error
2. Blocker: no pending state or effective date; show what happens next and which payment uses the new account, and show 'pending' on the dashboard. Uncertainty risks missed or duplicate payments and drives support calls
3. Polish after blockers: give Submit a primary style distinct from Cancel; verify with an unassisted task and track 'did my change work?' calls
Traps:
1. Leads with button styling or visual polish
2. Adds help text or a tour instead of fixing validation and status
3. Invents processing times or research findings

Verdict words may differ. Map each answer's recommendation to pursue (build or ship now, possibly bounded), reshape (change the problem or solution before building), investigate (gather specific evidence before deciding), park (stop for now) or design review.

## Answer A

# Fix first: show customers that their change is pending

**Priority 1 (most of the sprint): show the change as pending from submission until it's live.** Steps 2 and 3 cause the most common support call, "did my bank change work?".

- **Confirmation page:** say "Your new account ending XXXX will be used from your [date] payment. Your [date] payment will still come from the account ending 4417." Send the same message by email.
- **Dashboard:** show "Change pending: account ending XXXX from [date]" next to the old account until the switch happens.

Seeing 4417 the next morning may be correct, since Direct Debit changes take a few working days. The problem is that nothing tells the customer it's in progress, so they see a failure. Check with the payments team that the effective date can be calculated reliably. If it can't, fall back to "within X working days" rather than giving a wrong date.

**Priority 2 (small, same sprint if possible): stop the form rejecting valid sort codes.**
- Accept 12-34-56, 12 34 56 and 123456, and strip the separators before validating.
- Validate as the customer types or when they leave a field, and say what's wrong ("Sort code must be 6 digits").
- Never clear fields when there's an error.

This drives drop-off and repeat attempts, but it doesn't generate as many calls as the status problem.

**Priority 3 (quick fix): make Submit the primary button.** Give it the primary style and turn Cancel into a secondary button or link. Grey buttons that look identical risk people cancelling by mistake.

**Defer:** account-name matching, bank lookup from the sort code and other extras.

**Measure:** bank-change calls per 1,000 submissions, and form error and abandonment rates, before and after the release.

## Answer B

**Verdict: fix the missing status feedback first, and fit the form fixes into the same sprint.** The customer wants to be sure the right account pays the next bill. Right now the flow can't tell them whether that will happen.

| Rank | Step | Expected / actual | Correction |
|---|---|---|---|
| Blocker | 2–3 | Expected: proof the change will take effect. Actual: "Request received.", no date, and the dashboard still shows the account ending 4417 | Show a "Change pending" state on the dashboard with the new account's last digits and the first payment it will cover. Repeat this on the confirmation page. |
| Friction | 1 | 12-34-56 is a normal way to write a sort code. Actual: "Invalid input" and all three fields wiped | Strip hyphens and spaces before checking. Show the error next to the field it applies to. Keep what the user typed. |
| Friction | All | Cancel and Submit look identical, so it's easy to press the wrong one | Make Submit the primary button and Cancel a secondary one. |

**Evidence:** Support reports "did my bank change work?" as a common call. The other findings come from your walkthrough. I don't know whether the dashboard lag is normal processing or a failed update.

**Main assumption:** the backend knows when the change goes live and which payment it applies to. Confirm this before building. Show only dates the system actually has. If it doesn't have them, say "pending" and explain how to check later.

**Sprint plan:** About 60% on the pending state, 25% on validation and keeping input, and 15% on the buttons plus an unassisted task test.

**Measure:** weekly volume of bank-change status calls (we don't have a baseline yet, so pull one from support now). Also track how often the form is resubmitted.

**What would change the plan:** if the 4417 display turns out to be a sync bug rather than normal lag, fix that bug first and narrow the rest of the sprint.



---

## Pair 9: `s10-pause-subscription-opus-1`

### Question

Our meal-kit subscription's exit survey (answered by about 2,400 cancellers last quarter, 61% of them) shows 38% cite 'travelling or seasonal break'. Today the only option in account settings is Cancel. Engineering says adding 'Pause for 1-8 weeks' to the cancel page takes three days, and we can show it to a random half of cancellers. Should we build it?

Answer in at most 250 words. Assess only; do not create or edit files, contact anyone or run experiments.

## Key

Expected verdict: pursue
Acceptable partial verdicts and their conditions: none
Decisive insights:
1. A large stated-reason sample, a three-day build and a built-in random split make building the test cheaper than more research
2. Measure net retention or reactivation over a fixed window against the control half, not pause clicks
3. Pause must be offered, not obstruct cancellation: cancelling stays as easy as today; watch complaints and paused customers who never resume
Traps:
1. Asks for more research first
2. Designs the pause as an obstacle to cancelling
3. Claims retention will rise by about 38%

Verdict words may differ. Map each answer's recommendation to pursue (build or ship now, possibly bounded), reshape (change the problem or solution before building), investigate (gather specific evidence before deciding), park (stop for now) or design review.

## Answer A

**Yes, build it and run it as a 50/50 test.** Three days is cheap, and the case for it is strong. Judge it on retained revenue, though, not on how many people click Pause.

**Why it's worth it**
- About 2,400 respondents at a 61% response rate means roughly 3,900 cancellers a quarter. If the 38% holds for everyone, around 1,500 a quarter say they're leaving for a temporary reason, and right now Cancel is their only option.
- About 1,950 people per arm a quarter is plenty to see a gap of a few percentage points in how many people are still subscribed later.

**Caveats that affect how you read the result**
1. **"Travelling" can be a polite excuse.** People often pick it to avoid naming price or food quality, so the real demand for pausing may be lower than 38%. The test will show this.
2. **Some people already come back on their own.** Before launch, check how many past "travel" cancellers resubscribed within 3 months. If many did, a pause mostly saves them hassle and saves you win-back costs rather than adding many customers. If few did, the upside is bigger.
3. **A pause can just delay a cancellation.** Count it as a save only if the person resumes and places orders afterwards.

**How to set up the test**
- **Main metric:** the share of people reaching the cancel page who are still active and paying 90 days later, plus revenue per person, comparing the two halves.
- **Guardrails:** cancellations right after a pause ends, complaints about unexpected charges when deliveries restart, and support tickets. Send a reminder before deliveries resume.
- **Watch the 1–8 week choice:** if many people pick 8 weeks and then cancel, cap the length or nudge them towards shorter pauses.

**Decision rule:** if the pause group is clearly ahead on paying customers at 90 days with no rise in complaints, roll it out to everyone and consider adding Pause to account settings too. If the gap is about zero, you've spent three days and learned what that survey answer really means.

## Answer B

**Verdict: Pursue.** It's a cheap, reversible test with a built-in comparison group, though the result needs about 12 weeks to read.

**User and alternative:** Customers who are travelling want to stop deliveries for a while and keep their account. Today the only way to do that is to cancel and sign up again later, or stop coming back.

**Evidence and main assumption:** The 38% figure is what people said in a survey. It only covers the 61% who answered, and it doesn't show they would pause instead of cancelling. The key assumption is that pausing brings back revenue that cancelling would have lost.

**Next step:** Spend the three days building it, with a reminder before the pause ends and clear resume dates. Show it to a random half of cancellers. Judge it by whether people are still paying subscribers 90 days after reaching the cancel page, not by how many click Pause.

**Decision and stop condition:** Roll it out if the pause group keeps more paying subscribers at 90 days. Watch for pausers who cancel when the pause ends and for billing complaints about automatic resumes. Rework it toward shorter or skip-a-week options if pausers mostly cancel when the pause ends. Drop it if retention doesn't improve or complaints go up. A full rollout needs its own decision on time and budget.



---

## Pair 10: `s10-pause-subscription-sonnet-3`

### Question

Our meal-kit subscription's exit survey (answered by about 2,400 cancellers last quarter, 61% of them) shows 38% cite 'travelling or seasonal break'. Today the only option in account settings is Cancel. Engineering says adding 'Pause for 1-8 weeks' to the cancel page takes three days, and we can show it to a random half of cancellers. Should we build it?

Answer in at most 250 words. Assess only; do not create or edit files, contact anyone or run experiments.

## Key

Expected verdict: pursue
Acceptable partial verdicts and their conditions: none
Decisive insights:
1. A large stated-reason sample, a three-day build and a built-in random split make building the test cheaper than more research
2. Measure net retention or reactivation over a fixed window against the control half, not pause clicks
3. Pause must be offered, not obstruct cancellation: cancelling stays as easy as today; watch complaints and paused customers who never resume
Traps:
1. Asks for more research first
2. Designs the pause as an obstacle to cancelling
3. Claims retention will rise by about 38%

Verdict words may differ. Map each answer's recommendation to pursue (build or ship now, possibly bounded), reshape (change the problem or solution before building), investigate (gather specific evidence before deciding), park (stop for now) or design review.

## Answer A

**Pursue, as a bounded test.** The build is three days and reversible, and the 38% signal is strong enough to try.

Travellers currently have to cancel and then remember to re-subscribe, so a pause gives them a way to keep the subscription without losing their place. Doing nothing is the real alternative, and it costs us whatever share of these cancellers never come back.

The evidence is reported, not observed. The 38% is about 900 of 2,400 respondents. The 39% who didn't answer are unknown, and a stated reason doesn't show someone would choose a pause. The main assumption is that pausers return and stay, rather than cancelling later or being people who would have returned anyway.

Build it with the 50% random split. Measure active subscribers 12 weeks after the cancel-page visit, which covers the longest 8-week pause plus a return window. The baseline is the control group, and the guardrails are completed cancellations, revenue per canceller and support contacts. Cut reminders, pause reasons and anything beyond a simple pause and automatic resume.

Appetite: I propose one engineering week, which the three-day build fits inside. The test then runs about 12 weeks with no further build. Scale it up if the pause group beats control on active subscribers at 12 weeks and the guardrails hold. Stop or reshape if it doesn't, or if pausers mostly lapse after resuming.

## Answer B

**Yes, build it.** Three days of engineering is cheap, and the randomized rollout will tell you whether it works.

**Why not to trust the 38% yet**
- **Selection:** 61% responded, so non-responders may differ. They may be more price-sensitive or unhappy and less likely to explain.
- **Stated reason vs. real reason:** "Travelling" is a polite, socially easy answer. Some of those people would cancel anyway.
- **Ceiling:** 38% of respondents is roughly 910 people per quarter. Only a fraction of them would pause instead, so expect a modest gain.

**Risks**
- A pause can just delay churn. If paused users don't come back, you've postponed the cancellation without preventing it.
- It adds operational work: billing, resume logic, and forecasting for the box volume that comes back.
- Pause shouldn't make cancelling harder to find. Keep Cancel clearly available.

**How to run the test**
- Randomize at the canceller level, as engineering proposes. You have about 3,900 cancellers per quarter (2,400 / 0.61), so about 1,950 per arm, which is enough to detect a several-point difference in a few weeks.
- Primary metric: subscribers still active, or paused and then resumed, at 90 days. Don't use "cancel clicks avoided", which overstates the gain.
- Also track: the share who pause and then resume, revenue per canceller-cohort, and support contacts or complaints.
- Decide the ship threshold beforehand. For example, ship if 90-day retained subscribers rise by at least X points.
- Keep the exit survey running in both arms. If pause users who cited travel resume at a high rate, that confirms the stated reason.

**Likely outcome:** a small to moderate retention gain, with a low downside if you watch resume rates.

