# Coverage Note

This package is a selected / controlled public evidence sample for Sentigraph demo evaluation.

Sample status:
- candidate_demo_sample
- not production data
- not yet integrated into Event Plaza, Sandbox V2, or B-end report samples

It is not:
- not full-web coverage
- not full-platform coverage
- not full-thread coverage
- not official verification
- not causal proof
- not a judgment of who is right or wrong
- not a complete reconstruction of the public controversy

Sampling scope:
- case: donglu_sunjihai_youth_football_202606
- platforms: bilibili, dongqiudi, hupu, manual_context, tieba, weibo
- source URLs: 37
- time window: 2026-06-01T12:00:00.000Z to 2026-06-17T12:10:16.487Z
- approximate item count: 581
- known missing areas: private messages, deleted content, platform-wide baselines, unseen threads, non-exported profiles

Limitations:
- public visible data only where verified by local metadata
- no login/private content exported
- selected sample only
- author identities anonymized
- comments may overrepresent visible, high-emotion, or high-engagement users
- inaccessible/login-required pages are skipped and recorded in skipped_sources
- requires Sentigraph review before analysis
- live collection and private/restricted content were skipped or limited by safety gates
- sample composition may be biased by platform availability, safety gates, and local/manual snapshot choices
- minors, families, and sensitive personal details are not exposed
- raw author IDs, raw author display names, profile URLs, cookies, tokens, sessions, and secrets are not exported
- all evidence remains source_url_provided_unverified and review_needed until future human review
- private collector capabilities are not Sentigraph built-in crawler capabilities
- Sentigraph downstream integration requires a separate audit and development task

Warnings:
- Ephemeral hash salt was used for this local demo package. Hashes are not stable across runs.
