# Sentigraph Post-Baseline-v2.0 Risk-Prompt-2 Stdin-Transport Failure and Governed Runtime Baseline v2.1

## 1. Title and authority posture

This document is a docs-only governance rebaseline. It becomes effective only after it is committed, pushed, and independently accepted by ChatGPT. It is not runtime authority and does not grant permission to access artifacts, HKCU, the process environment, CIB, gates, application routes, persistence, production, export, or delivery.

This document records historical outcomes, closes Baseline v2.0 for future Prompt accounting, and establishes the planning structure for Baseline v2.1. It performs no engineering or runtime action.

## 2. Immutable authority anchors

```text
starting repository HEAD = be89a354b4e1fa76ccb159eda08a2762d619e029
starting HEAD message = Migrate B05 registry to accepted Provider Result
Baseline v2.0 establishment commit = 5c52a824441959a7fd39c059639d46b779658aa8
Risk Prompt 2 approval SHA-256 = 2fed799faa859f0b94ff8c64c9e7cbf1a3a44a632f7fe362e40c0fe53201b7bd
Baseline v2.1 docs-only approval SHA-256 = 166f80e8f1f8e5dcb83fff9ea56b33024d70c6374488187841cdbb69d187d785
```

The approval phrases themselves are intentionally excluded. These anchors do not confer runtime authority.

## 3. Baseline v2.0 closure

Baseline v2.0 is closed for all future Prompt accounting.

```text
Baseline v2.0 final engineering / fixed / conditional / risk = 6 / 2 / 3 / 1
Baseline v2.0 remaining fixed / conditional / risk = 0 / 0 / 1
```

The unused remaining Risk capacity is historical only. It is not transferred, reset, reused, merged, carried forward, erased, or reclassified as Baseline v2.1 capacity. All approvals, Goals, counters, executions, and terminal receipts retain their original historical identity.

## 4. Distinct preserved terminal history

The following outcomes remain separate and are preserved without reclassification.

### 4.1 Conditional Prompt 2

```text
Decision = blocked
classification = blocked_controller_static_audit_failure
direct scope conclusion = configuration state not established
```

### 4.2 Conditional Prompt 3

```text
Decision = ready
classification = ready_bounded_configuration_prerequisite_classification_one_or_more_missing
direct conclusion = all three approved entries were absent from that Goal's inherited process environment
```

### 4.3 Fixed Prompt 2

```text
Decision = blocked
classification = authoritative_value_derivation_blocked
direct conclusion = all three exact HKCU names were missing and no authorized exact local-path authority existed
artifact opens = 0
HKCU writes = 0
```

### 4.4 Risk Prompt 2

```text
Decision = blocked
classification = execution_integrity_blocked
direct conclusion = the one formal controller execution received empty stdin because the input transport closed before the protected payload was delivered
controller executions = 1
artifact opens = 0
HKCU reads / writes = 0 / 0
repository changes = 0
```

Risk Prompt 2 did not establish an artifact, path, Registry, Sentigraph application, or contract failure. Its terminal result is solely an execution-integrity stdin-transport failure.

## 5. Baseline v2.1 accounting

```text
Baseline v2.1 budget fixed / conditional / risk = 1 / 1 / 3
Baseline v2.1 starting engineering / fixed / conditional / risk = 0 / 0 / 0 / 0
Baseline v2.1 remaining fixed / conditional / risk = 1 / 1 / 3
```

This accounting begins only after this document is committed, pushed, and independently accepted. This docs-only establishment Goal does not consume a Baseline v2.1 Fixed, Conditional, or Risk reservation.

Budget reservation is planning capacity only. Budget reservation is not runtime authority, is not approval, and is not permission to access protected resources. Availability of a reservation does not select a route, authorize a Goal, or authorize execution.

## 6. Baseline v2.1 reservations

The reservations are exactly:

| Reservation | Reserved scope |
| --- | --- |
| Fixed Prompt 1 | Exact-path three-variable HKCU repair with one pre-Goal fixed-public sentinel stdin transport probe and one formal protected controller execution |
| Conditional Prompt 1 | Post-full-Codex-application-restart three-variable inherited-process configuration diagnostic |
| Risk Prompt 1 | CIB prerequisite diagnostic or CIB capture |
| Risk Prompt 2 | Governed B05 GET smoke |
| Risk Prompt 3 | Post-protected recovery reserve |

HKCU repair, process-inheritance verification, CIB action, and B05 GET smoke must not be merged into one Prompt merely to conserve accounting.

## 7. Goal, chat, and process lifecycle model

The lifecycle identities are distinct:

```text
Goal != Codex task or chat
Goal != Codex application or Windows process
Codex task or chat != Codex application or Windows process
```

A terminal blocked, failed, or completed Goal preserves its terminal receipt, approval consumption, and accounting consumption. Clearing the Goal slot does not make the Goal or its approval reusable.

A user manual Goal clear:

- empties the current active Goal slot;
- does not delete history;
- does not reverse approval consumption;
- does not reset counters;
- does not reclassify a terminal result;
- does not establish a fresh Codex application or Windows process;
- does not prove process-environment reinheritance.

A same-chat fresh Goal is allowed only when all of the following hold:

- the prior Goal is terminal;
- the user has manually cleared it when necessary;
- `get_goal = null`;
- no prior executor remains active;
- a fresh exact approval authorizes the new Goal;
- the old approval, Goal, controller, envelope, counters, and execution state are not reused.

A fresh task or chat is mandatory only when the exact approval requires it, context separation cannot otherwise be mechanically proved, or process-inheritance or stale-process concerns require a new process or task boundary. A fresh chat alone is not proof of a fresh Windows or Codex application process.

## 8. Same-Goal scheduler-nudge scope clarification

Any rule prohibiting Clear Goal during a manual scheduler nudge applies only to continuation of the same still-live Goal. It does not prohibit clearing a terminal Goal, preserving its history unchanged, and creating an independently approved fresh Goal in the same chat after `get_goal = null` and prior-executor inactivity are established.

## 9. Protected one-shot stdin transport rule

For any future one-shot protected controller input, the complete protected payload must be delivered in one noninteractive transfer. Acceptable design examples include `subprocess.run(..., input=complete_payload, ...)` and `Popen(...).communicate(input=complete_payload)`.

The implementation must not:

- start the protected child and later attempt an interactive stdin feed;
- depend on keeping an interactive terminal session open;
- send the protected payload in multiple phases;
- repeat the formal execution after a transport failure without fresh authority.

The formal protected controller execution remains exactly one unless a future exact approval explicitly states otherwise.

## 10. Mandatory public sentinel transport probe

Before Goal activation for a future protected stdin execution, one public sentinel transport probe is mandatory. The probe must use:

- a fixed public payload;
- no protected paths;
- no artifact data;
- no configuration data;
- no Registry or process-environment data;
- a fixed public acknowledgement;
- the same noninteractive stdin delivery primitive intended for formal execution.

The probe establishes only transport behavior, with a bounded result such as:

```text
fixed public input accepted = yes
fixed public acknowledgement received = yes
stdin remained available until complete input delivery = yes
protected inputs = 0
artifact access = 0
HKCU or environment access = 0
mutation = 0
repository write = 0
```

If the public probe fails:

- do not create or activate the protected Goal;
- do not consume the approval;
- do not alter accounting;
- do not access protected resources;
- return a bounded pre-Goal transport-guard receipt;
- keep the approval reusable unless another guard or explicit rule says otherwise.

## 11. Separation of pre-Goal and protected execution

```text
public sentinel probe = pre-Goal transport-integrity guard
formal protected controller = post-Goal authorized execution
```

A successful public probe does not authorize artifact or Registry access. A failed public probe is not a formal controller execution and does not consume a formal protected execution count.

## 12. Current non-authority boundary

Baseline v2.1 establishment creates no authority for:

- runtime controller execution;
- protected-path reads;
- Provider Result, manifest, or package-index reads;
- HKCU or process-environment reads or writes;
- environment broadcast;
- CIB fingerprint, binding, receipt, or salt access or action;
- gate reads, enablement, or mutation;
- application import or app-factory execution;
- TestClient or ASGI client execution;
- route, endpoint, or B05 GET execution;
- database or persistence access;
- production, public export, or delivery;
- Collector execution or network access;
- Project Source maintenance.

The document creates no generated runtime identity and changes no canonical Source count.

## 13. Project Source follow-up

This repository document does not modify ChatGPT Project Source, and the active Source count is unchanged by this Goal. After independent acceptance, a separate Source-maintenance action may update Canonical 00, 05, 08, or 09. Such Source maintenance creates no engineering or runtime authority.

## 14. Next default

After independent acceptance, the default next engineering route is Baseline v2.1 Fixed Prompt 1.

Its objective is exact-path three-variable HKCU repair using:

- one pre-Goal public sentinel stdin transport probe;
- one formal noninteractive protected controller execution;
- preserved exact-path, artifact, privacy, and zero-action boundaries.

This next-default statement does not authorize engineering execution.
