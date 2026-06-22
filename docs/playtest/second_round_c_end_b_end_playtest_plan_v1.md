# Second-Round C-End / B-End Playtest Plan v1

Status: docs-only playtest preparation. This plan does not implement product code, backend APIs, frontend routes, live data collection, report generation runtime, or Response Strategy Lab runtime.

## 1. Purpose

This second-round playtest checks whether invited viewers understand the current Sentigraph demo accurately.

The playtest should answer:

- Can C-end viewers understand the public event flow without believing it is full-web truth?
- Can B-end / professional viewers understand the report and sandbox value without believing it is production delivery?
- Do viewers understand sample boundaries, mock labels, and planned-only modules?
- Do viewers distinguish PeopleCluster, InfluenceCore, EchoBox, B-end report samples, and Response Strategy Lab planning status?
- Which page should be improved first before wider demo recording or business review?

## 2. Target Participants

### C-End Track

Recommended participants:

- General friends or non-technical users.
- Game, sports, ACG, brand, or online-community users.
- Users who may browse or share a public event page.
- Users who may request another event analysis.

### B-End Track

Recommended participants:

- PR, brand, community operations, MCN, agency, game operations, sports-content, or creator operations professionals.
- Product, strategy, or risk-management friends who can judge report value.
- Potential collaborator, client, or investor-facing reviewers.

## 3. Session Length

Use one of three formats:

| Format | Length | Best for | Output |
| --- | ---: | --- | --- |
| Quick look | 5-8 minutes | C-end friends, early confusion check | First impression and boundary misunderstanding notes |
| Guided playtest | 15-20 minutes | Most users | Route completion, ratings, confusion points |
| Professional interview | 30-45 minutes | B-end / industry reviewers | Decision value, report value, adoption blockers |

## 4. Route Order

### C-End Route

1. `/#/demo`
2. `/#/public-events`
3. `/#/public-events?guided=1`
4. `/#/public-events/helldivers-psn`
5. `/#/public-events/donglu-sunjihai-youth-football`
6. `/#/opinion-ecosystem`
7. `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football`
8. `/#/public-events/request`

Optional source explanation if the participant asks where the sample came from:

- `/#/external-collector`

### B-End Route

1. `/#/demo`
2. `/#/public-events`
3. `/#/public-events/donglu-sunjihai-youth-football`
4. `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football`
5. `/#/reports/donglu-sunjihai-youth-football-sample`
6. `/#/reports/helldivers-psn-sample`
7. `/#/public-events/request`
8. `/#/external-collector` if sample-source governance is relevant

## 5. What To Observe

Observe behavior before explaining too much:

- Does the participant understand what the product does from the first two pages?
- Do they identify which pages are event entry, event detail, sandbox, request mock, and report sample?
- Do they notice local demo / selected sample / mock labels without being prompted?
- Do they assume live crawling, full-web coverage, official verification, or causal proof?
- Do they understand PeopleCluster as anonymous groups, not real people?
- Do they understand InfluenceCore as content / narrative / official / media / meme core, not small balls?
- Do they treat report samples as fixed sample reports, not dynamic production reports?
- Do they notice Response Strategy Lab as planned-only, not active runtime?
- Do they ask for another event, screenshot, export, share link, or professional workflow?

## 6. What Not To Explain Too Early

Do not explain these before the participant first reacts:

- Detailed definitions of PeopleCluster and InfluenceCore.
- All sample limitations.
- Which route is "supposed" to be most useful.
- Which product persona the participant should imagine.
- Whether the report is C-end or B-end.
- Why votes are mock.

Ask the participant to describe what they think first. Then clarify boundaries.

## 7. Success Criteria

The playtest is successful if most participants can say:

- Sentigraph helps structure public event understanding and evidence review.
- Current event demos use selected samples or local fixtures.
- It is not full-web coverage or full-platform coverage.
- It is not live platform crawling.
- It is not causal proof or official verification.
- PeopleCluster means anonymous groups or clusters.
- InfluenceCore means content, narrative, official, media, or meme core.
- Request/vote is mock where labeled.
- B-end report sample is fixed sample report, not production report generation.

Additional C-end success signals:

- Participant wants to open another event.
- Participant understands why the event page is shareable.
- Participant finds the sandbox useful for event comprehension.

Additional B-end success signals:

- Participant can name a professional decision this could support.
- Participant can identify what evidence/report section they would need in real work.
- Participant asks about compliance, source provenance, review workflow, or client-ready export.

## 8. Confusion Signals

Record these as high-priority confusion:

- "So this crawls the whole internet?"
- "These votes are real heat, right?"
- "This proves what really happened."
- "These balls are individual users."
- "InfluenceCore means influential people."
- "The report is generated live for this client."
- "The system is already using real LLM judgment."
- "Response Strategy Lab is already running real actions."
- "External Collector Bridge is a built-in crawler."
- "The Dong Lu / Sun Jihai sample is official verification."

## 9. Stop Conditions

Pause or stop the session if:

- Participant asks to collect private data or login to a platform.
- Participant asks to use cookies, accounts, captcha bypass, anti-bot bypass, or proxy scraping.
- Participant asks for real platform collection during the playtest.
- Participant wants to paste or show private personal data.
- Participant sees or asks to reveal secrets, tokens, API keys, cookies, sessions, salts, or private browser state.
- Participant cannot distinguish mock/demo from real after two clarifications.

## 10. Privacy And Demo Safety Rules

- Use only local demo routes.
- Do not call real APIs.
- Do not fetch URLs.
- Do not scrape websites.
- Do not run provider or collector jobs.
- Do not open private collector internals unless explicitly explaining local package origin.
- Do not show `.env`, tokens, cookies, sessions, profile paths, salts, or browser accounts.
- Do not collect participant personal sensitive data.
- Do not record private chats, private platform pages, or non-public evidence.
- Treat feedback notes as product observations, not personal profiles.

## 11. Recording And Screenshot Policy

Recommended:

- Ask permission before recording.
- Record only the browser demo area where possible.
- Hide terminal windows unless they are needed for a controlled local demo.
- Avoid showing file explorer paths that reveal private directories.
- Capture screenshots of pages, not participant identity.
- Label screenshots as local demo / selected sample where relevant.

Do not record:

- API keys, `.env`, tokens, cookies, sessions, browser profiles, account pages, private messages, or raw author identifiers.
- Any external website or platform content opened outside the local demo.
- Anything from private collector project internals unless already sanitized and approved for demo explanation.

## 12. How To Summarize Feedback

After each session, write one short record:

- Participant type.
- Track: C-end or B-end.
- Session length.
- Route completed.
- First impression in participant words.
- Main misunderstanding.
- Strongest value signal.
- Lowest-trust moment.
- Page to improve first.
- Boundary text that worked.
- Boundary text that failed.
- Rating summary.
- Recommended follow-up.

After 5-8 sessions, summarize:

- Top 3 comprehension wins.
- Top 3 confusion patterns.
- Top 3 B-end value signals.
- Top 3 C-end share/request signals.
- Top 3 safety wording fixes.
- Recommended next product task.

## 13. What This Playtest Must Not Claim

Do not claim:

- full-web coverage
- full-platform coverage
- full-thread coverage
- live platform crawling
- official verification
- causal proof
- real public event platform production readiness
- real report generation runtime for the B-end samples
- real Response Strategy Lab runtime
- real LLM interpretation
- MediaCrawler integration
- OpenClaw production ingestion
- external delivery, public URL, signed URL, or file-byte download behavior

## 14. Recommended Outcome

After second-round playtest, decide one of:

- improve C-end navigation and boundary copy first
- improve Sandbox V2 terminology first
- improve B-end report sample framing first
- refresh screenshot / recording package first
- run a business / compliance packaging checkpoint first

Do not automatically continue backend refactor unless a playtest finding exposes a concrete blocker.
