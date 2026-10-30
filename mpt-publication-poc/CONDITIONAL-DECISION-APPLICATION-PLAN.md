# Conditional decision application plan - candidate 0.24 / order v2.2

## Order v2.4 / candidate0.25 - narrow coverage clarification

USER_CONDITIONAL_DIRECTION_RECORDED / FORMAL_APPROVAL_PENDING is a documentary tracking label
only; the consolidated declaration/conditions and ARCH-ADAPT-001 review are in
EXPECTED-DECISION-PACKAGE.md. All six actual approvals remain PENDING_HUMAN_APPROVAL.
Rows A/B/C below remain conditional and do not authorize editing or execution.
P04 must explicitly include representation-collision negatives as well as duplicate/permutation
controls; snapshot ordering determines neither UI display order nor MIR temporal eligibility.
P05 requires explicit independently reviewed PostgreSQL bounds before any DB-domain assurance;
until then finite extremes remain unproved/excluded, not inferred from Python/wire bounds.
P03 requires evidence of the actually applied DDL/view in addition to the candidate static proof.
These clarify evidence obligations only; no wire/DDL/source/test/patch change.

Binding consequence: H11 below identifies the preserved input0.23 decision packet, not the newly
extended0.25 packet. Keep H11 as historical provenance. Any future approval/application must bind
the current decision packet hash in the final0.25 MANIFEST as well as the preserved evidence
hashes; old H11 alone cannot approve new conditions. No existing signature is presumed.

PROPOSED / CANDIDATE_EDIT_ONLY / DECISION_APPLICATION_PLAN_READY / NOT_RUN.
This is a future application plan, not an approval or instruction to execute its steps now.
READY_FOR_HUMAN_DECISION describes the existing packet's completeness; neither that state nor
this plan means READY_FOR_EXECUTION. All six decisions below remain PENDING_HUMAN_APPROVAL.
Recommendations are CONDITIONAL_RECOMMENDATION; identities, decisions and signatures unresolved.

## Baseline and authority

Actual candidate0.23 verified:71 files /70 listed hashes, no mismatch; HEAD
27b2db3e3818e4325e5cd3df27f4ba1bc797ab15; input external manifest
d52f76155bf5e6b89daeb8a4727ab3f1cd5c9d4c82e477c0200411e55070bd50.
AGENTS.md, Decision Register, CURRENT-RESEARCH-CONTRACTS.md and MIR runtime contracts consulted.
D011-001, D014-005 and D014-007 preserve persistence/temporal/authority boundaries.
This plan changes no accepted contract and grants no RH, MIR, provider or scientific authority.
Bindings H01-H13 below identify exact preserved evidence, not ZIP/attachment equivalence.

## A. Six conditional application rows

All paths below are relative to this candidate directory. A listed file/symbol is a future
review/change surface, not an instruction to edit it in this round. Approved selection of an
already implemented candidate rule can require documentation alignment only, not a redundant
source rewrite. Any actual edit needs separately authorized scope. DCR = DOMAIN_CONTRACT_REVIEWER;
ICR = INDEPENDENT_CODEC_REVIEWER; API = API_CONTRACT_REVIEWER. All people UNRESOLVED.

| Decision / actual state / separate recommendation | Human-bound document/hash and exact proposed text | Future files/symbols only after approval and authorized edits | Bytes/version/fixtures/consumers | Required positives/negatives/compatibility/oracle | Missing evidence, owner and blocking condition | Rollback/version strategy |
| --- | --- | --- | --- | --- | --- | --- |
| P01 / PENDING_HUMAN_APPROVAL / CONDITIONAL_RECOMMENDATION retain prefix and all members | H01 Current rule; H11 section1 membership; candidate-0.15/P01 | Align FULL-SNAPSHOT-CONTRACT partition paragraph and central SNAP-P01 row if explicitly approved; review codec.snapshot/table_bytes, oracle.fixture_snapshot/relation, wire_review.validate_slots, reference.aggregate, emitter.streams; no source change needed if exact rule retained | Preserve22 scoped/8global, every empty scoped member per present position, GLOBAL without position; different prefix/membership requires new wire/recipe disposition and re-reviewed vectors, not silent @1 | complete_empty_and_multiple_partitions; partition_descriptor_and_link_tampering; independent P-A/P-B/empty-member literals; reject missing/extra/foreign scoped member and wrong version | ICR membership and literal review plus DCR decision; block on missing reviewer evidence or ambiguity in membership | R1 below: retain old rule/source/bundle, append superseding decision; no deletion of old evidence |
| P02 / PENDING_HUMAN_APPROVAL / CONDITIONAL_RECOMMENDATION full streams | H02 Proposed normative wording; identical quotation in H11 section2; candidate-0.15/P02 | Only after approval align FULL-SNAPSHOT-CONTRACT:124-125 and central P02 row; review codec.snapshot metadata, oracle.fixture_snapshot metadata_bytes, reference.metadata, wire_review.validate_slots, emitter.streams; add independently authored multirow metadata vectors/tests under separate edit authority | Existing candidate full streams unchanged; rows-only/outer-only/digest-pairs differ. If an approved @1 already means rows-only, block pending explicit new version/reader migration. Expected metadata/envelope/source hashes must be rebound | Existing typed/empty controls plus new multirow metadata with independent bytes/length/oracle; reject reordered/missing/extra streams, changed descriptor/count, rows-only @1; permutation must preserve canonical bytes | DCR resolves encoded-rows ambiguity and compatibility history; ICR reviews206/264-byte derivations and missing multirow oracle. MULTI has multirow position_guard, not metadata | R1 plus preserve both wire identities/fixtures if alternative chosen; never reinterpret stored @1 bytes |
| P03 / PENDING_HUMAN_APPROVAL / CONDITIONAL_RECOMMENDATION semantic nonnull under exact DDL | H03 field proof and serialization proposal; H12 exact schema.sql; candidate-0.15/P03 | Align central P03/proof references only after approval; review codec.snapshot view_schema/rows_bytes, oracle.fixture_snapshot/relation, reference.table, wire_review.scalar/validate_slots, collector view_columns; no DDL change implied | Eight nonnull fields and PK position_id preserved if exact proof adopted; descriptor/order/type change alters even empty-view digest and envelope and needs versioned expectations/reader review | Eight independent NULL mutations, missing/extra field, nullable descriptor tampering; positive empty/typed view; documentary SQL negatives for NULL projection version, PUBLISHED+NULL ordinal, pending/NULL; no DB execution allowed here | DCR+ICR review exact NOT NULL/biconditional/INNER JOIN proof. Deployed schema identity and SQL tests absent; block any deployment claim or changed DDL/view until separately proved | R1; invalidate applicability if DDL/view hash changes, preserve old proof scope; never broaden proof retroactively |
| P04 / PENDING_HUMAN_APPROVAL / CONDITIONAL_RECOMMENDATION distinct order domains | H04 Current rule and Byte example; candidate-0.15/P04 | Align central P04 and FULL contract sorting wording if needed; review codec.rows_bytes, oracle.relation/aggregate_stream, reference.table/aggregate, wire_review.table, emitter.streams | Full framed PK unsigned bytes, raw UTF8 keys/names; SQL collation/numeric order and event chronology remain separate. Any altered sort requires version/vectors; no inherited equality | empty_multirow_order_and_corruption; independently authored a,b,aa and duplicate-key oracle; reject payload-only order/duplicate PK, accept permutation; version dispatch negatives | ICR ordering/collision proof and DCR exact domain decision; block normalization or claim that canonical sorting proves time order | R1; preserve old ordered streams/digests and distinct new recipe/version |
| P05 / PENDING_HUMAN_APPROVAL / CONDITIONAL_RECOMMENDATION exact typed precision | H05 Current rule and exclusions; candidate-0.15/P05 | Align central P05 only after approval; review codec.scalar/decimal_bytes/json_value, oracle.scalar_fixture/numeric_payload/json_fixture, reference.scalar/number/json_node, wire_review.scalar/decimal_payload/json_node | SQL NULL vs JSON null, stored Decimal scale, raw bytea/UTF8, UTC micros remain distinct; never recover precision already lost or infer PostgreSQL finite extremes. Coercion/normalization is incompatible | scalar/nested JSON/time controls, manual NULL and1.0/1.00 literals; float/nonfinite/naive-time/invalid-Unicode rejection; microsecond distinctness and explicit boundary exclusions | ICR literal/precision review, DCR scope; block unsupported DB-range or original-input reconstruction claims | R1; new identity for changed representation; do not regenerate old results as if unchanged |
| report@3 / PENDING_HUMAN_APPROVAL / CONDITIONAL_RECOMMENDATION explicit incompatible seven-counter report | H06 exact proposal; H07 migration; H08 patch bound to H09 comparator and H10 tests | Future patch changes compare_frozen counter/version only and adds two test methods; authorized follow-up also addresses missing assertion/cases and actual readers. No observer, wire, DDL or authority migration implied | @2->@3 incompatible; existing six meanings retained, seventh added; no automatic shim; external consumers UNKNOWN; all reports/source approvals need exact new identity | Patch counter matrix/timeout-interruption plus existing abort/recheck/legacy controls; add second inequality, triple/extra duplicates and cross-version reader rejection; independent declarative counts not SUT-derived | API genuine decision and exact patch/source binding; missing readers/negative evidence and external inventory block rollout. Source drift blocks application until rereview | R1 plus retire @3 rollout explicitly if reversed; @3 artifacts retained, @2 only through explicitly selected reader, never relabel/strip metric |

R1 documentary rollback: before any future authorized application, preserve exact predecessor
documents/source/manifest and authentic decision evidence in immutable versioned custody.
If a decision is withdrawn, append its revocation/superseding rationale and affected versions,
stop further admission, and propose an explicitly reviewed successor. Do not edit historical
signatures, generated bundles, frozen expectations, failed runs or evidence to appear approved.
Restore a candidate document only as a new recorded revision referencing both old and new hashes.
No automatic reset, checkout, deletion, commit or archive is authorized by this plan.
A failed implementation/validation leaves that candidate unpromoted; prior approval cannot be
reused with changed bytes. Version-specific reader dispatch must remain explicit.

## B. Conditional API migration sequence

1. Receive genuine API decision binding H06-H10 and H11 plus actual identity/date/scope/rationale/
   verifiable record. APPROVE semantics alone does not authorize applying code or running tests.
   REVISE requires specified revisions; REJECT retains @2 without pretending to count valid
   comparisons; DEFER leaves refusal. A demand for observed-wire validation requires a different
   reviewed design, not reinterpretation of record_check.
2. Obtain separate edit authorization for the exact patch and any follow-up tests/readers.
   Re-hash sources and compare old-side hunks. If any binding or line/content changed, stop and
   re-review; no fuzz application or automatic conflict repair under an old decision.
3. Only in that later authorized task apply the reviewed patch, record exact before/after hashes,
   update approved caller contracts and prepare missing cases. No generation/freeze/compare occurs
   as a side effect. Unknown consumers block external integration, not honest inventory recording.
4. Obtain independent test/runtime permission and evidence for the approved candidate before
   rollout. This plan provides no such permission; source tests remain NOT_RUN.
5. If validation fails or authority changes, retain failure evidence and use R1. Never fall back
   to @2 by removing the version marker/seventh field from an @3 result.

### Exact seven-counter semantics and invariants

| Counter | Population (applies only to a returned completed comparison report) |
| --- | --- |
| required_slots | Unique required IDs |
| observed_slots | Entire observation list, including malformed/extra/duplicate entries |
| compared_valid_slots | Required IDs occurring exactly once, passing record_check, whose hex/length/sha256/error comparisons all finished, equal or different |
| matched_slots | Subset of compared_valid with four fields equal |
| missing_slots | Required IDs without indexed string ID; invalid presence is not absence |
| extra_slots | Distinct non-required string IDs, including invalid/duplicated extra IDs |
| invalid_slots | Set of malformed/record-invalid/duplicate entry indices; all duplicate occurrences invalid |

matched <= compared_valid <= required - missing <= required;
compared_valid <= observed - invalid; all counts nonnegative. Each counted comparison maps to
one unique valid observed entry. Metrics overlap and use different units; never add them into a
partition. All duplicate copies are invalid; a required invalid row is not missing; malformed ID
may leave a required ID missing; extras never count. Empty observation list has missing=required
and the other counts0 only if admission, diagnostics and recheck complete.
record_check validates fields, hex, bounded length/hash and null error; it does NOT validate
observed snapshot wire semantics. Consistent malformed-wire bytes may count but mismatch.
Expected validate_slots is not an observed-wire validator. No success or partial report after
admission/error/timeout/interruption/budget/recheck failure; local counters are not output.
The return remains after finally recheck. OS termination safety still requires real host evidence.

| Known consumer or missing surface | Future compatibility requirement / negative evidence |
| --- | --- |
| test_expected_bundle_review.ExpectedBundleReview.compare; direct negatives at218/334 | Only identified comparator callers; preserve args/admission, require explicit@3/seventh count; patch cases remain NOT_RUN |
| test_honest_counters and readers of differences in that test module | Preserve six prior meanings; assert explicit version, no legacy compared_slots inference |
| compare_frozen -> validate_frozen | Internal validation; no changed authority callback or schema/template semantics |
| Operational @2-only reader | None found; must reject@3/missing/unknown marker before consumption |
| Operational @3-only reader | None found; must reject@2/missing/unknown marker before consumption |
| External consumers | UNKNOWN; named owner inventory and migrated-reader evidence required for rollout |
| Host/report publisher | Not operationally qualified; no report on failed admission/recheck/forced termination |

No automatic shim, silent conversion, default field or zero-fill. Cross-version reader tests
cannot be claimed written against an absent reader. Test plan must include those two rejection
directions and abort input when the separately approved reader exists.
Additional unimplemented test requirements: second inequality assertion, triple duplicate,
duplicated extra, malformed-plus-missing, valid-record mismatch and real OS timeout/custody.
Existing patch has counter matrix and raised timeout/interruption cases, not real monitor proof.

### Textual applicability at this baseline

Five patch hunks were inspected as text, without applying or invoking code:
comparator old-side lines179,192,194,197 and test module line88. Old content and hunk line counts
all match exact H09/H10. H08 is unchanged. Not stale against candidate0.23/current0.24 sources.
This is not Python syntax validation, a test result or evidence of runtime behavior.
Any future comparator/test/patch hash change, reader change or semantic change triggers renewed
API review and hash binding; same filename or HEAD alone is insufficient.

## C. Decisions, infrastructure, phases and product gates

| Authority layer | Required real record/evidence | Responsible human role | Current state / consequence |
| --- | --- | --- | --- |
| Six semantic/API decisions | Separate APPROVE/REVISE/REJECT/DEFER for each; identity, UTC date, scope, exact version/hash, rationale/conditions and verifiable signature/record | DCR+ICR for each SNAP; API for report | All PENDING_HUMAN_APPROVAL; use blank six-row form in H11; AI must not fill actual decisions |
| Independent reviewers | Named qualification and separation from generator/implementer | SECURITY_AUTHORITY_OWNER | UNRESOLVED; role names are not people or evidence |
| OAA/verifier/trust policy | Qualified backend, genuine authenticated approval, scope/role/expiry/revocation negatives | SECURITY_AUTHORITY_OWNER | BLOCKED; default-deny interface only |
| Actual loaded bytes/runtime/import closure | Measured approved executable/stdlib/transitive modules and source identity; substitution negatives | RUNTIME_SECURITY_REVIEWER | BLOCKED; file hashes alone insufficient |
| Immutable handles | Protected stable file identity/ACL, no reopen fallback, TOCTOU and recheck evidence | RUNTIME_SECURITY_REVIEWER | BLOCKED |
| Network-free isolation and native limits | Owned process scope, denied network/privileges, finite CPU/memory/wall/output/cleanup limits, external monitor and forced-exit proof | OFFLINE_EXECUTION_OWNER | BLOCKED; local guards not external containment |
| GENERATE_EXPECTED | Separate bounded-run permission after semantic and technical closure; exact six inputs/support/runtime hashes and output custody | Authorized execution approver, identity UNRESOLVED | NOT_AUTHORIZED; future output only EXPECTED_UNVERIFIED/review=null plus immutable provenance |
| REVIEW_AND_FREEZE | Separate permission and independent per-slot review of original generated evidence | Independent human reviewer, identity UNRESOLVED | NOT_AUTHORIZED; generation does not grant freeze |
| COMPARE_FROZEN | Separate permission, authentic frozen binding, approved report/consumers, measured observer/host, finite controls | Authorized comparison approver, identity UNRESOLVED | NOT_AUTHORIZED; freeze does not grant comparison |
| Product | Separate gate decisions, outside this packet | Product gate owners UNRESOLVED | EXEC-G1/PERS-G1 OPEN; PUB-T13B PENDING_HUMAN_APPROVAL; A0 active |

No backend, verifier, algorithm, vendor, key, certificate, environment, monitor or identity
is selected/created. No filled form is authenticated human authority.
Logical MPT publication cut never substitutes MIR availableAt <= decisionTime.
RH historical evidence/contracts, T2a/T2b, T3a/TP, DO_NOT_NOTIFY and all accepted invariants remain.
The eight-entry capsule descriptor remains preserved historical candidate0.20 provenance; future
assembly requires separately reviewed provenance refresh and external binding, not automatic
inclusion of this plan or expected bundle as a ninth member.

## Immutable references for conditional decisions

Reference means exact current document bytes plus the indicated section in A/B; future changes
invalidate this binding until reviewed. The final external MANIFEST also binds this new plan.

| Ref | Preserved document/source | SHA256 |
| --- | --- | --- |
| H01 | SNAP-P01-DECISION.md | 017391c0fce1b9083c1b62a69ef9299615a8678752a4b98bd6cbc329eb16c048 |
| H02 | SNAP-P02-DECISION.md | 6632dcd7736f5d22297ff0c594a2c8d2c6f6c8bb9fda3807fad4ce186c4bd0b9 |
| H03 | SNAP-P03-DECISION.md | dc35055bfa2423eaa71898eb7407816d07effb415d11272a0e4437c57d32fd0b |
| H04 | SNAP-P04-DECISION.md | 8af1937c93d0583f9bdceb82802ee62c448738e8828805c9d3fa1646c5169fee |
| H05 | SNAP-P05-DECISION.md | e8ee7ac701eeedddf6ee1b7e7e1ba2ff39f1107c3e19b62afafc43b56cf91e36 |
| H06 | EXPECTED-COUNTER-PROPOSAL.md | e3092f9debe152025ebd5443f9b8bf071f0d15f0416ace22d357c180ce7a7863 |
| H07 | EXPECTED-API-MIGRATION.md | 93c77cf9fe4e58e7dd7698caf34ce6479716a5b8eefc700758a8e001201e3a63 |
| H08 | COUNTER-MIGRATION.patch | 89ddfa3fd93d0e2d5e4f6fb5ae5ecec33eb7bf8a2968c718fbe1ebd89fac7ea2 |
| H09 | runner/frozen_bundle_compare.py | 8d8ca372c5053f56a031935ef6c1574fbe04faaa46f38a16d48def8de333afe9 |
| H10 | runner/test_expected_bundle_review.py | 2545bfd378666f67e029b759edc87625c14c1b3046f5e3f31bff047d1cf37303 |
| H11 | EXPECTED-DECISION-PACKAGE.md | d9446cad9b026d290badc6c7739826ae05575f2bc718a8549acd8327568dc3eb |
| H12 | schema.sql | e1feebaf8b6cdce323fd4c7b95bdd08c2d1b0907f9d43f673e3cfd1933f6542a |
| H13 | SNAPSHOT-INTERPRETATION-REVIEW.md | 0e56704abe70a6c4f0f59b19240a4d97e6b3cd07cdcc0a262934d54b1b81d9c9 |

Status: DECISION_APPLICATION_PLAN_READY / NOT_RUN, not READY_FOR_EXECUTION.
428 defined slots (EMPTY43/TYPED287/MULTI98); generated0/reviewed0/frozen0/observed0; all UNRESOLVED.
No experimental conformance demonstrated. No concrete new source/patch incompatibility found;
the report-version break and P02 possible prior-@1 semantic conflict remain explicit decisions,
not bypassed assumptions. No Python/import/compile/tests/SQL/DB/container/runner/capsule/
generation/freeze/comparison/sign/install/network/controller/patch application/production edit/
accepted-contract edit/commit/ZIP occurred.
