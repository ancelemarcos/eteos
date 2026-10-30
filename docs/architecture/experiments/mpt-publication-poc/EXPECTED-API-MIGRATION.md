# API/report migration decision - candidate 0.19 / order v1.7

## Order v2.0 / candidate 0.22 — proposed formal disposition

Recommendation APPROVE report@3 record-level semantics for API_CONTRACT_REVIEWER decision;
actual decision/identity/date/signature UNRESOLVED. BLOCKED_ON_API_APPROVAL / NOT_RUN.
Patch unchanged and unapplied; executable comparator still emits report@2.

Static proof: invalid is a set of observation indices, each within the list; every occurrence
of a duplicated ID is inserted (first and subsequent). Each compared-valid ID selects one
distinct index outside invalid, establishing compared_valid <= observed - invalid.
It must also be required and present, so compared_valid <= required - missing <= required.
Only equal completed comparisons increment matched: matched <= compared_valid.
No summation of overlapping populations is valid. Three copies invalidate three indices;
duplicate extras add one extra ID but all copies invalid and zero compared. Invalid present
required records are not missing. A malformed ID cannot be indexed and may leave a requirement
missing. Empty observations yield compared=matched=observed=invalid=extra=0, missing=required,
only if all checks/recheck complete. Existing mixed tuple in patch is declarative, not a result.

The proposed increment is after all hex/length/sha256/error comparisons, irrespective of equality.
record_check validity includes canonical record bytes/length/hash/error, not observed wire semantics.
Any admission, observer, limits or recheck failure prevents return; raised timeout/interruption
does not yield a report. Forced termination still requires external publication/custody proof.
Partial local counters are not outputs. A second-invariant assertion and triple/duplicate-extra
tests remain documentary follow-up; the preserved patch does not magically add them.

Text search again found ExpectedBundleReview.compare and its direct negative calls only;
test_honest_counters reads six counters, other tests inspect differences. validate_frozen is
internally consumed by compare_frozen. No production reader identified; external consumers UNKNOWN.
The v1.9 compatibility matrix remains current: @3-only readers must reject @2, @2-only readers
must reject @3, both reject missing/unknown versions. No zero-fill, inference, fallback or silent
conversion. Consumer version-rejection tests remain NOT_WRITTEN because no operational reader
exists. Patch tests and existing abort tests remain NOT_RUN.

Formal human choices: APPROVE exact report identity/predicate and separately authorize later
application; REVISE to require observed-wire validation or a different migration; REJECT report@3
and retain @2 without claiming the missing metric exists. Approval record must bind exact proposal,
patch/source hashes, affected caller inventory and external rollout constraints. No choice is made here.


## Order v1.9 / candidate 0.21 reconciled opinion

Technical recommendation: APPROVE the proposed report@3 record-level contract for human
consideration. This is NOT approval to apply COUNTER-MIGRATION.patch or execute anything.
Actual API_CONTRACT_REVIEWER identity/decision/date/signature: UNRESOLVED.
Implementation remains report@2; patch remains byte-identical, BLOCKED_ON_API_APPROVAL.

Source inspection confirms the patch increments after all four fields have been compared,
only for a required ID present exactly once and passing record_check. Matching is a subset.
The fields are hex, length, sha256 and error. Record validity is not observed-wire conformity.
A self-consistent b00 record can count as compared and differ from expected valid wire.
Expected-only validate_slots must not be advertised as validating observed wire.

For every returned report: matched <= compared_valid <= required - missing <= required;
compared_valid <= observed - invalid. These count different, overlapping populations.
A duplicate makes every occurrence invalid; even an equal first copy cannot count.
Missing means no indexed string ID; a present invalid required record is not missing.
Extras count distinct non-required IDs; invalid counts entry indices (overlap allowed).
No observation yields required=missing=428 and all other counters zero only on completed
admission/comparison/recheck. These are declarative expectations, not measured results.
Admission, observer, diagnostic/output limits, timeout, interruption or recheck exception
must prevent report return; the finally recheck remains before return. A host must not
publish an intermediate result or synthesize zero counters after error.

| Consumer/surface found by text search | report@2 -> report@3 | Negative coverage and required behavior | Risk / state |
| --- | --- | --- | --- |
| test_expected_bundle_review.ExpectedBundleReview.compare and direct comparator calls | Same arguments and callback; seventh counter + version marker | Proposed test_proposed_report3_counter_matrix in unapplied patch | NOT_RUN; test-only caller |
| test_honest_counters and tests reading differences | Existing six meanings preserved; new count cannot be inferred from them | Existing duplicate/missing test; proposed mixed/invalid-extra/empty cases | NOT_RUN; source unchanged |
| compare_frozen -> validate_frozen internal call | Unchanged source inputs/admission/budgets | Existing legacy-keyword/default-admission tests reject before observation | No trust compatibility shim |
| ExpectedBundleReview.generate -> emitter.generate_expected | Not a report consumer; unchanged | Existing missing-adapter/generation-default rejection | Generation permission separate |
| Future @2-only reader | Must reject @3 until explicitly migrated | Required acceptance case: @3 input -> unsupported version, no partial display | No operational reader found; test NOT_WRITTEN |
| Future @3-only reader | Reject @2, absent marker, unknown marker; no zero-fill/guessing | Required four version cases plus abort/no-report input | Reader absent; implementation evidence BLOCKED |
| External consumers | UNKNOWN, not assumed empty | Owner inventory and migration attestations required before external rollout | API_CONTRACT_REVIEWER unresolved |
| Host/report publisher | Never publish successful result after any abort/recheck failure | Existing abort sentinel + proposed timeout/interruption test; real OS negative absent | Real host/monitor proof BLOCKED |

Search covered repository text and Python callers, excluding attachments; no production caller
or report renderer was identified. This is not dynamic/import discovery or proof about external
systems. The candidate patch's existing assertions cover the first invariant; the second has
declarative coverage here but no dedicated assertion in the preserved patch. Require that
assertion plus duplicate-extra/triple-duplicate cases in a later authorized test revision.
No test is claimed executed. Reject any interpretation of compared_valid as wire-valid or PASS.


## Order v1.8 / candidate 0.20 disposition

BLOCKED_ON_API_APPROVAL / NOT_RUN. Current code still emits report@2; no source/test edit.
COUNTER-MIGRATION.patch and EXPECTED-COUNTER-PROPOSAL.md now provide the exact proposed
report@3 change, record-structural validity definition and written seven-counter cases.
This supersedes the earlier "future code/test changes" statement: patch text is now authored,
but unapplied. Arguments, callbacks and exception control flow are unchanged by that proposal.
The existing consumer inventory below remains current after text inspection.

| Surface | Current behavior | Proposed compatibility / error behavior |
| --- | --- | --- |
| Explicit raw/binding/approval/schema/template/budgets | Required validation; legacy authority keyword rejects | Unchanged; never silently supply approval/default policy |
| AdmissionAdapter / observer | Default-deny; observer after admission and expected validation | Unchanged; failures return no report |
| Report@2 six metrics | No compared-valid field | @3 seventh field; explicit incompatible consumer migration required |
| Record-valid mismatch | Diagnostics, not matched | Increment compared_valid only after full field loop |
| Duplicate/error/extra/absent | Existing diagnostic classification | Exclude from compared_valid; retain existing distinct-ID vs entry units |
| Observer/limits/recheck timeout/interruption | Exception, no returned report | Unchanged; external host must forbid partial/synthetic success |
| Unknown report consumer | Not implemented | Reject unknown/missing versions; test remains blocked pending reader |

No snapshot binary format changes. Human approval must explicitly accept record validity versus
full observed-wire validity; otherwise the minimal patch is insufficient and must be redesigned.


PROPOSED / NOT_RUN. Recommendation: explicit breaking migration, no legacy compatibility shim.
No accepted contract, real backend or report format is promoted here.

## Consumer inventory from checkout text inspection

Repository search excluded attachments, not candidate source; no runtime imports/discovery.
References below are relative to this candidate directory. External callers are UNRESOLVED;
absence from repository search is not evidence that none exist outside checkout.

| Target / call | Actual consumer | Role and migration action |
| --- | --- | --- |
| expected_bundle_emitter.generate_expected | runner/test_expected_bundle_review.py:ExpectedBundleReview.generate; setUp and test helpers call this wrapper | Test-only SimulationAdmission and explicit budgets; no operational caller |
| emitter canonical/decode/digest and RULES | same test module:setUp, simulated_review, mutation tests and SimulationAdmission.authorize | Test helpers, never a human freeze pipeline; preserve simulation label |
| frozen_bundle_compare.compare_frozen | same test module:compare wrapper and direct negative-admission test | Supply schema/template bytes, budgets, AdmissionAdapter; reject omitted/legacy authority |
| frozen_bundle_compare.validate_frozen | frozen_bundle_compare.compare_frozen only | Internal admission returns expected mapping and receipt; no independent SUT observer |
| comparator.record_check | same test module:test_inventory_and_all_slots; comparator internals | Pure record consistency helper; not authority or execution entrypoint |
| test_expected_bundle_review.py | No importing caller or registered runner discovered | Source-only external suite; never append to original eight CodecConformance methods |
| report@2 counters | test_honest_counters reads six counters; remaining tests read differences | No production/report renderer consumer found; unknown report versions must fail closed in any future reader |
| descriptor tooling paths | OFFLINE-CAPSULE-MANIFEST.json.external_expected_proposal; documentation references | Inventory only, not import/execution hooks |
| legacy authenticate/compared_slots | Historical prose and test asserting absence of compared_slots | Historical descriptions do not authorize accepting old calls |
| run.py / original test_snapshot_conformance.py | No target API call found | Preserve unchanged; dynamic core tests are not a frozen comparison adapter |

## Proposed migration

| Aspect | Legacy | Current candidate | Acceptance / written negative |
| --- | --- | --- | --- |
| Authority | authenticate callable returning True | AdmissionAdapter with authorize/recheck; default always denies | test_legacy_keyword_and_generation_defaults_rejected; test_wrong_admission_receipt_and_legacy_true_callback |
| Generation | sources/rules/generation could be supplied alone | Explicit budgets and external adapter/approval required | Reject before streams; no automatic budget/approval activation |
| Frozen inputs | Nominal binding and raw bytes | Exact schema_bytes/template_bytes plus raw and binding | source drift rejected; no reopen/fallback; actual loaded-byte proof remains external |
| Observation | callback after claim checks | callback only after adapter, canonical and semantic checks; external recheck before return | test_abort_paths_never_publish_report, existing rejection controls |
| Report | compared_slots ambiguously 428 | report_spec@2 + required/observed/matched/missing/extra/invalid | test_honest_counters; no reader maps old compared_slots to matches |
| Unsupported format | Potential inferred compatibility | Reject unknown version or missing marker; never auto-upgrade or zero-fill | Future consumer acceptance case MIG-REPORT-UNKNOWN; reader absent/BLOCKED |
| Core execution scope | Eight exact CodecConformance methods | Same eight; candidate review tests remain external | File-hash and descriptor inventory inspection only |

No new adapter is activated. An accepted migration needs exact caller inventory, signed source
closure, backend/monitor review and separate runtime authorization. Compatibility cannot be
implemented by wrapping lambda True into an AdmissionReceipt.

## Counter audit: a real unresolved mismatch

Order v1.6 requested required_slots, observed_slots, matched_slots, missing_slots, extra_slots,
invalid_slots. Source report@2 implements those six. Order v1.7 also asks to distinguish
actually compared from matching. There is NO separate valid-comparison counter in report@2.
matched_slots is not compared; observed_slots includes invalid/extra/duplicate entries.
The six values cannot reliably reconstruct compared-valid count; invalid extra entries and
duplicate required IDs mix entry and identity cardinalities. Do not guess a formula.

Current definitions: required/missing/matched count unique required IDs; observed/invalid count
entries; extra counts distinct non-required IDs. invalid uses a set of entry indices, so one
duplicate-and-invalid entry is counted once there. All occurrences of a duplicated ID are invalid.
matched excludes duplicate/invalid entries. These categories overlap by design; they are NOT
a disjoint partition and must not be summed into a total. Existing test_honest_counters covers
one duplicate + one missing case only. No executed evidence supports any numeric outcome.

Recommendation for HUMAN DECISION (not implemented): a versioned report@3 with seven explicit
metrics, preserving extra_slots and adding compared_valid_slots. Define compared_valid_slots as
the number of unique required IDs observed exactly once with a valid record for which all fields
were compared, regardless of equality. Then matched <= compared_valid <= required - missing.
Alternative: stay with report@2 and explicitly waive the separate compared metric. Replacing
extra_slots silently or resurrecting the old ambiguous compared_slots name is rejected as a
migration proposal. Human decision and future versioned code/test changes remain BLOCKED.
No @3 report, empirical count or wire change is created by this document.

## Abort inspection and acceptance cases

compare_frozen returns only after validate_frozen, observe, bounds/diagnostics/output checks and
the finally admission.recheck. Any raised admission, semantic, observer, budget or recheck error
prevents the return. A local result dictionary may be constructed before recheck, but is not
returned or written by this module. There is no file writer. External hosts must not synthesize
a success report from an exception or expose local intermediates.
test_abort_paths_never_publish_report uses a sentinel return holder and a test-only recheck
counter for observer failure, diagnostic overflow and immutable-input recheck failure.
Tests are written only; OS termination and backend rejection remain separately unproved.

| Planned future consumer case | Required oracle | State |
| --- | --- | --- |
| MIG-REPORT-UNKNOWN | Unsupported/missing report_spec rejects, no partial/default dashboard | BLOCKED: reader not implemented |
| MIG-REPORT-ABORT | Exception/timeout cannot publish a successful report/counters | Candidate Python test written; host test BLOCKED |
| MIG-REPORT-COUNT | Duplicate + invalid extra + valid mismatch + missing independently classified | Full consumer test pending chosen report version |
| MIG-AUTH-LEGACY | Old keyword/callable/omitted adapter cannot reach SUT or generation streams | Candidate tests written, NOT_RUN |

Decision owner: API_CONTRACT_REVIEWER, identity UNRESOLVED. Approve/reject/request changes:
UNRESOLVED; decision ID/date/signature UNRESOLVED. This unresolved counter choice keeps the
overall candidate REQUIRES_HARDENING / NOT_RUN; it does not prevent reviewing this package.
