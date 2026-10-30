# SNAP-P03 decision page - Published view descriptor

## Order v2.8 - editorial identity clarification on candidate0.26

READY_FOR_REVIEW / NOT_RUN; PENDING_HUMAN_APPROVAL. The physical SQL/wire name is lifecycle
(schema.sql:110,830; snapshot_schema.json position_revision; codec.snapshot and oracle view
descriptors). lifecycle_status was the external audit's conceptual label, not an alias or
a second candidate column. FULL-SNAPSHOT-CONTRACT now states that mapping editorially.
IR-P03-F01 is CONFIRMED as a terminology discrepancy, REFUTED as inconsistent naming among
the candidate DDL/contract/descriptors. No rename, descriptor edit or wire change occurred.

The eight-field proof below is preserved: six revision fields and batch.domain_id have
NOT NULL; INNER JOIN does not null-extend; PUBLISHED plus the boolean biconditional requires
nonnull ordinal. CHECK can admit UNKNOWN generally; status NOT NULL and IS NOT NULL make
this biconditional two-valued. Neither ordinal>0 alone nor an enum CHECK proves nonnull.
IR-P03-F02 is CONFIRMED: static proof under exact enforced DDL is not deployed-state evidence.

Eight future independent negatives (all NOT_RUN): start from otherwise valid synthetic
relations and insert SQL NULL separately in revision.position_id, version, lifecycle, side,
remaining_quantity, average_entry_price; batch.domain_id; and batch.ordinal with PUBLISHED.
The first seven must reject by NOT NULL/PK; the eighth by the biconditional. For each same
field, independently inject NULL into the published serialization input/wire and require
rejection under nullable=false. These are specifications, not executable fixtures or results.
Distinguish absent join rows from emitted NULLs. Real deployment requires separately authorized
catalog/view/constraint identity evidence and observed negatives; none is supplied here.

## Order v2.0 / candidate 0.22 — field-by-field static proof

Technical opinion: APPROVE the existing semantic-nonnull descriptor for human decision,
conditional on the exact candidate DDL/view below. PENDING_HUMAN_APPROVAL / NOT_RUN.
This supplies the proof missing in v1.9; no database deployment or independent approval is claimed.

Scope: schema.sql:829-834 selects six direct r columns and two direct b columns through INNER
joins. There is no outer join, UNION, CASE, nullable computed expression or aggregate in this
view. Each classification below means "provably nonnull under this exact enforced DDL",
not "verified in a running database". Catalog view flags need not expose this logical proof.

| Output and type | Exact evidence chain in schema.sql | Classification | Counterexample boundary / proposed negative |
| --- | --- | --- | --- |
| position_id:text | r.position_id NOT NULL :108 and PK :115; projected :830; inner joins :832-833 | provadamente nao nulo | NULL injected into serialized view row must reject; nullable pp version yields no join row |
| version:bigint | r.version NOT NULL :108, PK :115; direct :830 | provadamente nao nulo | NULL r.version violates base constraint; unmatched pp reference contributes no row |
| lifecycle:text | r.lifecycle NOT NULL :110; direct :830 | provadamente nao nulo | CHECK IN alone would allow UNKNOWN, but NOT NULL separately forbids NULL; inject NULL -> reject |
| side:text | r.side NOT NULL :111; direct :830 | provadamente nao nulo | Same distinction: enum CHECK is not the null proof; injected NULL -> reject |
| remaining_quantity:bigint | r.remaining_quantity NOT NULL :112; direct :830 | provadamente nao nulo | >=0 alone insufficient; zero is valid nonnull, never convert to NULL; injected NULL -> reject |
| average_entry_price:numeric | r.average_entry_price NOT NULL :113; finite-value CHECK :124; direct :830 | provadamente nao nulo | Finiteness is separate from nullability; injected NULL rejects; scale preserved |
| domain_id:text | b.domain_id NOT NULL :67; direct :831; INNER b join :833 | provadamente nao nulo | FK alone not null proof; unmatched batch produces no view row; injected NULL -> reject |
| ordinal:bigint | b.publication_status NOT NULL :70-72; biconditional CHECK :82; view WHERE :834; direct :831 | provadamente nao nulo | Pending/blocked batch can have NULL ordinal but is filtered out; PUBLISHED+NULL violates :82; injected NULL -> reject |

Ordinal proof in SQL three-valued terms: IS NOT NULL is always TRUE or FALSE. Because status
is NOT NULL, status='PUBLISHED' is also two-valued. Their equality CHECK therefore cannot pass
as UNKNOWN. At the view WHERE, only TRUE status='PUBLISHED' survives; CHECK then requires
ordinal IS NOT NULL=TRUE. ordinal>0 at :73 alone would permit NULL (UNKNOWN) and is NOT used
as the null proof. Even the status predicate alone cannot prohibit a PUBLISHED/NULL base row
without the biconditional constraint. No assumption about publish_batch being the only writer
is necessary for this logical proof.

Persisted/public distinction: public_projection.position_version is nullable (:151-155);
NULL equality in INNER join is UNKNOWN and emits no row. plan_version is not selected.
Missing revision/batch does not null-extend a row. Pending and blocked batches cannot enter the
view. If persisted state changes PUBLISHED -> non-PUBLISHED consistently, that row disappears
rather than emitting a NULL ordinal. Joins do not prove unrelated columns nonnull; the direct
NOT NULL constraints do. Transactional completeness, maximal published version, tenant
authorization and MIR time admissibility are separate properties not established here.

No conforming counterexample for these eight outputs was found under the stated DDL.
Potential counterexamples require a changed/unenforced constraint, changed view (e.g. outer
join or nullable expression), untrusted collected row, or a different deployed schema.
Runtime catalog identity/constraint validity and same-snapshot collection are NOT demonstrated.
No field is classified "pode ser nulo" within this exact view; no deployed-field claim is proven.
If a future schema lacks any proof link, classify that output "nao demonstrado", fail closed,
and request a versioned descriptor decision; do not silently flip nullable flags.

### Snapshot mapping and serialization proposal

Full contract lists these eight columns/key; codec.snapshot:228-233, oracle.fixture_snapshot:140-145
and expected_wire_review.validate_slots:219-228 construct the same eight nonnull fields and
position_id PK. codec.rows_bytes and oracle.relation reject NULL in nonnull fields; reference.table
checks decoded NULL against descriptors; expected_wire_review.scalar checks nonnull independently.
Emitter.recipe supplies one typed published row only for TYPED@1, none for EMPTY/MULTI.
Those wire fixtures do not prove SQL/FK validity. Comparator validates expected structure first;
its observed record checks do not establish SQL semantics.
The disabled collector snapshot_collector.py:419-458 also reads the view definition and
constructs the same semantic nonnull columns, then reads published_positions; its conversion
guard rejects unexpected NULL (:37). This is unexecuted source, not deployed catalog evidence.

Proposed serialization: retain nullable=false for all eight columns in declared order, PK
position_id, normal typed encodings under /PUBLISHED. Reject missing/extra fields or SQL NULL
in any of the eight; never omit/coalesce/default a value. Manual descriptor flag false
62000000000000000130 differs from true ...31. SQL NULL 4e0000000000000000 (9 bytes) is rejected.
Changing descriptor flags changes even empty-view bytes and upper hashes; a catalog-flag
alternative needs explicit version/compatibility review, not an undocumented @1 fallback.

Documentary negative plan (not executable edits): one NULL mutation per field with independently
authored rejection expectation; malformed/missing field; nullable descriptor tampering; NULL
pp.position_version -> no view row; PUBLISHED/NULL ordinal -> base CHECK rejection; pending/
blocked NULL ordinal -> no view row. SQL cases require a separate future database authorization.
Existing test_fully_populated_typed_snapshot, test_manual_wire_rejection_oracle and
test_partition_descriptor_and_link_tampering remain NOT_RUN and do not cover the entire SQL proof.
Independent DDL/three-valued-logic review, per-field negative vectors and deployed-schema evidence
remain absent. DOMAIN_CONTRACT_REVIEWER + INDEPENDENT_CODEC_REVIEWER identities/signatures
UNRESOLVED. The proof enables deliberation; it approves neither schema nor SNAP-P03.


## Order v1.9 / candidate 0.21 decision summary

Technical opinion: REVISE (recommendation only, not a human decision).
Attach an independent eight-field nonnull proof before approving descriptor.
Manual example: nullable=false 62000000000000000130 versus true 62000000000000000131. No generated value or digest.
Alternative/binary risk: Catalog-nullability alternative changes even empty-view descriptor/digest.
Insufficient evidence: Insufficient independently reviewed predicate/CHECK proof for all eight fields; central table wording about ordinal is a candidate claim, not established proof.
Compared with SNAPSHOT-INTERPRETATION-REVIEW.md row SNAP-P03: same rule
candidate-0.15/P03, alternative and wire-impact description; no semantic change.
The component mappings and named written tests in the v1.8 review below remain applicable
and NOT_RUN; dependency on independent semantics/byte review is unresolved.
All changed interpretations require explicit version/migration disposition, not relabeling @1.
Owner: DOMAIN_CONTRACT_REVIEWER + INDEPENDENT_CODEC_REVIEWER; identities UNRESOLVED.
Actual decision/signature: UNRESOLVED. State: PENDING_HUMAN_APPROVAL.


## Order v1.8 / candidate 0.20 component review

PENDING_HUMAN_APPROVAL / NOT_RUN. Review focus: eight-field non-null published view.
Static evidence: emitter.recipe / streams; oracle.fixture_snapshot constructs candidate streams;
expected_wire_review.validate_slots / snapshot_reference.table independently parses the relevant layers.
Comparator validate_frozen invokes validate_slots on expected bytes; compare_frozen compares
record content, not an independent interpretation of observed wire semantics.
Changing nullable flags, field order, type or PK position changes descriptors and upper hashes. Recommend current eight fields conditional on independently reviewed SQL predicate/check proof. No SQL was executed; non-null assumptions remain unproved. A different descriptor requires versioned @2 proposal and view/envelope migration.
Manual fragments below are examples only; no SHA or slot result was generated.
The named source tests below are retained unchanged and NOT_RUN. Required future evidence:
independent positive/negative literals, reviewer proof for every affected layer, explicit
version rejection and reproducible authorized comparison. Existing tests do not establish
approval or binary compatibility. No emitter, comparator, parser, oracle or test was changed.
Owner: DOMAIN_CONTRACT_REVIEWER with INDEPENDENT_CODEC_REVIEWER; identities UNRESOLVED.
Decision required: accept the exact current rule and its compatibility rationale, or request
a separately reviewed versioned alternative. Neither route is approved by this review.

PROPOSED / PENDING_HUMAN_APPROVAL / NOT_RUN. Candidate0.19; no signature or decision supplied.
Rule identity remains candidate-0.15/P03; contract MPT-SNAPSHOT@1.

## Current rule
published_positions columns are position_id:text, version:bigint, lifecycle:text, side:text, remaining_quantity:bigint, average_entry_price:numeric, domain_id:text, ordinal:bigint; semantic nullable=false for each; PK position_id.

## Alternative
Use catalog view nullability rather than candidate semantic nonnull proof.

## Byte example
Descriptor nullable=false frame is 62000000000000000130; nullable=true is 62000000000000000131. SQL NULL frame 4e0000000000000000 is rejected in a nonnull field. These are manual fragments.
No generator, codec or digest calculation was used for this example. It fills none of the 428 slots.

## Compatibility and semantic risk
One descriptor flag changes even an empty view digest and its envelope. Changing flags cannot be treated as formatting-only.
The SQL predicate/CHECK may not prove every nonnull claim under all permitted states. A domain/DDL reviewer must examine the proof; this order runs no SQL.

## Positive / negative cases and affected contracts
Positive: exact current-rule representation and membership. Negative: the alternative encoded under
the unchanged current identity must be rejected, not normalized or accepted as equivalent.
Affected: FULL-SNAPSHOT-CONTRACT.md, SNAPSHOT-INTERPRETATION-REVIEW.md,
snapshot_schema.json/snapshot_compound_vectors.json as applicable, expected_bundle_emitter,
snapshot_oracle and expected_wire_review. Accepted ADR/MIR contracts remain unchanged.
Tests for review: test_fully_populated_typed_snapshot; test_complete_empty_and_multiple_partitions; test_manual_wire_rejection_oracle; expected_wire_review.table/validate_slots. All NOT_RUN.

## Recommendation for human consideration
Retain semantic flags only conditionally on an independently recorded proof for all eight fields. If proof is absent, keep this decision pending rather than falling back silently.

## Decision requested
Approve descriptor and proof references, or reject/request a versioned descriptor change.
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
