# Scenarios - candidate 0.9

REQUIRES_HARDENING / NOT_RUN. The single scenario/status mapping is
runner/SCENARIO-MATRIX.md; implementation is run.py plus coverage_controls.py.
All functional scenarios require a fresh approved schema, verified artifact/config/environment
header, validated runtime-role inventories and F0/F1. No execution is authorized now.

POC-T24: published close before AUTHORIZE, SUPPRESSED and no authorization/call.
HOLD-PENDING-CLOSE: pending close, HOLD_PENDING_CLOSE and no authorization/call.
T25A: prior authorization, close observed by fresh recheck,
SUPPRESSED_AFTER_AUTHORIZATION and zero calls.
T25B: close after final check, exactly one prior authorized logical synthetic delivery,
deduplicated receipt and audited ACK. PUB-T13A revokes before authorization.
PUB-T13B remains PENDING_HUMAN_APPROVAL; proposed pre-call suppression is not accepted.

T4-BACKEND controls terminate actual DB backends at before/after commit boundaries of
AUTHORIZE/RECHECK; they do not terminate an external controller or PostgreSQL server.
Historical replay cannot substitute for fresh pre-send revalidation.
T4-LEASE-LIFECYCLE observes lock contention and actual DB expiry; no sleep is an oracle.
ACK-RECEIPT-NO-CALL rejects ACK despite a synthetic receipt when no matching call exists.
WRITER-DELIVERY-BYPASS uses the ordinary writer and checks state equality after denials.

Existing TP lease/backend controls, immutable negatives, T2a/T2b, concurrent cuts, fixed
history, T3 NOTIFY/DO_NOT_NOTIFY, rollback and retry scenarios remain materialized but NOT_RUN.
Synthetic destination and fault injection are trusted owner exceptions; no external delivery proof.

SCOPE-PROPOSAL.md records the absent external-process controller and literal internal-member
fault seam as BLOCKING_EXECUTION_REVIEW, plus proposed functional/operational scope separation.
No scope reduction is accepted. Environment freeze and privileges remain unresolved.
EXEC-G1/PERS-G1 OPEN. Earlier scenario narratives are superseded by the 0.7 matrix.


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


## Current order v0.7 / candidate 0.9 disposition

CODEC-MATERIALIZATION.md is the current implementation-boundary reference. New snapshot
encoder/reference parser/schema/static vectors and pure worker identity validators are
MATERIALIZED_NOT_RUN. They are not imported by run.py or wired into collection/process control.
Previous statements that these modules do not exist are superseded; statements that no
collector/supervisor is operational remain true. Stub, schema.sql, publication APIs, run.py,
preflight and config are unchanged. Runtime policy remains 0.7; package revision is 0.9.
No order v0.6 was located in the available attachments/candidate docs; its content is not assumed.
Full codec equivalence and compound independent vectors remain BLOCKED. No preflight or test
was executed; proposed seam remains DOCUMENTED/BLOCKED. Gates remain open.


## Order v0.8 / candidate 0.10 current checkpoint

CODEC-CONFORMANCE-MATRIX.md is the current field/byte/oracle map and explicitly resolves
candidate partition placement, metadata streams, view semantic nullability, key ordering and
value precision. New snapshot_compound_vectors.json carries manual structure/byte expectations;
intermediate/full digest oracles remain UNRESOLVED. Codec/ref parser parity guards and strict
worker identity field typing were tightened; none were executed. No encoding helper is shared
with the independent reference parser.

SNAPSHOT-COLLECTOR-DESIGN.md and runner/snapshot_collector.py now provide a disabled-by-default,
unintegrated read-only MVCC collector candidate. Earlier statements that no collector source
exists are superseded; no collection/connection/test actually occurred. It requires approved
manifest/schema/config bytes, dedicated read-only connection/role, exact catalog/version and
one REPEATABLE READ READ ONLY snapshot, with rollback/close. No connect(), main or runner hook.
collector-approval.example.json remains false/UNRESOLVED. Safety/conformance validation BLOCKED.
No SQL publication function, active seam, operational supervisor or gate was changed.
