# Codec and pure identity materialization - candidate 0.9

## Order v1.3 / candidate 0.15

Expected bundle specification, 428-record template, review matrix, interpretation register and
exact eight-file capsule descriptor are now materialized without assembly or execution.
Full scalar/row emitter, bundle serializer and frozen-bundle comparator remain UNRESOLVED;
current layer_records covers table/upper layers, and current tests use dynamic expectations.
See EXPECTED-BUNDLE-SPEC.md. No code/SQL/configuration/test source changed in this round.

## Order v1.1 / candidate 0.13

Current coverage is recorded in TRANSPORT-AND-CONNECTED-VALIDATION.md. The independent oracle
now supports typed table fixtures and layer_records for every hash layer, including populated
view/metadata. Two additional conformance methods and four admission/plan tests are authored;
none executed. Frozen output bytes/digests remain UNRESOLVED. The new candidate transport
and connected harness are explicitly disarmed, not an operational collector or connected scheduler.
Collector batch/call limits and pre-ownership admission are authored; defaults remain false.
SNAP-P01..05 wire rules and all execution gates remain unchanged.

## Order v1.0 / candidate 0.12

Current source boundary: updated conformance matrix and collector design. New independent
snapshot_oracle.py and two candidate test files are MATERIALIZED_NOT_RUN; no tests executed.
Codec guards, reference aggregate/metadata/envelope parser, strict collector conversions,
budgets, privilege checks and cleanup preservation authored. No wire change or activation.
Native transport guard, independent digest freeze, connected harness and human decisions remain
BLOCKING_EXECUTION_REVIEW. Previous source-gap descriptions are superseded only as mapped.

## Order v0.9 / candidate 0.11

Current review: SNAPSHOT-DECISION-ADDENDUM.md and the updated conformance/safety matrices.
Compound vectors now include per-case provenance, explicit unknown oracle fields, multi-partition
inputs, fixed synthetic envelope inputs and negative precision/type cases. No source was executed
or changed. Independent full hashes, aggregate parser coverage and collector resource/privilege
closure remain BLOCKING_EXECUTION_REVIEW. All prior execution gates remain open.

MATERIALIZED_NOT_RUN source; end-to-end conformance BLOCKED. No executable artifact invoked.
No collector, adapter, DB connection or runner integration has been added.

## Artifacts and caller contracts

snapshot_schema.json contains the 30 table descriptors transcribed from actual schema.sql and
delivery-api.sql text, including PK-derived NOT NULL. Independent documentation inventory is
FULL-SNAPSHOT-CONTRACT.md. Future caller must validate actual catalog column order/type/
nullability/PK against the independently approved manifest-bound JSON before supplying data.
Encoder accepts exactly these table names; caller cannot treat arbitrary modified schema JSON
as approved. Manifest/config binding and actual catalog comparison are collector obligations.

snapshot_codec.scalar accepts None for SQL NULL, strict bool/int/str/bytes, finite Decimal,
aware datetime or TimestampMicros, and Jsonb wrapper. Plain Python floats are rejected.
parse_stored_jsonb parses a STORED JSON representation using Decimal and rejects duplicate
keys/nonfinite values; it is not a claim to preserve original pre-jsonb duplicates or whitespace.
TimestampMicros is exact stored microseconds and supports values outside datetime year range.
Caller must reject PostgreSQL infinities and map typed driver values losslessly.
snapshot takes complete supplied table lists, view rows and approved provenance hashes/run ID;
it performs no IO/collection and cannot prove that inputs came from one MVCC snapshot.

snapshot_reference independently parses frames and typed scalars/table descriptors/rows; it
returns tagged data (e.g. numeric coefficient/scale), not floating numbers. It does not import
the encoder, compute expected outputs from it, validate real catalog provenance or decode an
external process observation stream. Caller supplies immutable bytes. Unknown/truncated/type/
ordering/null violations reject; unexecuted code is not a verified hostile-input parser.

## Explicit candidate interpretations needing approval

1. Position table stream starts F(v,MPT-SNAPSHOT@1/POSITION), F(p,position_id), then normal
   F(t), descriptor, row-count, rows. Partition combination starts same F(v),F(p), then sorted
   F(t),F(h) pairs. GLOBAL uses its version prefix without F(p).
2. Publication metadata bytes are concatenated FULL normal table streams for barrier, batch,
   cut and projection in qualified-name order, not an unframed row-only concatenation.
3. Published view descriptor uses its eight declared fields and all nullable=false: joins to
   non-null revision/domain/ordinal for published rows supply this semantic constraint,
   despite PostgreSQL view catalogs often reporting loose nullability.
4. Rows sort by full F(k,PK frames), including length header as specified. This is not numeric
   sort and may differ from a prior informal example; it never establishes chronological order.

These precision choices resolve ambiguity for candidate source only. Without independent
review and vectors for those layers, equivalence is BLOCKED; no contract/decision promoted.

## Static independent vectors

snapshot_vectors.json was manually authored from F(tag,payload). Example: text A is tag54,
length 0000000000000001, payload41; numeric1.00 is tag44, length5, ASCII100:2;
JSON null is outer tag4a,length9 containing tag6e,length0. No encoder/decoder was executed
to derive them. Decoded expectations are JSON arrays representing reference tuples (recursive
tuple-to-list conversion only). Inputs describe exact constructors, never float conversions.
Positive vectors cover SQL NULL, empty text/bytea, UTF-8, bool/int/xid8, numeric scale/negative
zero, exact microseconds, JSON null/empty containers. Negative vectors cover truncation,
nonempty NULL, integer leading zero and invalid UTF-8.

No result digest was invented. Independent future acceptance must add complete-table empty/
multirow and composite-key vectors, nested JSON object ordering, table/global/partition/
published/metadata/envelope SHA-256 vectors, and cross-parser/type boundary vectors.
Until reviewed and authorized execution produces evidence, those gaps remain BLOCKED.
Documentary metamorphic oracles: scan-order permutation preserves bytes; one persisted field
change changes relevant table/global hash; exact replay preserves full state; NULL/text/json
null and distinct numeric scales remain distinct. Cryptographic collision resistance is an
assumption; expected digests must not be generated only by the candidate encoder.

## Pure identity acceptance cases (documentary, not run)

| Input change | validate_* expected result | External evidence still required |
| --- | --- | --- |
| Different run/sandbox/supervisor/creation/artifact/nonce | ValueError | OS identity/peer measurement |
| Equal-value but different capability object | ValueError | Real retained child capability, not Python token |
| Restart generation not old+1, reused nonce/creation/capability | ValueError | Actual old exit/new spawn evidence |
| IPC missing/extra field, sequence replay/gap, wrong operation | ValueError | Authenticated channel and bounded measured frame |
| now_tick >= deadline or noninteger/oversize frame | ValueError | Trusted monotonic clock/measured byte count |
| IDENTITY_CONFIRMED -> BEFORE_COMMIT/OPEN | New immutable state, sequence+1 | Actual DB open checkpoint |
| AFTER_COMMIT -> EXIT_CONFIRMED/COMMITTED | New immutable state, sequence+1 | Independent OS exit AND DB completion |
| Unknown commit outcome or wrong phase | ValueError, stop; no inferred rollback | Durable operation-identity recovery by future supervisor |

No validation function can issue a signal or invoke a stub lifecycle method. CheckState and
Binding are pure data, forgeable by in-process callers: they prove internal consistency only.
No OS security boundary can be implemented by object equality. Operational supervisor remains
blocked and unchanged, as do runner blocked-scenario gates.

## Future MVCC collection (not materialized)

Separately authorized observer begins a NEW read-only REPEATABLE READ transaction after
verified checkpoint/rollback and freezes all 30 tables plus published view in that one snapshot.
Verify schema against approved metadata first; preserve Decimal scale and timestamptz precision.
Materialize all rows consistently, capture snapshot/run/manifest/config evidence, then pass data
to the pure encoder. Never call the existing separate-query equality helper a consistent MVCC
collector. No code in this round connects to PostgreSQL or changes application READ COMMITTED.


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
