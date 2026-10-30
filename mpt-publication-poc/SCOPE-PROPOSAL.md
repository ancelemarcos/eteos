# Scope and pending decisions - candidate 0.9

PROPOSED / NOT_RUN. EXEC-G1/PERS-G1 OPEN. PUB-T13B PENDING_HUMAN_APPROVAL.
This documentation-only round leaves SQL, Python, config and non-operational stub unchanged.

The controller lifecycle, owned-child capability identity, IPC, deadlines, privileges and
future acceptance matrix are specified in WORKER-CONTROLLER-CONTRACT.md (H01-CTRL@1).
The complete persisted-data encoding, exact 30-table/column/PK inventory, type rules,
table/aggregate/global digests and documentary fixtures are in FULL-SNAPSHOT-CONTRACT.md
(MPT-SNAPSHOT@1). Both are specifications, not operational implementation.
runner/worker_controller_stub.py still rejects all lifecycle operations; no process is enabled.

INTRABATCH-SEAM-PROPOSAL.md concretely proposes a laboratory validation checkpoint after v2
and before v3, before the existing single TP publication update. It records candidate SQL-shaped
design text, fault-controller boundary, fixed hook, PZ501 proposal, explicit/implicit locks,
rollback and replay oracles. No executable SQL/DDL/grant was changed.
H05-SEAM-PENDING requires a complementary accepted ADR/Decision Register ID plus human
implementation authorization; the proposal is not approval. Existing COMPOUND-ROLLBACK
barrier-to-projection failure remains distinct.

Proposed functional minimum: immutable facts, canonical fixed cuts and T2 split, T3 persistence
then TP publication, DO_NOT_NOTIFY, bounded grants/leases/replay and T24/T25/T13A synthetic
delivery controls. Proposed expanded validation includes external worker/server crash, network
faults, production IAM/providers and performance. Exclusions are OUT_OF_SCOPE_PROPOSED only:
required missing controls remain BLOCKING_EXECUTION_REVIEW until explicitly decided.
No scope is reduced by silence and no physical exactly-once or temporal availability is claimed.

Next human decisions: approve isolation/child-capability/IPC and snapshot contract for a
separately authorized implementation; accept a complementary laboratory seam decision with
equivalence/lock/grant review; appoint independent environment/evidence approvers and freeze
measured values. Implementation and experimental execution each need separate authorization.
ENVIRONMENT-FREEZE.md records owners by responsibility, not invented names or signatures.


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
