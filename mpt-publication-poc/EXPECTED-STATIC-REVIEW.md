# Expected static review - order v1.5 / candidate 0.17

## Order v1.7 / candidate 0.19 final static checkpoint

REQUIRES_HARDENING / NOT_RUN. Source and call sites were inspected, not executed.
The candidate review is complete as a decision package; technical closure is not claimed.
EXPECTED-DECISION-PACKAGE.md separates human choices from absent mechanisms.
EXPECTED-API-MIGRATION.md records all discovered callers and the counter mismatch.

| Finding | File / function and protection | Written negative / acceptance evidence | External dependency and precise status |
| --- | --- | --- | --- |
| SR15-01 | expected_admission.AdmissionAdapter.authorize/recheck deny; require_admission binds phase/raw/context | test_disabled_and_external_rejections_before_observe; test_wrong_admission_receipt_and_legacy_true_callback; new test_legacy_keyword_and_generation_defaults_rejected; real signer/path/module attack evidence still required | Interface FIX_CANDIDATE; actual OAA/loader/monitor BLOCKED; authority choice PENDING_HUMAN_APPROVAL |
| SR15-02 | expected_bounds.parse/guard/canonical and comparator.compare_frozen bound local parsing/diagnostics/output | test_limits_abort_without_result; new test_abort_paths_never_publish_report; future native accounting/deadline/exit evidence | Local guards FIX_CANDIDATE; OS proof BLOCKED; budgets PENDING_HUMAN_APPROVAL |
| SR15-03 | comparator._validate_claims/validate_frozen exact order/JSON; expected_wire_review.validate_slots structural links | test_canonical_order_and_post_freeze_bytes; test_semantically_wrong_frame_with_consistent_hash; test_partition_descriptor_and_link_tampering; independently reviewed bytes required | FIX_CANDIDATE; five SNAP pages PENDING_HUMAN_APPROVAL; human truth absent |
| SR15-04 | test_expected_bundle_review separates SimulationAdmission from manual controls; extra legacy-keyword/abort tests added | Real backend negatives remain necessary; simulated propagation is not OS/signature evidence | Written plumbing FIX_CANDIDATE; real backend tests BLOCKED |
| SR15-05 | expected_wire_review no oracle/SUT imports; manual scalar frames retained; five per-rule forms expose common assumptions | test_manual_wire_rejection_oracle and supplemental type/time controls; human per-slot/semantic review required | Independent semantic assurance PENDING_HUMAN_APPROVAL; no executed closure |
| SR15-06 | comparator.compare_frozen returns report only after finally recheck; sets prevent repeated invalid-index counting; six @2 counters have mixed units | test_honest_counters and test_abort_paths_never_publish_report; new metric/consumer cases in migration document | Existing counters FIX_CANDIDATE; separate actually-compared measure absent/BLOCKED pending report decision |

Specific v1.7 issue: @2 counts extra IDs, not compared-valid required IDs. This is a mismatch
between requested reporting views, not a reason to redefine observed/matched or sum overlapping
counts. Recommend versioned seventh metric only after explicit decision; no report change here.
Abort source audit: validation exceptions precede observe; observer/budget errors propagate;
recheck in finally precedes return. No module writes a report. New sentinel tests are NOT_RUN.
Residual host risk: a future wrapper must never turn an exception/timeout into synthetic success.

## Order v1.6 / candidate 0.18 remediation (current disposition)

REQUIRES_HARDENING / NOT_RUN. Historical findings below are preserved as reviewed baseline.
No fix is runtime-validated, approved or closed by this source edit.

| Finding | Candidate implementation | Prepared test(s) in ExpectedBundleReview | Expected future evidence | External dependency / residual risk | Verdict |
| --- | --- | --- | --- | --- | --- |
| SR15-01 | expected_admission.AdmissionAdapter denies authorize/recheck by default; immutable receipt checks bind phase/raw/binding; emitter and comparator require explicit adapter/budgets, no bool callback | test_disabled_and_external_rejections_before_observe; test_wrong_admission_receipt_and_legacy_true_callback; test_expected_immutability_after_observer | Real signature/policy/path/module substitution refused before SUT; immutable-handle recheck after observer | Actual signature algorithm/authority/roles/revocation, stable OS handle, loaded runtime proof and monitor are unselected/unimplemented. Receipt is NOT proof by itself. SimulationAdmission exists only in tests | BLOCKED for real admission; fail-closed interface FIX_CANDIDATE |
| SR15-02 | expected_bounds pre-scans JSON byte/depth/node/string bounds, guards objects/Decimal, preflights canonical output; emitter bounds source/schema/fixtures/hex; wire parser bounds before slicing; comparator bounds records/diagnostics/output and removes repr | test_limits_abort_without_result; existing typed guards | Excess rejected without a result or truncated-success diagnostic | Proposed ceilings still require approval. Caller-created objects/observer allocations, native memory, deadlines and process exit require external enforcement | FIX_CANDIDATE; OS containment BLOCKED |
| SR15-03 | exact canonical JSON and sorted unique 428 IDs; expected_wire_review independently validates schema descriptors, row PK, scalar tags/ranges, JSON structure/order, partition identity/membership, cross-slot links and aggregate/metadata/view/envelope structure | test_canonical_order_and_post_freeze_bytes; test_semantically_wrong_frame_with_consistent_hash; test_partition_descriptor_and_link_tampering; test_manual_wire_rejection_oracle | Self-consistent wrong frames rejected independently of their digest before observer | Independent parser is new unexecuted code, not a human oracle. Uses existing candidate rules only; fixture-value truth and SNAP approvals remain pending | FIX_CANDIDATE / PENDING_HUMAN_APPROVAL |
| SR15-04 | Existing simulated tests adapted to explicit test-only admission; adversarial cases added, observer-call count assertions retained | New tests named above plus test_honest_counters | Separate plumbing failures, signed-backend controls and human/manual value checks | Fake rejection labels test propagation only, not real cryptography/OS attack handling; real backend tests blocked | FIX_CANDIDATE; external tests BLOCKED |
| SR15-05 | Wire-review module imports neither emitter/oracle/SUT/parser; manual literals retained for wrong type, NULL and temporal syntax; original supplemental tests unchanged | test_manual_wire_rejection_oracle; test_scalar_controls; test_partition_metadata_envelope_and_pk_controls | Independent human examination of manual frames, typed distinctions and all results | Shared wire contract and SNAP assumptions remain; no claim of semantic independence certified by imports | PENDING_HUMAN_APPROVAL |
| SR15-06 | Proposed report MPT-FROZEN-COMPARISON-REPORT@2 replaces compared_slots with six defined counters; no report on admission/overflow/observer/recheck failure | test_honest_counters; test_limits_abort_without_result | Missing/duplicate inputs yield exact counts; aborted run has no success report | API/report compatibility decision required; source tests unexecuted | FIX_CANDIDATE |

Candidate source additions: runner/expected_bounds.py, expected_admission.py, expected_wire_review.py.
Candidate source edits: expected_bundle_emitter.py, frozen_bundle_compare.py, test_expected_bundle_review.py.
Seven core payloads/eight core entries preserved. No runtime admission backend is included.
See EXPECTED-BUNDLE-SPEC.md for exact counter invariants, bounds and compatibility decision.
428 IDs unchanged, generated/reviewed/frozen/observed all zero. No runtime closure asserted.

REVIEW_ONLY / NOT_RUN. Overall verdict: REQUIRES_HARDENING / NOT_RUN.
This is source inspection by the authoring assistant, not independent human approval.
No Python import, compilation, test, emitter, comparator or capsule execution occurred.
No expected-result bytes/digests were generated. Counts below are structural document inspection.

## Authority and baseline

AGENTS.md and docs/ govern; D011-001..003 keep persistence outside the hot path and
rights-gated; D014-005 and MARKET-INTELLIGENCE-RUNTIME-CONTRACTS.md require
availableAt(input) <= decisionTime. Publication cuts cannot replace that condition.
FULL-SNAPSHOT-CONTRACT.md and SNAPSHOT-INTERPRETATION-REVIEW.md remain candidate semantics.
HEAD 27b2db3e3818e4325e5cd3df27f4ba1bc797ab15; 57 files; all 56 listed hashes matched.
Input manifest SHA-256 d0c0346e83b8cee0fe1601f53f8a2aa8548981df5fbfa594e4af6d19d80bf7f1.
No tracked diff existed; the candidate directory was untracked. This review preserves all code.

## Findings

| ID / severity | Evidence (relative to this directory) | Correction candidate / owner | Residual risk / disposition |
| --- | --- | --- | --- |
| SR15-01 BLOCKER | runner/frozen_bundle_compare.py:validate_frozen accepts authenticate(approval) == True, only checks bundle_path for truthiness/UNRESOLVED; no handle, filesystem identity, loaded-module evidence or external trust policy input. runner/expected_bundle_emitter.py:generate_expected hashes supplied emitter/oracle bytes, not loaded implementations. | External admission authority and measured loader contract in EXPECTED-EXTERNAL-FREEZE-CONTRACT.md; SECURITY_REVIEWER + OFFLINE_ENVIRONMENT_OWNER, people UNRESOLVED. Require pinned comparator/host/observer/emitter/oracle identities, absolute path/file identity and authenticated admission before invocation. | Unimplemented. Claimed hash equality cannot reject different loaded code or a nominal path pointing elsewhere. No execution readiness. |
| SR15-02 MAJOR | emitter:decode/canonical/generate_expected and oracle:numeric_payload/json_fixture allocate without input/output/depth/exponent bounds. comparator checks 8 MiB only after raw bytes exist; compare_frozen accepts unbounded observed list/strings and builds unbounded divergence output/repr. | Preallocation input/fixture/observed/output admission plus external memory/time enforcement; RUNTIME_REVIEWER. Select limits explicitly and reject overflow without truncating into success. | Existing local guard is not containment. Limits remain proposed; no runtime enforcement evidence. |
| SR15-03 MAJOR | comparator:validate_frozen verifies record byte/length/digest consistency but uses set equality for IDs; does not require sorted record order or canonical JSON bytes and does not validate binary tag/schema/layer semantics. A newly signed reordered or self-consistent wrong-frame bundle can pass these checks. Post-freeze byte mutation with unchanged signed hash is rejected. | Separate human semantic oracle and strict canonical/record-order admission; malformed-layer fixtures, binding-independent schema checks. CODEC_REVIEWER. | Integrity is not semantic conformance. Existing claims of rejecting all incoherent bytes/order must be narrowed. No wire change authorized. |
| SR15-04 MAJOR | test_expected_bundle_review.py:setUp/simulated_review/observe share generator-derived records; test_each_slot_comparison mutates only error; metadata/envelope checks reuse oracle.part/sha. No independent signed authority, path substitution, loaded-module substitution, post-observation immutability or canonical-order rejection test. | Add the planned controls below under separate reviewed host contract; INDEPENDENT_CODEC_REVIEWER and SECURITY_REVIEWER. | Tests are plumbing simulations, not independent expected-value validation; 428 subtests are not 428 semantic oracles. No test success claimed. |
| SR15-05 MAJOR | emitter and SUT tests share snapshot_oracle.fixture_snapshot/populated_fixture assumptions, schema and candidate SNAP rules. scalar_fixture(jsonb,None) denotes SQL NULL; top-level JSON null uses explicit part(J,json_fixture(None)) only. The 428-slot dataset contains no bytea column and does not exhaust scale/Unicode/time alternatives. | Human review of manual vectors, independent framing arithmetic and five SNAP decisions; retain supplemental typed controls outside 428-slot inventory. DOMAIN_CONTRACT_REVIEWER. | No direct SUT dependency found, but correlated semantic mistakes remain possible. No approval of NULL or temporal interpretation by this review. |
| SR15-06 MINOR | comparator:compare_frozen reports compared_slots=428 even for missing observations; malformed observed elements use repr; current field describes expected inventory, not actual successful comparisons. | Clarify metric as required slots and add observed/matched/invalid counts in future version; bound diagnostic representation. CODEC_REVIEWER. | Consumers must not interpret count as 428 comparisons completed or evidence of conformance. Documentation clarified; code unchanged. |

All six findings remain OPEN. No new architecture or dependency is accepted.

## Function-level inspection

| File / functions | Static result and boundary |
| --- | --- |
| runner/expected_bundle_emitter.py:canonical,digest | Sorted object keys, ASCII escapes, compact separators and allow_nan=False; deterministic for these inputs. Lists retain order, records explicitly sorted. No output bound. |
| same:unique_object,decode | Duplicate object keys reject. No nesting/size guard before JSON parse; malformed input raises, no result. Input admission must pin exact source bytes. |
| same:recipe | Versioned EMPTY@1/TYPED@1/MULTI@1; TYPED uses oracle plus explicit eight-field view; MULTI has two guard rows and one domain row. No observed input or SUT call. |
| same:streams | All 30 tables, scalar and row frames, 22 scoped/8 global tables, position aggregates, persisted/global/metadata/published/envelope. Row indices follow full framed-PK sorting. Dictionary assignment would overwrite repeated constructed IDs; exact pinned schema/fixture uniqueness is prerequisite. |
| same:generate_expected | Exact six byte-source keys; compares schema/oracle/vector digests to template; all five explicit rule IDs; checks 428 exact unique template IDs versus independently constructed keys. Returns EXPECTED_UNVERIFIED/review=null only. Does not verify template records' metadata/expected fields, trusted source signatures, source-to-module binding or interpretation document meaning. |
| runner/frozen_bundle_compare.py:sha,unique,record_check | Independent hashlib/JSON/re only; duplicate JSON keys reject. Exact record fields, lowercase hex, integer byte length, SHA and error=null; no expected fallback. A syntactically valid wrong binary frame is not detected by SHA. |
| same:validate_frozen | Whole bundle digest, external binding equality, mandatory verifier result, exact version/frozen state/source identities/rules/review/generation, 428 unique exact IDs before observer. It validates claims supplied by a trusted caller, not trust establishment, loaded code or path. Nonfrozen/partial/hash drift fails closed before observer under that boundary. |
| same:compare_frozen | Never imports emitter/SUT, rewrites expected raw bytes or promotes gates. Delayed observer follows validation. Reports duplicate/missing/extra/invalid records and all four field mismatches; duplicate payloads beyond first are classified, not fully field-compared. Unbounded diagnostic cost remains. |
| runner/test_expected_bundle_review.py:setUp,simulated_review,observe,reject | Generates expectations if run; fake approvals and mock observation only. It must not run during this review or in GENERATE_EXPECTED isolation. Observer-call count checks ordering of rejection, not authority authenticity. |
| same:test_inventory_and_all_slots | Verifies generated identity count and record self-consistency; not independent byte truth. |
| same:test_incomplete_duplicate_bytes_length_digest_and_identity | Written missing/duplicate/hex/length/digest/schema/oracle/rule/version mutations. Re-signs via test double to reach inner checks. NOT_RUN. |
| same:test_not_frozen_and_missing_approval,test_external_hashes_and_authentication | Written unfrozen/missing approval/binding drift/false callback controls. No signature cryptography or policy-revocation proof. |
| same:test_each_slot_comparison,test_divergences_not_short_circuited | Error-field mutation for every slot and several simultaneous divergences. No independent actual SUT data, no per-slot wrong-frame positive oracle. |
| same:test_emitter_cannot_read_observed | Checks emitter text and patches builtins.open after imports; rejects extra OBSERVED source key. Does not prove transitive import/OS isolation or block indirect/native IO. |
| same:test_scalar_controls | Manual bytea/time/nested JSON literals and distinction checks for scale/Unicode/NULL; timestamp negative types and wire endpoints. No PostgreSQL finite-range claim. |
| same:test_partition_metadata_envelope_and_pk_controls | P-A/P-B separation, four normal metadata streams, synthetic envelope and full PK a,b,aa order. Reuses oracle primitives; independent human review still required. |

Import graph inspected: emitter -> snapshot_oracle -> hashlib/struct/decimal; comparator ->
hashlib/json/re. No direct or transitive local import of snapshot_codec, snapshot_reference,
SUT tests or OBSERVED IO was found on this graph. Runtime stdlib/import-hook integrity is unproven.
Recipe values are shared specifications; semantic independence is not established by disjoint imports.

## Exact structural inventory

30 tables; 191 fields (text146, bigint26, boolean3, xid8 1, timestamptz10, numeric3,
integer1, jsonb1). No bytea column. Schema declares 22 position-scoped and 8 global tables.
Static reconstruction of expected ID names from schema and declared row/position counts matched
all 428 unique template IDs; no missing or extra ID. No binary streams were constructed.

| Fixture | Tables | Rows | Scalars | Partition tables | Global tables | Position aggregates | Other layers | Total |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EMPTY@1 | 30 | 0 | 0 | 0 | 8 | 0 | 5 | 43 |
| TYPED@1 | 30 | 30 | 191 | 22 | 8 | 1 | 5 | 287 |
| MULTI@1 | 30 | 3 | 6 | 44 | 8 | 2 | 5 | 98 |

Other layers are persisted/global/metadata/published/envelope. IDs encode fixture/layer/table/
position/row/column; schema order and full framed PK define the indices. All 428 trace rows persist.
Defined=428; generated=0; value-reviewed=0; frozen=0; observed=0; missing definitions=0;
missing expected results=428. Static inspection does not count as human value review.

## Required future controls (prepared cases, not implemented or run)

| Case | Independent input/oracle | Required result |
| --- | --- | --- |
| AUTH-SIGNATURE / AUTH-POLICY | Authentic authority fixture plus altered signature, wrong role/key, expired/revoked/out-of-scope approval; trusted offline policy snapshot | External verifier rejects before any SUT callback |
| LOAD-PATH / LOAD-MODULE | Approved nominal path replaced through alias/reparse/hardlink; unchanged source claim with different loaded module/stdlib/comparator | External measured loader refuses; callback count zero |
| FREEZE-MUTATION | Alter one bundle byte or record order after hash/signature freeze without reapproval | Whole-file hash/signature rejection; original artifact preserved |
| CANONICAL-ORDER | Reordered records or noncanonical JSON with internally consistent newly bound bytes | Future canonical admission rejects; current validator alone does not implement this |
| SLOT-SEMANTIC | Valid length/SHA but wrong tag/field order/partition prefix per independent manual frame tree | Semantic review/control rejects; current integrity check alone is insufficient |
| EXPECTED-IMMUTABILITY | Keep original frozen bytes/file identity, observer attempts replacement; remeasure after comparison | Reject mutation; preserve original expected and separate observed output |
| LIMITS | Over-limit input/depth/Decimal/observed output and timeout/memory pressure | External monitor safely terminates and preserves failure evidence; no partial conformance |

Actual signature policy, host/adapter implementation, limits and reviewer identities remain
UNRESOLVED. Candidate corrections are specified, not silently implemented under this review order.
Next human gate: review findings, decide SNAP-P01..05, choose independent freeze authority and
finite offline environment. Generation and comparison require separate subsequent authorizations.
EXEC-G1/PERS-G1 OPEN; PUB-T13B/SNAP-P01..05 PENDING_HUMAN_APPROVAL; A0/refusal retained.
