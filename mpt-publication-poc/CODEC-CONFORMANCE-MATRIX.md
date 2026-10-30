# Codec conformance matrix - candidate 0.10 / order v0.8

## Order v1.3 / candidate 0.15 - expected versus observed

EXPECTED-BUNDLE-SPEC.md defines typed bundle identity, completeness and freeze/comparison
interfaces. EXPECTED-REVIEW-MATRIX.md maps every fixture family/layer and all eight offline tests.
The 428-record template is EXPECTED_UNVERIFIED; unresolved expected outputs are explicit.
Current dynamic oracle tests do not consume REVIEWED_FROZEN data. No equivalence claim.

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

## Order v1.0 / candidate 0.12 - source/test coverage

Current state MATERIALIZED_NOT_RUN. Existing 30-table/191-column field map retained; schema/DDL
unchanged. SNAPSHOT-DECISION-ADDENDUM now maps each proposal to evidence, wire effect and
pending human decision. Wire int64, actual PostgreSQL finite range and Python datetime remain
distinct; exact PostgreSQL extreme oracles UNRESOLVED.

| Requirement | Materialized artifact / expected assertion | Remaining evidence |
| --- | --- | --- |
| Independent empty/multirow/partition/aggregate/envelope oracle | snapshot_oracle.py, no codec import; exact byte comparison in test_snapshot_conformance | Not executed; hashes derived only by future authorized oracle run; HUMAN_APPROVAL |
| Typed values / byte equality / round trip | test_scalar_bytes_and_decoding; test_nested_json_independent_bytes; table round trip | Literal/manual expected values, no successful observation |
| PK / NULL / unknown fields/version/length / corruption | permutation, absent/extra/duplicate/NULL rows, unknown type/version, truncated frames | Negative tests authored, NOT_RUN |
| Partition and metadata | oracle.fixture_snapshot; reference.aggregate/metadata/envelope; full empty and multiple partition test | Independent complete bytes/digest freeze UNRESOLVED |
| Temporal/Decimal/JSON/Unicode/bytea | manual scalar literals and rejection cases, collector strict conversion | DB boundary/timezone extreme execution UNRESOLVED |
| Collector bounds / cleanup | test_snapshot_collector fake transport budget/timeout/cancellation/cleanup cases | Fake tests not executed; no proof about real driver |
| Privilege/catalog/concurrency | expanded collector and COL-09 connected scenario contract | Connected fault harness and approved guard absent, BLOCKING_EXECUTION_REVIEW |

The independent oracle supports only declared empty/text/NULL compound fixtures; it must reject
other fixture scalar kinds rather than silently infer representations. No SUT output is persisted
as expected data. Aggregate parser shares no encoder helper. Supplemental round trips alone
cannot establish conformance. Standalone codec/reference recursion/allocation policies and exact
error-class parity remain gaps; the collector's bounded-input contract does not approve arbitrary
untrusted pure-codec input.

## Order v0.9 / candidate 0.11 - renewed static comparison

DOCUMENTED, not database conformance evidence. Textual comparison against current schema.sql
and runner/delivery-api.sql found no differences for 30 tables / 191 columns: exact ordered
names, canonical type (timestamptz maps to timestamp with time zone), nullable flags with
PK-implied nonnull, and ordered PK components. Every field in the existing matrix was included.
FULL-SNAPSHOT-CONTRACT inventory and PK order agree. No SQL was executed.

published_positions was separately inspected: eight projected columns in declared order;
position_id/version/lifecycle/side/remaining_quantity/average_entry_price from position_revision,
domain_id/ordinal from publication_batch. ordinal is nullable in the base descriptor; its
semantic nonnull view guarantee depends on PUBLISHED predicate plus the table CHECK.
Catalog view-nullability equality is deliberately not asserted. See SNAP-P03.

| Rule / source | Artifact / vector | Expected documentary result | Gap |
| --- | --- | --- | --- |
| Full field inventory / DDL + FULL-SNAPSHOT-CONTRACT | snapshot_schema.json; existing 191 field rows | Exact column/type/null/PK order | Actual catalog not observed |
| Partition / SNAP-P01 | codec.table_bytes, snapshot; PARTITION-P-A, MULTI-PARTITION | v,p prefix; independent partition isolation | Full byte/digest oracle UNRESOLVED |
| Metadata / SNAP-P02 | snapshot; FULL-EMPTY-AGGREGATE | Four full normal-version table streams | Independent digest UNRESOLVED |
| View / SNAP-P03 | collector, codec.snapshot | Eight semantic nonnull columns | Server definition hash/privileges UNRESOLVED |
| Ordering / SNAP-P04 | rows_bytes, reference.table; PK-ADVERSARIAL | a,b,aa; three rows, 288 bytes | Executed decode/hash unavailable |
| Values / SNAP-P05 | scalar/reference.scalar; scalar and negative cases | Exact typed bytes, no normalization/float | Human review pending |
| Temporal domains / addendum | TIMESTAMP-WIRE-BOUNDARIES, TIME-OUTSIDE-DATETIME | Wire checks distinct from DB/date library domain | Exact finite PostgreSQL oracle UNRESOLVED |
| Independent evidence / order A4 | per-vector provenance | Manual derivation and human review separate from execution | Parser has no aggregate/envelope decoding |
| Safety / order B | design; COL-09 cases | Fail closed, bounded complete collection | Byte/total-time bounds and privilege closure not implemented |

SNAPSHOT-DECISION-ADDENDUM.md submits five explicit interpretations for approval, without
changing wire version or accepted contracts. Error class parity, nested JSON/Decimal resource
bounds, full hex/digest oracles and runtime collection remain BLOCKING_EXECUTION_REVIEW.

MATERIALIZED_NOT_RUN source; overall conformance BLOCKED; no experimental evidence.
Baseline 0.9 manifest actually available; measured SHA-256
efe504ff8382cc6b71e956aa67ae22af1fb9f0ff44e9815325492c33eca5395b,
equal to previously reported value. All 30 listed artifact hashes matched. This is local
byte verification, not independent third-party conformance validation.

## Resolved candidate byte rules

The following resolves prior ambiguities for candidate review; it is not an accepted production ADR.
- Every field is F(tag,8-byte unsigned big-endian length,payload); no absent field is encoded.
  Missing/extra columns reject. SQL NULL is N+empty; empty text T+empty; bytea Y+empty;
  integer zero I+"0"; false B+"0"; JSON null J+n+empty remain distinct.
- Position partition table and combination streams start F(v,POSITION-version),F(p,position_id).
  Position metadata is NOT separately appended to the final envelope: it is auxiliary, while
  complete persisted-table digest is authoritative and covers the same application rows.
- Metadata digest covers concatenated FULL normal-version streams of publication_barrier,
  publication_batch, publication_cut, public_projection in sorted qualified-name order.
- View wire schema is the eight specified columns with semantic NOT NULL and key position_id.
  Actual view catalog nullability is not used as base-table nullability evidence; collector
  checks actual view shape, separately approved pg_get_viewdef hash and every returned value.
- Table order: unsigned UTF-8 qualified names. Row order: full F(k,PK frames) including length;
  JSON object key order: unsigned raw UTF-8 bytes. Neither rule is event chronology.
- Decimal coefficient and stored scale retained, including 1.0 versus1.00; negative numeric
  zero sign normalized only because stored SQL numeric has no independent negative-zero identity.
  JSONB parsed from stored text losslessly, no float; original duplicate keys/whitespace already lost.
- Time wire uses signed UTC microseconds from1970. No datetime.timestamp float or ms truncation.
  DB source precision is at most stored precision; pre-storage loss/timezone spelling cannot be
  recovered. Exact finite PostgreSQL date extremes require pinned build validation, UNRESOLVED;
  current codec guards broad int64 wire domain and rejects infinities, not full DB-calendar validity.

## Field-by-field map

Source: actual manifest-bound DDL plus snapshot_schema.json. Order is the row scalar ordinal,
PK number is the key component order; all descriptor names/types/nullability are hash inputs.
Error labels below are DOCUMENTATION labels, not newly persisted domain enums.
E-TYPE/E-RANGE/E-NULL/E-NONFINITE/E-JSON = ValueError; E-UTF8 may be UnicodeError.
E-SCHEMA = wrong/missing/extra field, metadata or PK, ValueError/CollectionBlocked.
Every field also inherits E-SCHEMA; no silent omission/default/coercion is allowed.

| Table.field | Order | PostgreSQL type | Nullable | PK order | Wire | Precision / representation | Reject |
| --- | --- | --- | --- | --- | --- | --- | --- |
| publication_domain.domain_id | 1 | text | NO | 1 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| publication_domain.policy_version | 2 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| publication_barrier.domain_id | 1 | text | NO | 1 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| publication_barrier.committed_ordinal | 2 | bigint | NO | — | I | signed int64 decimal | E-TYPE/E-RANGE/E-NULL |
| recipient_guard.tenant_id | 1 | text | NO | 1 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| recipient_guard.owner_id | 2 | text | NO | 2 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| recipient_guard.access_version | 3 | bigint | NO | — | I | signed int64 decimal | E-TYPE/E-RANGE/E-NULL |
| recipient_guard.access_allowed | 4 | boolean | NO | — | B | ASCII 0/1, distinct from integer | E-TYPE/E-NULL |
| position.position_id | 1 | text | NO | 1 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| position.domain_id | 2 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| position.tenant_id | 3 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| position.owner_id | 4 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| position.instrument_label | 5 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| position.persisted_version | 6 | bigint | NO | — | I | signed int64 decimal | E-TYPE/E-RANGE/E-NULL |
| position_guard.position_id | 1 | text | NO | 1 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| position_guard.pending_close_command | 2 | text | YES | — | T or N | UTF-8 exact, no normalization | E-TYPE/E-UTF8 |
| command_receipt.tenant_id | 1 | text | NO | 1 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| command_receipt.owner_id | 2 | text | NO | 2 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| command_receipt.command_id | 3 | text | NO | 3 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| command_receipt.position_id | 4 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| command_receipt.actor_id | 5 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| command_receipt.action | 6 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| command_receipt.expected_position_version | 7 | bigint | YES | — | I or N | signed int64 decimal | E-TYPE/E-RANGE |
| command_receipt.expected_plan_version | 8 | bigint | YES | — | I or N | signed int64 decimal | E-TYPE/E-RANGE |
| command_receipt.canonical_payload | 9 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| command_receipt.fingerprint | 10 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| command_receipt.response_code | 11 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| command_receipt.response_payload | 12 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| publication_batch.position_id | 1 | text | NO | 1 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| publication_batch.batch_id | 2 | text | NO | 2 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| publication_batch.domain_id | 3 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| publication_batch.origin_type | 4 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| publication_batch.origin_id | 5 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| publication_batch.fingerprint | 6 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| publication_batch.publication_status | 7 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| publication_batch.ordinal | 8 | bigint | YES | — | I or N | signed int64 decimal | E-TYPE/E-RANGE |
| publication_batch.failure_reason | 9 | text | YES | — | T or N | UTF-8 exact, no normalization | E-TYPE/E-UTF8 |
| publication_batch.content_frozen | 10 | boolean | NO | — | B | ASCII 0/1, distinct from integer | E-TYPE/E-NULL |
| publication_batch.state_version | 11 | bigint | NO | — | I | signed int64 decimal | E-TYPE/E-RANGE/E-NULL |
| publication_cut.cut_id | 1 | text | NO | 1 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| publication_cut.domain_id | 2 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| publication_cut.ordinal | 3 | bigint | NO | — | I | signed int64 decimal | E-TYPE/E-RANGE/E-NULL |
| publication_cut.resolution_policy_version | 4 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| publication_cut.frontier_position_id | 5 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| publication_cut.frontier_batch_id | 6 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| publication_cut.capture_transaction | 7 | xid8 | NO | — | X | unsigned int64 decimal | E-TYPE/E-RANGE/E-NULL |
| position_event.position_id | 1 | text | NO | 1 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| position_event.event_id | 2 | text | NO | 2 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| position_event.command_id | 3 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| position_event.event_type | 4 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| position_event.correction_of | 5 | text | YES | — | T or N | UTF-8 exact, no normalization | E-TYPE/E-UTF8 |
| position_event.recorded_at_observed | 6 | timestamp with time zone | NO | — | Z | exact UTC integer microseconds, no float | E-TYPE/E-RANGE/E-NONFINITE/E-NULL |
| position_event.user_reported_execution_at | 7 | timestamp with time zone | YES | — | Z or N | exact UTC integer microseconds, no float | E-TYPE/E-RANGE/E-NONFINITE |
| position_revision.position_id | 1 | text | NO | 1 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| position_revision.version | 2 | bigint | NO | 2 | I | signed int64 decimal | E-TYPE/E-RANGE/E-NULL |
| position_revision.predecessor_version | 3 | bigint | YES | — | I or N | signed int64 decimal | E-TYPE/E-RANGE |
| position_revision.event_id | 4 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| position_revision.batch_id | 5 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| position_revision.lifecycle | 6 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| position_revision.side | 7 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| position_revision.remaining_quantity | 8 | bigint | NO | — | I | signed int64 decimal | E-TYPE/E-RANGE/E-NULL |
| position_revision.average_entry_price | 9 | numeric | NO | — | D | exact coefficient:stored-scale, finite Decimal | E-TYPE/E-NONFINITE/E-NULL |
| position_revision.last_confirmed_at_observed | 10 | timestamp with time zone | NO | — | Z | exact UTC integer microseconds, no float | E-TYPE/E-RANGE/E-NONFINITE/E-NULL |
| plan.position_id | 1 | text | NO | 1 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| plan.persisted_version | 2 | bigint | NO | — | I | signed int64 decimal | E-TYPE/E-RANGE/E-NULL |
| plan_revision.position_id | 1 | text | NO | 1 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| plan_revision.version | 2 | bigint | NO | 2 | I | signed int64 decimal | E-TYPE/E-RANGE/E-NULL |
| plan_revision.predecessor_version | 3 | bigint | YES | — | I or N | signed int64 decimal | E-TYPE/E-RANGE |
| plan_revision.batch_id | 4 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| plan_revision.command_id | 5 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| plan_revision.stop_price | 6 | numeric | YES | — | D or N | exact coefficient:stored-scale, finite Decimal | E-TYPE/E-NONFINITE |
| plan_revision.target_price | 7 | numeric | YES | — | D or N | exact coefficient:stored-scale, finite Decimal | E-TYPE/E-NONFINITE |
| plan_revision.note | 8 | text | YES | — | T or N | UTF-8 exact, no normalization | E-TYPE/E-UTF8 |
| personal_journal_entry.position_id | 1 | text | NO | 1 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| personal_journal_entry.entry_id | 2 | text | NO | 2 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| personal_journal_entry.event_id | 3 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| personal_journal_entry.note | 4 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| personal_journal_entry.recorded_at_observed | 5 | timestamp with time zone | NO | — | Z | exact UTC integer microseconds, no float | E-TYPE/E-RANGE/E-NONFINITE/E-NULL |
| public_projection.position_id | 1 | text | NO | 1 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| public_projection.position_version | 2 | bigint | YES | — | I or N | signed int64 decimal | E-TYPE/E-RANGE |
| public_projection.plan_version | 3 | bigint | YES | — | I or N | signed int64 decimal | E-TYPE/E-RANGE |
| assessment_attempt.position_id | 1 | text | NO | 1 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| assessment_attempt.attempt_id | 2 | text | NO | 2 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| assessment_attempt.domain_id | 3 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| assessment_attempt.cut_id | 4 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| assessment_attempt.position_version | 5 | bigint | NO | — | I | signed int64 decimal | E-TYPE/E-RANGE/E-NULL |
| assessment_attempt.plan_version | 6 | bigint | YES | — | I or N | signed int64 decimal | E-TYPE/E-RANGE |
| assessment_attempt.rule_id | 7 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| assessment_attempt.rule_version | 8 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| assessment_attempt.parameter_identity | 9 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| assessment_attempt.execution_status | 10 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| assessment_attempt.assessment_mode | 11 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| assessment_attempt.decision_time_observed | 12 | timestamp with time zone | NO | — | Z | exact UTC integer microseconds, no float | E-TYPE/E-RANGE/E-NONFINITE/E-NULL |
| assessment_attempt.reconstructed_at_observed | 13 | timestamp with time zone | YES | — | Z or N | exact UTC integer microseconds, no float | E-TYPE/E-RANGE/E-NONFINITE |
| assessment_attempt.failure_code | 14 | text | YES | — | T or N | UTF-8 exact, no normalization | E-TYPE/E-UTF8 |
| assessment_result.position_id | 1 | text | NO | 1 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| assessment_result.result_id | 2 | text | NO | 2 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| assessment_result.attempt_id | 3 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| assessment_result.batch_id | 4 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| assessment_result.supersedes_result_id | 5 | text | YES | — | T or N | UTF-8 exact, no normalization | E-TYPE/E-UTF8 |
| assessment_result.fingerprint | 6 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| assessment_result.evaluability | 7 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| assessment_result.content_nature | 8 | text | YES | — | T or N | UTF-8 exact, no normalization | E-TYPE/E-UTF8 |
| assessment_result.content_text | 9 | text | YES | — | T or N | UTF-8 exact, no normalization | E-TYPE/E-UTF8 |
| assessment_result.limitation | 10 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| notification_decision.position_id | 1 | text | NO | 1 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| notification_decision.result_id | 2 | text | NO | 2 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| notification_decision.policy_id | 3 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| notification_decision.policy_version | 4 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| notification_decision.decision | 5 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| notification_decision.reason | 6 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| publication_member.position_id | 1 | text | NO | 1 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| publication_member.batch_id | 2 | text | NO | 2 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| publication_member.member_order | 3 | integer | NO | 3 | I | signed int32 decimal | E-TYPE/E-RANGE/E-NULL |
| publication_member.position_version | 4 | bigint | YES | — | I or N | signed int64 decimal | E-TYPE/E-RANGE |
| publication_member.plan_version | 5 | bigint | YES | — | I or N | signed int64 decimal | E-TYPE/E-RANGE |
| publication_member.result_id | 6 | text | YES | — | T or N | UTF-8 exact, no normalization | E-TYPE/E-UTF8 |
| notification.position_id | 1 | text | NO | 1 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| notification.notification_id | 2 | text | NO | 2 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| notification.batch_id | 3 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| notification.origin_type | 4 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| notification.command_event_id | 5 | text | YES | — | T or N | UTF-8 exact, no normalization | E-TYPE/E-UTF8 |
| notification.result_id | 6 | text | YES | — | T or N | UTF-8 exact, no normalization | E-TYPE/E-UTF8 |
| notification.policy_id | 7 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| notification.policy_version | 8 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| notification.destination_id | 9 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| notification.dedup_key | 10 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| notification.delivery_status | 11 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| outbox_event.position_id | 1 | text | NO | 1 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| outbox_event.outbox_id | 2 | text | NO | 2 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| outbox_event.batch_id | 3 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| outbox_event.command_event_id | 4 | text | YES | — | T or N | UTF-8 exact, no normalization | E-TYPE/E-UTF8 |
| outbox_event.result_id | 5 | text | YES | — | T or N | UTF-8 exact, no normalization | E-TYPE/E-UTF8 |
| outbox_event.notification_id | 6 | text | YES | — | T or N | UTF-8 exact, no normalization | E-TYPE/E-UTF8 |
| outbox_event.dispatch_status | 7 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| outbox_event.lease_token | 8 | text | YES | — | T or N | UTF-8 exact, no normalization | E-TYPE/E-UTF8 |
| outbox_event.lease_until_observed | 9 | timestamp with time zone | YES | — | Z or N | exact UTC integer microseconds, no float | E-TYPE/E-RANGE/E-NONFINITE |
| send_authorization.position_id | 1 | text | NO | 1 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| send_authorization.authorization_id | 2 | text | NO | 2 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| send_authorization.notification_id | 3 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| send_authorization.tenant_id | 4 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| send_authorization.owner_id | 5 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| send_authorization.access_version | 6 | bigint | NO | — | I | signed int64 decimal | E-TYPE/E-RANGE/E-NULL |
| send_authorization.policy_version | 7 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| send_authorization.final_check_position_version | 8 | bigint | NO | — | I | signed int64 decimal | E-TYPE/E-RANGE/E-NULL |
| access_audit.tenant_id | 1 | text | NO | 1 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| access_audit.owner_id | 2 | text | NO | 2 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| access_audit.access_version | 3 | bigint | NO | 3 | I | signed int64 decimal | E-TYPE/E-RANGE/E-NULL |
| access_audit.allowed | 4 | boolean | NO | — | B | ASCII 0/1, distinct from integer | E-TYPE/E-NULL |
| access_audit.reason | 5 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| delivery_audit.position_id | 1 | text | NO | 1 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| delivery_audit.audit_id | 2 | text | NO | 2 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| delivery_audit.notification_id | 3 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| delivery_audit.authorization_id | 4 | text | YES | — | T or N | UTF-8 exact, no normalization | E-TYPE/E-UTF8 |
| delivery_audit.reason | 5 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| delivery_audit.checkpoint | 6 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| synthetic_destination_receipt.destination_id | 1 | text | NO | 1 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| synthetic_destination_receipt.dedup_key | 2 | text | NO | 2 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| synthetic_destination_receipt.authorization_id | 3 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| synthetic_destination_receipt.payload_fingerprint | 4 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| synthetic_destination_call.call_id | 1 | text | NO | 1 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| synthetic_destination_call.destination_id | 2 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| synthetic_destination_call.dedup_key | 3 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| synthetic_destination_call.authorization_id | 4 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| synthetic_destination_call.checkpoint | 5 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| domain_resolution_policy.domain_id | 1 | text | NO | 1 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| domain_resolution_policy.policy_version | 2 | text | NO | 2 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| batch_recovery_audit.request_id | 1 | text | NO | 1 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| batch_recovery_audit.position_id | 2 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| batch_recovery_audit.batch_id | 3 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| batch_recovery_audit.expected_version | 4 | bigint | NO | — | I | signed int64 decimal | E-TYPE/E-RANGE/E-NULL |
| batch_recovery_audit.actor | 5 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| batch_recovery_audit.reason | 6 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| batch_recovery_audit.observed_at | 7 | timestamp with time zone | NO | — | Z | exact UTC integer microseconds, no float | E-TYPE/E-RANGE/E-NONFINITE/E-NULL |
| worker_lease.position_id | 1 | text | NO | 1 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| worker_lease.purpose | 2 | text | NO | 2 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| worker_lease.epoch | 3 | bigint | NO | — | I | signed int64 decimal | E-TYPE/E-RANGE/E-NULL |
| worker_lease.worker_id | 4 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| worker_lease.expires_at | 5 | timestamp with time zone | NO | — | Z | exact UTC integer microseconds, no float | E-TYPE/E-RANGE/E-NONFINITE/E-NULL |
| worker_lease_audit.position_id | 1 | text | NO | 1 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| worker_lease_audit.purpose | 2 | text | NO | 2 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| worker_lease_audit.epoch | 3 | bigint | NO | 3 | I | signed int64 decimal | E-TYPE/E-RANGE/E-NULL |
| worker_lease_audit.worker_id | 4 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| worker_lease_audit.actor | 5 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| worker_lease_audit.observed_at | 6 | timestamp with time zone | NO | — | Z | exact UTC integer microseconds, no float | E-TYPE/E-RANGE/E-NONFINITE/E-NULL |
| t4_operation_receipt.position_id | 1 | text | NO | 1 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| t4_operation_receipt.operation_id | 2 | text | NO | 2 | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| t4_operation_receipt.notification_id | 3 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| t4_operation_receipt.request_payload | 4 | jsonb | NO | — | J | recursive typed nodes, Decimal numbers | E-TYPE/E-JSON/E-NULL |
| t4_operation_receipt.request_fingerprint | 5 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |
| t4_operation_receipt.response | 6 | text | NO | — | T | UTF-8 exact, no normalization | E-TYPE/E-UTF8/E-NULL |

All30 base tables are included, no persisted audit/lease/capture-xid exclusions. No base-table
column/type/nullability/PK discrepancy was identified in textual comparison with current DDL.
No live catalog has been observed. View nullability is an explicit semantic/catalog distinction,
not a DDL change. bytea has wire vectors but no current base-table column.

## Parser compatibility and changes

snapshot_reference remains independent: no encoder imports or shared normalization.
Both reject unknown table-version/partition shapes and empty position IDs; candidate encoder
was tightened to match reference. Reference now rejects unknown descriptor types even for
empty tables/all-NULL rows, closing a static divergence. Scalar I supports int64; int32 restriction
is checked with table schema. Numeric values returned as coefficient/scale, not float.
Reference does not decode global/envelope hashes into provenance or prove catalog identity.
No compatibility claim is tested. Full hostile-input/resource-limit/parser review remains BLOCKED.

## Independent oracle register

| Case | Source / expected observation | Expected digest / status |
| --- | --- | --- |
| Empty table | compound_vectors TABLE-EMPTY: manual descriptor114-byte payload and200 total bytes for publication_domain | SHA-256 UNRESOLVED |
| Multirow adversarial PK | aa,b,a input -> a,b,aa by key-frame length then bytes | Table hash UNRESOLVED |
| NULL/absence/false/zero/empty | Existing scalar bytes; missing field ValueError | Bytes manually specified; no runtime result |
| Numeric scales | 1.0 ->10:1,1.00 ->100:2 | Distinct static frame bytes |
| Nested JSONB | object a -> [null,false]; explicit independent frame tree/lengths | Hash UNRESOLVED |
| bytea / Unicode | 00ff raw; composed/decomposed Unicode remain different | Manual scalar bytes |
| Negative/limit time | -1 microsecond frame; int64 sentinels reject | PostgreSQL finite-limit vectors UNRESOLVED |
| Position partition | P-A key, all position-scoped tables including empty; fixed prefix rule | Position/global hashes UNRESOLVED |
| All-table aggregate | Exactly30 empty tables, no position partitions, empty view | Intermediate table/persisted/published/metadata hashes UNRESOLVED |
| Envelope | v,h,h,h,m,c,r framing, real approved provenance required | Envelope and intermediate hashes UNRESOLVED |

runner/snapshot_compound_vectors.json is declarative/static independent arithmetic, not output
of either Python implementation. Pure wire fixtures can violate relational FKs and must not
be mistaken for database fixtures. Independent human review/calculation is required for all
expected bytes/lengths; no trusted digest oracle is available for compound layers this round.
No PASS. No encoder was invoked to manufacture expectations.

## Other boundaries

worker_identity now rejects differing identity field TYPES (e.g. observed generation true
must not compare equal to integer1) and malformed restart bindings. Capability object identity
is still supplied-data consistency, not child ownership/peer authentication.
H05 equivalence remains conditional; TP still locks roots->lease->batch->barrier and commits
once. No SQL, seam or process operation enabled. EXEC-G1/PERS-G1 OPEN; PUB-T13B pending.
