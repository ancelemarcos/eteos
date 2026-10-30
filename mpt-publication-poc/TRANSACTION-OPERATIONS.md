# Transaction operations - candidate 0.8

REQUIRES_HARDENING / NOT_RUN. Earlier operational versions are HISTORICAL / SUPERSEDED.
Named SQL bindings are in runner/operations.sql; runner/run.py owns transaction boundaries.

| Operation | Current boundary and identity |
| --- | --- |
| T1 fixture assembly | Root lock, immutable revisions/members and pending batch in one transaction; trusted synthetic writer, not a general production command gateway |
| TP | Position then valid TP lease then batch/barrier; publish complete ordered batch and advance frontier/projection atomically; stable batch retry |
| T2a / CUT | capture_cut(position, policy, candidate ID), COMMIT; UNIQUE domain/ordinal/policy selects canonical immutable cut |
| T2b / T2B | NEW transaction; persist attempt referencing committed cut and immutable historical versions; no current projection resolution |
| T3 / T3a | finalize_synthetic under position/attempt lock; result, decision and optional notification/outbox committed pending publication; identical retry returns original, divergent fingerprint fails |
| T4 | delivery_step under position and T4 lease; authorization/decision/audit/operation receipt commit together |
| Destination | Independent synthetic owner session records call and deduplicated receipt; explicitly outside T4 transaction |
| ACK | Requires matching committed authorization, destination call and receipt; state alone is not delivery proof |
| Recovery | Explicit fenced/trusted recovery APIs and audits; frozen batch content stays frozen after recovery |

## Delivery trust and idempotency

Writer INSERT permission is column-scoped to payload columns. Defaults are READY for
notification and PENDING with null lease for outbox. Initial-state triggers also reject
privileged initial states. Writer has no delivery state UPDATE permission. Dispatcher can
use only granted delivery functions; owner/superuser/DDL authority remains a trusted boundary.
Deployment must review actual login membership and inherited grants; schema grants alone
cannot constrain a superuser or owner who alters triggers.

T4 identity is (position_id, operation_id). Its canonical JSONB request is the ordered array
of protocol version T4-v1, position, notification, worker, epoch, phase, session_user;
the stored SHA-256 fingerprint and full payload must both match on retry.
The root position lock serializes contenders. A receipt is inserted atomically with the
unique delivery audit; replay returns its ORIGINAL response before lease/policy reevaluation.
Different arguments or login with the same identity raise T4_IDEMPOTENCY_CONFLICT without
additional effects. AUTHORIZE and RECHECK require separate operation IDs. ACK is also receipted.

A replayed SEND_AUTHORIZED is historical evidence, never renewed permission to call.
Every prospective send needs a fresh RECHECK operation under the current lease and policy.
T25A observes a close in that recheck and makes zero calls. T25B closes after the final
committed recheck and permits one previously authorized logical delivery, deduplicated by
destination/key. This bounded race does not promise cancellation or physical exactly-once.
External proof, transport semantics and stale-worker fencing remain unapproved.

Transition triggers require authorization for authorized/ACKED states, prohibit terminal
changes and require matching synthetic receipt/call proof for ACK. Synthetic destination
records are immutable but their trusted owner producer is not a real provider attestation.

## Time and deferred constraints

Use READ COMMITTED; SET CONSTRAINTS ALL IMMEDIATE precedes COMMIT in the runner.
Database wall-clock time is used for operational lease expiry only, never market decision
time. Cut ordinals are logical publication ordering, not MIR availableAt/decisionTime proof.
Unresolved temporal reconciliation and production persistence stay outside this experiment.
No operation, preparation, teardown or dependency installation is authorized by this file.


## Version 0.7 coverage and evidence binding

The normative coverage/status map is runner/SCENARIO-MATRIX.md (supersedes older coverage
claims). New executable candidates are in runner/coverage_controls.py. All are NOT_RUN.
Effective role/membership, column/function privilege inventories, extensions and installed
dependencies must match independently approved values before fixture mutation. Unknown
values fail closed. No collector secrets or DSNs belong in evidence.

TP_RENEW and BLOCK now have named parameterized bindings. The compound control fails at
projection update with SQLSTATE 23514 after batch/barrier mutation and verifies rollback of
all table rows. TP does not have separate per-member publication commits. Actual backend
termination before/after commit and reply-loss simulations are separate controls.


## Directed hardening contract 0.7

runner/SCENARIO-MATRIX.md is authoritative for individual coverage status and supersedes
older missing-control descriptions. T4 dispatcher lease lifecycle, backend termination before/
after AUTHORIZE and RECHECK commits, receipt-without-call ACK and writer delivery bypass
negatives are now MATERIALIZED_NOT_RUN in coverage_controls.py. They do not prove server
crash, raw network loss, all ACK-phase crashes or real-provider delivery.

SCOPE-PROPOSAL.md separately proposes a functional minimum and expanded operational scope;
no exclusion is accepted. External worker-process controller and literal compound member seam
remain BLOCKING_EXECUTION_REVIEW. A single TP transaction is mandatory; no per-member commit
was added. Current projection fault is not represented as an after-first-member seam.

Freshness parameters attestation_max_age_seconds and attestation_clock_skew_seconds must be
independently frozen alongside the signed collector identity. Preflight rejects missing,
invalid, stale or future-dated evidence; host clock accuracy and signer/collector privileges
remain explicit assumptions. No credentials/private keys are logged. Exact versions, digests,
privilege hashes and controller authorization remain UNRESOLVED.

PUB-T13B remains PENDING_HUMAN_APPROVAL, with proposed suppression on observed pre-call
revocation while retaining historical authorization. T24/T25A/T25B semantics are unchanged.


## Current preparation boundary (order v0.4)

runner/worker_controller_stub.py is a non-operational interface: no OS or database operations,
no arbitrary target inputs; every lifecycle method refuses. run.py unconditionally blocks
worker before/after-commit and member-seam scenarios before sessions. Materialization of the
real supervisor and SQL hook remains BLOCKING_EXECUTION_REVIEW, not covered by a stub.
SCOPE-PROPOSAL.md defines future identities/checkpoints/oracles and a pending single-TP
ordered validation seam. ENVIRONMENT-FREEZE.md maps independent approval/evidence to actual
preflight checks. No signature or config flag substitutes for missing implementation.


## Documentation-only revision 0.8 (order v0.5)

Executable SQL, Python, stub and approved-config example remain unchanged at implementation
policy version 0.7; no scenario is enabled. WORKER-CONTROLLER-CONTRACT.md (H01-CTRL@1)
specifies owned-child identity/IPC/exit/restart and independent future acceptance.
FULL-SNAPSHOT-CONTRACT.md (MPT-SNAPSHOT@1) defines the 30-table canonical snapshot, exact
columns/PKs/type encoding/digests and documentary oracles. That specification now exists;
its encoder/consistent collector/reference vectors remain unimplemented. Existing snapshot(lab)
JSONB equality is not that canonical algorithm or a guaranteed single MVCC snapshot.
INTRABATCH-SEAM-PROPOSAL.md specifies H05-SEAM-PENDING between v2/v3 logical validation,
with a fixed test-only hook and proposed PZ501; no active DDL, grant or SQL modification.
ENVIRONMENT-FREEZE.md assigns approval responsibilities and distinguishes observed values
from declarations and approval. All actual runtime evidence remains UNRESOLVED.
