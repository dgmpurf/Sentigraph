# Sentigraph Report Quality Rubric

Status: v4.4 mock/offline rubric implemented.

## Purpose

The report quality rubric adds deterministic, rule-based checks for generated public-opinion reports. It is part of the offline benchmark harness and is meant to catch structural regressions before future real LLM or real platform integrations are enabled.

The rubric does not call OpenAI, DeepSeek, Qwen, or any external LLM API. It does not judge reports with a model. It only checks safe, local report objects and optional Markdown exports.

## Dimensions

Each dimension is scored from 0 to 20. The total score is clamped to 0-100.

### Completeness

Checks that required report fields are present:

- overall summary
- key findings
- main risk factors
- top risk topics when topic-risk data exists
- recommended actions
- suggested public response

### Risk Explanation Quality

Checks whether the report:

- mentions a risk score or risk level
- explains why risk is elevated
- references top risk topics when available
- distinguishes real-crisis and manipulation/repeated-script risk signals when those fields are present

### Actionability

Checks whether:

- recommended actions are specific enough for an operator
- recommendations are not empty or generic only
- the suggested public response is calm, factual, and usable
- the response does not overpromise beyond verified facts

### Safety / Professionalism

Flags:

- raw JSON dumps
- API-key, token, or secret-like markers
- private contact data patterns
- aggressive or accusatory language
- unsupported legal/fraud conclusions such as "confirmed fraud" unless a future reviewed context explicitly supports that claim

### Language And Formatting

Checks that:

- `zh-CN` reports contain Chinese text
- representative comments remain in their original language
- Markdown exports contain expected report sections when Markdown is supplied
- the report is readable and not just disconnected fragments

## Grades

```text
pass    total_score >= 80 and no fail-severity findings
warning total_score >= 60 with warning findings, or total_score 60-79
fail    total_score < 60 or any fail-severity finding
```

Fail-severity findings include raw JSON dumps, secret/API-key exposure, private contact data patterns, unsupported overclaims, and aggressive/accusatory report language.

## Benchmark Coverage

The offline benchmark suite `report_quality_rubric` currently covers:

- high-quality brand/product crisis report
- missing recommended actions
- raw JSON dump
- vague recommendations and public response
- unsafe overclaim
- representative comment preservation
- Markdown report quality

The benchmark stores only score, grade, finding codes, missing section names, and dimension scores in per-case details. Generated `.benchmarks/` summaries remain summary-only and do not include raw report text or fixture payloads.

QA coverage also verifies that the suite participates in benchmark history/regression tracking, so a future `report_quality_rubric` pass-to-fail change is surfaced in the generated regression summary.

## Limitations

This rubric is intentionally coarse. It does not replace:

- human review
- a human-labeled report quality dataset
- factual verification against external sources
- real LLM-as-judge evaluation
- domain-specific legal or PR review

The rubric should catch obvious regressions, not decide whether a crisis response is production-ready.

## Future Work

- Add a human-labeled report quality dataset.
- Add scenario-specific report rubrics for brand, public figure, workplace, and safety/legal cases.
- Add optional LLM-as-judge evaluation only after real-provider safety gates, redaction, cost controls, and human review are complete.
- Add deeper Markdown readability and section-order checks if report formats diverge by report type.
