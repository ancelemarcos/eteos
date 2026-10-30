# Codec isolated validation plan - candidate 0.14 / order v1.2

## Order v1.6 / candidate 0.18

Three candidate support modules and revised emitter/comparator/tests remain outside original core.
The exact eight CodecConformance methods and seven core payload hashes are unchanged.
Default-deny admission is materialized, not an actual trusted host. Scope-specific test simulations
must not be added to the core execution list or interpreted as OAA/OS enforcement evidence.
No setup or invocation performed. New local budgets and report@2/API compatibility are proposed
in EXPECTED-BUNDLE-SPEC.md; external finite environment and separate authorizations remain gates.

## Order v1.5 / candidate 0.17 mandatory review boundary

REQUIRES_HARDENING / NOT_RUN. EXPECTED-STATIC-REVIEW.md supersedes earlier readiness wording.
Use EXPECTED-EXTERNAL-FREEZE-CONTRACT.md for the exact eight-method reconciliation, separate
oracles, actual-path/loaded-byte admission, authority ownership and finite proposed limits.
The descriptor retains all eight entries; seven payload hashes remain unchanged. No external
bundle, signature, host, adapter or capsule has been assembled or activated.
The comparator's supplied hash/path claims cannot establish actual loaded identity or authority.
Independent OAA and finite monitor are designs with UNRESOLVED owners/implementations/evidence.
Generation authorization must follow human review of findings/SNAP/authority/environment;
comparison then requires a distinct authorization after real value review and freeze.

## Current order v1.4 / candidate 0.16

READY_FOR_REVIEW / NOT_RUN for external emitter/comparator source only. Supersedes the older
statement that these modules do not exist; does not close admission or execution gates.
The descriptor still has exactly eight core entries. Seven payload files are unchanged.
MANIFEST.md is refreshed provenance, externally hash-bound as before.
Proposed external read-only expected path is C:/mpt-offline-review/expected/reviewed-frozen.json.
No file/directory at that path was created. New tooling remains outside the capsule.
The external host must be separately approved: authenticate signed reviewer decisions, measure
source/manifest/descriptor bytes and loaded Python identities, bind exact slot set and path,
enforce resources/isolation before import, then invoke comparator with a delayed observer.
Actual SUT observer adapter and authentication backend are UNRESOLVED/PENDING_HUMAN_APPROVAL;
existing eight tests are unchanged and cannot be claimed to consume frozen expected bundles.
No ninth file, Python invocation, capsule assembly, runtime pin, process or enforcement occurred.
See EXPECTED-BUNDLE-SPEC.md for exact supplied-data/trusted-caller boundary and non-circular freeze.

## Order v1.3 - review descriptor and incomplete frozen interface

OFFLINE-CAPSULE-MANIFEST.json enumerates exactly the same eight files and seven measured
source hashes. The final MANIFEST.md hash must be bound from this delivery's external digest by
an independent approval record. Embedding it inside a descriptor hashed by that manifest would
be circular. UNRESOLVED is an intentional fail-closed placeholder, never permission to skip it.
No capsule directory has been assembled or files copied.

The descriptor records exact CPython/build/stdlib identities as UNRESOLVED, all proposed bounds
as PENDING_HUMAN_APPROVAL, and import graph and OS enforcement obligations. An independent
reviewer must confirm transitive imports against the exact stdlib. No network denial, read-only
mount/ACL, unprivileged identity or memory/deadline limiter has actually been installed.
File/fixture admission belongs to a pre-import reviewer/validator; native memory and blocked-call
bounds need an approved external isolation/deadline mechanism as compared in the containment
decision. If that mechanism cannot prove the chosen metric/limits, refuse future execution.
The future command template above remains unexecuted; no broad discovery or added runner.

EXPECTED-BUNDLE-SPEC.md and EXPECTED-REVIEW-MATRIX.md specify interfaces and exact test names.
The expected template remains outside the capsule and EXPECTED_UNVERIFIED. A reviewed frozen
consumer would require explicit interface/capsule revision, since current tests regenerate
expectations dynamically. Preserve the exact eight-file constraint until that decision; do not
silently mount extra expected files. No REVIEWED_FROZEN or OBSERVED evidence exists.

PROPOSED / DOCUMENTED / NOT_RUN. Preparation only; no authorization to run these commands.
Objective: bounded offline evidence about MPT-SNAPSHOT@1 candidate bytes, not PostgreSQL,
transport, publication semantics, MIR temporal admissibility or production readiness.

## Four independent scopes

| Scope | Minimal artifacts | Exit evidence | Separate human gate |
| --- | --- | --- | --- |
| OFFLINE-CODEC | codec/reference/oracle, schema and vectors, conformance test only | Independent frozen expectations, observed comparisons and bounded environment record | Explicit offline-only execution authorization and interpretation-review scope |
| ISOLATED-TRANSPORT | Approved transport implementation and containment fixture | Native allocations, blocked-call, cancellation and owned-child cleanup evidence | Containment decision and specific experiment approval |
| CONNECTED-MVCC | Approved isolated DB, reader/writer fixtures, collector and connected harness | Single-snapshot/role/catalog/concurrency and cleanup observations | Environment/privilege/connection authority |
| PUBLICATION-POC | Publication scenario suite, approved controls and publication contracts | Publication-specific outcomes and invariants | Its own execution gates, including human PUB-T13B decision |

Approval/evidence never transfers automatically between rows. Offline tests can characterize
a pending candidate interpretation if explicitly authorized as such; they do not approve it.

## Exact minimal capsule and future invocation

Copy only the following eight hash-bound files into a dedicated immutable review capsule
in a future separately authorized preparation step:
snapshot_codec.py, snapshot_reference.py, snapshot_oracle.py, test_snapshot_conformance.py,
snapshot_schema.json, snapshot_vectors.json, snapshot_compound_vectors.json, plus a copy of
the candidate MANIFEST.md as provenance (the first seven are runner files, manifest is package root).
No collector, transport, connected harness, run.py, SQL, fake collector tests or credentials.
Use a pinned CPython build/stdlib, no pip or additional dependencies, fresh low-privilege isolated
environment with network denied, read-only capsule and separate bounded evidence output.
Record interpreter executable/build digest, OS, architecture, locale, clock, limits and all inputs.
Do not assume Python -I is an OS sandbox or a resource limiter.

Future command template, NOT executed, with absolute approved interpreter and capsule paths:

```text
<APPROVED_PYTHON> -I -B -c "import sys, unittest; sys.path.insert(0, r'<APPROVED_CAPSULE>'); suite=unittest.defaultTestLoader.loadTestsFromName('test_snapshot_conformance'); result=unittest.TextTestRunner(verbosity=2).run(suite); raise SystemExit(not result.wasSuccessful())"
```

Do not use broad unittest discovery: it would include collector/harness tests outside this scope.
Current minimal suite is the eight methods in CodecConformance. No command is added to run.py.
Before any run, independently review the capsule/import graph and freeze all expected inputs.
The command is a future invocation description, not an approval bypass or installed launcher.

## Proposed finite experiment envelope

Numbers below are proposed laboratory admission limits only, not production/wire limits.
They require human approval and external enforcement before the first run.

| Dimension | Proposed bound | Enforcement and gap |
| --- | --- | --- |
| Input file size | 1 MiB each; 8 MiB capsule data/source aggregate | Verify before interpreter import; no unbounded file loading |
| Fixture rows | At most 3 per table and 90 total persisted rows; published view at most 3 | Review fixture recipes before construction |
| Scalar UTF-8/bytea | At most 4096 bytes | Review decoded inputs; no huge adversarial allocations |
| JSON depth / nodes | Depth 16, at most 1024 nodes per value | Preconstruct admission inventory; recursive pure codec has no built-in guard |
| Decimal expansion | At most 128 coefficient digits and absolute exponent 128 | Review before Decimal formatting/encoding; exponent attacks excluded from first run |
| Malformed wire | At most 1 MiB actual bytes, including truncated headers with huge declared lengths | Must reject based on available bytes, never allocate declared payload blindly |
| Whole output | 8 MiB stdout/evidence cap | External bounded capture; no unbounded full-payload logging |
| Recursion | CPython configured limit no greater than 1000; inputs stay within declared depth | Record actual value; recursion limit is not memory isolation |
| Process memory / duration | Proposed 256 MiB accounted memory and 30 seconds wall time, plus 5-second cleanup budget | Independent approved isolation/deadline mechanism; exact metric/tolerance unresolved |

Do not execute huge-depth/exponent or allocation attacks in the first round. If any fixture cannot
be admitted, refuse the run and revise the experiment envelope before observation. Limit breaches
must invalidate evidence; truncating inputs/output to make a test succeed is forbidden.
Without enforceable environment limits, offline execution remains BLOCKING_EXECUTION_REVIEW.
No claim that pure codec/reference/oracle reject every oversized input has been established.

## Independent fixture source and expected/observed separation

Source recipes: existing hand-derived scalar literals in snapshot_vectors.json and compound
definitions in snapshot_compound_vectors.json, plus independent oracle.populated_fixture and
fixture_snapshot. Full typed fixture has all 191 fields across 30 tables, synthetic values and
a supplied typed view; it is wire-only and must never be inserted as a DB fixture.
Oracle uses its own construction (struct framing and fixed-point Decimal derivation), imports
neither codec nor parser, and layer_records names every table/partition/global/metadata/view/
envelope record. Hash algorithms alone do not make a shared semantic assumption independent.

| Evidence state | Meaning / permitted transition |
| --- | --- |
| EXPECTED_UNVERIFIED | Current literals/recipes, including any future independently generated but unreviewed bytes; not trusted conformity evidence |
| REVIEWED_FROZEN | Named independent reviewer approves provenance, interpretation, exact bytes/length/digests and schema/config identities BEFORE comparison run |
| OBSERVED | Actual codec/reference output with run identity and environment; stored separately and never used to overwrite expected data |

These labels classify test evidence, not new domain enums or gate promotion.
No expected bundle is REVIEWED_FROZEN and no OBSERVED bundle exists in this delivery.
Independent generation must happen in a separate authorized oracle-only step, with only oracle,
schema and frozen fixture recipe available; no SUT outputs or copied hashes. Preserve generated
bytes/length/SHA per layer as EXPECTED_UNVERIFIED, then obtain review and freeze immutable files.
The current suite computes oracle expectations dynamically; it is suitable only for provisional
comparison until a reviewed frozen bundle and its comparison adapter are available.
It does not yet consume a complete REVIEWED_FROZEN bundle. That is an explicit gap.
Never rename dynamically computed expectations to reviewed evidence after observing SUT output.
Future observed output must include differences and failures, not only success summaries.

## Coverage, rejection and temporal boundaries

| Requirement | Prepared test / input | Independent oracle | External dependency / evidence | Current state |
| --- | --- | --- | --- | --- |
| Empty/multirow/PK ordering | test_empty_multirow_order_and_corruption | Hand lengths 200/288 and independent relation framing | Byte comparison and typed decode, permutation same bytes | MATERIALIZED_NOT_RUN |
| NULL/Decimal/UTF-8/bytea | scalar bytes and negative typed tests | Manual literals and independent scalar_fixture | Exact type/scale and Unicode distinctions | MATERIALIZED_NOT_RUN |
| Nested JSONB | test_nested_json_independent_bytes | Manual tree and flattened literal, independent builder | No floats/duplicate/nonfinite tokens; exact UTF-8 keys | MATERIALIZED_NOT_RUN |
| All tables/partitions/global/metadata/view/envelope | empty/multipartition and fully populated tests | Independent fixture_snapshot/layer_records | Frozen hex/length/SHA for every layer, later observed comparison | UNRESOLVED frozen bundle |
| Malformed frames/types/fields/versions | test_rejections and corruption cases | Independent declared rejection grammar | Actual errors, not invented error parity | MATERIALIZED_NOT_RUN |
| Wire microseconds | Existing endpoint negative vectors and -1 scalar | Integer microseconds, reserved endpoints rejected under candidate rule | No float epoch | MATERIALIZED_NOT_RUN |
| Python datetime/timezone | test_python_time_domain_without_postgresql_claim | Hand-derived epoch hex, independent micros input, declared overflow | Offset equivalent to epoch; naive datetime rejected; UTC boundary overflow; not exhaustive | MATERIALIZED_NOT_RUN |
| PostgreSQL finite endpoints | POSTGRES-FINITE-EXTREMES | Exact pinned DB contract required | Not executable or proved by this offline scope; no database here | UNRESOLVED |

SQL NULL differs from JSON null and empty text/bytea. Decimal 1.0 and 1.00 retain distinct scale;
Unicode composed/decomposed strings retain distinct bytes. Infinity/-infinity remain rejected.
Python years 1..9999 and UTC-conversion overflow differ from broad wire int64 acceptance;
finite PostgreSQL storage limits must not be inferred from either. Stored microseconds do not
recover upstream precision or timezone spelling already lost in storage.

## Interpretation and approval register

SNAP-P01 partition prefixes/membership; P02 full normal-version metadata streams; P03 semantic
view nullability; P04 full framed-key ordering; P05 typed values are all PENDING_HUMAN_APPROVAL.
Existing source behavior is the named candidate under evaluation, not a new selection here.
Before frozen evidence, reviewer must identify which pending interpretation is being evaluated.
A contrary decision requires explicit compatibility/version changes and new oracle provenance.

Smallest future request: authorize only independent oracle generation/review and the eight
offline conformance methods for the exact capsule hashes, pinned environment, finite limits
and proposed interpretations. Transport, connections, SQL, supervisor and publication remain
excluded. A subsequent transport/MVCC/publication request must provide its own authority.
EXEC-G1/PERS-G1 OPEN; PUB-T13B PENDING_HUMAN_APPROVAL.
