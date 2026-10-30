# SNAP interpretation review - candidate 0.15

## Order v1.7 / candidate 0.19 individual decision pages

Each page preserves the current rule, presents an alternative/manual byte fragment, compatibility
risk, affected tests, justified recommendation and empty human approval/rejection fields:
- [SNAP-P01](SNAP-P01-DECISION.md): partition identity and empty-table membership.
- [SNAP-P02](SNAP-P02-DECISION.md): full metadata streams.
- [SNAP-P03](SNAP-P03-DECISION.md): semantic nonnull view descriptor and proof.
- [SNAP-P04](SNAP-P04-DECISION.md): framed-PK/UTF8 ordering.
- [SNAP-P05](SNAP-P05-DECISION.md): typed precision, NULL, JSON and temporal boundaries.

All remain PENDING_HUMAN_APPROVAL. Recommendations are not selections or signatures.
No wire, recipe, accepted ADR or generated expected result changed. Manual fragments fill none
of the 428 slots. EXPECTED-DECISION-PACKAGE.md identifies separate phase authorizations.

## Order v1.5 / candidate 0.17

REVIEW_ONLY / NOT_RUN. All five decisions remain PENDING_HUMAN_APPROVAL.
The matrix below now identifies human ownership and individual decision status. No rule changed.
Named assignees, signed decisions and compatibility acceptance remain UNRESOLVED.
See EXPECTED-STATIC-REVIEW.md and EXPECTED-EXTERNAL-FREEZE-CONTRACT.md for admission gaps.

## Current order v1.4 / candidate 0.16

The five rule IDs candidate-0.15/P01 through candidate-0.15/P05 identify exactly the candidate
rules in the table below, not an ACCEPTED decision. Emitter requires all IDs supplied explicitly.
Comparator requires the same IDs bound by authenticated external human approval; a pending state
or different rule rejects. No human decision has been made by this materialization.
Generation binds this document's bytes; any review-document drift invalidates the source identity.
Semantic independence, compatibility, reviewer assignments and all approvals remain pending.
READY_FOR_REVIEW / NOT_RUN describes only the authored interface.

DOCUMENTED / PENDING_HUMAN_APPROVAL. No accepted decision or wire change.
These five candidate rules are the explicit subjects of review, not new approvals.
A divergent decision requires a proposed new wire version, regenerated independent expectations,
compatibility/migration analysis and separate authorization before implementation.

| Proposal | Exact candidate rule | Alternative for human consideration | Byte/hash and compatibility impact | Positive / negative example | Affected documents/tests | Human decision | Human owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SNAP-P01 | Every POSITION table and aggregate starts F(v,MPT-SNAPSHOT@1/POSITION), F(p,exact position_id); include all scoped empty tables; GLOBAL has no p | Put identity only at aggregate level; omit empty tables | Prefix/membership change alters partition digests; incompatible with existing candidate expectations | P-A and P-B separate; empty or missing identity rejected | FULL-SNAPSHOT-CONTRACT, compound vectors, oracle, complete_empty_and_multiple_partitions | Approve exact prefix/membership or request versioned alternative | DOMAIN_CONTRACT_REVIEWER + INDEPENDENT_CODEC_REVIEWER; assignees UNRESOLVED | PENDING_HUMAN_APPROVAL |
| SNAP-P02 | Concatenate full normal-version table streams of publication_barrier, publication_batch, publication_cut, public_projection in qualified UTF-8 order | Serialize rows only or hashes only | Changes metadata digest and envelope; incompatible with candidate bytes | Four full streams; reordered/duplicate/absent stream rejected | FULL-SNAPSHOT-CONTRACT, reference.metadata, full snapshot tests | Approve full-stream recipe/order | DOMAIN_CONTRACT_REVIEWER + INDEPENDENT_CODEC_REVIEWER; assignees UNRESOLVED | PENDING_HUMAN_APPROVAL |
| SNAP-P03 | View has position_id,version,lifecycle,side,remaining_quantity,average_entry_price,domain_id,ordinal with canonical types and semantic nonnull; PK position_id | Use catalog view nullable flags | Descriptor change affects published/envelope hashes even for empty view | Published predicate plus CHECK implies nonnull ordinal; actual NULL rejects | DDL view inspected only, conformance field map, codec/ref view fixtures | Approve semantic descriptor and its proof obligation | DOMAIN_CONTRACT_REVIEWER + INDEPENDENT_CODEC_REVIEWER; assignees UNRESOLVED | PENDING_HUMAN_APPROVAL |
| SNAP-P04 | Rows sort unsigned lexicographically by full F(k,PK scalar frames), including length; JSON keys raw UTF-8; table names qualified UTF-8 | SQL collation, numeric ordering or payload-only key ordering | Different ordering changes row/table/upper hashes; no chronological meaning | a,b,aa; duplicate framed PK rejects | FULL-SNAPSHOT-CONTRACT, PK-ADVERSARIAL, permutation/corruption tests | Approve framed-key ordering, distinct from temporal order | DOMAIN_CONTRACT_REVIEWER + INDEPENDENT_CODEC_REVIEWER; assignees UNRESOLVED | PENDING_HUMAN_APPROVAL |
| SNAP-P05 | Typed scalar tags; SQL NULL distinct JSON null; finite Decimal coefficient/stored scale; no Unicode normalization; raw bytea; exact UTC micros; JSON lossless stored structure | Normalize scale/Unicode, use float/time milliseconds or plain JSON text | Representation changes all containing hashes and loses declared distinctions | 1.0 differs 1.00; composed/decomposed text differ; float/nonfinite/naive timestamp reject | snapshot_vectors, compound vectors, scalar/nested JSON/time tests | Approve typed/precision rules; finite PostgreSQL limits remain separate | DOMAIN_CONTRACT_REVIEWER + INDEPENDENT_CODEC_REVIEWER; assignees UNRESOLVED | PENDING_HUMAN_APPROVAL |

Compatibility column refers to the candidate 0.14 representation only; no binary equivalence has
been executed. Approved ADR semantics D011-001..003/D014-005 are unchanged. Local candidate
choice does not approve persistence execution or establish availableAt <= decisionTime.
Review roles: DOMAIN_CONTRACT_REVIEWER for semantics and INDEPENDENT_CODEC_REVIEWER for byte
derivation; both assignees and decision records UNRESOLVED. Each decision must identify proposal,
chosen alternative, exact contract/version, rationale, reviewer and timestamp. Until then every
proposal remains PENDING_HUMAN_APPROVAL; generation of fixtures is not consent.
