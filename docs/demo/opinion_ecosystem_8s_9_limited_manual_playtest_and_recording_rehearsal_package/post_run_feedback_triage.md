# Post-run Feedback Triage

## A. Purpose

Use this after an internal recording rehearsal or one trusted manual playtest to classify feedback and decide whether to stop, fix, or continue.

This document does not execute a playtest, record video, generate media, run collector jobs, call real APIs, call real LLMs, or modify product behavior.

## B. Severity Levels

### P0: Stop Immediately

P0 includes:

- privacy/safety issue
- secrets exposed
- raw author identifiers shown
- generated response text appears
- publish / send / post / execute CTA appears
- user cannot be corrected about live crawling / official truth
- visible 500 blocks primary route
- backend/frontend crash

Action: stop and create a `needs_fix` task.

### P1: Fix Before Wider Playtest

P1 includes:

- user misunderstands selected sample boundary
- PeopleCluster looks like a real person
- generated run looks like production score
- Dong/Sun route confusion
- B-end report sample unclear
- key boundary labels hidden

Action: do small copy/UX fix before any wider playtest.

### P2: Improve Soon

P2 includes:

- copy density
- layout polish
- route ordering
- minor terminology confusion
- recording pacing issue

Action: collect with other P2 items and fix when batching demo polish.

### P3: Nice To Have

P3 includes:

- minor wording preference
- optional screenshot request
- alternate route suggestion
- visual polish idea that does not block understanding

Action: keep as backlog.

## C. Next-phase Mapping

If P0:

- stop
- create needs_fix task
- do not run wider playtest
- do not record externally

If P1:

- do small copy/UX fix before any wider playtest
- re-run the affected route smoke

If only P2/P3:

- proceed to limited internal rehearsal or one trusted tester run
- keep feedback in the note sheet

## D. Source Update Rule

Only update Source after commit if phase status changes.

For 8S-9 package completion:

- update Source 00
- update Source 08
- update Source 09
- update Source 10

Do not update Source 11 unless Analysis Request / Provider / Import Governance behavior changes.
