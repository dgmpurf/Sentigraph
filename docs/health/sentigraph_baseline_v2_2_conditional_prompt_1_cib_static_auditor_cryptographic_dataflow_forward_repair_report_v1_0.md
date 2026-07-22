# Sentigraph Baseline v2.2 Conditional Prompt 1 CIB Static-auditor Cryptographic-dataflow Forward Repair Report v1.0

## 1. Status and scope

status = candidate_completed_pending_independent_ChatGPT_acceptance

Decision = candidate_completed_pending_independent_ChatGPT_acceptance

runtime classification = ready_cib_static_auditor_cryptographic_dataflow_repaired_pending_independent_acceptance

milestone = SENTIGRAPH-BASELINE-V2-2-CONDITIONAL-PROMPT-1-CIB-STATIC-AUDITOR-CRYPTOGRAPHIC-DATAFLOW-FORWARD-REPAIR

This Conditional Prompt 1 result forward-repairs the committed file-based static auditor only. It performs no actual CIB capture, accesses no process-environment value, generates no real salt, creates no real canonical object, computes no configuration-derived binding, creates no receipt, and grants no runtime authority.

Conditional Prompt 1 forward repair = candidate completed pending independent acceptance

effective file-based transport hardening = retained

effective cryptographic dataflow conformance = candidate pending independent acceptance

## 2. Exact approval and Goal lifecycle

Exact approval received = yes

Compact approval phrase SHA-256 = 8292589bde2c5ef49bd104e65bdf73e29569b1b44147a78c82235206bc176591

Conditional Repair Contract V1 SHA-256 = 61a875457a9927900339d559b06316da052b69330ebbb66bff58417372eddb19

Before verified fresh Goal activation, approval consumed / reusable = no / yes

After verified fresh Goal activation, approval consumed / reusable = yes / no

Goal title = Sentigraph Baseline v2.2 CIB Auditor Cryptographic Dataflow Repair

Goal activated = yes

Goal reusable = no

Conditional Prompt 1 consumed = yes

## 3. Starting repository and immutable identities

repository / branch = dgmpurf/Sentigraph / main

starting HEAD = 7161fa1f74e03dc4210831bcc70dc8a2aca13c1c

starting message = Harden CIB capture static audit transport

starting worktree = clean

Baseline v2.2 overlay blob / SHA-256 / bytes = 4a828454c4f99bf624c7ad1330843e69eedde3c7 / 83fed1e8a7e4aa854a95d0dc93f916611e0fd12d79d8a3dc78bf250127a98fad / 16153

historical CIB-P1 contract blob = 939190f8794468b0485051e9ab6801a484129cb8

current B05 service blob = f0c4a8768060a840ea1921aeba47a97f2e41f9e3

starting auditor SHA-256 / blob / bytes = e9820e2e4729d1ab0387bba7c67a98532b89d40acaf3dc3b11c96f8719b01056 / 4d61a63b03bd04c3de1044cffb82018b60acd6b4 / 39587

Fixed Prompt 1 report SHA-256 / blob / bytes = 2927437f030925ea732668e5259827866a97c2e60fa4d95ccc6baae64ddc275e / f468df1341117865c1cccb20c02cad0e1a21e8ae / 11512

committed source reads / reopens = 5 / 0

product imports or executions = 0

## 4. Preserved Risk Prompt 1 blocked history

Risk Prompt 1 Decision = blocked

Risk Prompt 1 runtime classification = blocked_pre_capture_runner_static_audit

Risk Prompt 1 approval / Goal reusable = no / no

Risk Prompt 1 reclassified = no

Risk Prompt 1 remains consumed and nonreusable. This repair neither reruns nor restores that authority.

## 5. Preserved Fixed Prompt 1 needs-fix history

Fixed Prompt 1 independent Decision = needs_fix

Fixed Prompt 1 independent classification = needs_fix_static_auditor_missing_salt_and_combined_digest_dataflow_binding

Fixed Prompt 1 approval / Goal reusable = no / no

Fixed Prompt 1 reclassified = no

Its effective file-based transport hardening is retained. Its independent needs-fix history is not replaced by this forward-repair candidate.

## 6. Independent defect finding

The starting auditor established the presence and count of the salt-generation and canonical SHA-256 calls but did not prove that their returned values flowed through the required direct assignments into the canonical object and safe receipt. A discarded real call plus a forged constant therefore satisfied the old call-count checks.

defect class = missing salt-to-salt_hex and canonical-hash-to-receipt AST identity binding

genuine RED reproduced = yes

## 7. Exact cryptographic dataflow repair

The existing EXACT_ONE_SALT_GENERATION check now proves one direct ordinary `salt` assignment from the sole 32-byte generation call, one direct `salt_hex` assignment from the sole zero-argument `salt.hex()` call, exact Store and Load counts, and identity-equal use of the same `salt_hex` name in the canonical and receipt dict-literal fields.

salt dataflow assignment binding = pass

salt to salt_hex binding = pass

canonical and receipt salt_hex identity = pass

salt Store / Load counts = 1 / 1

salt_hex Store / Load counts = 1 / 2

The existing EXACT_ONE_COMBINED_SHA256 check now proves the sole `canonical_bytes` argument, the direct `.hexdigest()` parent chain, the direct ordinary `combined_binding_sha256` assignment, exact Store and Load counts, and identity-equal receipt use.

combined-hash direct assignment binding = pass

receipt combined-binding identity = pass

canonical_bytes Store / Load counts = 1 / 1

combined-binding Store / Load counts = 1 / 1

The current-constant check also requires `canonical_object` and `safe_receipt` to have one dict-literal Store and one exact compact-serialization Load, preventing aliasing, subscript replacement, or mutating-method use.

canonical_object immutable single-use = pass

safe_receipt immutable single-use = pass

repaired auditor candidate SHA-256 / bytes = aaeac66a098045c02d9a9aa8f57382548f92231114e6a569b89c72c707bd8ecb / 52273

output schemas changed = no

CHECK_NAMES changed = no

## 8. Genuine pre-repair RED

pre-repair negative audit executions / retries = 2 / 0

pre-repair negative runner reads / reopens = 2 / 0

pre-repair false accepts = 2

forged-salt source bytes / SHA-256 = 4735 / d192c65d7b09d38392a24a5c3354f74d63bbddf57c482279aca2206d6f5d59b5

forged-salt pre-repair status / checks passed / failed = pass / 16 / 0

forged-hash source bytes / SHA-256 = 4757 / 7bfaf6e501f9294db4b244a228eac2bf08f18e6ecd4f5072fd66020886b54c12

forged-hash pre-repair status / checks passed / failed = pass / 16 / 0

These hashes identify fixed-public source text only. They are not configuration-derived hashes.

## 9. Expanded 16-fixture self-test

self-test process executions / retries = 1 / 0

self-test fixtures passed / total = 16 / 16

prior 14 fixtures retained = yes

new fixtures = exactly 2

fixture 15, unused real salt with forged salt_hex = pass; intended failure EXACT_ONE_SALT_GENERATION observed

fixture 16, unused real hash with forged combined digest = pass; intended failure EXACT_ONE_COMBINED_SHA256 observed

self-test schema / version / status = sentigraph_cib_capture_static_auditor_self_test_result_v0_1 / 0.1 / pass

self-test environment access / runner execution = false / false

## 10. Public post-repair regression matrix

post-repair external audit executions / retries = 3 / 0

post-repair external runner reads / reopens = 3 / 0

forged-salt post-repair status / checks passed / failed = fail / 15 / 1

forged-hash post-repair status / checks passed / failed = fail / 15 / 1

valid source bytes / SHA-256 = 4730 / d53db8112563c160544fa6397211169766917bc7d02e964a0e9638d6d08d5f8f

valid post-repair status / checks passed / failed = pass / 16 / 0

post-repair forged runners rejected = 2 / 2

post-repair valid runners accepted = 1 / 1

total audited-runner executions = 0

total environment access = 0

public regression matrix = pass

## 11. Baseline v2.2 accounting

before Conditional Prompt 1 activation, engineering / fixed / conditional / risk = 2 / 1 / 0 / 1

after Conditional Prompt 1 activation, engineering / fixed / conditional / risk = 3 / 1 / 1 / 1

remaining fixed / conditional / risk = 0 / 0 / 2

Conditional Prompt 1 consumed = yes

Risk Prompt 2 = reserved / unconsumed / unauthorized

Risk Prompt 3 = reserved / unconsumed / unauthorized

Neither remaining Risk reservation is selected by this report.

## 12. Zero-action and privacy ledger

actual capture runner creation / execution = 0 / 0

actual process-environment source sessions / reads = 0 / 0

other-name reads / environment enumeration = 0 / 0

environment writes / deletes = 0 / 0

HKCU / HKLM reads or writes = 0 / 0

real salt generations = 0

real canonical objects = 0

real configuration-derived SHA-256 computations = 0

real per-variable hashes = 0

real safe CIB receipt creations = 0

artifact / package / Provider Result access = 0 / 0 / 0

gate read / enable / mutation = 0 / 0 / 0

application import / app factory / client = 0 / 0 / 0

route / endpoint / B05 GET = 0 / 0 / 0

database / persistence = 0 / 0

provider / collector / network / browser / LLM = 0 / 0 / 0 / 0 / 0

production / public export / delivery = 0 / 0 / 0

Project Source generation / replacement = 0 / 0

Public static source parsing and source-integrity SHA-256 values do not represent real salt, binding, or configuration-derived operations.

## 13. Current authorization boundary

actual CIB capture = not performed

new capture authority = not created

B05 GET eligibility or authority = not created

artifact, package, gate, application, endpoint and B05 GET access remain unauthorized. No remaining Risk route is selected.

next engineering route = not selected by this report

## 14. Git finalization

Ready-only finalization requires the exact auditor modification and this one report, cached diff validation, commit message `Repair CIB auditor cryptographic dataflow checks`, an ordinary push of current `main` to `origin/main`, local/remote alignment, and a clean final worktree.

The terminal receipt records the resulting commit and committed blob identities. This report does not self-assert its own final commit identity.

## 15. Claims not established

This candidate does not establish:

- a successful actual CIB capture;
- a real salt, canonical object, combined binding, or safe receipt;
- confidentiality or correctness of any configuration value;
- artifact or Provider Result identity, existence, safety, or accessibility;
- gate enablement or application readiness;
- authority or eligibility for a governed B05 GET;
- persistence, production, export, public, or delivery readiness;
- selection or authorization of a next engineering route;
- reuse or reclassification of Risk Prompt 1 or Fixed Prompt 1.

The required next action is to stop after ready-only Git finalization and return the repaired auditor plus committed forward-repair report for independent ChatGPT review.
