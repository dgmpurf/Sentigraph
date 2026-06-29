# Internal Operator UI Safe Display Matrix v0.1

## A. Safe Display Matrix

| Field / section | Display allowed? | Display level | Source category | Notes | Prohibited transformations |
| --- | --- | --- | --- | --- | --- |
| `staging_candidate_id` | Yes | Identifier label | Safe metadata | Stable safe candidate identifier. | Do not convert into production evidence ID. |
| `provider_result_id` | Yes | Identifier label | Safe metadata | Provider result metadata reference only. | Do not link to private collector paths. |
| `package_name` | Yes | Text label | Safe metadata | Package label only. | Do not expand into absolute path or export root. |
| `package_role` | Yes | Text label | Safe metadata | Role label such as synthetic/test package. | Do not imply production import. |
| `case_id_hint` | Yes | Hint label | Safe metadata | Hint only. | Do not create or link production case. |
| `validation_status` | Yes | Status badge | Safe metadata | Validation status code only. | Do not claim official verification. |
| `evidence_count` | Yes | Numeric count | Safe metadata | Count only. | Do not expose row content. |
| `source_count` | Yes | Numeric count | Safe metadata | Count only. | Do not expose source records. |
| `warning_count` | Yes | Numeric count | Safe metadata | Count only. | Do not expand into raw evidence. |
| `error_count` | Yes | Numeric count | Safe metadata | Count only. | Do not expand into raw package logs. |
| Safe coverage summary | Yes | Summary panel | Safe metadata | Coverage limitation summary. | Do not imply full-web/full-platform coverage. |
| Blockers | Yes | Code list | Safe metadata | Safe blocker codes only. | Do not include raw rows or paths. |
| Warnings | Yes | Code list | Safe metadata | Safe warning codes only. | Do not include raw comments or identifiers. |
| `allowed_actions` labels | Yes | Label list | Safe metadata | Labels only. | Do not implement as active mutation buttons in this phase. |
| `blocked_actions` labels | Yes | Label list | Safe metadata | Boundary labels only. | Do not provide bypass or action controls. |
| `safety_flags` | Yes | Boolean flag table | Safe metadata | False/true boundary flags. | Do not convert flags into runtime controls. |
| Route status | Yes | Status banner | Route metadata | Disabled/enabled synthetic fixture status only. | Do not expose env values or secrets. |
| Route disabled reason | Yes | Safe reason text | Safe error metadata | Safe reason code only. | Do not expose stack traces or config paths. |
| Synthetic mode label | Yes | Badge | Route metadata | Test-only fixture label. | Do not imply production access. |

## B. Forbidden Display Matrix

| Field / category | Display allowed? | Reason | Safe substitute if any |
| --- | --- | --- | --- |
| Raw evidence rows | No | Would expose unreviewed row content. | `evidence_count` only. |
| Raw comments | No | May expose sensitive or identifying content. | Comment count or warning code only. |
| Raw author IDs/names | No | Raw identity exposure. | None; use anonymized count only if later approved. |
| Profile URL actual values | No | Identity/path exposure. | `profile_url_present = true/false` only if later approved. |
| Cookies | No | Credential/secret exposure. | None. |
| Sessions | No | Credential/session exposure. | None. |
| Tokens | No | Secret exposure. | None. |
| Passwords | No | Secret exposure. | None. |
| API keys | No | Secret exposure. | None. |
| Browser profile paths | No | Private environment exposure. | None. |
| Absolute private paths | No | Private filesystem exposure. | Safe path status code only. |
| Private messages | No | Private content exposure. | None. |
| Evidence items file contents | No | Evidence row preview remains blocked. | Counts and safe validation status only. |
| `response_text` | No | Generated response is not approved. | None. |
| `generated_public_message` | No | Public message generation is not approved. | None. |
| `target_user_list` | No | Targeting is not approved. | None. |
| `persuasion_score` | No | Persuasion scoring is not approved. | None. |
| `truth_score` | No | Truth scoring/verification is not approved. | None. |
| `official_verified` | No | Official verification claim is not allowed. | Validation status only, with boundary wording. |
| `prediction_probability` | No | Prediction probability is not approved. | None. |
| `psychological_profile` | No | Personality profiling is not approved. | None. |
| `personality_diagnosis` | No | Personality diagnosis is not approved. | None. |

## C. UI Action Matrix

| Label / action | Allowed as displayed label? | Allowed as active button now? | Future gate required? | Notes |
| --- | --- | --- | --- | --- |
| `continue_review` | Yes | No | Yes | Label only in this phase. |
| `request_more_metadata` | Yes | No | Yes | Label only in this phase. |
| `mark_manual_review_required` | Yes | No | Yes | Label only in this phase. |
| `reject_package` | Yes | No | Yes | Label only in this phase. |
| `block_privacy_issue` | Yes | No | Yes | Label only in this phase. |
| `request_future_evidence_preview_gate` | Yes | No | Yes | Label for a future gate request only. |
| `request_future_dedup_gate` | Yes | No | Yes | Label for a future gate request only. |
| `request_future_promotion_gate` | Yes | No | Yes | Label for a future gate request only. |
| `approve_production_evidence` | Boundary label only | No | Yes | Forbidden as active action. |
| `create_production_case` | Boundary label only | No | Yes | Forbidden as active action. |
| `start_analysis_run` | Boundary label only | No | Yes | Forbidden as active action. |
| `generate_report` | Boundary label only | No | Yes | Forbidden as active action. |
| `generate_public_event` | Boundary label only | No | Yes | Forbidden as active action. |
| `generate_public_response` | Boundary label only | No | Yes | Forbidden as active action. |
| `publish` | Boundary label only | No | Yes | Forbidden as active action. |
| `send` | Boundary label only | No | Yes | Forbidden as active action. |
| `post` | Boundary label only | No | Yes | Forbidden as active action. |
| `execute` | Boundary label only | No | Yes | Forbidden as active action. |
| `target_individuals` | Boundary label only | No | Yes | Forbidden as active action. |
| `download_package` | No | No | Yes | No package download UI. |
| `export_data` | No | No | Yes | No data export UI. |
| `open_raw_file` | No | No | Yes | No raw file opening. |
| `refresh_live_collector` | No | No | Yes | No live collector runtime. |
| `fetch_url` | No | No | Yes | No URL fetching. |
| `scrape_page` | No | No | Yes | No scraping. |

## D. Route / UI Exposure Matrix

| Surface | Allowed now? | Future docs-only candidate? | Implementation allowed now? | Notes |
| --- | --- | --- | --- | --- |
| Internal operator UI | No | Yes | No | Contract only; implementation requires later approval. |
| Local developer UI | No | Yes | No | Contract only; local-only/auth boundary required first. |
| Security reviewer UI | No | Yes | No | Contract only; safe metadata only if ever approved. |
| Customer dashboard | No | No | No | Internal route must not become customer-facing. |
| C-end public UI | No | No | No | No public/C-end exposure. |
| B-end customer UI | No | No | No | No B-end/customer exposure. |
| Provider callback UI/API | No | No | No | No provider callback or direct provider route. |
| Private collector callback | No | No | No | No collector callback, no HTTP/API bridge. |

## E. Stop Rule

Any request to implement UI, wire frontend to route, add active actions, add storage, preview evidence rows, expose public/customer route, or connect collector runtime must stop and require separate explicit user approval.

This display matrix is a contract for future safety review, not frontend implementation approval.
