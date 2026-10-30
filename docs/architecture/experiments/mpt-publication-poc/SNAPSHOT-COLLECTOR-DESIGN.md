# Isolated snapshot collector design - candidate 0.10

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

## Order v1.0 / candidate 0.12 - current implementation boundary

MATERIALIZED_NOT_RUN; REQUIRES_HARDENING / NOT_RUN. This section supersedes 0.11 source-gap
descriptions only where a corresponding control is now authored. It does not certify safety.

collector-approval.example.json remains false with ALL new resource/environment values UNRESOLVED.
collect refuses unresolved/nonpositive/bool bounds before ownership transfer. It requires the
dedicated direct login mpt_snapshot_reader, no role memberships, separate DDL and privilege
quiescence approvals, exact extension list, security-catalog digest and transport-guard identity.
No role, GRANT, connection, DSN, main, runner hook or operational transport guard was created.

| Control | Candidate code | Accounting / remaining limit |
| --- | --- | --- |
| Value / row / table / total bytes | Budget.row/relation; BoundedConnection | UTF-8 text/raw bytes/ASCII bool-int length plus 9 bytes per value and row. Includes SQL NULL marker. Data totals include view separately, not canonical wire size |
| Metadata buffers | BoundedConnection max_catalog_rows and max_buffer_bytes | Same fetch/value/row checks for catalogs; no unbounded fetchall from driver |
| Retained memory | Budget.memory and max_memory_bytes | Deep Python graph estimate; graph of raw/converted/previous rows checked. Not proof of peak allocation or native memory |
| Total time | Monotonic deadline; remaining budget passed on execute/fetch | Not market time. Each cleanup call separately bounded; collection deadline plus up to three cleanup budgets on an error path |
| Completeness | Same-MVCC count(*) plus exact fetched count, strict row width and PK uniqueness | Reject partial/extra/duplicate results; malicious driver replacing data cannot be certified by count alone |
| Types / precision | convert strict types, integer/xid/wire ranges, finite Decimal, stored JSON | No float-to-Decimal, int coercion, bytes coercion; JSON depth and Decimal expansion bounds |
| Catalog | 30-table/191-field schema precheck; existing exact column/PK/view checks | Fresh live evidence unavailable; snapshot_schema bytes remain bound to approval |
| Privileges | No membership; global schema CREATE/ownership, database TEMP/CREATE/owner, cross-schema mutation/sequence/RLS and callable privileged/custom functions | Effective PUBLIC rights inspected; default ACL, roles/memberships, relation/column/function/schema/database ACL and extensions hashed against independent review |
| Cleanup | finish and cursor cleanup preserve original BaseException, attach cleanup_errors/cursor_cleanup_error | Cleanup-only error suppresses result; cancellation/loss never becomes valid partial output |

### Required bounded transport interface - unresolved implementation

The external caller supplies an already open dedicated connection and a separately reviewed
transport_guard. The guard has artifact_sha256 and methods execute(raw, query, params,
timeout_ms, max_buffer_bytes, max_memory_bytes), fetch(cursor, count, timeout_ms,
max_buffer_bytes, max_memory_bytes), close_cursor(cursor, timeout_ms), rollback(raw, timeout_ms),
close(raw, timeout_ms). fetch returns at most count rows and [] only on verified completion.
It must enforce deadlines during blocking operations and native-buffer/peak-memory admission
before allocation, including one oversized field and metadata. A post-return check is insufficient.
This package intentionally provides NO implementation of this driver-specific guard. A hash or
method name cannot establish that it enforces limits. Independent source/provenance verification,
driver version freeze and authorized failure-injection evidence are mandatory.
Missing guard blocks collect; no fallback to raw unbounded connection.execute exists.

The object graph check occurs after Python materialization and does not prove peak heap bounds.
CPU-bound conversion and parse interruption also need independent guard/runtime review.
Thus native buffers, peak allocation and interruption remain BLOCKING_EXECUTION_REVIEW, not
implemented operational guarantees. Cleanup errors stay on the primary exception object, without
logging raw values/credentials. External caller must persist sanitized error evidence later.
Pre-transfer refusals leave connection untouched; caller owns cleanup. After transfer, rollback
and close are both attempted even if one fails. Lost-connection rollback needs independent
server evidence; local close alone does not prove it.

Security catalog digest serializes the query-label map with sorted keys, ASCII JSON and compact
separators; values are ordered lists of row_to_json text tuples. Exact pinned environment/OIDs
are intentional; this is not portable schema hash. Every effective privilege path still needs
human review, including callable built-in functions, extension implementation and role defaults.
Privilege/DDL quiescence must cover the entire session; a catalog snapshot is not a lock on GRANT.
Application SQL, H05 and lock order are unchanged. Independent connected tests remain prohibited.

## Order v0.9 / candidate 0.11 - current safety disposition

DOCUMENTED; source remains MATERIALIZED_NOT_RUN. Overall BLOCKING_EXECUTION_REVIEW.
This section supersedes earlier suggestions that row limits alone bound collection resources.

Proposed dedicated role: mpt_snapshot_reader, read-only on exactly the 30 tables and
published_positions. Schema USAGE and necessary SELECT only; no ownership, SUPERUSER,
CREATEDB, CREATEROLE, REPLICATION, BYPASSRLS, mutating table/column rights, CREATE on database
or schema, temporary-object creation, privileged function execution or inherited/settable
writer/owner roles. Effective PUBLIC grants and all reachable role memberships must be reviewed.
No role or GRANT has been installed or verified. Existing mpt_reader is not proof of this role.
External connection provider must attest login/current role, no pooling/reuse, no temp objects,
approved server/build, exact package/config hash and independently approved credentials.
No DSN, main, connect call or run.py integration is authorized.

| Threat / boundary | Candidate source inspection | Required future evidence / disposition |
| --- | --- | --- |
| Ownership / excessive rights | Checks current role, memberships, flags, mpt_poc write and CREATE privileges | Also audit reachable SET ROLE rights, PUBLIC, other schemas and privileged SECURITY DEFINER functions; current query only covers mpt_poc functions. BLOCKING_EXECUTION_REVIEW |
| Catalog / RLS / view drift | Exact table inventory, ordered columns/types/null/PK, view definition digest, RLS refusal and temp namespace check | DDL quiescence must begin before BEGIN and persist through cleanup; ACCESS SHARE alone does not prove catalog snapshot coherence. COL-09-DDL |
| MVCC update | One REPEATABLE READ READ ONLY transaction; metadata and all scans share snapshot | Explicit concurrent writer checkpoint after snapshot establishment. COL-09-UPDATE |
| Row / partial read | LIMIT cap+1 rejects overflow rather than truncates | Transport completion, row width and driver integrity need explicit validation. zip can silently omit surplus values today. COL-09-PARTIAL |
| Bytes / memory | fetchall has no byte or memory cap | Require approved max_bytes_per_value, max_bytes_per_relation, max_bytes_total covering projected transport values; reject before retaining over-budget values. Server cursor/protocol buffering and oversize single field must be reviewed. Post-fetch measurement alone is insufficient. COL-09-BYTES |
| Total time | Per-statement and lock timeout only | Require approved total_collection_timeout_ms, monotonic deadline established at ownership transfer, remaining budget on every query/fetch and bounded cleanup. No unlimited sum of individually bounded queries. COL-09-TIME |
| Unexpected type | Numeric/JSON/time conversion present; other raw values returned | Require strict declared types, integer ranges, exact row width and no lossy coercion. Decimal(float), int conversion and bytes conversion must not accept unexpected driver objects. COL-09-CONVERT |
| Exception / cancellation | finally attempts rollback then close | Cleanup errors can mask original error; preserve both and never return partial data. Network loss requires external evidence of session termination; close is not proof of server rollback. COL-09-LOSS / INTERRUPT |
| Activation / approval | Default enabled=false; example false/unresolved; hash-bound config | Independent approval required, never inferred from hashes. No collection performed |

Connection ownership: validation refusals before transfer leave the supplied connection untouched;
the external caller MUST close it in its own finally. After transfer the collector attempts rollback
and close on every normal/error path. This two-party cleanup obligation is mandatory; no claim
that pre-transfer refusals close the caller's connection. Cleanup failure blocks evidence.

All resource limits must be independently frozen positive integers before execution. Their actual
values and reliable driver-level enforcement are UNRESOLVED. No fields were added to the example
to imply implementation of missing bounds. The collector remains disabled; this order specifies
the hardening contract and negative oracles, not an operationally safe collector verdict.
No application SQL or active checkpoint was changed.

MATERIALIZED_NOT_RUN in runner/snapshot_collector.py; safety/conformance validation BLOCKED.
No database was opened, no query executed, no module imported. No integration into run.py.
collector-approval.example.json is false/UNRESOLVED; no grant/DDL was created.

## Boundary and authorization

collect receives a dedicated already-open psycopg-compatible connection from a future separately
approved caller; it contains no connect/DSN/main function. enabled defaults false and rejection
touches no connection. Before ownership transfers, exact independently supplied config SHA-256,
collector_authorized=true, contract, schema/manifest byte hashes and approved runtime/bounds
must match. No self-approval, signing, environment creation or dependency installation.
Caller must independently verify full package inventory and signed environment/collector evidence;
this module checks supplied approval/manifest bytes, not that signatures or target host are honest.

Once validated, the function owns and closes that dedicated connection. Requires autocommit=true
and idle transaction status. It begins ONE REPEATABLE READ READ ONLY transaction, fixes local
search_path to pg_catalog, UTC and approved positive statement/lock timeouts.
Initial catalog queries establish the MVCC snapshot; all catalog/table/view reads stay in it.
DDL quiescence must be independently approved for the entire connection/collection window,
including before relation locks are acquired; no automatic proof is claimed from locks alone.
Temporary namespaces are rejected and row_security=off makes unexpected RLS fail instead of
silently filtering rows. The example ddl_quiescence_approved flag remains false.
ACCESS SHARE locks on all30 tables and view prevent DDL drift during collection; relation
inventory, type/nullability/column order and PK are verified before data reads.
No application write, role switching, schema mutation, write lock or owner function is used.

## Least privilege and catalog checks

Future dedicated reader needs SELECT on all30 tables/view and read-only catalog access,
NOT mpt_reader as currently provisioned (that role exposes only the public view).
No grants are added now. Approved current/login identities and exact server patch/version
must match actual observations. Reject superuser/CREATEROLE/CREATEDB/replication/BYPASSRLS
through login memberships, schema/database CREATE, table ownership/membership, row security,
application INSERT/UPDATE/DELETE/TRUNCATE/TRIGGER or column INSERT/UPDATE, and executable
application functions. Lack of SELECT or monitor visibility fails naturally, not a partial result.
READ ONLY is additional defense, not a substitute for actual read-only credentials or trusted DB.

Compare exactly30 ordinary tables plus published_positions view; reject unexpected partition/
foreign/materialized relations. Base metadata uses format_type (including typmods), nullable
flags and PK order. Dropped invisible column slots are not logical snapshot fields.
View name/type/order must match; separate approved view-definition hash and nonnull returned
values support semantic NOT NULL. PostgreSQL catalogs often mark view columns nullable;
never rewrite base metadata to accommodate that. Pin viewdef hash to exact server build.

## Value fidelity and separation

Numeric and xid8 are read as text; Decimal/int conversion is exact. JSONB is read as stored text
then parsed with Decimal via the existing codec representation adapter; this is not independent
reference validation. Timestamptz is converted by PostgreSQL numeric extract(epoch)*1000000
to text, rejecting nonfinite/fractional microseconds; no Python float/year-range loss.
No bytea column exists today; raw bytes conversion is prepared.

Return separates tables, published_rows and provenance (actual environment, MVCC snapshot ID,
run/config/manifest/schema/view hashes). It does NOT call snapshot(), produce canonical bytes/
digests or verdict PASS. Future independent encoding uses supplied-data codec after schema
and provenance verification. Observed snapshot ID is not an ordering/availability guarantee.
No DSNs/credentials/raw secrets are logged; no JSONL output is written by this collector.

## Bounds, errors and cleanup

Each table read uses LIMIT cap+1; exceeding approved cap rejects instead of truncating.
Maximum in-memory row count bounded by31*(cap+1); byte volume still depends on row sizes and
requires environment sizing. No performance claim. Statement/lock timeout errors propagate;
there is no cross-transaction retry that would mix snapshots.
Success issues ROLLBACK to close the read-only snapshot and closes connection; failure rolls
back when needed and closes in finally. No partial result returns on timeout, catalog drift,
conversion error or privilege mismatch. Errors before ownership transfer leave connection to
caller, which must close it. Cleanup errors may mask the original failure; future evidence layer
must preserve both, currently BLOCKED until reviewed. Do not share a connection with runner.

## Required future validation (no execution now)

Disabled/default -> no connection method call. Approval/schema/server/catalog/role mismatch ->
no fixture/data result. Concurrent publisher commit between table reads -> one consistent old
snapshot, no mixed states. DDL conflict -> blocked/timeout, never silently drift. Numeric scale,
nested JSONB and extreme finite DB timestamps -> independent vectors. Error mid-scan -> rollback/
close, no partial output. Verify pg transaction state/locks after cleanup.
These are DOCUMENTED/BLOCKED; code is MATERIALIZED_NOT_RUN, not independently verified.

Next approval: dedicated reader grants and isolated connection/provenance/limits, independent
catalog/vector review and authorized tests, then separately reviewed runner integration.
No current authorization enables that integration, process control or H05 seam.
