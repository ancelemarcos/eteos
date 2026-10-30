# Invariant enforcement - candidate 0.8

REQUIRES_HARDENING / NOT_RUN. Every test below is authored or proposed, never observed PASS.
Database enforcement assumes installed schema AND delivery-api.sql, enabled triggers,
reviewed non-owner role memberships and no privileged DDL bypass.

| Invariant | SQL / privilege protection | Operation | Positive / negative control | Expected evidence | Residual gap |
| --- | --- | --- | --- | --- | --- |
| Initial delivery cannot be fabricated | Column INSERT grants; READY/PENDING defaults; guard_initial_delivery; writer no state UPDATE | Fixture/T3 | FNOTICE / DELIVERY-FORGE-01 writer and owner attempts | 42501 or P0001; no auth/call/receipt/public effect | Owner/superuser trusted; runtime membership review pending |
| ACK is not a bare flag | Transition triggers require auth and matching immutable call/receipt; dispatcher API only | T4 ACK | t25b / ACK_WITHOUT_RECEIPT rejection path | Linked auth/call/receipt and ACKED | ACK-NEGATIVE covers missing auth/call/receipt and call-only; ACK-RECEIPT-NO-CALL now covers receipt-only rejection; synthetic owner sink trusted |
| T4 logical retry exactly once | Root lock; operation PK; full payload + SHA-256; audit FK and immutable receipt | AUTHORIZE/RECHECK | T4-ACK-AUTH and T4-ACK-RECHECK identical/divergent retry | One audit/receipt for LOST-OP; original reply, conflict on divergence | Physical transport loss not tested; fresh recheck needed to send |
| New cut not retained across attempt insertion | capture transaction ID; guard_attempt; canonical UNIQUE/FKs | T2a COMMIT then T2b | concurrent_cut / same-transaction guard rejection | Two actual attempts, one cut; stable historical versions | T2-SAME-TRANSACTION authored; candidate boundary still requires review |
| T2/TP no retained cut-FK cycle | Separate transactions; root/batch locking; FK edges explicit | T2-TP-FK-CYCLE | Controlled wait then release | pg_blocking_pids and successful attempt | Authored schedule only, no universal deadlock proof |
| Historical cut immutable | Revision/batch ordinal predicates, cut policy identity | FIXED-CUT | Publish v2 between reads; both v1 | Same cut and two v1 reads | No real market-time reconciliation |
| Publication prefix and complete batch | Deferred member/content constraints; barrier/frontier; ordered fenced TP | TP | compound / blocked_recovery successor refusal | No skip; projection v3 | COMPOUND-ROLLBACK covers projection failure after batch/frontier mutation; literal per-member seam remains blocked |
| Block/recovery never changes content | Permanent content_frozen; child guards; immutable facts; recovery audit | BLOCK/RECOVER/TP | blocked_recovery mutation rejection and repeat recovery | Identical fingerprint/member sets before/after | Full payload mutation matrix missing, BLOCKING_EXECUTION_REVIEW |
| Result/decision/intent atomic | Deferred consistency constraints; synthetic finalizer identity | T3a then TP | notify/quiet; divergent retry | One result, exact decision/intent counts | General command/result gateway remains trusted-writer scope |
| Stale workers cannot publish | Position/purpose lease epoch and expiry checks | TP/T4 | stale_worker old/new epoch | Rejection then one publication | LEASE-LIFECYCLE and SESSION controls authored for TP; T4 lease/backend controls added; external process scope remains blocked |
| Close/revocation schedule explicit | Guard state, publication status, auth history, fresh recheck | T4 | POC-T24/HOLD-PENDING-CLOSE/t25a/t25b/t13a | Exact status/auth/call/receipt counts | PUB-T13B unapproved; external fencing unproved |
| Reader cannot see pending facts | View-only reader; owner-controlled base tables | privileges | Published view / forbidden table read | 42501 then public row | Production IAM/RLS and login inheritance not verified |
| Evidence bound to actual artifacts/environment | SHA-256 inventory/config/manifest; actual HEAD; signed external inspection; server/version probes | Preflight | Approved environment / mismatched values refused | Provenance and settings before mutations | Collector/trust/freshness/dependency freeze unresolved, BLOCKING_EXECUTION_REVIEW |

Trusted writer responsibilities remain command payload correctness, expected-version discipline,
domain ownership, synthetic meaning, fixture sequencing and full identity/payload construction
where no general command gateway is provided. SQL enforces declared FKs, checks, immutable
facts, controlled delivery states and publication constraints; it does not establish empirical
market validity, licensing, arbitrary application honesty or safety against schema owners.

No new accepted architecture, delivery performance, scientific result or production capability
is implied. EXEC-G1 OPEN; PERS-G1 OPEN; PUB-T13B PENDING_HUMAN_APPROVAL.


## Version 0.7 coverage and evidence binding

The normative coverage/status map is runner/SCENARIO-MATRIX.md (supersedes older coverage
claims). New executable candidates are in runner/coverage_controls.py. All are NOT_RUN.
Effective role/membership, column/function privilege inventories, extensions and installed
dependencies must match independently approved values before fixture mutation. Unknown
values fail closed. No collector secrets or DSNs belong in evidence.


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
