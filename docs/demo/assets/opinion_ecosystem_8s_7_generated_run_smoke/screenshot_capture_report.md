# Phase 8S-7 Generated-run Screenshot Capture Report

Capture time: 2026-06-27 12:41:11 +08:00

## URLs

- `http://127.0.0.1:5173/#/opinion-ecosystem`
- `http://127.0.0.1:5173/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football`

## Click Behavior

- Before click: the static Opinion Ecosystem explanation remained visible and the generated-run panel was visible.
- Explicit click: `Load backend local generated run` called the local backend fixture route.
- After click: generated-run metadata, boundary labels, warnings/blockers area, and module output cards rendered.
- No auto backend call was observed before the explicit click.
- Network check: both routes made `0` generated-run requests before click and `1` local fixture generated-run request after click.

## Default Route Result

Status: pass

- Generated-run panel visible before click: yes
- Backend local generated run visible after click: yes
- `sentigraph_opinion_ecosystem_run_v0_1` visible after click: yes
- `sample_helldivers_psn` visible after click: yes
- Boundary copy visible: yes
- Module output cards visible: yes

## Dong/Sun Route Result

Status: pass

- Dong/Sun query route preserved the Dong/Sun selected sample: yes
- No fallback to Helldivers after page load or click: yes
- Backend local generated run visible after click: yes
- `sample_donglu_sunjihai_youth_football` visible after click: yes
- Boundary copy visible: yes
- Module output cards visible: yes

## Console And Visible Issue Scan

- Console error count: 0
- Console warning count: 0
- Visible `Request failed with status code 500`: no
- Visible `[object Object]`: no
- Visible `undefined`: no
- Visible `NaN`: no
- Visible publish/send/post/execute CTA: no
- Visible forbidden score fields: no
- Visible generated public response text: no
- Raw author identifiers visible: no

## Copy Polish Made

Small frontend display polish was made during QA:

- Structured module field values now render as a bounded safe JSON summary block.
- The display remains read-only and still filters forbidden keys.
- No backend API, route, schema, calculator, runtime, or persistence behavior changed.

## Known Notes

- The generated-run route is a local fixture route for browser QA and is not production scoring.
- Screenshots are QA evidence only. They do not complete manual playtest or external demo recording.
- The browser automation used local Chrome with an isolated automation context and did not use the user's browser profile, login state, cookies, or sessions.

## Final Decision

ready_for_8S_8_manual_playtest_or_recording_readiness_decision
