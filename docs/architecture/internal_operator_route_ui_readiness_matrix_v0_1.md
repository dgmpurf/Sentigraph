# Internal Operator Route/UI Readiness Matrix v0.1

## A. Readiness Matrix

| Area | Current status | Readiness level | Implementation approved now? | Missing prerequisite | Next allowed gate |
| --- | --- | --- | --- | --- | --- |
| Route skeleton | Accepted after enabled fixture smoke | Accepted governance checkpoint | No further expansion approved | Safety test plan for future expansion | 8T-21 route/UI safety test plan docs-only |
| Disabled-mode smoke | Passed | Ready as disabled-route evidence | No runtime change approved | None for current disabled mode | Source patch or safety test plan docs |
| Enabled synthetic fixture smoke | Passed | Ready as test-only fixture evidence | No production mode approved | None for synthetic/test-only mode | Source patch or safety test plan docs |
| Auth/local-only contract | Accepted docs-only | Contract ready | No | Runtime test plan and explicit approval | Auth/runtime test plan docs if needed |
| UI contract | Accepted docs-only | Contract ready | No | Frontend safety test plan and explicit approval | UI safety test plan docs |
| Safe response schema | Existing/skeleton-safe | Adequate for current skeleton | No expansion approved | Future implementation needs targeted tests | Safe response regression plan |
| Route safety test plan | Needed | Not created | No | Dedicated test plan | 8T-21 safety test plan docs-only |
| Auth/local-only runtime | Not implemented | Not approved | No | Test plan, explicit approval, safe denial behavior | Future implementation-slice design docs only |
| Internal operator UI | Not implemented | Not approved | No | UI safety tests, browser smoke plan, explicit approval | Future implementation-slice design docs only |
| Persistent staging storage | Not implemented | Blocked | No | Storage/privacy design and explicit approval | Separate storage design gate only |
| Evidence row preview | Blocked | Blocked | No | Row redaction/privacy design and explicit approval | Separate evidence preview design gate only |
| Production import | Blocked | Blocked | No | Promotion/import governance approval | Separate production import gate only |
| Public / C-end / B-end exposure | Blocked | Blocked | No | Not a near-term direction | None |
| Collector runtime / API bridge | Blocked | Blocked | No | Not a near-term direction | None |

## B. Risk Matrix

| Risk | Current mitigation | Remaining gap | Required next gate |
| --- | --- | --- | --- |
| Privacy leak risk | Safe metadata-only contracts; forbidden display lists | No UI/runtime tests for future implementation | Route/UI safety test plan docs-only |
| Path exposure risk | Contracts forbid absolute paths and private collector roots | Future runtime must prove no path leaks | Safe response and UI regression tests |
| Raw row exposure risk | Evidence row preview remains blocked | No future row redaction design accepted | Separate evidence row preview gate |
| Raw identifier exposure risk | Raw author IDs/names/profile URL values forbidden | Future UI/runtime must enforce key/value filtering | Safety test plan before implementation |
| Secret exposure risk | Cookies/sessions/tokens/API keys forbidden | Future implementation must scan payloads and UI text | Static and runtime safety tests |
| Route accidentally public risk | Route family is internal-only and GET-only | Future UI route could accidentally expose customer surface | Route/UI exposure tests and explicit approval |
| UI action overreach risk | Active production/public actions forbidden | Future UI may turn labels into buttons if not tested | UI action safety test plan |
| Production import confusion risk | Docs distinguish labels from import approval | Future wording may imply import readiness | Copy review and browser smoke before implementation |
| Collector bridge confusion risk | Collector runtime/API bridge blocked | Future handoff language may imply direct integration | Source/docs review plus static scan |

## C. Readiness Verdict

```text
route_ui_runtime_readiness = not_approved_for_implementation_now
ready_for_safety_test_plan_docs = yes
ready_for_first_slice_design_docs = yes
ready_for_source_patch = yes, optional
ready_for_ui_implementation = no
ready_for_auth_runtime = no
ready_for_storage = no
ready_for_evidence_row_preview = no
ready_for_production_import = no
```

The route/UI contracts are ready for planning a safety test plan or a narrow implementation-slice design. They are not approval to implement UI, auth runtime, storage, evidence row preview, production import, public exposure, or collector runtime bridge.
