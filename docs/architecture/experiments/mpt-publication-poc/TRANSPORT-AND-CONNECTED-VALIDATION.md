# Transport and connected validation - candidate 0.13 / order v1.1

## Order v1.2 / candidate 0.14 - bounded review scope

Current decision preparation is in TRANSPORT-CONTAINMENT-DECISION.md; future offline-only
validation is in CODEC-ISOLATED-VALIDATION-PLAN.md. These documents authorize no execution.
Collector/transport/harness code and false configurations are unchanged. Eight offline tests
are prepared; connected/fake tests are excluded from the minimal codec invocation.
READY_FOR_REVIEW / NOT_RUN applies to these review artifacts, not executable readiness.
Native transport and connected gates remain BLOCKING_EXECUTION_REVIEW.

| Requirement | Artifact | Prepared test | Independent oracle | External dependency | Required evidence | State |
| --- | --- | --- | --- | --- | --- | --- |
| Distinct field/native/process/call/cancel/child/cleanup containment | TRANSPORT-CONTAINMENT-DECISION.md alternatives A0..A6 | Future platform/driver fault cases; existing no-call fake tests | Declared containment obligations, not fake success | Pinned builds and approved isolation | Native allocation, owned-child identity, deadlines and actual cleanup | DOCUMENTED; execution BLOCKING_EXECUTION_REVIEW |
| Minimal offline codec scope | CODEC-ISOLATED-VALIDATION-PLAN.md | Eight CodecConformance methods only | Literal/manual plus independent oracle recipes | Approved finite capsule/environment/limits | Separate expected freeze and observed byte/digest comparisons | DOCUMENTED / MATERIALIZED_NOT_RUN |
| Temporal Python boundary | test_python_time_domain_without_postgresql_claim | UTC offset epoch, naive rejection, UTC overflow, broad wire value | Manual epoch hex and independently typed micros | Pinned CPython; PostgreSQL excluded | Actual outcomes under later offline authority | MATERIALIZED_NOT_RUN |
| Evidence provenance | Isolated plan EXPECTED_UNVERIFIED / REVIEWED_FROZEN / OBSERVED lifecycle | Independent-generation then immutable comparison plan | No expected output taken from codec | Independent reviewer and future frozen-bundle adapter | Reviewed exact byte/length/SHA records before observed comparison | UNRESOLVED |
| Connected activation/roles | Containment effective-role matrix and existing guarded source/config | Existing admission tests; connected scenarios remain unrun | No calls without proven approval; role/ACL observations later | Build/privilege/quiescence/limits and trusted caller | Exact effective rights and native guard evidence | BLOCKING_EXECUTION_REVIEW |
| Independent approval scopes | Isolated plan four-scope table | Offline vs isolated transport vs MVCC vs publication | Scope-specific evidence only | Separate human approvals | No inherited approval; unchanged EXEC-G1/PERS-G1/PUB-T13B | PENDING_HUMAN_APPROVAL |

DOCUMENTED / MATERIALIZED_NOT_RUN. Overall REQUIRES_HARDENING / NOT_RUN.
No connection, process, SQL, test, driver import, installation or execution occurred.

## Identified driver/API and guarantee boundary

Current runner/run.py imports psycopg and supplies a synchronous psycopg connection; the exact
driver/Python/libpq/server build remains UNRESOLVED in ENVIRONMENT-FREEZE.md. This is the
candidate's actual API family, not a newly introduced database dependency.
Official API sources consulted 2026-10-29:
- [Psycopg cursor types](https://www.psycopg.org/psycopg3/docs/advanced/cursors.html)
- [Psycopg connection API](https://www.psycopg.org/psycopg3/docs/api/connections.html)

Client-side Cursor receives the result into client storage. A named ServerCursor permits partial
retrieval through fetchmany, but counting fetched rows does not establish a maximum byte size
for one field, libpq allocation or Python object expansion. The current documentation is rolling
and displayed a development version; it is not evidence of an installed/frozen dependency.
cancel_safe availability/semantics must be verified for the pinned build. Sending cancellation
does not establish rollback, termination or a hard upper bound for every blocked call.

snapshot_transport_candidate.py provides an immutable SELECT plan and API recipe, with all
operational methods refusing admission before touching a connection. A boolean or matching
hash cannot activate this revision. Collector invokes guard.admission before ownership transfer.
This is a concrete fail-closed candidate boundary, not a functioning natively bounded driver.
No fallback to raw execute/fetch is authorized. Any useful transport execution requires a
separately reviewed implementation revision and evidence of the missing native guarantees.

## Limit ownership

| Limit | Responsible component | Current candidate behavior |
| --- | --- | --- |
| Column / row bytes | Collector accounting plus required pre-allocation transport | Post-return check authored; native oversize-field prevention UNRESOLVED |
| Fetch rows / batch bytes | Named server cursor recipe plus collector single-row batch cap | Plan and cap authored; driver execution blocked |
| Table / total logical bytes | Collector Budget.relation | Explicit caps; excludes native allocator overhead and catalog from logical data totals |
| Native buffers / peak memory | Future verified transport/runtime mechanism | UNRESOLVED; current adapter cannot admit |
| Retained Python graph | Collector Budget.memory | Estimate after allocation; never a peak-memory guarantee |
| Per-call timeout | Guard required; collector min(total remaining, statement, call budget) | Budget propagation authored; blocked-call enforcement UNRESOLVED |
| Total duration | Collector monotonic deadline | Checks between calls; actual interruption requires verified guard |
| Cancel | Future driver/build-specific cancellation plus independent termination evidence | Current adapter refuses; ignored cancellation invalidates run/quarantines session |
| Cleanup | Guard bounded rollback/close; collector original-error preservation | Fake source coverage only; caller owns cleanup before transfer |
| JSON nesting / Decimal expansion | Collector conversion | Explicit approved bounds; raw standalone codec admission policy remains unresolved |

## Inert connected harness

connected_snapshot_harness.prepare verifies independently supplied configuration hash, manifest,
environment and scenario hashes, explicit isolation/fixture/cleanup/oracle approvals, frozen build
identities and a dedicated mpt_snapshot_reader. Candidate config has no host, DSN or secrets.
Credentials stay with a future independently approved external session provider.
Preparation returns an immutable CasePlan and evidence template only. dispatch unconditionally
passes through the concrete disarmed adapter admission; no provider callback is invoked.
A connected scheduling implementation and trustworthy environment verifier remain absent.
Hashes bind evidence; they do not prove signatures, isolation, privileges or scientific validity.

connected-scenarios.json specifies ten deterministic cases. Separate disposable database fixtures
and administrative/writer roles are required for adversarial cases; the observer must never gain
those roles. C0 prepares the approved fixture outside this harness. C1 fixes the observer MVCC
snapshot. C2 performs the approved writer action/fault through an independently instrumented
session. C3 captures complete observer output or rejection. C4 records cleanup and residual state.
For MVCC-UPDATE, C2 commits B only after C1 acknowledgement; observer must see A while a new
observer sees B. No sleeps imply checkpoint completion. DDL/view/privilege drift is introduced
before BEGIN in separate fixtures; mid-snapshot drift is a distinct quiescence violation,
not evidence that catalog MVCC alone protects GRANT or DDL.
No scenario changes publication functions, TP/T3a, locks, H05 or production data.

Expected rejection is not a successful validation result. Actual exception class/SQLSTATE must
be recorded, never guessed. Evidence includes exact artifacts/config/builds, session/snapshot
identities, ordered checkpoints, before/after rows, independent byte/hash oracles, effective ACLs,
memory/deadline observations and original/cleanup errors without secrets/raw licensed payloads.
Rollback/close failures are preserved; uncertain sessions require external quarantine review.
No automatic DROP, kill, PID selection or cleanup migration exists in this harness.

## Oracle coverage and compatibility

snapshot_oracle.py independently constructs all declared scalar kinds, whole tables, every
position table and aggregate, global partition, persisted aggregate, metadata, published view
and envelope. populated_fixture covers all 30 tables and 191 fields with explicit synthetic values;
these are wire fixtures, not relationally valid insert data. layer_records prepares exact
hex/length/SHA-256 records for future independent evaluation; none were generated in this round.
Digests and unsupported finite PostgreSQL limits remain UNRESOLVED.
The oracle imports no encoder/parser; tests import each side only to compare independently
constructed expectations. Round trip is supplemental. Scalar literals remain manual provenance.
SNAP-P01 prefix/partition membership, P02 metadata concatenation, P03 semantic view nullability,
P04 full-key ordering, P05 typed values are byte-compatible with 0.12 and require human decisions.
Any contrary decision needs an explicit version/compatibility plan and corresponding fixture changes.

## Requirement, evidence and dependency matrix

| Requirement / invariant | Implementation | Prepared test | Independent oracle | External dependency | Required evidence | Status | Blocker |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Native buffer and single-field limits | snapshot_transport_candidate admission refuses; SelectPlan documents named server cursor | test_no_driver_operation_even_if_cancellation_is_ignored | No connection method called | Pinned psycopg/libpq and enforceable pre-allocation guard | Native high-water, oversized-field and blocked-call evidence | BLOCKING_EXECUTION_REVIEW | Named cursor/fetchmany do not supply hard native byte bounds |
| Column/row/batch/table/total and call budget | Collector Budget, batch cap, call timeout minimum; admission before conn access | Collector boundary cases; resource scenario | Exact cap vs cap+1, no partial result | Approved numerical limits and guard | Complete size accounting and monotonic observations | MATERIALIZED_NOT_RUN | UNRESOLVED values; post-allocation checks not peak-memory proof |
| Cancel and cleanup | Disarmed adapter; collector preserves primary/cleanup exceptions | Fake timeout/loss/cleanup; CANCEL-IGNORED/CLEANUP-FAILURE plans | No valid output, primary retained, uncertain session quarantined | Independent cancellation/termination mechanism | Actual timeout, cancellation, rollback and close evidence | BLOCKING_EXECUTION_REVIEW | Cancellation request alone is not termination |
| MVCC consistency | Prepared connected harness C1/C2/C3 sequence | MVCC-UPDATE plan | Observer A; separate new observer B | Isolated DB, approved writer, scheduler | Snapshot IDs, commit acknowledgement, full rows | MATERIALIZED_NOT_RUN | Dispatch intentionally blocked; connected scheduler unavailable |
| Catalog and privilege drift | Collector exact checks and security digest; harness scenarios | SCHEMA-DRIFT, VIEW-DRIFT, PRIVILEGE-DRIFT, OWNER-SUPER | Rejection before valid data result | Isolated preconfigured fixtures/admin role | Actual catalog/ACL/role observations | MATERIALIZED_NOT_RUN | No DB fixture installed; no permissions approved |
| Partial/type/resource errors | Collector counts/width/PK/types; connected instrumentation plans | PARTIAL-READ, CONVERSION, RESOURCE-LIMITS | Reject missing/extra/invalid values, never coerce | Reviewed fault transport | End-of-stream, counts, sanitized type/error evidence | MATERIALIZED_NOT_RUN | Fake tests are not connected evidence |
| Complete typed table/partition/global/metadata/view/envelope oracle | Independent typed oracle and layer_records | test_fully_populated_typed_snapshot plus existing empty/multirow/multipartition cases | Independently built bytes and every SHA layer | Separate execution authority and independent reviewer | Frozen bytes/length/digests, provenance and review | UNRESOLVED | Source materialized, no output computed/frozen |
| NULL/Decimal/JSON/bytea/Unicode/key ordering | Independent scalar_fixture and negative cases | Oracle typed negatives plus existing literal tests | Literal/manual bytes, typed decoded values | Independent review | Actual byte comparison and error observations | MATERIALIZED_NOT_RUN | NOT_RUN |
| Wire vs Python vs PostgreSQL time | Existing temporal contract; POSTGRES-FINITE-EXTREMES vector | Wire endpoint negatives; DB extremes pending | Integer microseconds, finite stored values only | Exact pinned PostgreSQL bounds | Independent endpoint and timezone vectors | UNRESOLVED | No unsupported date extremes inferred |
| SNAP-P01..05 compatibility | Current wire unchanged; proposal matrix retained | Empty/typed/partition/metadata byte comparisons | Documented candidate layout | Human decision | Recorded approval or versioned alternative | PENDING_HUMAN_APPROVAL | No proposal promoted |

EXEC-G1 OPEN; PERS-G1 OPEN; PUB-T13B PENDING_HUMAN_APPROVAL.
No MIR availableAt/decisionTime reconciliation, supervisor or H05 activation is authorized.
