# Counter proposal — candidate 0.20 / order v1.8

PROPOSED / BLOCKED_ON_API_APPROVAL / NOT_RUN.
COUNTER-MIGRATION.patch is unapplied text. No Python or test source changed.
Decision owner: API_CONTRACT_REVIEWER; identity, decision, date and signature UNRESOLVED.

## Exact proposed meaning

For this proposal, "structurally valid observation" means an observation record passing
frozen_bundle_compare.record_check and occurring exactly once under a required ID.
That predicate checks exact fields, ID type, canonical hex, bounded bytes, exact length,
SHA-256 and null error. It does NOT certify the observed snapshot's wire semantics.
Expected bytes separately pass expected_wire_review.validate_slots before observation.
A record with self-consistent malformed wire bytes is a valid record-level comparison
and a content mismatch, not evidence of wire conformance. This distinction is an explicit
API decision required before applying the patch. If full observed-wire validity is required,
reject this minimal patch and design a separately reviewed per-slot structural validator;
validate_slots is currently a whole expected-bundle validator, not such an observed API.

Let R be required IDs, O the observation list, I the invalid entry indices, and U the IDs
occurring exactly once with a valid record. Let C be IDs in R intersect U for which all
four content fields (hex, length, sha256, error) have finished comparison.
- required_slots = size R.
- observed_slots = length O, including every extra, duplicate and malformed entry.
- compared_valid_slots = size C, independent of equality.
- matched_slots = IDs in C whose four compared fields all match.
- missing_slots = required IDs absent from the index of string IDs (invalid presence is not absence).
- extra_slots = distinct string IDs outside R, including invalid or duplicated extra IDs.
- invalid_slots = distinct entry indices malformed, record-invalid, or belonging to a duplicated ID.
All occurrences of a duplicated ID are invalid, including the first occurrence.

0 <= matched <= compared_valid <= required - missing <= required.
compared_valid <= observed - invalid. Invalid and extra may overlap; units are different.
No sum of these seven metrics partitions observations. No legacy metric reconstructs C.
Zero observations gives (required=428, observed=0, matched=0, missing=428, extra=0,
invalid=0, compared_valid=0), only if admission, diagnostics and recheck complete.
These numbers are declarative test expectations, not experimental results.

## Version and compatibility decision

Current public output is report@2 with six counters. Adding the seventh with these semantics
requires report@3. Repository callers are only ExpectedBundleReview helpers/direct negative
tests; no operational reader exists. External consumers remain unknown, not presumed absent.
No adapter, observer signature, source binding, budget or snapshot wire changes are proposed.
@2 readers must reject @3 until explicitly migrated; @3 readers must reject @2/missing/unknown
markers rather than infer zero or map observed/matched to compared. Reader implementation
and its acceptance test remain absent. No compatibility shim is proposed.

The patch increments only after the complete field loop and only for unique valid required
records. Diagnostics may still describe invalid records, but those never increment C.
Any admission failure, observer error, diagnostic/output limit, timeout, interruption or
recheck failure yields no returned report or counters. COMPARISON_ONLY is not a success verdict.
The patch preserves the existing finally/recheck and return placement. External forced
termination/report publication safety still requires a real monitored host.

## Written tests and evidence limits

The unapplied patch contains test_proposed_report3_counter_matrix: empty/all, record-valid
mismatch, invalid/error, missing, duplicate, extra, invalid extra, malformed, and mixed cases.
Its b00 mismatch deliberately exercises record validity without claiming wire validity.
test_proposed_report3_timeout_interrupt_no_return covers raised timeout and interruption.
Existing legacy keyword/default rejection and abort/recheck sentinel tests remain unchanged
and NOT_RUN. Proposed tests are not discovered or imported, and no new core method is added.
Real consumer rejection of unsupported reports and OS-enforced termination remain BLOCKED.

Required decision: approve report@3 and the exact record-level predicate, enumerate/migrate
consumers, or request a wider observed-wire validation design. Then separately authorize
patch application and controlled validation. This order authorizes neither execution nor
public migration. SNAP-P01..05/PUB-T13B remain pending; EXEC-G1/PERS-G1 OPEN; A0 active.
