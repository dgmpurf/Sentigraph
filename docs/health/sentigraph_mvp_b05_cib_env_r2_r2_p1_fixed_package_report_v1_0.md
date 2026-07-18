# Sentigraph MVP-B05-CIB-ENV-R2-R2-P1A Environment Broadcast Static Hardening Report v1.0

## 1. Decision

```text
Decision = ready
privacy_issue_stop = no
milestone = MVP-B05-CIB-ENV-R2-R2-P1A
status = candidate_completed_pending_independent_ChatGPT_acceptance
classification = Baseline v1.9 fixed Prompt 2
hardening_scope = fixed Windows environment-change broadcast semantics only
P1_reclassified = no
helper_execution = 0
broadcast_execution = 0
protected_access = 0
runtime_authority_created = no
```

P1A is a forward static-safety hardening of the independently accepted P1
package. It does not execute the fixed helper, repair the environment, capture
configuration identity, or authorize P2.

## 2. Governance Binding

```text
repository = dgmpurf/Sentigraph
branch = main
starting_commit = ddde6d6266e460c43d452582e70b15090bcf9824
Baseline_v1_9_document_blob = c32e5d8574d57cb6112b2e0b50144baeb6a23cc3
approval_SHA256 = 4e43a4f9d01e19f319642cce94681ebcce68ce44ea04576bec2619f9bf1ef325

consumed engineering/fixed/conditional/risk after Goal activation = 2/2/0/0
remaining fixed/conditional/risk = 0/4/3
```

The initial CIB-P2, ENV-R1, ENV-R2, and ENV-R2-R1 outcomes remain distinct,
consumed, nonreusable, and unreclassified. P1 remains completed and independently
accepted at `ddde6d6266e460c43d452582e70b15090bcf9824`.

## 3. Previous Accepted P1 Identities

```text
fixed helper SHA-256 = 73a067c2a6dfef3de6a206f121300cfa128e611d3d4386dceb2ada477cc8ed5f
static auditor SHA-256 = ee855827f3885d89896965c843988adf0d475c2c3cac183182f4260848bfae1a
fixtures SHA-256 = 8324157052fe09a5daf02260b505f9cc7b72ccc268ff58233866a2f0433ea8c4
manifest SHA-256 = 919f068ab34e1eec14f3037ea6a18051a9f1e32ba415b07cd3fe1ed7945ac70c
report SHA-256 = e05864f9dc65c35b4b758a2adde1409196a716eb7771f04067a18cf258365615
```

## 4. P1A Replacement Identities

```text
fixed helper SHA-256 = 4ed37dc12515569f2b774717358106d46cc5d6e9a0f28df05857b3c2d2e996e8
fixed helper bytes = 13787

static auditor SHA-256 = 5a6290e8abcc73bd082c852dcf7d25a6ffdc0d7fbd4fcd06538a1f43909b43e0
static auditor bytes = 26547

fixtures SHA-256 = 1e2a6682f2f68291d3a4b5ffc0019f43c72f44160ca4cf89dc59c7ee0c4af884
fixtures bytes = 32473

manifest SHA-256 = a81ddf6ce9cf93e84e67fe8ee7df018ad30b68652c9d397ae11c3ea38547745d
manifest bytes = 3064

report SHA-256 and bytes =
  externally bound by the final exact Codex Prompt to avoid self-reference
```

All files remain UTF-8, no BOM, LF-only.

## 5. Fixed Helper Broadcast Contract

The hardened helper remains `.py.txt`, nonimportable by normal module
resolution, uncompiled, uncopied, and unexecuted in P1A.

After the exact three `REG_SZ` readbacks pass, it performs one bounded Windows
environment-change notification before any success output:

```text
HWND_BROADCAST = 0xFFFF
WM_SETTINGCHANGE = 0x001A
SMTO_ABORTIFHUNG = 0x0002
ENVIRONMENT_BROADCAST_LPARAM = Environment
BROADCAST_TIMEOUT_MS = 2000 per window

binding =
  ctypes.WinDLL("user32", use_last_error=True)
  SendMessageTimeoutW with exact pointer-sized argtypes/restype

order =
  three exact readbacks
  -> one broadcast attempt
  -> broadcast PASS
  -> three variable PASS labels
  -> final repair PASS
```

The broadcast uses a pointer to the exact wide string `Environment`, clears
last error before the call, and requires a nonzero return. Failure after registry
repair emits only the frozen bounded broadcast-blocked status and performs no
retry, second broadcast, rollback write, or additional registry read.

No last error, message result, window count, handle, path, value, ID, or registry
content is emitted.

## 6. Auditor Self-test Matrix

The existing stdout and reparse positive/negative fixtures remain.

P1A adds:

```text
broadcast_positive_exact_bounded_after_readbacks = PASS
broadcast_negative_missing_broadcast = PASS
broadcast_negative_wrong_message = PASS
broadcast_negative_wrong_lparam = PASS
broadcast_negative_before_readback = PASS
broadcast_negative_dynamic_lparam = PASS
broadcast_negative_non_timeout_send = PASS
broadcast_negative_ignored_return = PASS
broadcast_negative_retry_or_second_broadcast = PASS

AUDITOR_SELF_TEST = PASS
```

The auditor validates semantic constants, exact WinDLL and
`SendMessageTimeoutW` binding, pointer-sized types, one-call limit, readback
ordering, nonzero-return enforcement, bounded output ordering, and the dedicated
broadcast-failure status.

## 7. Fixed-helper Static Audit

One static audit must report:

```text
HELPER_AUDIT_SOURCE_PARSE = PASS
HELPER_AUDIT_CONSTANTS = PASS
HELPER_AUDIT_IMPORTS = PASS
HELPER_AUDIT_FORBIDDEN_CALLS = PASS
HELPER_AUDIT_STDOUT = PASS
HELPER_AUDIT_REPARSE = PASS
HELPER_AUDIT_REGISTRY = PASS
HELPER_AUDIT_BROADCAST = PASS
FIXED_HELPER_STATIC_AUDIT = PASS
```

The auditor parses the fixed helper with `ast`. It does not import, compile,
copy, or execute it.

## 8. P1A Zero-action Ledger

```text
fixed helper imports/compiles/copies/executions = 0/0/0/0
broadcast executions = 0
Provider Result searches/opens/reads/hashes = 0/0/0/0
package searches/safe metadata reads = 0/0
environment reads/writes = 0/0
registry reads/writes = 0/0
configuration capture/hash/salt/canonical object/binding/receipt = 0/0/0/0/0/0
artifact access/hash = 0/0
application imports = 0
endpoint/B05 GET = 0/0
provider/collector/network/LLM/browser = 0/0/0/0/0
database/persistence = 0/0
product code/test/config/route/API/frontend changes = 0/0/0/0/0/0
Project Source/tag/release changes = 0/0/0
```

## 9. Authorization Boundary

```text
P1A independently accepted = no

ENV-R2-R2-P2 =
  selected / eligible / authorized / executed =
  yes / no pending P1A acceptance / no / no

CIB-P2-R1 =
  selected / eligible / authorized / executed =
  yes / no / no / no

B05-P5 =
  selected / eligible / authorized / executed =
  no / no / no / no
```

P1A completion does not authorize helper execution, local discovery,
environment or registry access, broadcast execution, configuration capture,
artifact access, application import, endpoint calls, persistence, production,
public, export, or delivery work.

## 10. Next Boundary

```text
next_boundary = independent ChatGPT acceptance only
```

After independent acceptance, P2 still requires a separate fresh exact risk
approval and fresh Goal bound to all five committed replacement identities.
