# Dedup Group Review Audit Readiness Policy v1

## Purpose

This policy defines the audit requirements for Dedup Group Review Completion Gate evaluation.

The audit trail is the evidence that a human review-only group action happened. It is not official verification, production dedup, Evidence Layer write, or analysis permission.

## Required Audit Coverage

Every group whose status is not `review_needed` must have at least one audit record.

The latest relevant audit must support the current group status.

For example:

- `confirmed` requires a `confirm_group` audit.
- `representative_changed` requires a `change_representative` audit.
- `marked_weak` requires a `mark_group_weak` audit.
- `rejected` requires a `reject_group` audit.
- `needs_more_source` requires a `request_more_source` audit.
- `privacy_hold` requires a `hold_group_for_privacy` audit.
- `split` requires a `split_group` audit.
- `review_needed` after reset should have an append-only `reset_group_review` audit when reset happened.

## Required Audit Fields

Each audit record must include:

- `audit_id`
- `request_id`
- `review_case_id`
- `dedup_preview_id`
- `group_candidate_id`
- `reviewer_label`
- `action`
- `previous_group_status`
- `new_group_status`
- `reviewed_at`
- `affected_item_ids`
- `analysis_effect`
- `dedup_effect`
- no-production side-effect flags
- boundary notes

When representative changed, the audit must include:

- `representative_before`
- `representative_after`

When split occurred, the audit must include:

- `split_item_ids`
- affected item ids

## No-Production Side-Effect Requirements

Audit records must show that these flags remain false:

- `write_evidence_layer_now`
- `create_production_case_now`
- `create_production_review_queue_now`
- `run_production_dedup_now`
- `run_analysis_now`
- `generate_report_now`
- `generate_sandbox_now`
- `generate_public_event_now`

If any audit claims or implies a production side effect, the completion gate must be `blocked`.

## Append-Only Audit Rule

Audits must preserve old decisions.

`reset_group_review` does not delete old audit records.

Changing a representative, splitting a group, rejecting a group, or marking a group weak must append a new audit record instead of rewriting history.

## Missing Audit Behavior

Missing audit means `incomplete`.

Examples:

- group status is `confirmed` but no `confirm_group` audit exists
- group status is `marked_weak` but no weak audit exists
- group status is `representative_changed` but representative before/after values are missing
- group status is `split` but split item metadata is missing

## Inconsistent Audit Behavior

Inconsistent audit means `blocked`.

Examples:

- audit `request_id` does not match the gate input
- audit `dedup_preview_id` does not match the group
- latest audit `new_group_status` contradicts the group status
- affected item ids are outside the group
- representative after value is outside group `item_ids`
- audit says production dedup ran
- audit says analysis can run now
- audit attempts trust upgrade to high or official verification

## Privacy Audit Behavior

Audit with secrets or raw/private fields means `privacy_hold` or `blocked`.

Forbidden values or fields include:

- `raw_author_id`
- `raw_author_name`
- `profile_url`
- private message values
- cookie / token / session values
- API key values
- `.env` values
- password-like values
- email or phone-like values

These labels are allowed only as detection rules or boundary text. They must not appear as exposed real values.

## Readiness Decision

The completion gate can proceed only when:

- all non-`review_needed` groups have required audits
- latest audit supports current group status
- no audit contains production side-effect flags
- no audit contains raw/private/secret-like values
- audit timeline is append-only
- rejected groups remain excluded
- weak groups remain warning-marked
- confirmed groups remain review-only

