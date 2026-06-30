# Opinion Ecosystem Dense Graph Route Test Plan v0.1

## A. Purpose

This document defines future tests before any backend dense graph route implementation.

No tests are implemented now.

No backend route is implemented now.

No frontend integration is approved now.

## B. Future Required Tests

Future route implementation must include tests for:

- disabled by default
- falsey env disabled
- enabled values `1`, `true`, and `yes`
- unknown env value disabled
- GET-only route surface
- known sample returns safe dense graph response
- unknown sample returns safe `unsupported_sample`
- no arbitrary path input
- no path traversal
- no private collector path
- no evidence items raw row output
- node and edge limits bounded
- degraded attachment returns degraded status
- blocked attachment returns blocked status without unsafe payload
- no raw author identifiers
- no `response_text`
- no `generated_public_message`
- no publish/send/post/execute fields
- no `target_user_list`
- no `persuasion_score`
- no `truth_score`
- no `official_verified`
- no `prediction_probability`
- no `psychological_profile`
- no `personality_diagnosis`
- runtime side-effect flags false
- no Evidence Layer write
- no production case
- no production `analysis_run`
- no frontend changes
- no real API call
- no real LLM call
- no collector run

## C. Future Validation Commands

Possible future implementation validation:

```text
python -m pytest backend/app/tests/test_opinion_ecosystem_dense_graph_route.py
python -m pytest backend/app/tests/test_opinion_ecosystem_dense_graph_generated_run_integration.py
python -m pytest backend/app/tests/test_opinion_ecosystem_dense_graph_generated_run_adapter.py
python -m pytest backend/app/tests/test_opinion_ecosystem_dense_graph_builder.py
python -m pytest backend/app/tests/test_analysis_request_golden_contracts.py
python -m py_compile backend/app/api/v1/routes/<future_route_file>.py
git diff --check
```

If route implementation touches shared API setup, future validation should also include the relevant API route registration tests.

## D. Stop Rules

Stop future implementation if:

- route enabled by default
- route exposes public, C-end, B-end, or customer surface
- route accepts arbitrary path or URL
- route reads private collector path
- route parses raw evidence rows outside controlled sample policy
- route exposes raw author identifiers
- route emits generated response text
- route creates Evidence Layer write
- route creates production case
- route creates production `analysis_run`
- route adds frontend integration
- route calls real API
- route calls real LLM
- route runs collector
- route sends, publishes, posts, or executes platform actions
- route exposes target-user, persuasion, truth, official verification, prediction, or psychological profiling fields
