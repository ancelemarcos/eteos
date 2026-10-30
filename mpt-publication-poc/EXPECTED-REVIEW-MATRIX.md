# Expected oracle and test review matrix - candidate 0.15

## Order v1.8 / candidate 0.20 — current review

REQUIRES_HARDENING / NOT_RUN. This section supersedes prior counter-proposal status.
No executable source changed. COUNTER-MIGRATION.patch is proposed only, BLOCKED_ON_API_APPROVAL.
EXPECTED-COUNTER-PROPOSAL.md defines seven metrics and the explicit record-level validity
boundary; it does not claim full observed-wire validation.

| Finding | Correction/proposal | Written test | Required evidence | Blocker | Owner (identity unresolved) |
| --- | --- | --- | --- | --- | --- |
| Six metrics omit completed valid comparisons | Unapplied report@3 patch, preserve extra metric | Proposed test_proposed_report3_counter_matrix | Approved predicate, actual seven values and independent review | BLOCKED_ON_API_APPROVAL | API_CONTRACT_REVIEWER |
| Unknown public consumers/report compatibility | Reject missing/unknown/@2 marker in future @3 reader; no guessed conversion | Existing test_legacy_keyword_and_generation_defaults_rejected; reader test NOT_WRITTEN (reader absent) | Consumer inventory and reader rejection traces | API migration + missing reader | API_CONTRACT_REVIEWER |
| Abort must not publish report | Preserve return after recheck; prohibit host partial reports | Proposed timeout/interruption test; existing test_abort_paths_never_publish_report | Actual admission/observer/budget/recheck/OS-abort traces | No execution or real host | RUNTIME_SECURITY_REVIEWER |
| Five wire choices remain unapproved | Five updated SNAP pages, manual examples and component impact | Existing typed/partition/order/manual-wire controls named on pages | Independent byte review plus decision IDs/hashes | PENDING_HUMAN_APPROVAL | DOMAIN_CONTRACT_REVIEWER / INDEPENDENT_CODEC_REVIEWER |
| Claims are not authentic authority | Default-deny interface retained | Existing simulated admission rejection tests | Real signed policy/identity/expiry/revocation rejection evidence | No OAA/signature backend | SECURITY_AUTHORITY_OWNER |
| Path/hash not proof of loaded bytes | Stable protected handles and measured loader proposal | Existing simulation tests only, real integration test NOT_WRITTEN | TOCTOU, handle substitution and loaded-module identity proof | Loader/immutable handle absent | RUNTIME_SECURITY_REVIEWER |
| In-process budgets not finite OS enforcement | External owned scope and monitor proposal | Existing limits_abort_without_result; real monitor tests NOT_WRITTEN | Memory/CPU/wall/output/cleanup enforcement and process identity | Monitor/isolation absent | OFFLINE_EXECUTION_OWNER |

428 defined (EMPTY43/TYPED287/MULTI98); generated0, value-reviewed0, frozen0, observed0.
These zeros count absent artifacts, not measured test outcomes. All 428 values remain UNRESOLVED.
EXEC-G1/PERS-G1 OPEN; PUB-T13B/SNAP-P01..05 pending; A0 active.


## Order v1.7 / candidate 0.19

EXPECTED-STATIC-REVIEW.md now gives the current six-row SR15 function/protection/test/dependency
matrix. EXPECTED-API-MIGRATION.md covers actual callers, rejected legacy usage and report consumers.
Two additional candidate tests are written only: test_legacy_keyword_and_generation_defaults_rejected
and test_abort_paths_never_publish_report. No method added to the eight-method core.
SNAP-P01-DECISION.md through SNAP-P05-DECISION.md are independent human decision forms, not
new expected results or approvals. Actual compared-valid count is absent from report@2;
mixed-unit counters must not be summed or reinterpreted. Overall REQUIRES_HARDENING / NOT_RUN.

## Order v1.6 / candidate 0.18

REQUIRES_HARDENING / NOT_RUN. Current SR15 implementation/test/evidence/dependency/verdict
matrix is EXPECTED-STATIC-REVIEW.md, order v1.6 section. All named tests are authored only.
Independent structural admission is runner/expected_wire_review.py, with no emitter/oracle/SUT
import. Test-only SimulationAdmission does not verify signatures or filesystem/runtime identity.
External substitution tests use labeled simulated rejection; real-backend proofs remain BLOCKED.
Manual negative wire literals and prior SQL NULL/JSON null, bytea, Decimal, Unicode, micros and
framed-key controls remain supplemental to 428 slots. They are not replaced by generated truth.
Original eight CodecConformance methods and their exact capsule scope are unchanged.

## Order v1.5 / candidate 0.17 review correction

REVIEW_ONLY / REQUIRES_HARDENING / NOT_RUN. Earlier test mappings describe written intentions.
test_each_slot_comparison changes error only; it does not provide independent byte truth for
428 slots. The emitter-fed fixtures and oracle reuse are plumbing/relationship controls.
EXPECTED-STATIC-REVIEW.md enumerates absent signature-policy/path/module/order/post-freeze
mutation/expected-immutability controls and candidate corrections; none have been run.
EXPECTED-EXTERNAL-FREEZE-CONTRACT.md reconciles the same eight CodecConformance tests with the
unimplemented external adapter and separates integrity, typed/layer, time, rejection and
immutability oracles. All six static findings remain OPEN; generation is not authorized.

## Current order v1.4 / candidate 0.16

This section supersedes earlier missing-emitter/comparator implementation statements.
READY_FOR_REVIEW / NOT_RUN for authored tooling; actual frozen evidence remains unavailable.
428 exact per-slot rows are in EXPECTED-SLOT-TRACEABILITY.md, linked to unchanged template IDs.
Defined slots 428; computed/filled slots 0; UNRESOLVED slots 428; reviewed/frozen slots 0.
All tests below are only source code in runner/test_expected_bundle_review.py.

| Requirement | Implementation | Written test (ExpectedBundleReview) | Independent oracle | Dependency | Future evidence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| Full independent generation/serialization | expected_bundle_emitter.generate_expected/streams/recipe | test_inventory_and_all_slots | snapshot_oracle scalar_fixture/part/fixture_snapshot; template inventory | explicit five candidate rules, exact sources | immutable generated bytes | READY_FOR_REVIEW / NOT_RUN |
| Per-slot comparison | frozen_bundle_compare.compare_frozen | test_each_slot_comparison | externally reviewed expected bundle; simulated observer only in source tests | authenticated human freeze | 428 actual SUT comparisons | NOT_RUN |
| Incomplete/duplicate/byte/length/hash/schema/recipe/interpretation/version rejection | validate_frozen | test_incomplete_duplicate_bytes_length_digest_and_identity | independent inventory + SHA recomputation | trusted bound template | pre-observer rejection evidence | NOT_RUN |
| Missing review/unfrozen/external drift/authentication | validate_frozen | test_not_frozen_and_missing_approval; test_external_hashes_and_authentication | external signed human decision, not a generator claim | trusted authenticator pending | rejection with observer-call count zero | NOT_RUN |
| All divergences, including errors | compare_frozen | test_divergences_not_short_circuited | deliberately changed simulated observed fields | approved adapter pending | full immutable divergence list | NOT_RUN |
| No observed/SUT reading by emitter | strict sources keys; no IO/import edge | test_emitter_cannot_read_observed | source inspection and denied open during generation | external source isolation | import/IO audit; semantic reviewer | NOT_RUN |
| SQL NULL/JSON null, numeric scale, UTF8, bytea, JSON nesting, exact micros/rejections | existing oracle, no SUT dependency | test_scalar_controls | hand-derived frames and typed distinction controls | SNAP-P05; DB limits unresolved | independent controls and actual comparison | NOT_RUN |
| Multiple partitions, metadata, envelope and PK ordering | recipe/streams plus existing oracle | test_partition_metadata_envelope_and_pk_controls | declarative layer relationships and manual key-order example | SNAP-P01..05 | bytes/digests compared after review | NOT_RUN |

Mock approval acceptance is explicitly unit-test simulation, never approval or independence proof.
No missing/invalid snapshot slot can be excused as an expected error. Error controls expect
ValueError for declared invalid timestamps; successful output is forbidden. No DB-range inference.

DOCUMENTED / NOT_RUN. All expected records are EXPECTED_UNVERIFIED.
Reviewer role for every row: INDEPENDENT_CODEC_REVIEWER; person and approval UNRESOLVED.
Full slot inventory is runner/expected-bundle.template.json; no slot is implicitly frozen.

| Requirement | Fixture | Layer | Expectation | Comparison method | Reviewer | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 30 tables / 191 fields and ordered PK | EMPTY@1, TYPED@1, MULTI@1 | schema/table | Exact bound metadata and set; template copies all ordered fields | Exact inventory then per-field equality, not count only | Independent codec reviewer | EXPECTED_UNVERIFIED; output UNRESOLVED |
| Empty table inclusion | EMPTY@1 | table/global/persisted | All 30 descriptors and empty rows included, no positions | Full bytes/length/SHA per slot | Same, unassigned | EXPECTED_UNVERIFIED; UNRESOLVED |
| Populated scalar/row coverage | TYPED@1 | scalar/row/table | 191 typed field slots, one row per table | Independent emitter needed, compare bytes and digest | Same | EXPECTED_UNVERIFIED; emitter UNRESOLVED |
| Empty and multiple partitions | MULTI@1 | partition-table/position/global | P-A/P-B and every scoped table including empty; globals separate | Exact position/scoped sets then bytes/SHA | Same | EXPECTED_UNVERIFIED; UNRESOLVED |
| Metadata / view / envelope | all three | metadata/published/envelope | SNAP-P02/P03 and full hash hierarchy | Independent records and raw digest framing | Same | EXPECTED_UNVERIFIED; UNRESOLVED |
| SQL NULL vs JSON null | SQL-NULL@1 / JSON-NULL@1 | scalar | Manual hex 9 vs 18 bytes; distinct tags | Literal comparison; SHA not calculated | Same | EXPECTED_UNVERIFIED; digest UNRESOLVED |
| Decimal/JSONB/bytea/UTF-8 | existing scalar/compound fixtures | scalar/row | Scale and Unicode distinctions; exact nested structure | Manual literals plus independent typed oracle | Same | EXPECTED_UNVERIFIED |
| Wire/Python/DB time separation | existing timestamp fixtures | scalar | UTC epoch, microseconds, rejection boundaries; no DB-range inference | Independent micros and declared errors | Same plus DB specialist for later DB scope | EXPECTED_UNVERIFIED; DB extremes UNRESOLVED |
| Malformed/unknown/duplicate inputs | existing negative fixtures | input/parser boundary | Reject rather than coerce or return partial success | Exact input/category with recorded actual error later | Same | EXPECTED_UNVERIFIED |

## Exact proposed offline test set

All names are methods of CodecConformance in test_snapshot_conformance.py. No discovery,
collector, driver, database or harness test belongs to this offline set.

| Method | Inputs / independent expectation | Required outcome / failure |
| --- | --- | --- |
| test_scalar_bytes_and_decoding | Manual scalar hex; text/Unicode/NULL/bool/Decimal/bytea/-1 microsecond | Byte equality and typed decode; mismatch retained |
| test_nested_json_independent_bytes | Nested a:[null,false], independent frame tree | 56 bytes and exact decoded structure |
| test_empty_multirow_order_and_corruption | Empty and aa,b,a rows; independent relation; truncated/unknown frames | 200/288 bytes; canonical a,b,aa; malformed rejects |
| test_complete_empty_and_multiple_partitions | EMPTY@1 and MULTI@1 | Every upper hash equals independent derivation; missing aggregate/metadata rejects |
| test_rejections | Unknown schema/types/version, NULL/missing/extra/duplicate PK, float/nonfinite, malformed frame/JSON | Declared ValueError/UnicodeError; no coerced valid output |
| test_fully_populated_typed_snapshot | TYPED@1 plus typed eight-field view | All table bytes and upper hashes equal independently built records |
| test_oracle_negative_typed_values | Oracle invalid types/nonfinite/wire endpoint/lone surrogate and numeric scales | Oracle rejects independently; 1.0 and 1.00 distinct |
| test_python_time_domain_without_postgresql_claim | Offset epoch, naive input, year-1 UTC overflow, broad wire year-10000 value | Literal epoch equality; ValueError/OverflowError; no PostgreSQL validity claim |

Admission conditions: exact eight-file capsule and external provenance hash closure; reviewed
import graph; pinned CPython/stdlib/OS; no network/privileges; enforced finite resource envelope;
approved interpretation scope and specific execution authority. All remain pending.
Current tests use dynamic independent expectations, not a frozen-bundle consumer. Until that
gap is resolved they cannot prove reviewed-frozen conformance. Provisional execution would need
explicitly limited authorization and could not promote EXPECTED_UNVERIFIED automatically.
