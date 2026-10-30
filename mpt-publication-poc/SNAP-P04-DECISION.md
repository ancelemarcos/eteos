# SNAP-P04 decision page - Canonical key ordering

## Order v1.9 / candidate 0.21 decision summary

Technical opinion: APPROVE (recommendation only, not a human decision).
Retain full framed-PK ordering, raw UTF8 JSON-key and qualified-name ordering.
Manual example: a key 6b000000000000000a54000000000000000161; aa key 6b000000000000000b5400000000000000026161. No generated value or digest.
Alternative/binary risk: SQL/numeric/payload-only ordering changes row streams and upper digests.
Insufficient evidence: Independent ordering/collision review and human version decision remain missing; canonical order proves no chronology.
Compared with SNAPSHOT-INTERPRETATION-REVIEW.md row SNAP-P04: same rule
candidate-0.15/P04, alternative and wire-impact description; no semantic change.
The component mappings and named written tests in the v1.8 review below remain applicable
and NOT_RUN; dependency on independent semantics/byte review is unresolved.
All changed interpretations require explicit version/migration disposition, not relabeling @1.
Owner: DOMAIN_CONTRACT_REVIEWER + INDEPENDENT_CODEC_REVIEWER; identities UNRESOLVED.
Actual decision/signature: UNRESOLVED. State: PENDING_HUMAN_APPROVAL.


## Order v1.8 / candidate 0.20 component review

PENDING_HUMAN_APPROVAL / NOT_RUN. Review focus: framed PK ordering and raw UTF8 name ordering.
Static evidence: emitter.streams / oracle.relation and aggregate_stream constructs candidate streams;
expected_wire_review.row / table / validate_slots; snapshot_reference.table / aggregate independently parses the relevant layers.
Comparator validate_frozen invokes validate_slots on expected bytes; compare_frozen compares
record content, not an independent interpretation of observed wire semantics.
Framed key order is not SQL or numeric order: manual a/aa frames show length-prefix significance. Keep raw UTF8 only for the declared name/JSON-key domains. Alternative sorting changes streams; propose @2 ordering and re-reviewed vectors rather than silently reinterpret @1.
Manual fragments below are examples only; no SHA or slot result was generated.
The named source tests below are retained unchanged and NOT_RUN. Required future evidence:
independent positive/negative literals, reviewer proof for every affected layer, explicit
version rejection and reproducible authorized comparison. Existing tests do not establish
approval or binary compatibility. No emitter, comparator, parser, oracle or test was changed.
Owner: DOMAIN_CONTRACT_REVIEWER with INDEPENDENT_CODEC_REVIEWER; identities UNRESOLVED.
Decision required: accept the exact current rule and its compatibility rationale, or request
a separately reviewed versioned alternative. Neither route is approved by this review.

PROPOSED / PENDING_HUMAN_APPROVAL / NOT_RUN. Candidate0.19; no signature or decision supplied.
Rule identity remains candidate-0.15/P04; contract MPT-SNAPSHOT@1.

## Current rule
Rows sort by unsigned lexicographic bytes of complete F(k,PK scalar frames), including length. JSON keys use raw UTF8 order; qualified table names use UTF8 order. No temporal ordering implied.

## Alternative
Sort by SQL collation, numeric value, or PK payload without framing length.

## Byte example
Full key for text a: 6b000000000000000a54000000000000000161. For aa: 6b000000000000000b5400000000000000026161. Length prefix explains manual a,b,aa order.
No generator, codec or digest calculation was used for this example. It fills none of the 428 slots.

## Compatibility and semantic risk
An alternative changes row/table/aggregate bytes whenever ordering differs; no compatibility inheritance.
Confusing canonical order with event chronology or SQL numeric order; permitting duplicate framed keys; normalizing Unicode keys.

## Positive / negative cases and affected contracts
Positive: exact current-rule representation and membership. Negative: the alternative encoded under
the unchanged current identity must be rejected, not normalized or accepted as equivalent.
Affected: FULL-SNAPSHOT-CONTRACT.md, SNAPSHOT-INTERPRETATION-REVIEW.md,
snapshot_schema.json/snapshot_compound_vectors.json as applicable, expected_bundle_emitter,
snapshot_oracle and expected_wire_review. Accepted ADR/MIR contracts remain unchanged.
Tests for review: test_empty_multirow_order_and_corruption; test_partition_metadata_envelope_and_pk_controls; test_canonical_order_and_post_freeze_bytes (record ID order is separate). All NOT_RUN.

## Recommendation for human consideration
Retain framed-key ordering for consistency with the written candidate and deterministic byte identity. Document that it is not database or market-time ordering.

## Decision requested
Approve all three ordering domains explicitly, or request a versioned alternative.
A rejection does not authorize redesign or execution. Record a new version/proof before any change.

| Human decision field | Value |
| --- | --- |
| Decision (APPROVE / REJECT / REQUEST_CHANGES) | UNRESOLVED |
| DOMAIN_CONTRACT_REVIEWER identity | UNRESOLVED |
| INDEPENDENT_CODEC_REVIEWER identity and independence evidence | UNRESOLVED |
| Rationale and proof references | UNRESOLVED |
| Approved exact document/rule hashes | UNRESOLVED |
| Compatibility/version disposition | UNRESOLVED |
| Decision ID / date / external signature reference | UNRESOLVED |
| Current status | PENDING_HUMAN_APPROVAL |

This page is a decision form, not approval. Execution/freeze authorization remains separate.
