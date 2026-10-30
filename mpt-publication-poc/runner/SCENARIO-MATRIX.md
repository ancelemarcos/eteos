# Coverage matrix - candidate 0.9

## Current order v1.4 / candidate 0.16

Added candidate external review source: expected_bundle_emitter.py, frozen_bundle_compare.py,
test_expected_bundle_review.py. NOT_RUN; not registered with run.py or the eight-file capsule.
EXPECTED-REVIEW-MATRIX.md maps requirements to written tests and EXPECTED-SLOT-TRACEABILITY.md
maps all 428 slots. Zero filled/frozen/observed slots. No runtime/SQL scenario was executed.
Approval/authentication, schema/recipe/manifest/capsule drift, duplicates, incomplete expected
data and pending interpretations must reject before delayed observer access. Complete observed
differences are retained. Test approvals are explicitly simulated and have no authority.
EXEC-G1/PERS-G1 OPEN; PUB-T13B/SNAP-P01..05 PENDING_HUMAN_APPROVAL; A0 remains active.

## Order v1.3 / candidate 0.15 - independent freeze preparation

NOT_RUN. Current eight test names, inputs and required failures are in EXPECTED-REVIEW-MATRIX.md.
No new test or runtime code was required for this documentation-only preparation.

| Requirement | Artifact | Prepared comparison/test | Independent oracle | Dependency / evidence | State |
| --- | --- | --- | --- | --- | --- |
| Complete expected identities/slots | expected-bundle.template.json, EXPECTED-BUNDLE-SPEC | 428 slot IDs; exact 30 tables/191 fields/PK order check specified | Bound recipes and independent oracle only | Full emitter/serializer and reviewed bytes/hashes absent | EXPECTED_UNVERIFIED / UNRESOLVED |
| Freeze lifecycle and non-circular comparison | EXPECTED-BUNDLE-SPEC | GENERATE_EXPECTED / REVIEW_AND_FREEZE / COMPARE_FROZEN contracts | No encoder/parser accessible to expected generator | Independent human reviewer and frozen consumer needed | BLOCKING_EXECUTION_REVIEW |
| Five explicit interpretation decisions | SNAPSHOT-INTERPRETATION-REVIEW | Positive/negative cases and impact mapping | Candidate contract and independently derived bytes | Named semantic/codec reviewers and versioned decision | PENDING_HUMAN_APPROVAL |
| Eight-file capsule identity/admission | OFFLINE-CAPSULE-MANIFEST.json, isolated plan | Exact eight tests; no broad discovery | Frozen schema/recipes, manual literals | Final manifest hash external binding; exact environment/resource proof | DOCUMENTED / UNRESOLVED |
| Containment separate from codec | TRANSPORT-CONTAINMENT-DECISION | C-FIELD..C-CLEANUP proof matrix | Independent native/OS/session evidence | Separate driver/isolation authority; A0 retained | BLOCKING_EXECUTION_REVIEW |

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

## Order v1.1 / candidate 0.13 - current guarantees

This section supersedes earlier absence statements only for the newly authored candidate
adapter, harness and typed oracle. No native transport or connected execution is operational.
See TRANSPORT-AND-CONNECTED-VALIDATION.md for driver sources, responsibilities and checkpoints.

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

## Order v1.0 / candidate 0.12 - nonexecuted test mapping

| Scenario | Authored code / documentary arrangement | Required result | Status |
| --- | --- | --- | --- |
| CODEC-10-BYTES | test_snapshot_conformance scalar/table cases | Independent exact bytes, length, typed decode; round-trip supplemental | MATERIALIZED_NOT_RUN |
| CODEC-10-COMPOUND | independent snapshot_oracle + empty/multiple partitions | Every table and hash layer equal independently derived expectation | MATERIALIZED_NOT_RUN; frozen digests UNRESOLVED |
| CODEC-10-CORRUPTION | truncated header/payload, unknown tag/version/type, duplicate/missing fields/PK, metadata inventory | Reject malformed input without coercion | MATERIALIZED_NOT_RUN |
| COL-10-BOUNDS | test_each_budget_boundary; bounded fetch overflow | Exact boundary accepted; +1 and total deadline rejected | MATERIALIZED_NOT_RUN |
| COL-10-CONVERT | strict type/finite/JSON depth/Decimal expansion cases | Reject lossy or oversized conversion | MATERIALIZED_NOT_RUN |
| COL-10-CLEANUP | fake TimeoutError/ConnectionError/KeyboardInterrupt; failing rollback and close | Preserve primary error, attach both cleanup failures; cleanup-only failure blocks result | MATERIALIZED_NOT_RUN |
| COL-10-PRIV / DRIFT | Existing COL-09-PRIV/DDL plus global grant/extension/catalog digest mutations | Fail closed under each direct/PUBLIC/membership/owner/RLS drift case | DOCUMENTED; connected harness BLOCKING_EXECUTION_REVIEW |
| COL-10-CONCURRENT / PARTIAL | Existing COL-09-UPDATE/PARTIAL with count before fetch and row widths/PK | One MVCC state, reject incomplete stream | DOCUMENTED; connected harness BLOCKING_EXECUTION_REVIEW |
| COL-10-NATIVE-BOUNDS | Real guard oversized field/native buffer/blocked socket/cleanup fault | Enforce approved memory/deadline before allocation/blocking, no partial result | UNRESOLVED / BLOCKING_EXECUTION_REVIEW |

No module imported, tests discovered/run, SQL executed or guard installed. Fake transport code
is laboratory source only; it cannot establish real PostgreSQL privilege or concurrency behavior.

## Order v0.9 / candidate 0.11 - deterministic future collector scenarios

All rows DOCUMENTED / NOT_RUN; missing enforcement is BLOCKING_EXECUTION_REVIEW.
These checkpoints are documentary injection boundaries, not installed hooks or H05 changes.
Prerequisites for every connected case: separately approved environment, dedicated reader,
complete schema/view manifest, independent immutable before-state, no unrelated writers,
approved bounds and explicit execution authorization. Outcomes below are required oracles.

| ID | Arrangement / checkpoint | Expected oracle and evidence |
| --- | --- | --- |
| COL-09-DDL | At C0 before BEGIN, deliberately change one column type/order/nullability/PK or approved view definition; separate case during catalog scan | Reject mismatched catalog/definition; no result. During scan DDL must wait on held locks or fail boundedly; quiescence violation invalidates run even if bytes agree |
| COL-09-UPDATE | C1 establish snapshot by observation; second approved session commits known value B replacing A before data scan C2 | Collector consistently returns A for every affected relation/view; new independent observer sees B. Never compare whole hashes across different provenance as proof |
| COL-09-TIME | At C2 hold relation lock past lock budget; separate slow read past statement/total budget | Abort within approved budget plus cleanup bound, no partial result; record actual exception/SQLSTATE rather than assume one |
| COL-09-INTERRUPT | C2 after first relation, inject cancellation using future approved harness | No result; rollback/close attempts observed; original cancellation and cleanup errors both retained |
| COL-09-LOSS | C2 sever approved synthetic connection after first relation | No snapshot output; connection unusable; independent server/session evidence required before rollback completion claim |
| COL-09-PARTIAL | C2 driver yields row with missing/extra field or deliberately incomplete relation stream | Reject width/completion failure, never zip-truncate; a silently lying driver cannot be detected by row cap alone, trusted transport/completeness evidence required |
| COL-09-CONVERT | C2 inject float numeric, bool integer, invalid JSON duplicate/nonfinite, NULL required, fractional timestamp | Reject without coercing precision/type or publishing partial rows |
| COL-09-BYTES | C2 exact cap then cap+1 for value/relation/whole snapshot; many small rows and one large field | Boundary accepted only under all other predicates; cap+1 rejects before unbounded retention; driver buffering evidence required |
| COL-09-PRIV | C0 independently add each prohibited direct/PUBLIC/inherited privilege | Reject before data publication; audit other-schema privileged function and SET ROLE paths |
| COL-09-DISABLED | C0 enabled absent/false, or false approval | No connection method touched; external caller closes its dedicated connection |
| CODEC-09-ORACLE | Fixed independent vector inputs with source/derivation/reviewer | Exact bytes/length/typed decode and all hash layers match only after independently authorized evaluation; unresolved oracles block conclusion |

Coverage: A1 field map; A2 SNAP-P01..05; A3/A4 compound vector provenance; A5/C1..3
addendum and negative cases; B1..5 safety matrix and COL-09 cases. No scenario is registered as
executed, no successful database observation is supplied, and no existing runner invokes these cases.

CANDIDATE_EDIT_ONLY / NOT_RUN. Supersedes 0.5 coverage descriptions.
Implementation: runner/run.py (R), runner/coverage_controls.py (C).
All rows marked M are MATERIALIZED_NOT_RUN. No SQL, Python or tests were executed.
Every run starts from a fresh approved schema, F0/F1 and a valid publisher lease.
JSONL logs SQL/parameters, backend IDs, actual role inventories, checkpoints, SQLSTATE,
commits and oracle comparisons under the verified manifest/config/environment header.

| Scenario | Impl / role | Checkpoint, operation and failure | Unique expected oracle / evidence | Status |
| --- | --- | --- | --- | --- |
| SESSION-BEFORE-COMMIT | C / publisher; owner controller | TP changes pending, before commit; terminate actual backend, confirm absent, reconnect | Frontier0 after termination, one publication after retry; full rows unchanged on second retry | MATERIALIZED_NOT_RUN |
| SESSION-AFTER-COMMIT | C / publisher; owner controller | TP commit acknowledged, terminate backend, reconnect/retry | Frontier remains1; no duplicate mutation/audit on second retry | MATERIALIZED_NOT_RUN |
| LEASE-LIFECYCLE | C / publisher | Renew, release, hold claimant transaction; observe contender blocked; commit winner; short lease abandonment; poll actual DB expiry; stale attempts | Expiry extended, loser rejected P0001, increasing epochs, expired renewal/old token rejected; recovered TP frontier1 | MATERIALIZED_NOT_RUN |
| COMPOUND-ROLLBACK | C / publisher; owner fault controller | FB23 after B1; injected projection CHECK fails after batch/barrier updates; 23514; remove fault, retry | All stored rows unchanged after failed TP, frontier/projection1; retry frontier2/projection3 | MATERIALIZED_NOT_RUN |
| ACK-NEGATIVE | C / dispatcher; owner synthetic call producer | No auth; auth without call/receipt; call without receipt; ACK each stage | P0001 and identical full content after each rejected ACK | MATERIALIZED_NOT_RUN |
| T2-SAME-TRANSACTION | C / evaluator | Capture plus attempt without commit, then corrected split | P0001; complete rollback; committed capture then attempt1/cut1/version1 | MATERIALIZED_NOT_RUN |
| IMMUTABLE-NEGATIVE | C / writer | Published B1/BR1, blocked B2, completed attempt/result/auth/receipts; denied UPDATE/DELETE; restricted INSERT and frozen member INSERT | 42501 or P0001 as specified in C; full-row snapshot identical after EACH negative | MATERIALIZED_NOT_RUN (bounded matrix) |
| DELIVERY-FORGE-01 | R / writer, owner trigger exception | Privileged initial INSERT denied; legitimate FNOTICE | 42501/P0001, no public/delivery effects; READY/PENDING | MATERIALIZED_NOT_RUN |
| T4-ACK-AUTH | R / dispatcher | Simulated lost AUTHORIZE reply; close; identical/divergent replay; fresh recheck | Original reply, one operation receipt/audit, collision P0001, then suppression with zero calls | MATERIALIZED_NOT_RUN |
| T4-ACK-RECHECK | R / dispatcher | Same schedule for RECHECK | Historical reply never replaces fresh check; auth1/calls0/receipts0 | MATERIALIZED_NOT_RUN |
| T2-TP-FK-CYCLE | R / evaluator/publisher | T2a commit; TP locks; T2b wait observed; release TP | Attempt completes using cut/version1 | MATERIALIZED_NOT_RUN |
| concurrent_cut | R / two evaluators, publisher | Concurrent capture UNIQUE wait; persist two attempts; publish v2 afterward | Attempts2/distinctcut1/version1, historical read remains1 | MATERIALIZED_NOT_RUN |
| FIXED-CUT | R / evaluator/publisher | Publish v2 between two READ COMMITTED reads at same cut | Both resolve version1 | MATERIALIZED_NOT_RUN |
| blocked_recovery | R / recovery/writer/publisher | Block B2, reject child mutation/skip, recover twice, publish | Content/fingerprint unchanged; one recovery; frontier3/projection3 | MATERIALIZED_NOT_RUN |
| compound | R / publisher | Publish successful ordered [v2,v3] | Frontier2/projection3 | MATERIALIZED_NOT_RUN |
| stale_worker | R / publisher | Release, replace epoch; old/incorrect token rejected | P0001 then one publication | MATERIALIZED_NOT_RUN |
| concurrent_publish | R / two publishers | Actual lock dependency before first commit | Both return ordinal1; frontier1 | MATERIALIZED_NOT_RUN |
| ack_loss | R / dispatcher; owner sink | Simulated dropped response after synthetic destination commit | Two calls, one logical deduplicated receipt | MATERIALIZED_NOT_RUN |
| POC-T24 | R / dispatcher/publisher | Close published before AUTHORIZE | SUPPRESSED; auth0/calls0/receipts0 | MATERIALIZED_NOT_RUN |
| HOLD-PENDING-CLOSE | R / dispatcher/writer | Close pending before AUTHORIZE | HOLD_PENDING_CLOSE; auth0/calls0/receipts0 | MATERIALIZED_NOT_RUN |
| t25a / POC-T25A | R / dispatcher | Auth committed, close before fresh recheck | SUPPRESSED_AFTER_AUTHORIZATION; auth1/calls0/receipts0 | MATERIALIZED_NOT_RUN |
| t25b / POC-T25B | R / dispatcher; owner sink | Close after final recheck, then prior authorized send | ACKED; auth1/calls1/receipts1 | MATERIALIZED_NOT_RUN |
| t13a / PUB-T13A | R / recovery/dispatcher | Revoke before authorization | SUPPRESSED; auth0/calls0/receipts0 | MATERIALIZED_NOT_RUN |
| notify | R / evaluator/writer/publisher | Split T2 then T3 identical/divergent retries, TP | NOTIFY with one intent; pending becomes published | MATERIALIZED_NOT_RUN |
| quiet | R / evaluator/writer/publisher | Same with no alert decision | DO_NOT_NOTIFY with no notification/outbox; result still published | MATERIALIZED_NOT_RUN |
| privileges | R / reader/writer | Base-table, TP, projection and truncate denials | 42501; reader sees published view | MATERIALIZED_NOT_RUN |
| t13b / PUB-T13B | R / no SQL | Stops before sessions | NOT_RUN; requires human policy approval | BLOCKING_EXECUTION_REVIEW |

## Directed controls added in 0.6

All implementations below are in runner/coverage_controls.py; preconditions are notice fixture,
published B1 and approved T4 lease. M means MATERIALIZED_NOT_RUN, never PASS.
Individual transaction boundaries, actual roles and statements appear in JSONL, with snapshot
equality, exact SQLSTATE and call/receipt counts as the deterministic oracles.

| Identifier | Transaction / role | Checkpoints and failure | Oracle / evidence | Status |
| --- | --- | --- | --- | --- | --- |
| T4-BACKEND-AUTHORIZE-BEFORE | T4 AUTHORIZE / dispatcher; trusted owner terminator | After SQL, before COMMIT; terminate backend, confirm absent, reconnect/retry | Original rows restored; retry creates exactly one auth/operation audit/receipt; fresh close recheck suppresses with calls0 | MATERIALIZED_NOT_RUN |
| T4-BACKEND-AUTHORIZE-AFTER | Same | Commit then terminate backend; reconnect/replay | Historical reply and full state stable; one operation audit/receipt; fresh recheck required | MATERIALIZED_NOT_RUN |
| T4-BACKEND-RECHECK-BEFORE | T4 RECHECK after BASE auth / dispatcher | Before recheck commit, terminate backend | Original auth survives, recheck audit rolled back; retry audit/receipt1; no call | MATERIALIZED_NOT_RUN |
| T4-BACKEND-RECHECK-AFTER | Same | After recheck commit, terminate/reconnect | Replay no new audit; close then fresh check gives SUPPRESSED_AFTER_AUTHORIZATION/auth1/calls0/receipts0 | MATERIALIZED_NOT_RUN |
| T4-LEASE-LIFECYCLE | T4 lease and delivery transactions / dispatchers | Renewal, lock-observed contender, DB expiry, takeover, stale authorize/recheck/ACK | Increasing epoch, stale P0001, fresh PRE-SEND then ACKED/auth1/calls1/receipts1 | MATERIALIZED_NOT_RUN |
| ACK-RECEIPT-NO-CALL | T4 ACK / dispatcher; owner fixture | Auth and receipt committed, no call | P0001; full-state equality; auth1/calls0/receipts1 | MATERIALIZED_NOT_RUN |
| WRITER-DELIVERY-BYPASS | Each negative isolated / writer | Privileged INSERT/UPDATE/DELETE, SET ROLE owner/dispatcher, delivery function bypass | 42501 and full-state equality after every attempt | MATERIALIZED_NOT_RUN |
| PROCESS-WORKER-AFTER-COMMIT | Proposed external worker transaction / dispatcher child, isolated supervisor | Non-operational worker_controller_stub.py; run.py blocks before sessions; future kill after COMMITTED IPC/restart | Required: actual child exit/new identity, audit1/auth1, calls0, fresh recheck; operational controller absent | BLOCKING_EXECUTION_REVIEW |
| COMPOUND-MEMBER-SEAM | Single TP / publisher | No mutable member stage exists; reviewed instrumentation decision needed | Required: fail after first internal member, all rows/cuts/frontier unchanged, retry single publication | BLOCKING_EXECUTION_REVIEW |

## Remaining dependencies

External worker process controller/IPC/isolation and literal compound member seam are not
materialized. SCOPE-PROPOSAL.md specifies the verifiable prerequisites and does not waive them.
Whole-server crash/restart and real-provider behavior are OUT_OF_SCOPE_PROPOSED for a proposed
functional minimum, never approved exclusions. Environment freeze (exact versions/digests,
signature trust, collector freshness/clock tolerance, role inventories and controller privileges)
is unresolved and BLOCKING_EXECUTION_REVIEW.

The adversarial matrix enumerates selected protected fields and privileges; it does not prove
all payload combinations or defend against trusted owner/superuser DDL. Freezing that threat
boundary requires review. Raw network-disconnect and ACK-phase backend crash schedules are
not materialized; backend AUTHORIZE/RECHECK boundary tests do not imply their coverage.
PUB-T13B remains PENDING_HUMAN_APPROVAL: proposed pre-call revocation suppression preserves
historical authorization, but is not accepted or executable.

REQUIRES_HARDENING / NOT_RUN. EXEC-G1/PERS-G1 OPEN.


## Version 0.7 entry-point and oracle reconciliation

All active rows above are MATERIALIZED_NOT_RUN, never observed PASS. Each scenario inherits
fresh prepared schema, F0/F1, approved leases/roles and completed preflight as prerequisites.
BLOCKING_EXECUTION_REVIEW rows below refuse before connections even if listed as approved.

| Identifier | Implementation / role | Transaction/checkpoint/failure | SQLSTATE and deterministic oracle | Required evidence / status |
| --- | --- | --- | --- | --- |
| PROCESS-WORKER-BEFORE-COMMIT | run.py refusal + worker_controller_stub.py; no runtime role | Future dispatcher child OPEN transaction IPC, terminate owned child, confirm rollback, restart | N/A for current refusal; future full-row rollback hash, then auth/audit/receipt1 and calls0 after recovery | NOT_RUN/BLOCKING_EXECUTION_REVIEW; child identity/handle/isolation/IPC/exit/hash proof absent |
| PROCESS-WORKER-AFTER-COMMIT | Same | Future COMMITTED IPC, actual child exit, restart/replay | N/A for refusal; future identical full-row replay hash and one logical audit/receipt, fresh check | NOT_RUN/BLOCKING_EXECUTION_REVIEW; no executable supervisor |
| COMPOUND-MEMBER-SEAM | run.py refusal; SCOPE-PROPOSAL pending design | Single TP; proposed after first ordered validation before batch update; no per-member commit | N/A for refusal; injection SQLSTATE pending; unchanged rows/cut/frontier/projection then retry one ordinal/v3 | NOT_RUN/BLOCKING_EXECUTION_REVIEW; approved seam/equivalence/oracle absent |

For existing controls: expected runtime privilege denials are 42501; state/fencing/identity/
ACK/T2 negatives are P0001; projection fault is 23514. Successful operations have SQLSTATE
N/A (no exception). Backend termination is verified by successful controller result and absent
pg_stat_activity PID; no client exception code is fabricated as the oracle. Any unexpected
SQLSTATE fails its negative. Every statement/result/checkpoint/commit and full-state comparison
is logged under verified provenance; no elapsed sleep establishes concurrency.
Full-row comparisons in existing controls remain equality comparisons, not claimed canonical
process-evidence hashes. The latter encoding is explicitly pending for future worker controls.

No runtime privilege in the current schema enables the proposed member hook. The candidate
policy does not accept arbitrary PID/command/SQL hook inputs. ENVIRONMENT-FREEZE.md is the
mandatory current evidence checklist; all unresolved values block before initial fixtures.


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

| Documentary fixture / contract | Preconditions / transactions / role | Checkpoint and oracle | Actual implementation / status |
| --- | --- | --- | --- |
| H01-CTRL@1 / PROCESS-WORKER-BEFORE-COMMIT | Approved owned-child capability/IPC; dispatcher child OPEN auth transaction; independent observer | Confirm actual child and backend exit; complete snapshot rollback; restart one auth/audit/receipt, calls0 | Stub refuses; BLOCKING_EXECUTION_REVIEW |
| H01-CTRL@1 / PROCESS-WORKER-AFTER-COMMIT | Same; committed auth/audit/receipt then child exit | Same ID replay unchanged; fresh recheck before any call | Stub refuses; BLOCKING_EXECUTION_REVIEW |
| SNAP-ROLLBACK-1 | Same-snapshot read-only observer, no unrelated writers, auth uncommitted then confirmed rollback | All table/global/public hashes identical | Documentary fixture only; BLOCKING_EXECUTION_REVIEW |
| SNAP-ACK-LOSS-1 / SNAP-REPLAY-1 | Committed op then same ID retry, no lease renewal between observations | Only declared initial delta; replay full-state equality | Canonical encoder absent; BLOCKING_EXECUTION_REVIEW |
| SNAP-DIVERGENCE-1 | Changed payload at existing operation ID | P0001, complete digest equality | Existing retry negative exists; new canonical oracle absent; BLOCKING_EXECUTION_REVIEW |
| SNAP-CONTENT-1 / SNAP-ORDER-1 / SNAP-TYPES-1 | Independent encoded fixtures; no DB mutation required | Content/types differ; scan-order permutation equal | Documentary reference vectors only; BLOCKING_EXECUTION_REVIEW |
| H05-SEAM-PENDING / COMPOUND-MEMBER-SEAM | Approved complementary decision and trusted lab fault fixture; B23 v2/v3 inside one TP | Proposed PZ501 after v2 before v3; rollback hashes/public view unchanged; retry one ordinal/projected v3 | Design only, entry point blocked; BLOCKING_EXECUTION_REVIEW |

All new rows require future evidence bound to manifest/config/runtime/role and actual process
identity. No numeric expected digest, successful observation or approval is fabricated.
Existing MATERIALIZED_NOT_RUN rows remain authored controls, not equivalent implementations
of these new contracts. Proposed scope exclusions remain OUT_OF_SCOPE_PROPOSED.


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

| Requirement / scenario | File / function | Prerequisite / independent oracle | Implementation and limit | Status |
| --- | --- | --- | --- | --- |
| MPT-SNAPSHOT@1 / SNAP-TYPES-1 | snapshot_codec.scalar; snapshot_reference.scalar | Exact typed supplied inputs; hand-derived snapshot_vectors bytes/decoded tuples | Pure encoder and independently written parser, no execution | MATERIALIZED_NOT_RUN |
| MPT-SNAPSHOT@1 / SNAP-ORDER-1 | snapshot_codec.rows_bytes/table_bytes; reference.table | Manifest-approved schema, unique PKs; documentary permutation oracle | Stable byte ordering and schema checks authored; full independent table vectors missing | BLOCKED |
| MPT-SNAPSHOT@1 / SNAP-CONTENT-1 | snapshot_codec.snapshot | All30 tables/view from one future MVCC snapshot; independent content-delta oracle | Hash layers authored, interpretations need approval/compound vectors | BLOCKED |
| SNAP-ROLLBACK/ACK-LOSS/REPLAY/DIVERGENCE | FULL-SNAPSHOT-CONTRACT + CODEC-MATERIALIZATION | Future approved observer, actual checkpoint/SQLSTATE, immutable complete inputs | No collector/integration or actual hashes produced | DOCUMENTED |
| H01-CTRL@1 / CTRL-IDENTITY/IPC | worker_identity.validate_identity/validate_checkpoint | Reference expected identity, capability object, nonce/sequence/time; documentary rejection matrix | Consistency only, cannot prove OS authentication | MATERIALIZED_NOT_RUN |
| H01-CTRL@1 / CTRL-RESTART | worker_identity.validate_restart | Same run/artifacts, new generation/creation/nonce/token | No process actions; future OS exit/spawn proof absent | MATERIALIZED_NOT_RUN |
| H05-SEAM-PENDING | INTRABATCH-SEAM-PROPOSAL equivalence analysis | Accepted complementary decision and no-fault/fault independent oracles | SQL and publication functions unchanged | DOCUMENTED |
| Process/collector/seam execution | unchanged worker_controller_stub and run.py blocks | Separate isolation/capability/environment/implementation/execution approvals | No activation possible from these new modules | BLOCKED |

File/hash checks, source materialization and experimental evidence are separate: first two
occurred, experimental evidence does not exist. Existing MATERIALIZED_NOT_RUN scenarios retain
prior bounded meanings and do not prove new canonical-hash/process contracts.


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

| New/revised control | Implementation / prerequisite | Independent oracle | Status |
| --- | --- | --- | --- |
| CODEC-FIELD-MAP | Conformance matrix +30-table schema | Current DDL text, wire rules and manual vectors | DOCUMENTED |
| CODEC-COMPOUND | snapshot_compound_vectors.json | Manual frame lengths/order; expected hashes UNRESOLVED | MATERIALIZED_NOT_RUN / UNRESOLVED digests |
| COLLECTOR-DISABLED | snapshot_collector.collect, enabled=false/default | No connection method should be touched | MATERIALIZED_NOT_RUN; acceptance BLOCKED |
| COLLECTOR-CATALOG | Approved dedicated read role/schema/manifest/config | Exact name/type/null/PK/version plus view hash mismatch refusal | MATERIALIZED_NOT_RUN; acceptance BLOCKED |
| COLLECTOR-MVCC | One read-only repeatable-read snapshot; concurrent publisher | All observations from one MVCC snapshot, never mixed states | DOCUMENTED / BLOCKED until authorized independent execution |
| COLLECTOR-FAILURE | Approved caps/timeouts and injected mid-read failure | No partial result, rollback/close, no application mutation | DOCUMENTED / BLOCKED |
| WORKER-TYPE-REPLAY | worker_identity.validate_identity/restart | generation true versus1 rejects; replay/identity mismatch rejects | MATERIALIZED_NOT_RUN |

No existing runner scenario invokes the collector. Query exceptions are future SQLSTATE
evidence only; no successful/error database result is supplied in this round. Full collector
validation, exact finite timestamp oracles and composite digest oracles remain BLOCKED.
