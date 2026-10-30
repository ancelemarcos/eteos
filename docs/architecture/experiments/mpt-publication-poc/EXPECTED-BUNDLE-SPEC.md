# Independent expected bundle specification - candidate 0.16

## Order v1.8 / candidate 0.20

Current comparator remains report@2. The seventh compared_valid_slots is only proposed in
COUNTER-MIGRATION.patch, with exact semantics in EXPECTED-COUNTER-PROPOSAL.md.
BLOCKED_ON_API_APPROVAL / NOT_RUN. Record-level validity is not observed-wire conformance.
No sources, bundle identity, rule IDs, recipe, template or 428 expected values were modified.


## Order v1.7 / candidate 0.19 decision boundary

Current API/implementation unchanged. EXPECTED-API-MIGRATION.md inventories consumers and proposes
a strict breaking migration; no legacy callback adapter. New written tests exercise unexpected
authenticate keyword, omitted generation admission and abort non-publication.
report@2 does NOT separately measure valid comparisons: its six metrics include extra_slots.
Do not derive compared count from observed/matched or sum overlapping counters. A seventh
compared_valid_slots metric in a future version is recommended for human review only; no @3
format is implemented or accepted. This unresolved requirement keeps REQUIRES_HARDENING / NOT_RUN.
See EXPECTED-DECISION-PACKAGE.md for separate human decisions and technical gaps.

## Order v1.6 / candidate 0.18 (supersedes API/metric descriptions below)

REQUIRES_HARDENING / NOT_RUN. Current source implements local FIX_CANDIDATE controls;
actual authority and runtime enforcement remain BLOCKED / PENDING_HUMAN_APPROVAL.

### Disabled admission contract

Public generate_expected now requires explicit budgets and an AdmissionAdapter; default None
rejects. compare_frozen/validate_frozen require the same plus exact schema_bytes/template_bytes.
The previous authenticate=True callback interface is removed. AdmissionAdapter.authorize and
recheck always raise unless a separately approved external implementation is supplied.
No enabling switch, trust store, signing algorithm, real authority or OS loader is selected.
AdmissionReceipt is immutable phase/binding/raw digest/evidence reference; structural receipt
equality is not authentication. The external adapter must verify signed scope, identities,
reviewer separation, validity/revocation, approved budgets, actual protected path/file handle and
actual loaded code/runtime before returning it. It must recheck immutability after observation.
Tests alone contain SimulationAdmission; it is deliberately NOT proof of any external property.
A malicious in-process adapter cannot be made trustworthy by these Python types; external host
is the trust root and its absence is a blocker. No public observer API bypasses required admission.

### Local resource checks (all limits proposed, not approved configuration)

Budgets ceilings: input8MiB/source1MiB/output8MiB/wire1MiB/scalar4096B; JSON document depth32,
nodes100000, string2097152 chars; observed records856, diagnostics4096; Decimaldigits128/
absolute exponent128. Wire JSON further caps depth16/nodes1024. Schema fixed30 tables/191
fields, names128/type32 chars, columns/table32; fixture rows remain fixed and view count0/1.
Document depth is distinct from wire-JSON depth. Conservative 4-byte text accounting and
ASCII/Unicode escaping preflight (up to 12 bytes per character) may reject an otherwise
byte-small object; do not silently raise limits.
Any new ceiling needs human review; supplying Budgets does not activate authorization.
JSON scanning occurs before json.loads; output preflight before encoder allocation; wire length
before slicing/hex decode; Decimal checks before formatting; source/fixture dimensions before
oracle generation; observed collection/diagnostic/output bounds before controlled copying.
No repr of untrusted observations. Overflow aborts without a comparison result; no truncation.
Caller has already allocated raw input/Decimal/observed objects; callback/native/process memory
and deadlines cannot be contained by these guards. External finite monitor remains mandatory.

### Structural semantics and canonical data

Expected format MPT-FROZEN-COMPARE@1 and recipe identity CANDIDATE-0.16-EXPECTED@1 are retained:
no fixture or wire version change, no regeneration. Source identities will differ after edits.
Canonical ASCII sorted-key compact JSON must match exact input bytes; record order must be
sorted exact 428 unique IDs. Schema/template bytes must match signed source identities.
expected_wire_review parses frames independently: lengths/tags, SQL types, nullability, numeric
scale syntax, UTF8, wire timestamp range, nested JSON/key order, exact column/PK descriptors,
canonical PK row order, per-slot row/scalar links, partition prefix/membership, normal/global
rows, aggregate children/digests, full metadata streams, eight-field view and synthetic envelope.
This checks structure and consistency, not independent truth of arbitrary fixture values.
It reuses candidate SNAP rules without approving them. PostgreSQL finite dates remain unresolved.
Hash-valid but structurally wrong frames reject before observer; no regeneration/fallback.

### Comparison report proposal and invariants

New report_spec=MPT-FROZEN-COMPARISON-REPORT@2 is a PROPOSED incompatible report change:
- required_slots: exact expected inventory size (428 after validation).
- observed_slots: number of list entries returned by observer, including invalid/duplicate ones.
- matched_slots: unique required IDs present exactly once with a valid record equal in all fields.
- missing_slots: required IDs absent from all keyed observed entries.
- extra_slots: count of distinct keyed observed IDs outside required inventory.
- invalid_slots: number of observed entries malformed, invalid by record checks, or belonging to
  a duplicated ID (all occurrences of duplicate IDs count invalid).

0 <= matched_slots <= required_slots - missing_slots <= required_slots;
0 <= invalid_slots <= observed_slots. Counters are not a partition: a valid extra entry is extra
but not necessarily invalid; a present malformed required entry is not missing. They must never
be summed as if mutually exclusive. An aborted attempt returns no comparison report.
Every duplicate/missing/extra/invalid entry or differing hex/length/digest/error field is identified
without embedding payload copies. Preserve bounded original observation separately via external
host. Expected raw bytes are immutable; external recheck runs even if observation fails.

Human decision requested: accept candidate admission API replacement, tightened acceptance/budget
profile and report@2 migration before any use. No implicit compatibility or execution approval.
All callers using authenticate/compared_slots must be updated under that decision. Current tests
use explicit simulation to exercise the proposed interface; original capsule tests are unchanged.
New support module hashes must be pinned in external loaded-code inventory via final manifest;
the six generator source fields alone do not attest the complete import closure.

## Order v1.5 / candidate 0.17 static-review disposition

REQUIRES_HARDENING / NOT_RUN supersedes earlier interface readiness claims.
EXPECTED-STATIC-REVIEW.md records six OPEN findings; no Python source changed.
EXPECTED-EXTERNAL-FREEZE-CONTRACT.md defines proposed OAA authentication, signed hash closure,
actual handle/loaded-byte admission, separate generation/freeze/comparison and finite environment.
Current validator rejects internally inconsistent or hash-drifted bundles, but cannot establish
authority, actual paths/loaded-code identity, canonical record order or binary semantic validity.
The phrase "no approval survives any bound identity drift" applies only to checked supplied claims;
actual runtime/path/identity drift must be rejected by the unimplemented external host.
compared_slots=428 is required inventory size, not a count of observed successful comparisons.
All runtime and human approvals remain absent. No READY_FOR_EXECUTION or codec conformity.

READY_FOR_REVIEW / NOT_RUN applies only to authored interfaces. No expected output generated.
The 0.15 template remains immutable input (MPT-EXPECTED-REVIEW@1); emitted format is separately
versioned MPT-FROZEN-COMPARE@1. No silent replacement of the template format.

## GENERATE_EXPECTED

runner/expected_bundle_emitter.py:generate_expected receives keyword-only sources (six exact
byte inputs: schema, template, oracle, emitter, interpretations, vectors), interpretations and
generation environment/run_id. It has no file access, CLI, encoder/parser/test dependency,
observed input or automatic execution. Extra source keys, including OBSERVED, reject.
Dependencies: stdlib hashlib/json/decimal and existing snapshot_oracle only. No oracle edits.
Source bytes must match the actual loaded emitter/oracle, as proven by externally approved
pre-import admission; merely supplying claimed bytes cannot prove loaded-code identity.

Caller must explicitly select all five candidate-0.15/P01..P05 rule IDs; no default selection.
This means generation intent, NOT semantic approval. The exact review document bytes are bound.
recipe() defines EMPTY@1 empty all tables; TYPED@1 populated_fixture plus the eight-field typed
view; MULTI@1 two position_guard rows P-B/null, P-A/C-1 and publication_domain D/1.
Rows index canonical framed-PK order, not insertion order. streams() independently builds
scalar/row frames and reuses fixture_snapshot for all other layers. It checks exact equality
with all 428 template IDs. No parsing of SUT output. Synthetic envelope manifest zero bytes,
config 11 repeated and VECTOR-ONLY are explicit recipe constants, never real provenance hashes.

Serialization is ASCII JSON, sorted object keys, compact separators, no NaN, records sorted by ID.
For identical inputs/provenance, byte output is deterministic. Every record has id, lowercase hex,
integer length, sha256 and error=null. Scalar/row digests are review-local, no wire change.
Root binds contract, version, bundle ID, six source hashes, generation and interpretations.
State is ALWAYS EXPECTED_UNVERIFIED and review=null. No source hash is an approval.
The emitter output has no own hash field and no real manifest/capsule digest, avoiding cycles.
Actual output and all 428 expected bytes/lengths/digests remain UNRESOLVED in this checkout.

## REVIEW_AND_FREEZE (human process, no implementation that autoapproves)

Independent named reviewer must examine all recipe/slot derivations, semantic independence,
SNAP-P01..05 alternatives, source/load identity and environment/resource constraints.
Only after a real decision may a separately edited copy carry REVIEWED_FROZEN and review
{reviewer,decision_id,timestamp}. Record original generated hash and reviewed-copy hash in the
external human decision history; retain both copies. No such copies or approvals exist now.
The external signed approval has reviewer, decision_id, timestamp, state=APPROVED, binding,
signature. Binding pins bundle_sha256, manifest_sha256, capsule_sha256 (descriptor-file hash),
all six sources, exact required_slot_ids, selected interpretations and explicit bundle_path.
These final hashes live OUTSIDE all manifest-bound files. Signature verification/trust store
integration is PENDING_HUMAN_APPROVAL; no permissive default verifier is supplied.
Tests use visibly simulated in-memory records solely for admission plumbing, not review evidence.

## COMPARE_FROZEN

runner/frozen_bundle_compare.py accepts immutable raw bytes, a separately trusted binding,
external approval, mandatory authenticate callback, and delayed observe callback.
validate_frozen checks file bound, hash syntax, whole-file digest, approval identity/authentication,
exact version/state, source and interpretation identities, 428 unique exact IDs and per-record
hex/length/digest before observe is invoked. No emitter import or dynamic expectation fallback.
Trusted slot set/sources must come from independently approved original template/source inventory,
NEVER be reconstructed from untrusted bundle claims. The caller must verify actual manifest,
descriptor and source bytes against the signed binding and prove the read-only path/loaded code.
The comparator checks binding consistency; it does not itself open files or authenticate people.
The verifier must authenticate the entire immutable approval, not merely return a user-supplied flag.

observe returns a list of records with id,hex,length,sha256,error. All 428 expected slots are
successful snapshot bytes; error expectations belong to negative source controls, not replacement
snapshot slots. Any observed error is reported as invalid-observed and an error-field divergence.
Missing/extra/duplicate/malformed observations and every differing byte/length/digest/error field
are retained. Result COMPARISON_ONLY never certifies the codec or promotes gates.
Malformed expected data rejects before SUT access. No approval survives any bound identity drift.

## Capsule and limits

The eight-entry core is preserved. Seven source payloads remain byte-identical; MANIFEST is the
normal refreshed provenance artifact with external binding. New tools are external review tooling,
not a ninth capsule member. Proposed absolute read-only path:
C:/mpt-offline-review/expected/reviewed-frozen.json (proposal only; nothing created there).
Descriptor records this interface; path/hash/authenticator/observer adapter and hosting approval
remain pending. Existing eight tests do not consume this interface and remain provisional.
No capsule is assembled, no SUT adapter activated. Separate authorization is required.

8 MiB raw comparator bound is a candidate local guard, NOT memory/time containment.
External file/source/JSON/Decimal limits, total memory, deadline, no-network, unprivileged identity,
read-only inputs and separate bounded output require actual enforcement before any import.
All limits, runtime identities and isolation evidence remain pending; post-allocation checks
cannot supply those guarantees. PostgreSQL finite timestamp extrema remain unresolved.

EXEC-G1/PERS-G1 OPEN; PUB-T13B and SNAP-P01..05 PENDING_HUMAN_APPROVAL.
