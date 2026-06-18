# Sentigraph Two-Event Demo Package

## Purpose

This package gives a compact, ready-to-present path for the current Sentigraph demo. It lets a presenter explain the C-end public event experience, the Opinion Ecosystem Sandbox, and B-end report sample value through two event chains without reading the whole repository.

The package is for recording, customer preview, internal review, cooperation review, and product-context recovery.

## Audience

- Internal product and engineering review.
- C-end users who need to understand public event pages.
- B-end customers such as brand, game, sports, media, community, MCN, public relations, and operations teams.
- Potential partners, platform reviewers, and vendor reviewers.
- Early investor or collaborator review.

## Current Demo Status

Sentigraph currently supports a local, frontend-first two-event demo:

- Helldivers / PSN selected public sample.
- Dong Lu / Sun Jihai youth football controlled candidate public sample.
- Event Plaza and guided demo entry.
- Opinion Ecosystem Sandbox V2 local historical replay.
- Fixed B-end report sample pages.
- External Collector Bridge explanation for local exported packages.

## What Is Implemented

- C-end guided demo: `/#/demo`
- Event Plaza: `/#/public-events`
- External Collector Bridge: `/#/external-collector`
- Request / vote mock flow: `/#/public-events/request`
- Helldivers public event detail page.
- Helldivers Opinion Ecosystem Sandbox route.
- Helldivers B-end report sample.
- Dong/Sun public event detail page.
- Dong/Sun Opinion Ecosystem Sandbox route.
- Dong/Sun B-end report sample.
- Screenshot packages for Sandbox V2, Dong/Sun C-end, and Dong/Sun B-end report sample.

## What Is Not Implemented

- No full-web collection.
- No full-platform collection.
- No full-thread reconstruction.
- No real-time monitoring claim for these demo pages.
- No official verification.
- No causal proof.
- No real platform API integration in the demo flow.
- No real report export runtime.
- No PDF / Markdown / briefing deck generation.
- No backend export job.
- No Response Strategy Lab runtime; it is planned-only.
- No automatic public parser fetch.
- No collector job is run from Sentigraph during the demo.

## Route Map

### Shared / C-End Routes

- Guided demo: `/#/demo`
- Event Plaza: `/#/public-events`
- External Collector Bridge: `/#/external-collector`
- Request / vote mock: `/#/public-events/request`

### Helldivers Chain

- Event detail: `/#/public-events/helldivers-psn`
- Sandbox: `/#/opinion-ecosystem`
- B-end report sample: `/#/reports/helldivers-psn-sample`

### Dong/Sun Chain

- Event detail: `/#/public-events/donglu-sunjihai-youth-football`
- Sandbox: `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football`
- B-end report sample: `/#/reports/donglu-sunjihai-youth-football-sample`

## Recommended Presentation Order

1. Start at `/#/demo`.
2. Open `/#/public-events`.
3. Explain Event Plaza is a local demo event list, not a real hot list.
4. Open the Helldivers event as the earlier international / game-community selected public sample.
5. Open Sandbox V2 historical replay.
6. Open Helldivers B-end report sample.
7. Return to Event Plaza.
8. Open the Dong/Sun Chinese event sample.
9. Open Dong/Sun Sandbox V2 local historical replay.
10. Open Dong/Sun B-end report sample.
11. Explain Response Strategy Lab is planned-only.
12. Explain the future Search-to-Report pipeline.

## C-End Demo Path

Use the C-end path to show how a non-specialist user can find an event, read its public sample boundary, open the sandbox, and understand why evidence needs review.

Key points to say:

- Event Plaza is not a real hot list.
- Request / vote is mock only.
- Selected public sample and controlled candidate public sample do not mean full coverage.
- PeopleCluster means anonymous groups or clusters, not real individuals.
- InfluenceCore means content, narrative, official, media, meme, or community cores, not people balls.

## B-End Report Sample Path

Use the B-end path to show how Sentigraph could organize evidence-backed context into an executive report format.

Key points to say:

- These are fixed frontend report samples.
- Report export is planned-only.
- Response Strategy Lab is planned-only.
- Suggested actions are decision-support examples, not automatic instructions.
- Evidence remains `review_needed` / `source_url_provided_unverified` until reviewed.

## External Collector Bridge Explanation

The External Collector Bridge explains where a local Evidence Export package can enter Sentigraph.

Safe wording:

- Private collector capability is external to Sentigraph.
- Sentigraph does not present private collector capability as a built-in crawler.
- The bridge reads local exported package metadata when configured.
- It does not run crawler jobs during the demo.
- It does not search the web, fetch URLs, or call real platform APIs.

## Screenshot / Asset Folder References

- Sandbox V2 screenshots: `docs/demo/assets/opinion_ecosystem_sandbox_v2/`
- Sandbox V2 timeline screenshots: `docs/demo/assets/opinion_ecosystem_sandbox_v2_timeline/`
- Dong/Sun C-end screenshots: `docs/demo/assets/donglu_sunjihai_c_end_demo/`
- Dong/Sun B-end report screenshots: `docs/demo/assets/donglu_sunjihai_b_end_report_sample/`
- Helldivers screenshots: `docs/demo/assets/helldivers_opinion_ecosystem/`

## Recording Preparation

- Start the frontend locally.
- Open only local Sentigraph pages.
- Keep terminal windows with secrets hidden.
- Do not show private collector internals unless intentionally explaining local export package boundaries.
- Confirm the visible page contains boundary copy before recording.
- Keep the route list nearby so the presenter can recover quickly.

## Risk / Boundary Notes

Always state:

- Frontend-only local demo.
- Selected public sample or controlled candidate public sample.
- Evidence coverage limitation.
- Not full-web coverage.
- Not full-platform coverage.
- Not full-thread coverage.
- Not official verification.
- Not causal proof.
- Not production data.
- Not real prediction.
- Not real report export.
- Not a judgment of who is right or wrong.

## Do-Not-Say List

Avoid:

- "Full-web coverage is complete."
- "All platform data is connected."
- "This is official verification."
- "This proves causality."
- "This predicts the future."
- "This is a crawler product."
- "This is real-time platform monitoring."
- "This report can be exported now."
- "The system decides who is right or wrong."
- "The system identifies the easiest people to persuade."
- "The system can covertly shape or seed consensus."

Avoid Chinese phrases that imply covert manipulation, forced narrative control, fake consensus, or targeted persuasion.

## Known Limitations

- Helldivers is a selected public sample.
- Dong/Sun is a controlled candidate public sample.
- Sandbox V2 historical replay is local and sample-based.
- B-end reports are fixed frontend report samples.
- Search-to-Report pipeline is future planning.
- Response Strategy Lab is planned-only.
- Report export is planned-only.
- Real provider gates remain separate legal, product, and API approval work.

## Next Development Options

- Source 10 / project-context update for the two-event demo state.
- Record the 3-minute two-event walkthrough.
- Record the 8-minute two-event walkthrough.
- Prepare a customer-facing slide deck with screenshot references.
- Improve demo copy based on feedback.
- Plan Search-to-Report pipeline only after provider and compliance gates are clear.
- Keep real provider adapters out of scope until official permission, contract, quota, and safety gates are complete.
