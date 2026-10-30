# Laboratory intrabatch checkpoint H05-SEAM-PENDING - candidate 0.8

PROPOSED / BLOCKING_EXECUTION_REVIEW / NOT_RUN.
This document contains SQL-shaped design text only. Do not copy into schema.sql, prepare.sql,
operations.sql or delivery-api.sql under the current authorization. No executable SQL changed.
Needs an accepted complementary ADR/Decision Register ID approving laboratory instrumentation,
equivalence boundary, privileges and ordering; H05-SEAM-PENDING is not such an accepted ID.

## Exact placement and single-transaction invariant

For synthetic B23 with members (order1,position_version2) and (order2,position_version3),
insert a validation-only ordered pass in publish_batch AFTER position/lease/batch locks and
pending-state check, BEFORE barrier acquisition and the existing batch publication UPDATE.
Validate v2 structurally/logically, invoke the fixed laboratory checkpoint, then validate v3.
Validation reads immutable membership/revision facts; it does not publish or allocate ordinals.
The existing batch/frontier/projection updates and one caller COMMIT remain unchanged.
A PUBLISHED retry takes the existing early return and does not re-inject the fault.

Candidate design, NOT an executable artifact or implementation:

```sql
-- Inside the existing TP transaction; pseudocode helpers are NOT implemented.
FOR member IN
  SELECT * FROM mpt_poc.publication_member
  WHERE position_id=p AND batch_id=b ORDER BY member_order
LOOP
  -- Proposed pure helper must reuse the accepted deferred semantic predicates.
  -- No independent alternative predecessor policy and no writes.
  PERFORM lab_validate_member_candidate(p,b,member);
  -- For exact B23 fixture: after logical v2 validation, before iteration for v3.
  PERFORM mpt_lab.fixed_member_checkpoint(p,b,member.member_order);
END LOOP;
-- Existing barrier lock -> batch UPDATE -> frontier -> projection -> constraints -> one COMMIT.
```

lab_validate_member_candidate must verify the member's matching revision/batch identity,
version/predecessor linkage and existing publication prerequisite; v3 can have its predecessor
v2 within THIS complete batch even though neither has been individually published.
Existing deferred completeness/predecessor constraints remain authoritative and unchanged.
Equivalence for plan/result-only batches and no-fault execution must be reviewed before code.
Reject implementing a second semantic policy that conflicts with existing constraints.

## Fault control and permissions

Proposed fixed checkpoint reads a run-bound immutable fixture row installed BEFORE TP by a
dedicated lab fault-controller identity under a separately authorized migration/fixture action.
Fields: fixture version, run nonce, approved manifest/config hashes, session_user identity,
position P-A, batch B23, member_order1, one active fault. No caller-supplied SQL/function name.
A fixed owner-defined SECURITY DEFINER function with pg_catalog,mpt_lab,pg_temp search_path
raises SQLSTATE PZ501 (proposed lab-only exception, not an accepted domain code) on exact match.
No control-table UPDATE or DELETE inside TP; exception rollback must not consume the arm record.
Trusted controller disarms in a separate committed operation only AFTER failure/rollback
confirmation; a retry then follows unchanged TP. Log arm/disarm as process/control evidence.

No PUBLIC or runtime writer/dispatcher/evaluator EXECUTE, schema CREATE, control-row access or
mutation grants. The publisher role has only existing TP entry point; TP owner would call the
fixed checkpoint internally. Fault-controller must not be production writer or arbitrary client.
Owner/DDL remains trusted. Arm/disarm never runs concurrently with TP; no general custom GUC
or arbitrary function callback that clients can forge. Require explicit capability review and
separate test schema installation; no such objects/grants exist today.

## Lock map and failure visibility

Existing order: recipient_guard -> position_guard -> position -> plan (FOR UPDATE in lock_position);
then purpose TP worker_lease; then target publication_batch. Proposed ordered member SELECT and
immutable revision reads hold ordinary relation read locks/MVCC snapshots, not new FK writes.
The fixed immutable fault-row read adds relation read locks only. Do not lock control rows after
barrier or mutate them within TP. Later unchanged order: domain publication_barrier FOR UPDATE,
batch/frontier changes, projection INSERT/UPDATE, deferred checks at commit.

Existing INSERT/UPDATE paths also involve UNIQUE index arbitration and referenced-row FK
KEY SHARE locks; projection FK references position/revisions, revision/member relationships
are checked by existing constraints. Validation loop does not add a new INSERT or FK edge.
Concurrent ordinary fixture writes must obey root/batch protocol and immutable-child guards;
DDL/fault configuration is excluded during scenario. No universal deadlock claim.
Review every proposed helper for hidden locks/volatile queries before acceptance.

At the injected PZ501, v2 was READ/VALIDATED only. No publication UPDATE or ordinal allocation
has happened. Transaction abort releases its locks; neither v2 nor v3 becomes public.
If instrumentation placement later changes, this contract/version must be re-reviewed.

## Future acceptance oracles

Preconditions: B1 published ordinal1/version1; B23 pending containing exactly v2/v3; valid TP
lease; fresh canonical snapshot S0 and public-view reader; independent approved fault fixture.
1. TP reaches v2 checkpoint, PZ501 before v3. Confirm rollback, new observer snapshot S1.
2. S1 persisted global digest and all table digests equal S0 under MPT-SNAPSHOT@1. No new cut,
   ordinal/frontier change, projected v2/v3, extra audit or partial member publication.
3. Separate reader still sees version1/ordinal1; child facts remain pending, not removed.
4. Trusted controller disarms outside application snapshot tables. Retry SAME batch once:
   frontier2, one batch ordinal2, final projected v3; immutable rows/member set unchanged.
5. Retry again: identical complete application snapshot; no duplicate publication or audit.

The lab control schema is outside MPT-SNAPSHOT@1 application table scope and must have its
own arm/disarm evidence digest; it may never be silently included/excluded by an encoder.
Actual creation of that schema requires separate inventory/provenance contract review.
COMPOUND-ROLLBACK (existing 23514 after barrier, before projection completes) remains distinct.
No test ran; no PZ501 implementation, ordinal result, proof or acceptance is asserted.

## Order v0.7: candidate equivalence analysis (no SQL change)

No-fault trace A (current): root/lease/batch locks -> pending checks -> barrier -> one batch
publication update -> frontier/projection -> deferred constraints -> one commit.
Proposed trace B inserts only ordered, deterministic, read-only member validation between
pending checks and barrier. To claim committed-state equivalence, prove that validation uses
exactly the existing final predicates, sees stable immutable member/revision facts under the
same locks, cannot raise on any state that A would validly commit, and has no side effects.
No separate ordinal allocation, member visibility, audit write or commit may be introduced.

This is a proof obligation, NOT a proof. Deferrable constraints may legitimately see state
created later in TP; an early validator could reject it. Volatile reads, concurrent fixture
writers, helper locks, errors/timing or row-order assumptions could change observable behavior.
Therefore equivalence is limited to committed application state under a frozen fixture/locking
contract even after review, not identical error timing/performance or universal concurrency.

Fault trace: fixed lab hook after v2 logical validation raises proposed PZ501 before v3 and
before publication updates. Entire TP aborts, new observer snapshot equals prestate, public
reader remains v1; disarm outside TP then retry one ordinal/projected v3, repeat unchanged.
COMPOUND-ROLLBACK remains the existing later 23514 barrier/projection fault. The different
fault positions must not be represented by one test or evidence bundle.

Required complementary decision: approve lab-only validation/hook boundary, ordinary role
inaccessibility, fixed SECURITY DEFINER search path, no-fault predicate equivalence, dependency/
lock ordering and independent snapshot/public-view oracles. H05-SEAM-PENDING remains BLOCKED.
No schema.sql, publication function, active SQL or runner activation was changed by v0.7.


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

Reinspection of actual publish_batch confirms recipient/position roots -> lease -> batch ->
barrier -> batch/frontier/projection -> deferred checks/one commit. Proposed validation remains
before barrier and no-fault equivalence is conditional on stable facts/identical final predicates.
Existing deferred constraints can reject only at commit; early rejection is observable, so
no universal equivalence is asserted. Fault rollback/public v1 then retry final v3 are separate
oracles from the existing later projection failure. H05-SEAM-PENDING remains BLOCKED.
