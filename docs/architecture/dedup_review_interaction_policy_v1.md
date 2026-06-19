# Dedup Review Interaction Policy v1

## Purpose

This document defines how future human review should interact with dedup group candidates.

Dedup group candidates are review-only governance objects. They are not production evidence, not analysis input, and not verified facts.

## Allowed Future Actions

Future dedup group review may support:

- `confirm_group`
- `split_group`
- `change_representative`
- `mark_group_weak`
- `reject_group`
- `request_more_source`
- `hold_group_for_privacy`

Every action must remain review-only until a later promotion gate.

## Action Semantics

### confirm_group

Reviewer confirms that the candidate group may be treated as one duplicate group in a later gate.

Effects:

- no analysis run
- no Evidence Layer write
- no report generation
- no production case update
- group remains candidate until promotion

### split_group

Reviewer separates items that should not be grouped.

Effects:

- affected item ids must be recorded
- previous grouping remains audit-visible
- no downstream count effect yet

### change_representative

Reviewer selects a different representative item.

Effects:

- old and new representative ids must be recorded
- trust is not upgraded
- evidence is not verified

### mark_group_weak

Reviewer keeps the group but marks it weak.

Effects:

- warning state required
- no analysis inclusion
- future reports must not overstate this group

### reject_group

Reviewer rejects the group candidate.

Effects:

- group is excluded from later analysis consideration
- underlying items remain audit-visible
- no deletion of review history

### request_more_source

Reviewer needs better source context.

Effects:

- group remains blocked
- no dedup confirmation
- no analysis

### hold_group_for_privacy

Reviewer detects privacy or safety risk.

Effects:

- group enters privacy hold
- future gates block
- no production side effect

## Audit Requirements

Each future dedup group review action must append an audit record with:

- previous group state
- new group state
- reviewer label
- reason
- affected item ids
- representative changes
- analysis effect
- trust label effect
- no production side effect flags
- timestamp
- boundary notes

Audit records must not expose:

- `raw_author_id`
- `raw_author_name`
- `profile_url`
- `private_message`
- cookie / token / session values
- email / phone / password-like values

## Boundaries

Confirming a dedup group does not run analysis.

Confirming a dedup group does not write the Evidence Layer.

Confirming a dedup group does not generate a report.

Confirming a dedup group does not generate Sandbox fixtures or public event pages.

Split/merge actions remain review-only until a later promotion gate.

Duplicate groups are candidates, not facts.

## Safe Reviewer Copy

Use this wording in future UI:

> This confirms only a review-only duplicate group candidate. It does not run dedup, does not run analysis, does not write production evidence, and does not verify source truth.

## Unsafe Claims To Avoid

Avoid:

- dedup completed
- evidence verified
- production evidence merged
- analysis-ready
- official duplicate
- risk score updated

