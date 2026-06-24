# Second-Round Playtest Screenshot Package

Status: screenshot / recording QA asset package only. These assets do not implement product features, backend behavior, report runtime, public delivery, data collection, or platform integrations.

## Purpose

This folder contains local browser screenshots for the second-round Sentigraph C-end / B-end playtest and optional 3-minute / 8-minute demo recording.

Source package:

- `docs/demo/second_round_playtest_package/README.md`
- `docs/demo/second_round_playtest_package/demo_recording_script_3min.md`
- `docs/demo/second_round_playtest_package/demo_recording_script_8min.md`
- `docs/demo/second_round_playtest_package/screenshot_checklist.md`

## Routes Covered

- `/#/demo`
- `/#/public-events`
- `/#/public-events/donglu-sunjihai-youth-football`
- `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football`
- `/#/reports/donglu-sunjihai-youth-football-sample`

Optional route checked but not captured:

- `/#/analysis-requests` was skipped because the local backend was not running and the page showed a visible 500 marker.

## Screenshot Inventory

| File | Recording Use |
| --- | --- |
| `01_demo_home.png` | 3-min and 8-min intro: guided demo entry. |
| `02_public_events_plaza.png` | Public Event Plaza, with local demo / not hotlist context. |
| `03_dong_sun_event_detail_top.png` | Dong/Sun event detail top section. |
| `04_dong_sun_evidence_summary.png` | Dong/Sun evidence / sample coverage context. |
| `05_dong_sun_sandbox_entry_cta.png` | Event detail to Sandbox transition. |
| `06_dong_sun_sandbox_v2_overview.png` | Sandbox V2 overview with EchoBox / timeline / sample boundary. |
| `07_dong_sun_t0_t6_controls.png` | T0-T6 historical replay controls. |
| `08_marker_peoplecluster_boundary.png` | Sandbox marker and PeopleCluster / InfluenceCore boundary context. |
| `09_dong_sun_b_end_report_hero.png` | B-end report sample hero. |
| `10_report_evidence_coverage.png` | Report evidence coverage / executive summary. |
| `11_report_response_tempo.png` | Report response tempo / lifecycle context. |
| `12_report_boundaries.png` | Report boundary and export-governance section. |

## Boundary Reminder

Use these screenshots only with the matching demo boundary language:

- Sentigraph is not a crawler product.
- Event Plaza is not a real hotlist.
- Dong/Sun is a controlled candidate public sample.
- Sandbox V2 is frontend-only local historical replay.
- PeopleCluster is anonymous aggregate group / behavioral proxy, not a real person.
- InfluenceCore is content / narrative / official / media / KOL / meme core, not people balls.
- No full-web coverage.
- No full-platform coverage.
- No official verification.
- No causal proof.
- No real API or LLM in this demo.
- No real request / vote / support / sponsorship.
- Local Exchange Reader is disabled-by-default metadata-only scaffold, not real private collector integration.

## Capture Status

Screenshots were actually captured from the local frontend dev server at `http://127.0.0.1:5173/`.

Video recording remains manual-only. No MP4 or video files were produced in this task.
