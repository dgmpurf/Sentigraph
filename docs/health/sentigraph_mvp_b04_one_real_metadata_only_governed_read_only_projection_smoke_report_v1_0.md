# Sentigraph MVP-B04 One Real Metadata-only Governed Read-only Projection Smoke Report v1.0

## Decision and privacy status

- Decision: `ready`.
- Privacy issue stop: `no`.
- The smoke used one exact metadata-only Provider Result and retained only bounded counters, status labels, and lowercase hashes.
- No source payload, package content, complete endpoint response, evidence/source/log row, credential, secret, traceback, socket identity, handle, address, runner source, private environment value, or external absolute path is present in this report.
- Public export and delivery remain disabled.

## Approval and Goal lineage

- Goal requested: `MVP-B04-R3-R3 Type-preserving Socket Guard Risk Recovery and Final Real Projection Smoke`.
- Goal activation verified: `yes`.
- Goal completion gate: `ready`, subject only to the ready-only report commit and push.
- R3-R3 approval SHA-256 verified: `c02b59d93cb6dbdbc69d02fe3cec130e518952b2f30af9f2694f158416867855`.
- Historical R3, R3-R1, and R3-R2 remain distinct, consumed, blocked, and nonreusable.
- R3-R3 approval reusable: `no`.
- R3-R3 Goal reusable: `no`.

### Historical R3

R3 stopped before the protected action because its audit treated the passive
`uvicorn_server_processes` counter name as active execution evidence. That was
an AST-audit false positive. Runner execution, application import, artifact
access, projection GET, and repository changes were all zero.

### Historical R3-R1

R3-R1 made one application-import attempt, completed zero imports, and stopped
with `ModuleNotFoundError` because the external runner did not place the backend
root at `sys.path[0]`. Artifact access, projection GET, and repository changes
were zero.

### Historical R3-R2

R3-R2 completed one application import and one direct artifact open/read, then
entered an ambiguous protected state after one projection GET attempt. Its
runner replaced `socket.socket` with a function after event-loop construction,
breaking socket type semantics during a Windows Proactor callback. GET
completion and B01/B03 call counts were therefore unknown, and no safe receipt
existed. This was a Class B post-protected runner-instrumentation defect, not a
Sentigraph product defect. Repository changes were zero.

### R3-R3 recovery

R3-R3 preserved `socket.socket`, `socket.SocketType`, and all built-in socket
class methods exactly. It created the single event loop after the successful
application import and before installing the process-lifetime audit hook and
higher-level network guards. It captured only the preexisting loop-internal
socket objects needed to distinguish loop wakeup activity from external
network activity.

## Baseline v1.6 accounting

| Accounting point | Consumed engineering/fixed/conditional/risk | Remaining fixed/conditional/risk |
| --- | --- | --- |
| Before R3-R3 activation | `3/1/2/0` | `1/2/2` |
| Final after R3-R3 activation | `4/1/2/1` | `1/2/1` |

Arithmetic check: this fresh Goal added exactly one engineering accounting
event and consumed exactly one risk prompt. Fixed and conditional consumption
did not change; remaining risk decreased from two to one.

## Repository and frozen identities

- Repository identity: `dgmpurf/Sentigraph`.
- Branch: `main`.
- Starting HEAD: `96e318d9051670e3c66280753d11bfb6dbd32cef`.
- Origin alignment before execution: `0/0`; HEAD equaled `origin/main`.
- Tracked and nonignored worktree before execution: clean.
- B01 bridge blob: `ef36b4370495b7f1e5c9c5c433d5b38c5cf9aa6d`.
- B03 projection-service blob: `534bdf02e211134b52b2e7714d01a0dd615210b4`.
- B03 route blob: `fefea779e7a401122bd20d446ac711cd742ea466`.
- FastAPI application blob: `bc9927f381edae55f4f46e676412eb262322d5a0`.
- Accepted B02 report blob: `82236d1329005ef794cfdb29e4c5d1d0a02f86f1`.
- Accepted B03 report blob: `fc0f8510af1f597e17d9cab13d22f0207cab35f7`.
- The target B04 report was absent at preflight, prior blocked attempts had no
  repository changes, MVP-B04 remained incomplete, and MVP-B04-D1 had not run.

## Runner and static AST identity

- Runner SHA-256: `1942214defdbd74e767fd95049e807c12efc76451f1d24ad2eca900a5dc94b94`.
- Runner UTF-8 readback count: `1`.
- Pre-protected validation attempts: `2`.
- Pre-protected correction: the auditor replaced a quote-sensitive UTF-8 check
  and selected the environment-binding assignment after guard installation;
  the runner was not edited.
- AST parser: pass.
- Import-alias resolution: pass.
- Active `ast.Call` target resolution: pass.
- Raw-source substring matching used as execution evidence: no.
- Passive identifiers used as execution evidence: no.
- `socket.socket` or `socket.SocketType` assignment/replacement found: no.
- Built-in socket class-method mutation found: no.
- Active Uvicorn imports/calls: zero.
- Active forbidden calls: zero.
- AST audit outcome: pass.
- Application-package and application-main specs were found through two
  explicit `PathFinder` resolutions and matched the expected backend surface.
- Backend root was at `sys.path[0]`, and `app` plus `app.main` were absent from
  `sys.modules` before the one application import.
- UTF-8 transport was explicit; PowerShell default decoding was not used.
- Collector-root SHA-256 `364783f26b06dbd849c2ed9138a1289754d20b9a4b3135a2a6d43fe1382d355e`
  matched, and export/results locations were directly derived without external
  collector directory discovery.

## One-time application and event-loop ledger

| Operation | Result |
| --- | --- |
| Runner executions | `1` |
| Application import attempts/completed/retries | `1/1/0` |
| Event-loop creations | `1` |
| `run_until_complete` calls | `1` |
| `asyncio.run` calls | `0` |
| Event-loop close attempts/completed | `1/1` |
| Preexisting loop-internal socket identities captured | `yes` |
| Preexisting loop-internal socket count | `2` |

The event loop was created only after the application import. The type-
preserving network instrumentation was installed only after the loop had
created its internal self-pipe objects.

## Socket type-identity and network-guard proof

- `socket.socket` identity preserved before the protected action: yes.
- `socket.SocketType` identity preserved before the protected action: yes.
- Socket class/type and `isinstance` semantics preserved: yes.
- Direct simulated audit-hook self-test: pass.
- Simulated new-socket event rejected: yes.
- Simulated address-resolution event rejected: yes.
- Simulated captured loop-internal send event allowed: yes.
- Real socket actions during the self-test: zero.
- Audit hooks installed after loop creation: `1`.
- Higher-level network guards installed: yes.
- New non-loop socket creation attempts: `0`.
- External connect/bind/listen/accept/address-resolution attempts: `0`.
- Event-loop internal socket activity, counted separately: `0`.
- `socket.socket` identity preserved after cleanup: yes.
- `socket.SocketType` identity preserved after cleanup: yes.

## Exact artifact identity ledger

- Exact filename: `provider_result_helldivers2-psn-demo_20260614_055754.json`.
- Expected SHA-256: `6297f09939b205877940d1de964f9d7a0a6dec1f5817d7a6520949357cf8e553`.
- Actual SHA-256: `6297f09939b205877940d1de964f9d7a0a6dec1f5817d7a6520949357cf8e553`.
- Artifact identity match: yes.
- Direct identity opens/reads/reopens: `1/1/0`.
- Direct seeks: `0`.
- Direct SHA-256 computations: `1`.
- Direct JSON parses: `0`.

The bytes used for the direct identity check were discarded immediately after
the one hash computation. There was no replacement selection, discovery,
fallback, retry, or second direct open.

## Projection acceptance

- Projection endpoint: `/api/v1/internal/staging/review-only/local-exchange/projections/provider_result_helldivers2-psn-demo_20260614_055754.json`.
- Projection GET attempts/completed: `1/1`.
- Automatic retries: `0`.
- Second GETs: `0`.
- Candidate/alternate endpoint calls: `0/0`.
- HTTP status: `200`.
- B01 bridge calls: `1`.
- B03 projection-builder calls: `1`.
- Projection schema: `sentigraph_local_exchange_review_only_candidate_projection_v0_1`.
- Projection version: `0.1`.
- Exact top-level field count: `52`.
- Response-key order exactly matched the frozen `PROJECTION_FIELDS` tuple: yes.
- Projection status: `ready_for_human_review`.
- Projection error code: null.
- Response canonical SHA-256: `04e8e9514ac2e80b5c37df4bb95cd0e136622bd9a95c518709126e5059be15f9`.

The accepted bounded statuses were:

- reader/adapter/provider/package: `metadata_ready` / `adapted` /
  `accepted_metadata_only` / `accepted_metadata_only`;
- candidate/review/promotion/staging: `1` / `ready_for_human_review` /
  `promotion_required` / `ready_for_human_review`;
- candidate persistence: `in_memory_only`;
- blockers: empty;
- metadata-only, review-only, human-review-required, and
  no-automatic-trust-upgrade flags: true;
- every persistence, review-write, Evidence Layer write, production-object,
  frontend, public-output, export-delivery, path-exposure, metadata-exposure,
  trust-approval, production-ready, promotion-completed, and mutable-authority
  flag: false.

No persisted identifier, reservation identifier, candidate identity digest,
database-column value, exact-target audit value, source payload, package
content, or absolute path was returned in the accepted projection contract.

## Metadata-access ledger

| Read class | Opens/reads |
| --- | --- |
| Provider Result request-path metadata | `1/1` |
| Safe package metadata | `5/5` |
| Evidence/source/log rows | `0` |

The five package metadata basenames were exactly `manifest.json`,
`validation_report.json`, `validation_report.md`, `coverage_note.md`, and
`README.md`. External collector directory enumerations were zero.

## No-side-effect ledger

| Guarded class | Attempts or effects |
| --- | --- |
| Request-path writes | `0` |
| Persistence/database connections or mutations | `0` |
| Review-decision writes | `0` |
| Evidence Layer writes | `0` |
| Production objects | `0` |
| External network/socket/HTTP calls | `0` |
| Post-import external-process attempts/launches | `0/0` |
| Uvicorn server processes | `0` |
| Provider/collector/browser/LLM calls | `0` |

The loop-internal socket activity count is deliberately not included in the
external-network row; it remained zero in this run.

## Restoration and temporary-artifact ledger

- Higher-level guards restored exactly: yes.
- Six Sentigraph environment entries restored to their exact prior
  present/absent states and values: yes.
- `PYTHONDONTWRITEBYTECODE` restored exactly: yes.
- `sys.dont_write_bytecode` restored exactly: yes.
- Original `sys.path` list restored exactly: yes.
- Single event loop closed: yes.
- Runner created/read/executed/deleted: `1/1/1/1`.
- Safe result created/read/deleted: `1/1/1`.
- Safe result validation: pass.
- Repository changes from the protected execution: zero.

## Product interpretation

This smoke demonstrates that the frozen B01 bridge and B03 projection builder
can consume the exact approved real metadata-only Provider Result through the
existing governed in-process read-only route and return the exact bounded
52-field human-review projection. It does not create, approve, persist,
promote, publish, export, or deliver an Evidence Item, Case, Analysis Run,
Analysis Result, review decision, or other production object. It does not
grant trust or mutable authority.

This result validates the existing frozen product surface for this one exact
input. It does not authorize another artifact access, application import,
event-loop creation, endpoint call, route change, code change, test run, or
MVP-B04-D1 action.

## Changed-file boundary and next boundary

- Changed files: exactly this health report.
- Unexpected files: none.
- Project Source changed: no.
- Tag: none.
- Release: none.
- MVP-B04-D1 executed: no.
- Next boundary: independent ChatGPT acceptance.
- Do not access the artifact, import the application, create an event loop, or
  call either endpoint again.
- Do not begin D1 or another milestone automatically.
