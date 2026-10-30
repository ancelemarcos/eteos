# SNAP-P01 decision page - Partition identity and membership

## Order v1.9 / candidate 0.21 decision summary

Technical opinion: APPROVE (recommendation only, not a human decision).
Retain explicit partition identity and empty-table inclusion.
Manual example: 22 scoped tables and 8 global tables; P-A frame 700000000000000003502d41. No generated value or digest.
Alternative/binary risk: Aggregate-only identity or omission of empty tables changes table/aggregate digests.
Insufficient evidence: Independent full membership/literal review and named reviewer decision remain missing.
Compared with SNAPSHOT-INTERPRETATION-REVIEW.md row SNAP-P01: same rule
candidate-0.15/P01, alternative and wire-impact description; no semantic change.
The component mappings and named written tests in the v1.8 review below remain applicable
and NOT_RUN; dependency on independent semantics/byte review is unresolved.
All changed interpretations require explicit version/migration disposition, not relabeling @1.
Owner: DOMAIN_CONTRACT_REVIEWER + INDEPENDENT_CODEC_REVIEWER; identities UNRESOLVED.
Actual decision/signature: UNRESOLVED. State: PENDING_HUMAN_APPROVAL.


## Order v1.8 / candidate 0.20 component review

PENDING_HUMAN_APPROVAL / NOT_RUN. Review focus: partition prefix and full empty membership.
Static evidence: emitter.streams / oracle.part, relation, aggregate_stream constructs candidate streams;
expected_wire_review.table / validate_slots; snapshot_reference.table / aggregate independently parses the relevant layers.
Comparator validate_frozen invokes validate_slots on expected bytes; compare_frozen compares
record content, not an independent interpretation of observed wire semantics.
Removing a position prefix or omitting empty members changes bytes and digests. Retain candidate-0.15/P01 only pending approval; an alternative requires MPT-SNAPSHOT@2 proposal with independently regenerated expected inventory, explicit dual-version readers and no @1 relabeling.
Manual fragments below are examples only; no SHA or slot result was generated.
The named source tests below are retained unchanged and NOT_RUN. Required future evidence:
independent positive/negative literals, reviewer proof for every affected layer, explicit
version rejection and reproducible authorized comparison. Existing tests do not establish
approval or binary compatibility. No emitter, comparator, parser, oracle or test was changed.
Owner: DOMAIN_CONTRACT_REVIEWER with INDEPENDENT_CODEC_REVIEWER; identities UNRESOLVED.
Decision required: accept the exact current rule and its compatibility rationale, or request
a separately reviewed versioned alternative. Neither route is approved by this review.

PROPOSED / PENDING_HUMAN_APPROVAL / NOT_RUN. Candidate0.19; no signature or decision supplied.
Rule identity remains candidate-0.15/P01; contract MPT-SNAPSHOT@1.

## Current rule
Every POSITION table and aggregate includes F(v,MPT-SNAPSHOT@1/POSITION), then F(p,exact position_id); all 22 scoped tables included for each known position, including empty ones. Eight non-position tables form GLOBAL without p.

## Alternative
Put identity only in aggregate, or omit empty position tables.

## Byte example
Manually transcribed fragment F(p,P-A): 700000000000000003502d41; P-B changes final byte to 42. This is a framing example, not a generated slot result.
No generator, codec or digest calculation was used for this example. It fills none of the 428 slots.

## Compatibility and semantic risk
Removing p changes every position table digest; omitting empty tables changes aggregate membership. GLOBAL must not acquire an inferred position.
Misassigning global audit/destination data to a position, missing an empty scoped table, or accepting a different prefix can hide divergence.

## Positive / negative cases and affected contracts
Positive: exact current-rule representation and membership. Negative: the alternative encoded under
the unchanged current identity must be rejected, not normalized or accepted as equivalent.
Affected: FULL-SNAPSHOT-CONTRACT.md, SNAPSHOT-INTERPRETATION-REVIEW.md,
snapshot_schema.json/snapshot_compound_vectors.json as applicable, expected_bundle_emitter,
snapshot_oracle and expected_wire_review. Accepted ADR/MIR contracts remain unchanged.
Tests for review: test_complete_empty_and_multiple_partitions; test_partition_metadata_envelope_and_pk_controls; test_partition_descriptor_and_link_tampering. All NOT_RUN.

## Recommendation for human consideration
Retain explicit prefix and empty-table inclusion as the candidate proposal: identity is locally auditable and coverage is deterministic. This recommendation is not acceptance.

## Decision requested
Approve exact prefix/membership, or reject and require a versioned alternative.
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
