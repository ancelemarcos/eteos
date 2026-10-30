# SNAP-P05 decision page - Typed values, precision and time

## Order v1.9 / candidate 0.21 decision summary

Technical opinion: APPROVE (recommendation only, not a human decision).
Retain typed distinctions, stored scale and exact UTC microseconds.
Manual example: SQL NULL 4e0000000000000000; JSON null 4a00000000000000096e0000000000000000. No generated value or digest.
Alternative/binary risk: Scale/Unicode normalization, float or millisecond alternatives change bytes and erase distinctions.
Insufficient evidence: Independent literal/time review remains missing; PostgreSQL finite-range claims remain excluded.
Compared with SNAPSHOT-INTERPRETATION-REVIEW.md row SNAP-P05: same rule
candidate-0.15/P05, alternative and wire-impact description; no semantic change.
The component mappings and named written tests in the v1.8 review below remain applicable
and NOT_RUN; dependency on independent semantics/byte review is unresolved.
All changed interpretations require explicit version/migration disposition, not relabeling @1.
Owner: DOMAIN_CONTRACT_REVIEWER + INDEPENDENT_CODEC_REVIEWER; identities UNRESOLVED.
Actual decision/signature: UNRESOLVED. State: PENDING_HUMAN_APPROVAL.


## Order v1.8 / candidate 0.20 component review

PENDING_HUMAN_APPROVAL / NOT_RUN. Review focus: typed null, stored decimal scale and exact microseconds.
Static evidence: emitter.recipe / oracle.scalar_fixture, json_fixture, numeric_payload constructs candidate streams;
expected_wire_review.scalar / decimal_payload / json_node; snapshot_reference.scalar / number / json_node independently parses the relevant layers.
Comparator validate_frozen invokes validate_slots on expected bytes; compare_frozen compares
record content, not an independent interpretation of observed wire semantics.
SQL NULL and JSON null frames differ; 1.0 and 1.00 preserve different scale. Reject float/coercion/normalization alternatives under @1. A normalized numeric/Unicode/time representation requires @2 and separate boundary vectors. Python representability is not PostgreSQL finite-range proof.
Manual fragments below are examples only; no SHA or slot result was generated.
The named source tests below are retained unchanged and NOT_RUN. Required future evidence:
independent positive/negative literals, reviewer proof for every affected layer, explicit
version rejection and reproducible authorized comparison. Existing tests do not establish
approval or binary compatibility. No emitter, comparator, parser, oracle or test was changed.
Owner: DOMAIN_CONTRACT_REVIEWER with INDEPENDENT_CODEC_REVIEWER; identities UNRESOLVED.
Decision required: accept the exact current rule and its compatibility rationale, or request
a separately reviewed versioned alternative. Neither route is approved by this review.

PROPOSED / PENDING_HUMAN_APPROVAL / NOT_RUN. Candidate0.19; no signature or decision supplied.
Rule identity remains candidate-0.15/P05; contract MPT-SNAPSHOT@1.

## Current rule
Typed scalar tags; SQL NULL differs from JSON null; finite Decimal coefficient/stored scale; raw bytea; UTF8 without normalization; lossless nested JSON structure; signed UTC microseconds and candidate wire guards.

## Alternative
Normalize numeric scale/Unicode, use float or milliseconds, or plain JSON text.

## Byte example
Manual SQL NULL: 4e0000000000000000; JSON null: 4a00000000000000096e0000000000000000. Numeric1.0: 44000000000000000431303a31; 1.00: 4400000000000000053130303a32.
No generator, codec or digest calculation was used for this example. It fills none of the 428 slots.

## Compatibility and semantic risk
Normalization collapses distinctions and changes containing row/table/envelope hashes. Any change requires a new recipe/wire compatibility decision.
Top-level jsonb None in the independent oracle means SQL NULL, not JSON null. Python/wire bounds do not prove PostgreSQL finite timestamps; stored scale and licensed data semantics cannot be inferred.

## Positive / negative cases and affected contracts
Positive: exact current-rule representation and membership. Negative: the alternative encoded under
the unchanged current identity must be rejected, not normalized or accepted as equivalent.
Affected: FULL-SNAPSHOT-CONTRACT.md, SNAPSHOT-INTERPRETATION-REVIEW.md,
snapshot_schema.json/snapshot_compound_vectors.json as applicable, expected_bundle_emitter,
snapshot_oracle and expected_wire_review. Accepted ADR/MIR contracts remain unchanged.
Tests for review: test_scalar_bytes_and_decoding; test_nested_json_independent_bytes; test_oracle_negative_typed_values; test_python_time_domain_without_postgresql_claim; test_scalar_controls; test_manual_wire_rejection_oracle. All NOT_RUN.

## Recommendation for human consideration
Retain typed distinctions and exact precision as the proposal; keep PostgreSQL finite-date limits outside offline assertions and require manual scalar/JSON review.

## Decision requested
Approve exact typed rules and explicitly excluded DB-range claims, or request versioned alternative.
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
