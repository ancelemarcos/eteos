# Snapshot interpretation addendum - candidate 0.11 / order v0.9

## Order v1.3 interpretation review

SNAPSHOT-INTERPRETATION-REVIEW.md is the current separate proposal register: exact rule,
alternative, byte/hash effect, compatibility, positive/negative example, affected artifacts and
human decision for each SNAP-P01..05. All five remain PENDING_HUMAN_APPROVAL. No wire change.

## Order v1.1 compatibility checkpoint

SNAP-P01..05 remain PENDING_HUMAN_APPROVAL. No wire layout changed from 0.12.
P01 affects partition table/aggregate prefixes and multipartition tests; P02 affects metadata
streams and complete snapshot hashes; P03 affects published view descriptor and NULL tests;
P04 affects complete PK/key ordering and permutation tests; P05 affects typed scalar, Decimal,
JSONB, Unicode, bytea and temporal vectors. The existing proposal/evidence/consequence matrix
continues to govern. New typed oracle and test_fully_populated_typed_snapshot cover these effects;
compatibility is documentary/source-level only, never an executed equivalence claim.
Any alternative requires an explicit versioned binary compatibility decision and changed oracles.

## Order v1.0 / candidate 0.12 - proposal evidence and approval matrix

All five proposals remain PROPOSED; HUMAN_APPROVAL pending, no Decision Register promotion.

| Proposal | Evidence available / artifact | Binary consequence | Human decision still required |
| --- | --- | --- | --- |
| SNAP-P01 | FULL-SNAPSHOT-CONTRACT; independent oracle.relation/aggregate_stream; multi-partition test authored | POSITION v,p prefix and all empty scoped tables per position | Approve exact prefix and partition membership; independent review/evaluation pending |
| SNAP-P02 | Metadata recipe; oracle.fixture_snapshot; reference.metadata and test authored | Hash four full normal-version streams in qualified-name order | Approve stream concatenation and normal version |
| SNAP-P03 | DDL view predicate plus PUBLISHED constraint; static field matrix | Eight semantic nonnull view fields; ordinal differs from base nullable flag | Approve semantic descriptor; exact live definition remains unresolved |
| SNAP-P04 | Manual a,b,aa vector; independent relation oracle; permutation test | Full PK frame including length header sorts rows | Approve byte ordering; not temporal or numeric order |
| SNAP-P05 | Frozen scalar hex, nested JSON flattening, precision rejection tests | Typed NULL, Decimal scale, UTF-8 without normalization, UTC microseconds | Approve exact typed representation and scope of upstream precision disclaimer |

Source hardening rejects unknown SQL type even for NULL, unknown schema metadata fields and
unknown aggregate versions/digest widths. Valid candidate wire layout is unchanged.
Reference now decodes aggregate/envelope/metadata independently; earlier absence statements
are superseded. snapshot_oracle.py is a separate declarative empty/text/NULL fixture construction
using struct.pack and its own digest calls, never encoder imports/results. It is not a universal
second implementation or executed oracle. Human provenance review and full frozen digests remain
UNRESOLVED. Raw codec/reference resource admission outside collector remains a concrete gap.
Temporal-domain distinctions above remain unchanged; no finite PostgreSQL extremes asserted.

PROPOSED / DOCUMENTED / NOT_RUN. These local proposal IDs are not accepted Decision Register IDs.
Approval is pending; no production contract, binary version or existing SQL changes.

| Proposal | Candidate interpretation submitted for approval | Authority / consequence |
| --- | --- | --- |
| SNAP-P01 | POSITION table and aggregate streams begin F(v,POSITION-version), F(p,exact position_id), then existing fields. GLOBAL has no p. Empty position identity rejects. | FULL-SNAPSHOT-CONTRACT; partition identifiers are hash inputs |
| SNAP-P02 | Metadata is concatenation of FULL normal-version table streams for publication_barrier, publication_batch, publication_cut, public_projection, in unsigned UTF-8 qualified-name order. | No row-only serialization or alternate partition version |
| SNAP-P03 | published_positions has eight semantic nonnullable columns and position_id key. Catalog view null flags are not base-table nullability. Check shape, approved definition and returned values. | ordinal is nullable in publication_batch but PUBLISHED check plus view predicate imply nonnull; not catalog proof |
| SNAP-P04 | Compare complete F(k,PK frames), including unsigned length header. JSON keys use raw UTF-8, table names use qualified UTF-8. | a,b,aa ordering; no chronology or locale semantics |
| SNAP-P05 | Preserve typed NULL, bool, integer, exact Decimal coefficient/scale, JSONB stored structure, bytea and raw Unicode. Negative numeric zero loses sign but retains scale. | No floats, Unicode normalization or reconstruction of pre-storage data |

These proposals restate the candidate interpretation implemented in 0.10. They do not
authorize execution, new schema or MPT/MIR equivalence. D011-001..003 and D014-005 remain
unchanged. publicationCutId alone cannot establish availableAt <= decisionTime.

## Temporal domains and error contract

Wire: exact integer UTC microseconds since 1970; current candidate accepts
-9223372036854775807 through 9223372036854775806. The two int64 endpoints are rejected
by the existing guard; values outside int64 also reject. This is a wire check only.
PostgreSQL finite timestamp domain: separately constrained by actual pinned server/build;
exact endpoints and independent conversion vectors UNRESOLVED. Do not infer finite
PostgreSQL validity from passing the wire check. infinity/-infinity reject.
Python datetime represents years 1..9999; aware values can overflow when converted to UTC
near the endpoints. Such overflow must abort, never clamp or wrap. TimestampMicros permits
wire values outside datetime without claiming that PostgreSQL can store every such value.
No float epoch conversion; preserve stored microseconds only, not discarded upstream precision.

Encoder/reference inspection: strict integer and JSON grammar, duplicate keys and PK checks,
scale retention and type separation are authored. Reference parser imports no encoder and
covers scalar/table decoding only; independent aggregate/envelope parser and full hash oracles
remain UNRESOLVED. Invalid UTF-8 can raise UnicodeError; malformed JSON can raise
JSONDecodeError (ValueError); datetime conversion can raise OverflowError. These abort
collection/comparison, but exact cross-module error-class parity is not established.
Resource limits for Decimal exponent expansion and recursively nested JSON are not specified
in codec/reference source: BLOCKING_EXECUTION_REVIEW for untrusted/oversized inputs.
No binary semantics were changed to hide these gaps.

## Vector provenance

snapshot_compound_vectors.json is a documentary oracle specification, never executed evidence.
Each case records independent manual derivation, source and pending human review. F expressions
are declarative concatenations, not calls to snapshot_codec. Unknown flattened bytes, lengths
and digests are explicitly UNRESOLVED. Synthetic provenance bytes in ENVELOPE are fixture
constants, not real manifest approval or collection authority. Human approval of this addendum
does not supply the missing independent execution or digest evidence.
