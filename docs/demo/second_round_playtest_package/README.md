# Second-Round Playtest Demo Package

Status: demo / QA / documentation packaging only. This package does not implement product features, live data collection, backend runtime behavior, report generation runtime, public delivery, or platform integrations.

## Purpose

This package helps run a second-round Sentigraph playtest with two audiences:

- C-end friends / normal users who should understand the public event experience.
- B-end / professional reviewers in PR, operations, media, MCN, sports, brand, or community roles who should judge report value and boundary clarity.

It also supports an optional self-recorded demo video.

## What To Test

Primary routes:

- `/#/demo`
- `/#/public-events`
- `/#/public-events/donglu-sunjihai-youth-football`
- `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football`
- `/#/public-events/request`
- `/#/reports/donglu-sunjihai-youth-football-sample`

Optional technical-governance route:

- `/#/analysis-requests`

## Package Files

- `c_end_playtest_quick_start.md`: short C-end route, prompts, and misunderstanding checks.
- `b_end_review_quick_start.md`: B-end route, value questions, and professional review prompts.
- `demo_recording_script_3min.md`: tight 3-minute recording script.
- `demo_recording_script_8min.md`: deeper 8-minute recording script.
- `screenshot_checklist.md`: suggested screenshots and filenames.
- `boundary_talking_points.md`: safe wording and claims to avoid.
- `observer_note_template.md`: note template for live observation.
- `post_playtest_feedback_triage_template.md`: post-session feedback grouping template.

Related existing docs:

- `docs/playtest/second_round_c_end_b_end_playtest_plan_v1.md`
- `docs/playtest/second_round_c_end_b_end_playtest_script_v1.md`
- `docs/playtest/second_round_c_end_b_end_feedback_form_v1.md`
- `docs/playtest/second_round_c_end_b_end_observation_checklist_v1.md`

## What Not To Claim

- Sentigraph is not a crawler product.
- Event Plaza is not a real hotlist.
- The Dong/Sun and Helldivers demos are controlled candidate / selected public samples.
- Sandbox V2 is frontend-only local historical replay, not future prediction.
- There is no full-web coverage, full-platform coverage, official verification, or causal proof.
- This demo does not call real APIs or real LLMs.
- Request, vote, support, and sponsorship flows are mock only.
- Local Exchange Reader is disabled-by-default metadata-only scaffold, not a private collector integration.
- Provider output is evidence, not truth.

## How To Record Feedback

During playtest, record:

- Original user question.
- Route where confusion happened.
- Screenshot or timestamp if available.
- Whether the issue is navigation, wording, visual comprehension, business value, or compliance risk.
- Whether the suggestion is tentative or needs code confirmation.

Do not record private account data, platform login state, secrets, cookies, tokens, or personal sensitive information.

## Current Boundary Summary

This playtest package is for local demo review. It does not touch the private collector project, does not read real exchange dirs, does not parse `evidence_items.jsonl` or `evidence_items.csv`, does not write the Evidence Layer, and does not create production cases, analysis runs, reports, Sandbox fixtures, public events, public URLs, signed URLs, or download routes.
