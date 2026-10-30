# SNAP-P02 decision page - Publication metadata representation

## Order v2.0 / candidate 0.22 — static evidence and proposed resolution

Technical opinion: APPROVE the full-stream proposal for human decision; actual state remains
PENDING_HUMAN_APPROVAL / NOT_RUN. This supersedes v1.9's request for a missing explanatory
package, not the unresolved human choice. No accepted contract or wire changed.

### Exact conflict and affected closure

FULL-SNAPSHOT-CONTRACT.md:103 defines the descriptor; :108 defines complete table digest input;
:124-125 calls metadata "same-snapshot encoded rows" without saying those words include the
table version/name/descriptor/count/outer row container. :126-128 hashes this metadata inside
the envelope. The contract does NOT explicitly prescribe full streams at :124.
SNAPSHOT-INTERPRETATION-REVIEW.md's SNAP-P02 row explicitly selects full normal-version streams.
CODEC-CONFORMANCE-MATRIX.md:97 and snapshot_compound_vectors.json:452,506 do likewise.
This is a proposal-to-proposal ambiguity, not an accepted ADR override. D011-001..003 and
D014-005 do not decide metadata wire layout.

| Source/function | Actual candidate behavior / affected fields |
| --- | --- |
| snapshot_codec.table_bytes / snapshot:234-242 | canonical table bytes concatenated; publication_metadata_sha256 and envelope_sha256 |
| snapshot_oracle.relation / fixture_snapshot:138-153 | normal streams -> metadata bytes -> SHA(metadata) in envelope |
| snapshot_reference.metadata:215-230 | exactly five top-level frames per table; validates normal version, qualified name, columns, PK |
| expected_bundle_emitter.recipe / streams:52-83 | EMPTY/TYPED/MULTI metadata and envelope records copied from independent oracle; bytes/length/sha256 |
| expected_wire_review.validate_slots:231-255 | metadata equals sorted four already-parsed table slots; envelope contains raw metadata digest |
| frozen_bundle_compare.validate_frozen / compare_frozen | expected structural admission then per-record hex/length/sha256/error comparison; observed wire not independently parsed |
| template / compound vectors | EMPTY@1/metadata, TYPED@1/metadata, MULTI@1/metadata and their envelope slots; full table slots remain unchanged if only metadata composition changes |
| source-binding closure | oracle/emitter/interpretations/vectors hashes, final manifest and frozen bundle approval must be rebound on any approved change |

Exact qualified-name order is public_projection, publication_barrier, publication_batch,
publication_cut (all prefixed mpt_poc.). Underscore precedes 'a' in raw UTF8; prose enumeration
order must not override sorting. All fields of these four tables participate, including nullable
values, ordinal/status/failure fields, capture_transaction and projection versions.
Fixtures: EMPTY has four empty metadata tables; TYPED has one row each; MULTI's two rows are
position_guard, not metadata. MULTI therefore is NOT evidence of multirow metadata coverage.

### Manual derivation (illustration, no generated expected slot)

F(tag,payload) has 9 overhead bytes. For the real two-column publication_barrier descriptor:
domain_id:text nonnull contributes (9+9)+(9+4)+(9+1)=41 bytes;
committed_ordinal:bigint nonnull contributes (9+17)+(9+6)+(9+1)=51;
PK frame contributes 9+(9+9)=27. Descriptor S = F(s,119-byte payload), length128.
V = F(v,MPT-SNAPSHOT@1), length23, hex 76000000000000000e4d50542d534e415053484f544031.
Name frame for mpt_poc.publication_barrier has length36 (27 payload).
C0 = F(c,ASCII 0), length10, hex 63000000000000000130.
R0 = F(r,empty), length9, hex 720000000000000000.
Full empty barrier stream V+name+S+C0+R0 has 23+36+128+10+9 = 206 bytes.
Rows-only concatenation is empty (0 bytes); a rows-container-only variant is R0 (9 bytes).
Thus even before hashing the alternatives are distinct; the four-table empty full stream
is nonempty whereas the unwrapped rows-only metadata is empty. No digest literal is claimed.

For illustrative rows (domain_id=D, committed_ordinal=0) and (E,1):
T(D) = 54000000000000000144; I(0) = 49000000000000000130, each10 bytes.
RowD = 720000000000000014 + T(D) + I(0), length29.
RowE substitutes final text byte45 and integer byte31, also29; PK ordering is D then E.
Two-row container = 72000000000000003a + RowD + RowE, length67.
C2 = 63000000000000000132; full barrier stream length23+36+128+10+67 = 264.
Rows-only alternative is RowD+RowE, length58; container-only alternative length67.
These are hand-derived local examples, not FK-valid database fixtures or populated slot values.

Let Tn be each complete normal table stream and Rn its sorted row-frame concatenation.
Proposed metadata digest Hfull = SHA256(concat_sorted(Tn));
alternative Hrows = SHA256(concat_sorted(Rn)).
Envelope = SHA256(F(v,ENVELOPE-version)+F(h,Hpersisted)+F(h,Hpublished)+F(h,Hmetadata)
+F(m,manifest32)+F(c,config32)+F(r,run_id)).
No numeric SHA value computed. Different inputs invalidate byte compatibility; this is not a
mathematical promise that SHA256 can never collide.
Changing a descriptor nullable flag replaces 62000000000000000130 with ...31: full streams
change even when empty, rows-only does not. Changing a stored ordinal 0->1 changes row bytes
in both alternatives. Reversing scan order changes neither after canonical sorting. Moving
identical row frames between tables can be ambiguous under bare row concatenation; complete
name/descriptor/count framing preserves the boundaries. Name+digest pairs are a third binary
format, not an equivalent full-stream encoding.

### Proposed normative wording — not applied to FULL-SNAPSHOT-CONTRACT

"Publication metadata SHALL be the raw concatenation of the complete normal-version
MPT-SNAPSHOT@1 table streams for mpt_poc.public_projection, mpt_poc.publication_barrier,
mpt_poc.publication_batch and mpt_poc.publication_cut, ordered by unsigned qualified-name
UTF8 bytes. Each stream SHALL contain version, qualified name, schema descriptor, ASCII
row count and outer row container with canonically ordered Row frames. All four streams,
including empty tables, SHALL be present from the same snapshot. Publication metadata
SHALL NOT mean bare Row frames, outer row containers alone, or name/digest pairs.
Its SHA256 SHALL enter the existing envelope metadata-digest frame."

This preserves current candidate @1 bytes, but cannot assert compatibility with an independently
approved rows-only @1 consumer. Human reviewer must accept this as clarification of the unaccepted
candidate or require a new wire identity. If a deployed/approved @1 means rows-only, or if an
alternative is selected, use a separately reviewed new version, reader dispatch and regenerated
independent expectations; never relabel old bytes under the same identity.

Required evidence still absent: named independent reviewer accepting the wording and manual
derivation; complete independent vectors including actual multirow metadata; explicit version
disposition. Existing test_complete_empty_and_multiple_partitions,
test_fully_populated_typed_snapshot and test_partition_metadata_envelope_and_pk_controls are
written/NOT_RUN. Proposed negative cases: rows-only/outer-only/hash-only under @1, missing/extra/
reordered table, changed descriptor, wrong count and two rows reversed/duplicated; retain
canonical permutation equality. Additional cases are documentary, not new executable tests.
Owner: DOMAIN_CONTRACT_REVIEWER + INDEPENDENT_CODEC_REVIEWER, identities UNRESOLVED.


## Order v1.9 / candidate 0.21 decision summary

Technical opinion: REVISE (recommendation only, not a human decision).
Clarify the older encoded-rows wording before approving full metadata streams.
Manual example: Normal-version prefix 76000000000000000e4d50542d534e415053484f544031. No generated value or digest.
Alternative/binary risk: Rows-only or hash-only alternatives omit descriptors/version/count and change metadata/envelope digests.
Insufficient evidence: Insufficient authority to resolve full streams versus encoded rows under @1; explicit rationale and compatibility disposition required.
Compared with SNAPSHOT-INTERPRETATION-REVIEW.md row SNAP-P02: same rule
candidate-0.15/P02, alternative and wire-impact description; no semantic change.
The component mappings and named written tests in the v1.8 review below remain applicable
and NOT_RUN; dependency on independent semantics/byte review is unresolved.
All changed interpretations require explicit version/migration disposition, not relabeling @1.
Owner: DOMAIN_CONTRACT_REVIEWER + INDEPENDENT_CODEC_REVIEWER; identities UNRESOLVED.
Actual decision/signature: UNRESOLVED. State: PENDING_HUMAN_APPROVAL.


## Order v1.8 / candidate 0.20 component review

PENDING_HUMAN_APPROVAL / NOT_RUN. Review focus: complete metadata table streams.
Static evidence: emitter.streams / oracle.relation and fixture_snapshot constructs candidate streams;
expected_wire_review.validate_slots / snapshot_reference.metadata independently parses the relevant layers.
Comparator validate_frozen invokes validate_slots on expected bytes; compare_frozen compares
record content, not an independent interpretation of observed wire semantics.
Row-only metadata differs from full descriptors/table streams; FULL-SNAPSHOT-CONTRACT wording is ambiguous. @1 compatibility cannot be declared until the human reviewer selects the exact representation. Prefer explicit full streams for self-description; otherwise propose @2, new metadata/envelope vectors and explicit reader dispatch.
Manual fragments below are examples only; no SHA or slot result was generated.
The named source tests below are retained unchanged and NOT_RUN. Required future evidence:
independent positive/negative literals, reviewer proof for every affected layer, explicit
version rejection and reproducible authorized comparison. Existing tests do not establish
approval or binary compatibility. No emitter, comparator, parser, oracle or test was changed.
Owner: DOMAIN_CONTRACT_REVIEWER with INDEPENDENT_CODEC_REVIEWER; identities UNRESOLVED.
Decision required: accept the exact current rule and its compatibility rationale, or request
a separately reviewed versioned alternative. Neither route is approved by this review.

PROPOSED / PENDING_HUMAN_APPROVAL / NOT_RUN. Candidate0.19; no signature or decision supplied.
Rule identity remains candidate-0.15/P02; contract MPT-SNAPSHOT@1.

## Current rule
Metadata is the concatenation of full normal-version table streams of publication_barrier, publication_batch, publication_cut, public_projection, sorted by qualified UTF8 table name.

## Alternative
Concatenate row frames alone, or table-name/digest pairs.

## Byte example
Normal version prefix F(v,MPT-SNAPSHOT@1) is 76000000000000000e4d50542d534e415053484f544031. A rows-only alternative lacks this prefix. Example is manual and partial, not a metadata slot.
No generator, codec or digest calculation was used for this example. It fills none of the 428 slots.

## Compatibility and semantic risk
Descriptor/count/version are part of candidate metadata bytes. Replacing full streams changes metadata hash and envelope, even if logical rows agree.
Shared oracle/SUT misunderstanding of the older phrase 'encoded rows' could produce matching but incorrect metadata. Human interpretation is required.

## Positive / negative cases and affected contracts
Positive: exact current-rule representation and membership. Negative: the alternative encoded under
the unchanged current identity must be rejected, not normalized or accepted as equivalent.
Affected: FULL-SNAPSHOT-CONTRACT.md, SNAPSHOT-INTERPRETATION-REVIEW.md,
snapshot_schema.json/snapshot_compound_vectors.json as applicable, expected_bundle_emitter,
snapshot_oracle and expected_wire_review. Accepted ADR/MIR contracts remain unchanged.
Tests for review: test_complete_empty_and_multiple_partitions; test_fully_populated_typed_snapshot; test_partition_metadata_envelope_and_pk_controls. All NOT_RUN.

## Recommendation for human consideration
Prefer full streams for explicit schema/count/version coverage and consistency with candidate implementation; acknowledge the ambiguity in older wording and require explicit human decision.

## Decision requested
Approve full-stream recipe/order, or require a new wire version and regenerated independent expectations.
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
