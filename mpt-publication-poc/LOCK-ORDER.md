# Lock order - candidate 0.8

REQUIRES_HARDENING / NOT_RUN. This replaces operational descriptions in versions 0.1-0.4 (HISTORICAL / SUPERSEDED). EXEC-G1 and PERS-G1 OPEN.

## Single T2 boundary

T2a calls capture_cut and COMMITs in a short READ COMMITTED transaction.
T2b begins a NEW transaction and inserts AssessmentAttempt referencing that immutable cut.
The attempt derives position/plan versions from immutable revisions whose published ordinal
is at most the cut. Eligibility and resolution policy remain attached to the captured cut;
later publications do not advance it. A new capture's transaction ID is recorded by the
database; guard_attempt rejects insertion in that same transaction (T2_SPLIT_REQUIRED).
This is a candidate choice requiring review, not an accepted architecture decision.

T2a reads the frontier and may acquire FK KEY SHARE locks on its referenced publication batch.
Canonical-cut UNIQUE conflict may wait on another capture; the loser returns the committed
canonical ID. T2a never acquires position locks for attempt insertion.
T2b acquires position/cut FK locks only AFTER T2a releases its transaction locks.
Reusing an already committed cut is permitted; it does not retain a new capture's FK lock.

## Mutation order and implicit locks

Position-scoped mutation APIs lock position / position_guard first. Fenced TP/T4 then lock
the purpose-specific worker lease. TP locks the target batch and domain publication barrier
before projection/member effects; T4 locks its delivery rows before authorization/audit receipt.
T3 locks position, then attempt, then creates its result batch and associated immutable facts.
Recovery follows position then batch. Multi-position operations are outside this candidate.

INSERTs also acquire referenced-row FK locks; UNIQUE indexes arbitrate command, batch,
cut, authorization, destination dedup and operation identities. Deferred triggers check
batch completeness and intent consistency at commit. These locks are not optional merely
because they are absent from explicit FOR UPDATE statements. Fixture assembly follows
root-before-child ordering; owner fixture setup is trusted and not an application API.

The problematic cycle was T2 holding a new cut's batch FK lock while waiting on position,
with TP holding position while waiting on batch. The T2a COMMIT removes that retained edge.
T2-TP-FK-CYCLE captures/commits, lets TP retry hold locks, observes T2b blocked through
pg_blocking_pids, commits TP, then requires T2b completion. No elapsed sleep is an oracle.
This authored schedule is NOT proof of deadlock freedom until executed and reviewed.

Errors roll back the entire transaction. Timeout or unexpected lock dependencies produce
inconclusive/failing evidence, not silent retry success. Whole-transaction retries retain
their logical identities; divergent payload reuse is rejected. No claim covers arbitrary
SQL by an owner, multiple domains, real providers or untested interleavings.


## Version 0.7 coverage and evidence binding

The normative coverage/status map is runner/SCENARIO-MATRIX.md (supersedes older coverage
claims). New executable candidates are in runner/coverage_controls.py. All are NOT_RUN.
Effective role/membership, column/function privilege inventories, extensions and installed
dependencies must match independently approved values before fixture mutation. Unknown
values fail closed. No collector secrets or DSNs belong in evidence.

Lease contention holds the winning root/lease transaction while observing the losing backend
in pg_blocking_pids. Expiry is observed from the DB lease row and clock_timestamp; client time
only bounds failure. Termination controls confirm pg_stat_activity absence before recovery.
The trusted compound fault controller uses ALTER TABLE on projection between transactions,
then removes the injected constraint; it is not a concurrent production migration contract.


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
