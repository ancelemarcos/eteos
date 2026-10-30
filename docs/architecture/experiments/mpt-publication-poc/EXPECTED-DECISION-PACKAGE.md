# Human deliberation record - candidate 0.23 / order v2.1

## Order v2.5 / candidate0.26 - operational independent-review matrix

READY_FOR_INDEPENDENT_REVIEW / NOT_RUN means the review assignment is specified, not that
independence has been established, review has occurred or any choice has been approved.
This is the single operational matrix for this round; older sections retain decision/evidence
history. No new plan, reviewer identity or approval record is created.
Input0.25:72 actual files/71 hashes matched; HEAD27b2db3e3818e4325e5cd3df27f4ba1bc797ab15;
external input manifest84f241b76c198275e535d48ffa8691303c8ba9c7fc9df4556e0fa303355d8573.
The twelve H01-H12 bindings in section7 below still match unchanged evidence bytes.
The application plan's H11 is explicitly historical0.23, not the current packet; no silent repair.
Current review must bind this packet via the final manifest and external manifest hash.

### Evidence tasks and objective acceptance

S = static document/source inspection, no execution or connection.
E = experimental test/implementation requiring later explicit authorization.
C = actual database/environment evidence; no connection allowed now.
H references here use this packet's section7, not the application plan's different H numbering.
All owners below are roles with person/authority/date/signature UNRESOLVED.
"Accept" and "reject" are criteria for a human review result, never outcomes recorded by this AI.

| Task / pending condition | Exact sources and hashes | Evidence available | Independent proof / deliverable still required | Role, objective accept/reject and dependencies | Connected environment? |
| --- | --- | --- | --- | --- | --- |
| IR-P01:22/8 membership, empty members and negatives | H01 P01 page; H09 snapshot_schema; H10 DDL; H12 FULL contract | Enumerated22 scoped/8global; manual P-A/P-B prefix and existing written partition controls | S: derive membership from DDL and contract without oracle output; return30-row membership ledger, empty-member rules, manual wrong/missing/foreign prefix cases with exact source refs. E: independent fixtures and rejection traces | DCR+ICR; accept iff exact sets/no duplicates/no omission, all22 members per present position and8 globals without position. Reject any mismatch or unsupported inferred assignment. Depends on frozen source hashes and independent reviewer | S:no; E:isolated offline only, later permission; no DB needed for this scope |
| IR-P02:independent full-stream derivation, multirow and@1 history | H02 P02 page; H11 central interpretation; H12 FULL contract; extra vector/oracle hashes below | Manual206-byte empty/264-byte two-row barrier examples; symbolic hashes; EMPTY/TYPED/MULTI definitions; known MULTI metadata gap | S:return independent frame/length worksheet and@1 compatibility evidence search record. E: author multirow metadata fixture using at least two rows in a metadata table, independent expected bytes and rejected rows-only/order/count variants | DCR+ICR; accept derivation iff frames/lengths/order match exactly; no computed digest invented. Incompatible previously approved@1 blocks same-version adoption and requires human version disposition. Missing history yields UNRESOLVED, not compatible. Depends on reviewer and source identity | S:no runtime/network; historical external records supplied by human if absent. E:offline authorization; no DB needed for wire fixture |
| IR-P03:exact-DDL proof and eight NULL cases | H03 proof; H10 schema.sql; H09 schema; H08 source tests | Field-level NOT NULL/INNER JOIN/biconditional ordinal proof, not deployment proof | S:return eight-row proof ledger with exact clauses and counterexamples under changed constraints/view. E:return one independently specified NULL mutation per output plus missing/extra/descriptor cases. C:actual applied DDL/view/constraint identity and SQL behavior evidence | DCR+ICR+deployment reviewer; accept static proof only under exact DDL. NULL injection must reject each field; NULL pp version/pending batch emits no published row; PUBLISHED+NULL ordinal cannot satisfy constraint. Deployment remains blocked without C. Do not merge static and DB verdicts | S:no; E:offline later; C:requires authorized access to intended DB/environment, possibly local; no network presumed necessary or permitted |
| IR-P04:unambiguous framing, duplicates and permutations | H04 P04 page; H12 framing contract; extra codec/reference/vector hashes below | Manual a,b,aa order and written permutation/corruption tests | S:independent length/tag boundary derivation and distinguish PK bytes, SQL collation, event/UI order. E:adversarial text/composite/boundary keys, duplicate canonical encoding rejection, permutations yielding identical canonical bytes | ICR+DCR; accept iff admitted values have unambiguous frames, duplicate framed PK rejects and permutations preserve bytes. Reject accidental representation collisions or temporal/UI equivalence claim. SHA collision-freedom is not proved by finite tests. Depends on typed domain/P05 and exact schema | S:no; E:offline later; no DB needed to establish canonical byte order |
| IR-P05:typed precision and explicit PostgreSQL domain | H05 P05 page; H09 schema; H12 scalar contract; extra scalar vectors below | NULL/JSON distinction, stored scale, raw bytes/UTF8, UTC micros; Python/wire limits explicitly separate | S:independent literal worksheet and exact intended PostgreSQL version/type/precision boundary evidence from authoritative documentation supplied for review. E:adversarial NULL/JSON/decimal/nonfinite/UTF8/binary/time tests and second encoder/parser. C:round-trip/storage boundary evidence when DB claims are sought | ICR+DB-domain reviewer; accept only explicitly bounded supported domain, no lost-precision reconstruction. Unsupported extremes remain excluded. Reject float rounding, normalization/coercion or conflated SQL/JSON null. Depends on versioned DB evidence and lawful data/fixtures | S:no code; external documentation may need separately permitted retrieval. E:offline later; C:authorized DB access later. No access now |
| IR-API:readers, inequalities and version rejection | H06 unapplied patch; H07 comparator; H08 tests; API/counter proposal hashes below | Existing test-only callers; five textual patch hunks matched prior round; six-counter implementation and proposed seventh; declarative mixed cases | S:owner-confirmed internal/external inventory and independent count truth table; E:second inequality, triple/extra duplicate, malformed/missing, valid mismatch, both version-rejection directions and abort/recheck/host failure cases | API reviewer+ICR; accept iff both inequalities and all seven populations hold, unsupported/missing versions reject and failure returns no report. External consumers UNKNOWN until attested. No operational reader exists: its tests remain absent, not waived. Depends on explicit API decision, edit/test authority and real host for OS proofs | S:no; external inventory requires human evidence, not assumed empty. E:offline later; real host/environment permission separate; no DB inherently required |

Exact supplementary source bindings (preserved files; hash values are integrity only):

| Artifact | SHA256 |
| --- | --- |
| runner/snapshot_oracle.py | 097835f23ff0da42e413abffe57bfb44e21a7e1c49afb13dea0c0182bc81a172 |
| runner/snapshot_codec.py | bc493979eaddcaa4a168d5a5366e3dddf05a3883390869bdbac073cfa2dae6c6 |
| runner/snapshot_reference.py | 3bde406558c2ae1bfc47a82c6df3817d252ab0d61128386728bce20ea037af0e |
| runner/snapshot_vectors.json | 12ee250e42a8ba57eb3cd48b52293d5bc5478618ad0cf91e0f731d7b177928e6 |
| runner/snapshot_compound_vectors.json | 9261d75de4e0be8b85271225cd04367b3cd11cc8b4b41d917fb0736a50e3ab69 |
| runner/expected_bundle_emitter.py | 94ee85b44d4e4353e1fa021b5b75051d2f81741143825848a48fdd62d14a9ad4 |
| runner/expected_wire_review.py | 87b1c7b80d460ceea420651f59812b77b3590b689511dc587492dc1c801f72f3 |
| EXPECTED-API-MIGRATION.md | 93c77cf9fe4e58e7dd7698caf34ce6479716a5b8eefc700758a8e001201e3a63 |
| EXPECTED-COUNTER-PROPOSAL.md | e3092f9debe152025ebd5443f9b8bf071f0d15f0416ace22d357c180ce7a7863 |

### Independence and human handoff

The designated human reviewer receives this packet, final manifest/external hash and exact
H01-H12/supplementary sources. The task is to return a per-task review record IR-P01..IR-API
with inspected hashes, reviewer identity/authority/independence, assumptions, derivation,
counterexample or corroboration, missing evidence and APPROVE/REVISE/REJECT/DEFER recommendation.
Return it to the owner for authenticated decision recording; no record is pre-filled as accepted.

For S work, independently derive frames, membership, SQL-null reasoning and count tables from
the written contracts/DDL. Do not obtain expected truth by running or copying snapshot_codec,
snapshot_oracle, emitter output or the same fixture factory under another wrapper.
A second implementation can later be useful only with separate derivation and no imported
shared encoding/oracle helpers; disclose all shared dependencies and correlated-error risks.
Existing reference parser/oracle separation is source evidence, not proof of independent people.
S reviews can identify defects without execution. E results require immutable actual traces;
C results additionally bind exact deployed environment/DDL identity. Preserve failed/inconclusive
reviews rather than replacing them with successful-looking summaries.

External review tasks ready for assignment: IR-P02 compatibility-history disposition, IR-P03
deployed-DDL evidence request, IR-P05 exact DB boundary evidence, IR-API external consumer
inventory, plus named security/environment reviewers. Their deliverables are the specific
ledgers/records in the matrix, referencing exact files/hashes; none has been requested from
another person or completed here. No messages, identities or signatures invented.

### ARCH-ADAPT-001 targeted architecture checklist

PROPOSED / REVIEW_ONLY; no seventh accepted decision or executable mechanism.
Use the exact contract references in the v2.4 compatibility section below.

| Review check / expected artifact | Objective review criterion and evidence gap | Milestone / unidentified role |
| --- | --- | --- |
| Qualified source boundary: adapter-to-canonical map with missing/correction/ordering/rights cases | Provider details stay in adapter/native boundary; canonical missingness preserved; no scientific equivalence inherited. Need actual product/version/right evidence; no provider selected | DM-2 source/rights owner; D013-001..009 |
| Version/migration: affected-contract and immutable-history map | Incompatible APIs/normalization explicit; no historical RH rewrites or implicit fallback. Need human compatibility-window decision; D010-004 remains PROPOSED | DM-4 architecture owner, DM-6 protocol owner |
| Critical path: capture/admission/analytics/persistence/publication dependency sketch | No UI/slow-client backpressure into analytical core, no synchronous snapshot/replay work in MIR path. Need topology/resource ownership evidence, not a new abstraction by default | DM-4 architecture owner; DM-7 operations owner |
| UI policy: event-versus-state and render/publication cadence table | May reduce renders/coalesce permitted projections; never drop analytical inputs or required event history to relieve UI. Explicit quality/freshness/resync; UI order not SNAP PK or market eligibility | DM-6 client/product owner; ADR-010 sections64-66/123 |
| Overload: queue/limit/loss-to-quality/abstention failure matrix | Bounded resource proposal must expose losses/delays and suspend dependent conclusions; no control failure as alpha. Required vs optional capabilities remain distinct. Need real containment evidence later | DM-4 design, DM-7 capacity/recovery owners |
| Measurement: stage metric dictionary and representative workload specification | Units/clock domains/windows/measurement overhead declared, no thresholds chosen without data; instrumentation must not block hot path | DM-7 performance/operations owner, DM-2 workload/rights dependency |
| Cross-domain change check: RH/MIR/MPT/UI impact ledger | RH determinism/history, MIR PIT, MPT cut/TP semantics and UI freshness reviewed independently. availableAt(input)<=decisionTime remains required, not inferred from publication cut | DM-4 architecture and scientific owners; DM-6 UI; DM-7 exit review |

Candidate measurable metrics for the metric dictionary, not current measurements or targets:
per-stage elapsed latency in microseconds with p50/p95/p99 over declared windows; admitted/
processed throughput in events/s; queue depth in entries and oldest age in milliseconds;
process CPU utilization with denominator/core count; heap/native memory in bytes; GC pause
duration/count; typed failure/loss counts with denominator; freshness lag under explicit clock
domain; UI render duration and rendered updates/s. Separate source-time latency from monotonic
local elapsed duration and document clock uncertainty. Record workload provenance, burst profile,
capture rights, runtime, hardware and instrumentation overhead before setting numeric goals.
No metric sample, benchmark, threshold, configuration or infrastructure is created now.
Real load claims and source switching remain unproved by synthetic extension milestones.

### Short prioritized next actions

1. Documentary, no execution: designate independent reviewers and hand them the hash-bound
   matrix; prioritize IR-P02 full-stream/multirow derivation and compatibility history, then
   IR-P03 eight-field proof ledger. They can inspect evidence and return unresolved findings.
2. Documentary/external evidence: obtain exact deployment/version evidence for P03/P05 and
   owner-attested consumer inventory for API; complete independent P01/P04/P05/manual-counter
   worksheets. No connection, external message or retrieval is authorized by this packet.
3. Human decisions: resolve each of the six forms individually from those records; assign the
   narrow ARCH checklist items to DM-2/4/6/7 owners. Missing evidence means DEFER/REVISE, never
   AI-filled approval. Semantic acceptance does not close infrastructure blockers.
4. Later authorization only: approve scoped fixture/reader/patch edits and independent tests,
   qualify OAA/loaded bytes/handles/isolation/native limits/monitor, and then consider each
   GENERATE_EXPECTED, REVIEW_AND_FREEZE, COMPARE_FROZEN permission separately.

This packet is READY_FOR_INDEPENDENT_REVIEW because each missing proof has a bounded task,
source binding, reviewer role and objective disposition. It is not independently reviewed,
approved, implemented, experimentally conformant or READY_FOR_EXECUTION.
428 defined slots remain UNRESOLVED; generated0/reviewed0/frozen0/observed0. A0 active;
EXEC-G1/PERS-G1 OPEN, PUB-T13B and formal SNAP/API approvals pending; all three phases
NOT_AUTHORIZED. RH/MIR/MPT, availableAt(input)<=decisionTime, T3a versus TP and DO_NOT_NOTIFY
preserved. No code/wire/DDL/patch/accepted-contract edit, test or workload execution.

## Order v2.4 addendum / candidate 0.25 - consolidated conditional directions

DECISION_RECORD_PREPARATION_ONLY / NOT_RUN.
Tracking label only: USER_CONDITIONAL_DIRECTION_RECORDED / FORMAL_APPROVAL_PENDING.
This is descriptive candidate documentation, not a new accepted enum or authenticated approval.
Provenance: the user explicitly requested processing ETEOS-MPT-CODEX-ORDER-v2.4-ADENDO.md;
section2 of that supplied document declares the six conditional directions transcribed below.
The document's assertion that they were previously expressed in the conversation is not
independent identity/authority evidence. We record the supplied direction, not an inferred
prior approval. Actual reviewer identity, authority proof, verified decision date, signature,
condition fulfilment and formal decision remain UNRESOLVED.
The six individual decision rows/forms below and all supporting evidence pages are preserved.

| Item | User-supplied declared direction (section2, summarized) | Prior technical recommendation | Open conditions / required evidence | Human owner, affected artifacts and next gate |
| --- | --- | --- | --- | --- |
| SNAP-P01 | Preserve exact position prefix/identity,22 scoped and8 global tables including empty members | CONDITIONAL_RECOMMENDATION to retain candidate-0.15/P01 | Independent membership/literal review and negative cases | DCR+ICR persons UNRESOLVED; P01 page, central rule, partition codec/oracle/fixtures; formal semantic decision PENDING_HUMAN_APPROVAL |
| SNAP-P02 | Four complete streams: public_projection, publication_barrier, publication_batch, publication_cut; canonical order/version/name/descriptor/count/rows | CONDITIONAL_RECOMMENDATION full streams | Independent manual derivation, multirow metadata vectors and @1 compatibility history; stop on incompatible approved@1, require explicit version proposal | DCR+ICR UNRESOLVED; P02 page, FULL contract proposed wording, metadata/oracle/vectors; PENDING_HUMAN_APPROVAL |
| SNAP-P03 | Preserve eight required nonnull published-view fields | CONDITIONAL_RECOMMENDATION under exact DDL/view | Independent proof, eight field negatives, evidence of actually applied DDL/view; static proof is not deployment evidence | DCR+ICR and deployment evidence reviewer UNRESOLVED; P03 page/schema/view descriptor; PENDING_HUMAN_APPROVAL |
| SNAP-P04 | Complete framed-PK byte order, separate from SQL/market chronology | CONDITIONAL_RECOMMENDATION separate ordering domains | Independent duplicate/representation-collision/permutation controls, version incompatible changes; snapshot order establishes neither temporal eligibility nor UI order | DCR+ICR UNRESOLVED; P04 page/sorting/vectors; PENDING_HUMAN_APPROVAL |
| SNAP-P05 | SQL NULL/JSON null, stored decimal scale, admitted UTC micros, raw binary/UTF8 without implicit normalization | CONDITIONAL_RECOMMENDATION typed precision with exclusions | Independent adversarial review and explicit PostgreSQL limits for any DB claim; no recovery of already lost precision | DCR+ICR/DB boundary reviewer UNRESOLVED; P05 page/scalars/time vectors; PENDING_HUMAN_APPROVAL |
| report@3 | Incompatible seven-counter proposal; compared_valid counts unique required record_check-valid IDs with all four comparisons completed, equal or different | CONDITIONAL_RECOMMENDATION explicit breaking migration | Internal/external consumer inventory, independent invariants and adversarial/cross-version tests; record validity is not observed-wire semantics | API_CONTRACT_REVIEWER UNRESOLVED; counter proposal/API migration/patch/sources; PENDING_HUMAN_APPROVAL and BLOCKED_ON_API_APPROVAL; patch unapplied |

DCR/ICR retain the meanings in section1 below. Each formal record still requires a genuine
APPROVE/REVISE/REJECT/DEFER, identity/authority, exact scope/version/hash, justification,
conditions, verified date and verifiable record. None is filled by this update.
The existing conditional application plan covers all six directions; only a narrow coverage
clarification is added for UI ordering, representation collisions and PostgreSQL boundaries.
No new generic plan or normative-contract change.

Technical blockers remain independent: genuine OAA/verifier/trust policy; named independent
reviewers; actually loaded bytes and runtime/import closure; immutable handles; no-network
isolation; external CPU/memory/time/output/cleanup limits and operational monitor.
GENERATE_EXPECTED, REVIEW_AND_FREEZE, COMPARE_FROZEN all NOT_AUTHORIZED.
EXEC-G1/PERS-G1 OPEN; PUB-T13B and all SNAP PENDING_HUMAN_APPROVAL; A0/fail-closed active.

## ARCH-ADAPT-001 compatibility review - PROPOSED / REVIEW_ONLY

Not a seventh approved decision. Recommendation: retain as a traceable candidate checklist
using existing boundaries; obtain human architectural review of genuinely new mechanisms.
No new framework, adapter, topology, data supplier, numeric target or implementation selected.
References below are repository-relative and identify exact decision IDs/contract sections.

| Candidate requirement | Existing authority / extension point | Compatibility, missing proof and review dependency |
| --- | --- | --- |
| 1 Source adapters | DECISION-REGISTER D005-001/002, D013-001..009; CANONICAL-MARKET-INGESTION-AND-CAPABILITY-CONTRACTS sections4-12 | Aligned with qualified canonical/native separation, SourceLineage/ObservationContext and purpose admission. Missing semantics remain missing; common API never proves scientific equivalence. Adapter declarations cannot self-certify. Real provider/mapping/rights still require DM-2. |
| 2 Versioned contracts/local changes | D005-001, D010-004, D011-004; canonical ingestion sections4,15; CURRENT-RESEARCH-CONTRACTS Change discipline | Aligned with versioned normalization and immutable historical evidence. Exact client compatibility window is PROPOSED, not accepted. Do not rewrite frozen RH material or invent universal migration compatibility. |
| 3 Critical-path separation | D010-001, D011-001, D014-009; MIR sections6,10; ADR-010 sections3,5,6 | Existing Publication Port/Gateway and analytics boundaries support this. MIR excludes synchronous persistence, remote calls, explanation rendering and heavy per-observation work. Physical queues/threading/deployment isolation and heavy snapshot/replay contention are not proven; review under DM-4/DM-7. |
| 4 Efficient presentation | AGENTS sections12,16; ADR-010 lines1277-1299,1447,2261-2301; D010-001/004 | Render cadence can be a client concern; specific configurable rate/aggregation policy remains candidate. Coalescing UI projections must never discard method-required events or reinterpret SNAP ordering as UI/time ordering. Freshness/quality explicit; no production UI assurance claimed. |
| 5 Safe overload | canonical ingestion section13 (lines211-217), D013-006/007; MIR sections7,10; ADR-010 client backpressure boundary | Explicit gaps/quality and scope-specific rejection/abstention aligned. Required capability failure must affect its dependent scope; optional absence degrades explicitly. Transport/control failures are not market evidence. Client backpressure must not propagate into Market Engine. Native containment/limits/load behavior unproved. |
| 6 Observability/performance budgets | AGENTS sections10,11,16; ADR-010 telemetry lines2211-2261; MIR section10 line254; canonical ingestion section13 | Stage p50/p95/p99, throughput/backlog/CPU/heap/native memory/GC/errors/freshness/render metrics are candidate measurements, not existing SLOs. Define units, clocks, measurement overhead and representative workload before targets. No arbitrary capacities/latencies or benchmark run. |
| 7 Change validation | D014-005/007; MIR sections7,9,10; CURRENT-RESEARCH-CONTRACTS authority/change discipline; DM-2-SOURCE-AND-RIGHTS-QUALIFICATION-CONTRACTS sections1-3 | Determinism/PIT/integrity/right checks align. Assess RH scientific truth, MIR analytical meaning, MPT publication and UI separately. MPT cut never replaces availableAt(input)<=decisionTime. Synthetic conformance does not certify real feed performance or inherited provider science. |
| 8 Operational simplicity | AGENTS sections10,14; canonical ingestion sections5,13; MIR sections6,10 | Compact immutable context and pre-resolved catalogs already offer extension points. Avoid speculative plugin/discovery layers, per-event registry/rights work or new infrastructure without accepted authority and measured need. |

Exact reference locations:
- docs/architecture/DECISION-REGISTER.md: D005, D010, D011, D013, D014 rows cited above.
- docs/architecture/CANONICAL-MARKET-INGESTION-AND-CAPABILITY-CONTRACTS.md: sections4-15,17.
- docs/architecture/MARKET-INTELLIGENCE-RUNTIME-CONTRACTS.md: sections6,7,9,10,12.
- docs/architecture/decisions/ADR-010-real-time-publication-client-gateway-and-websocket-protocol.md:
  sections3/5/6, rendering/freshness/telemetry line references above.
- docs/research/CURRENT-RESEARCH-CONTRACTS.md: Implemented baselines and Change discipline.
- docs/architecture/DELIVERY-ROADMAP.md: sections2-6, particularly DM-2/4/5/6/7.
- docs/market-data/DM-2-SOURCE-AND-RIGHTS-QUALIFICATION-CONTRACTS.md: sections1-3.
- docs/market-data/SOURCE-QUALIFICATION-REGISTER.md: lines46-51;
  docs/regulatory/EVIDENCE-REGISTER.md: lines80-104.
- AGENTS.md: sections8,10,11,12,14,16.

Existing mechanisms versus assurances: the register/roadmap report bounded synthetic canonical
ingestion and MIR slices IMPLEMENTED / VALIDATED, including source-extension proofs. Those are
existing documented milestones, not tests repeated or independently revalidated in this round.
They do not establish real B3/Nelogica throughput, safe production overload, deployment isolation,
UI quality or scientific equivalence. Publication Port/Client Gateway are accepted architectural
boundaries, not evidence that every production component is implemented.
Roadmap DM-2 qualification is incomplete; ProfitDLL remains BLOCKED / NOT SELECTED and B3 direct
a future candidate. DM-4 scaffold, DM-6 rights/security/client and DM-7 operational gates remain
the extension path; this MPT order neither starts them nor selects data/rights.

No direct semantic conflict found if these restrictions hold. Potential conflicts needing
explicit prevention: UI aggregation erasing analytical input; backpressure silently losing history;
interchangeability implying scientific equivalence; runtime-specific classes/data leaking into
the neutral core; speculative dynamic discovery on the hot path; arbitrary performance targets.
Human architecture owner (UNRESOLVED) must decide any new UI configuration/version-window/
topology proposal under its own Decision ID and scope. Source/rights owner must qualify data and
use; operations owner must supply representative measurements and containment evidence. Roles
are not assigned identities. ARCH-ADAPT-001 stays PROPOSED / REVIEW_ONLY, with no gate promotion.

PROPOSED / DECISION_PREPARATION_ONLY / READY_FOR_HUMAN_DECISION / NOT_RUN.
This is the single current deliberation document. It replaces the accumulated opinions formerly
in this file; individual evidence pages remain unchanged and hash-bound below.
Technical recommendations are CONDITIONAL_RECOMMENDATION, not APPROVED.
No AI-filled text is a human decision, authenticated approval or execution authorization.

Baseline: actual candidate0.22, 71 files /70 hashes verified without mismatch; HEAD
27b2db3e3818e4325e5cd3df27f4ba1bc797ab15; external input manifest
4ed64c13abf4d4a8e49cf8ee70036ebed6169a88628e07fee0e059948f04a839.
AGENTS.md and Decision Register apply; D011-001..003 and D014-005 do not approve these
candidate wire interpretations, persistence execution or any empirical result.

## 1. Individual SNAP decisions

All current rule IDs are candidate-0.15/P01..P05 under proposed MPT-SNAPSHOT@1.
For each row, recommended rejection of an alternative is an opinion, never an actual decision.
DCR = DOMAIN_CONTRACT_REVIEWER; ICR = INDEPENDENT_CODEC_REVIEWER; persons UNRESOLVED.
H01..H05 below bind exact unchanged individual pages; those pages contain detailed proof.

| Decision / current rule | Recommended choice; alternative recommended for rejection | Binary impact | Written tests/vectors (NOT_RUN) | Independent evidence absent | Human owner / state / hash |
| --- | --- | --- | --- | --- | --- |
| P01 / P01: POSITION prefix + exact position ID; 22 scoped and 8 global tables | Retain all scoped members including empty; reject aggregate-only identity or omitted empty members | Removing prefix/members changes partition table and upper bytes/digests | complete_empty_and_multiple_partitions; partition_descriptor_and_link_tampering; compound vectors | Independent membership/literal signoff | DCR+ICR / CONDITIONAL_RECOMMENDATION; PENDING_HUMAN_APPROVAL / H01 |
| P02 / P02: four full normal table streams in qualified UTF8 order | Adopt exact wording in section 2; reject bare rows, row containers alone and name/digest pairs | Candidate bytes retained; conflicting approved rows-only @1 requires new identity, vectors and reader migration | fully_populated_typed_snapshot; partition_metadata_envelope_and_pk_controls; EMPTY/TYPED/MULTI | Independent manual derivation, actual multirow metadata vectors, explicit compatibility decision | DCR+ICR / CONDITIONAL_RECOMMENDATION; PENDING_HUMAN_APPROVAL / H02 |
| P03 / P03: eight typed view fields, semantic nonnull, PK position_id | Retain descriptor conditional on exact enforced DDL; reject catalog-nullability fallback | Any flag/order/type change affects even empty-view digest and envelope | fully_populated_typed_snapshot; manual_wire_rejection_oracle; per-field negatives proposed only | Independent static proof signoff, eight NULL cases, deployed schema verification | DCR+ICR / CONDITIONAL_RECOMMENDATION; PENDING_HUMAN_APPROVAL / H03 |
| P04 / P04: full framed-PK byte order; raw UTF8 JSON keys/table names | Retain distinct ordering domains; reject SQL collation/numeric/payload-only replacement | Different sorting changes rows/tables/upper digests | empty_multirow_order_and_corruption; PK-adversarial vectors | Independent ordering/collision literal review | DCR+ICR / CONDITIONAL_RECOMMENDATION; PENDING_HUMAN_APPROVAL / H04 |
| P05 / P05: typed NULL/JSON, stored Decimal scale, raw bytea/UTF8, exact UTC micros | Preserve stored precision; reject float, normalization, millisecond truncation | Changes collapse distinctions and alter containing bytes/hashes | scalar_bytes_and_decoding; nested_json_independent_bytes; python_time_domain_without_postgresql_claim | Independent scalar/time review; no PostgreSQL extreme-range evidence | DCR+ICR / CONDITIONAL_RECOMMENDATION; PENDING_HUMAN_APPROVAL / H05 |

P01 membership checked from snapshot_schema.json using presence of a position_id column,
consistent with FULL-SNAPSHOT-CONTRACT and oracle partition construction. These are names,
not inferred ownership from a relationship to a position.
Scoped22: assessment_attempt, assessment_result, batch_recovery_audit, command_receipt, delivery_audit, notification, notification_decision, outbox_event, personal_journal_entry, plan, plan_revision, position, position_event, position_guard, position_revision, public_projection, publication_batch, publication_member, send_authorization, t4_operation_receipt, worker_lease, worker_lease_audit.
Global8: access_audit, domain_resolution_policy, publication_barrier, publication_cut, publication_domain, recipient_guard, synthetic_destination_call, synthetic_destination_receipt.
For every position appearing in ANY scoped table, include all22 scoped tables, including empty
members; global8 never acquire a position prefix. Empty data has no invented position.
Manual P-A prefix fragment: 700000000000000003502d41 (12 bytes); P-B changes final41 to42.

P04 framed key for a: 6b000000000000000a54000000000000000161; aa:
6b000000000000000b5400000000000000026161. Length participates; a,b,aa is canonical here.
This is distinct from SQL sort/collation and never defines event chronology or market time.

P05 SQL NULL 4e0000000000000000 differs from JSON null 4a00000000000000096e0000000000000000.
1.0 and1.00 retain scale. Python/wire limits do not prove PostgreSQL finite extremes. Encoding
cannot restore timezone, sub-microsecond precision or JSON input details already lost in storage.
All fragments are manual illustrative evidence, not generated slots or experimental outputs.

## 2. P02 exact proposed normative wording and compatibility

The unresolved conflict is FULL-SNAPSHOT-CONTRACT.md:124-125 ("encoded rows") versus central
SNAP-P02 and codec/oracle/reference full-stream composition. The following is proposed text
only; neither the original candidate contract nor any accepted contract is edited:

"Publication metadata SHALL be the raw concatenation of the complete normal-version
MPT-SNAPSHOT@1 table streams for mpt_poc.public_projection, mpt_poc.publication_barrier,
mpt_poc.publication_batch and mpt_poc.publication_cut, ordered by unsigned qualified-name
UTF8 bytes. Each stream SHALL contain version, qualified name, schema descriptor, ASCII
row count and outer row container with canonically ordered Row frames. All four streams,
including empty tables, SHALL be present from the same snapshot. Publication metadata
SHALL NOT mean bare Row frames, outer row containers alone, or name/digest pairs.
Its SHA256 SHALL enter the existing envelope metadata-digest frame."

Order is public_projection, publication_barrier, publication_batch, publication_cut, each with
mpt_poc. prefix. For publication_barrier, manual framing gives version23 + name36 +
descriptor128 + count10 + empty-container9 =206 bytes. Bare empty rows=0, container-only=9.
For two illustrative D/0,E/1 rows, each Row has29 bytes: full stream264, bare rows58,
container-only67. C0=63000000000000000130; R0=720000000000000000;
T(D)=54000000000000000144; I(0)=49000000000000000130.
SHA256(concat sorted full streams) and SHA256(concat sorted row frames) are formulas only;
no digest calculated. Different bytes invalidate binary equivalence, not prove collision impossibility.
Descriptor-only changes affect full metadata even when empty; stored-value changes affect both.
MULTI's two rows are position_guard, not metadata: actual multirow metadata coverage is absent.
Independent review must approve clarification for the unaccepted candidate @1 or require a new
wire identity if an approved/deployed @1 already means rows-only. No silent compatibility claim.

## 3. P03 static proof boundary

Premises: exact schema.sql NOT NULL/CHECK constraints are enforced and view :829-834 is
unchanged: direct projection of six r fields and two b fields through INNER joins.
Under these premises all eight fields are provably nonnull:
- position_id/version: position_revision NOT NULL :108 (also PK :115).
- lifecycle/side: NOT NULL :110/:111, independent of enum CHECK.
- remaining_quantity/average_entry_price: NOT NULL :112/:113.
- domain_id: publication_batch NOT NULL :67.
- ordinal: status NOT NULL :70-72, biconditional CHECK :82 and WHERE PUBLISHED :834.
The status equality and IS NOT NULL are two-valued, so CHECK cannot pass UNKNOWN; a surviving
PUBLISHED row must have ordinal nonnull. ordinal>0 alone would NOT prove this.
Nullable pp.position_version causes no matching INNER-join row; it does not null-extend output.
Pending/blocked batches with NULL ordinal are filtered out. No assumption that publish_batch
is the only writer is needed. An outer join, altered constraint/view or untrusted collected row
invalidates this proof. Deployment/catalog/constraint identity has not been checked in a database.
Per-field serialization rule: exact eight fields/order/types, nullable=false, reject any NULL;
no coalescing or omitted field. Proposed negatives: eight separate NULL mutations, missing/extra
field, tampered descriptor, pp NULL->no row, PUBLISHED/NULL->constraint rejection, pending/NULL
->no row. SQL cases are documentary only and need separate future authority.
Independent review remains absent; no database conformance, tenant authorization or MIR proof.

## 4. API report@3 decision

Recommendation: CONDITIONAL_RECOMMENDATION to adopt explicit incompatible report@3 semantics.
Current implementation is report@2. COUNTER-MIGRATION.patch remains unapplied and
BLOCKED_ON_API_APPROVAL. API_CONTRACT_REVIEWER identity/decision is UNRESOLVED.

| Counter | Exact population |
| --- | --- |
| required_slots | Unique required IDs |
| observed_slots | All observation list entries, including extra/malformed/duplicate |
| compared_valid_slots | Required IDs occurring once, passing record_check, with all hex/length/sha256/error comparisons completed, whether equal or not |
| matched_slots | Subset of compared_valid with all four fields equal |
| missing_slots | Required IDs absent from indexed string IDs; invalid presence is not absence |
| extra_slots | Distinct string IDs outside requirements, including invalid/duplicate extras |
| invalid_slots | Distinct entry indices malformed, record-invalid or belonging to any duplicated ID |

Record validity means exact fields, canonical hex, bounded bytes, exact length/SHA and null error,
not semantic observed-wire validity. Self-consistent malformed wire can count as compared but
mismatching. Expected-only validate_slots does not certify observations.
0 <= matched <= compared_valid <= required - missing <= required;
compared_valid <= observed - invalid. Each compared ID maps to a distinct valid entry, proving
the second bound. Categories overlap and mix entry/ID units; do not sum them.
All copies of duplicate required/extra IDs are invalid; extras/absences/invalids never count as
compared. Zero observations gives required=missing=428, all other counts0 only if checks finish.
Any admission/observer/limit/timeout/interruption/recheck failure prevents report return; no
partial or synthetic zero/success report. COMPARISON_ONLY is not a success verdict.

| Reader/caller | Migration and required negative behavior |
| --- | --- |
| ExpectedBundleReview.compare plus direct negatives :218/:334 | Only identified comparator callers; same arguments, explicit new version/seventh field |
| test_honest_counters / tests reading differences | Existing six meanings preserved; proposed patch adds seven-counter cases, NOT_RUN |
| compare_frozen -> validate_frozen | Internal only; unchanged admission/schema/template/budgets |
| Operational @2-only reader | None found; must reject @3 before display/use, never auto-upgrade |
| Operational @3-only reader | None found; must reject @2/missing/unknown marker, never infer seventh metric |
| External consumers | UNKNOWN; owner inventory required before external rollout |

No automatic shim or fallback. Proposed counter/timeout tests and existing abort/legacy controls
are NOT_RUN. Dedicated second-invariant assertion, triple/duplicate-extra coverage and real
version-reader/OS negatives remain absent; do not invent their completion.
Patch textual hunks checked against exact current sources: all five old-side locations/content
and hunk counts match. It has NOT aged relative to this baseline; this is textual analysis,
not applying/importing/testing the patch. Any future source/hash change requires renewed review.
Exact patch and source SHA256 bindings are H06-H08 below.

## 5. Six independent human decision records

Every field is intentionally UNRESOLVED. Human must supply APPROVE / REVISE / REJECT / DEFER
per row, not approve the packet as if all choices were inseparable. This form grants no authority.

| Item | Choice | Human identity/role | Date UTC | Exact scope/version/hash | Rationale/conditions | Verifiable signature/record |
| --- | --- | --- | --- | --- | --- | --- |
| SNAP-P01 | UNRESOLVED | UNRESOLVED / DCR+ICR | UNRESOLVED | UNRESOLVED; proposed P01/H01 | UNRESOLVED | UNRESOLVED |
| SNAP-P02 | UNRESOLVED | UNRESOLVED / DCR+ICR | UNRESOLVED | UNRESOLVED; proposed P02/H02 + section2 | UNRESOLVED | UNRESOLVED |
| SNAP-P03 | UNRESOLVED | UNRESOLVED / DCR+ICR | UNRESOLVED | UNRESOLVED; proposed P03/H03 + exact DDL | UNRESOLVED | UNRESOLVED |
| SNAP-P04 | UNRESOLVED | UNRESOLVED / DCR+ICR | UNRESOLVED | UNRESOLVED; proposed P04/H04 | UNRESOLVED | UNRESOLVED |
| SNAP-P05 | UNRESOLVED | UNRESOLVED / DCR+ICR | UNRESOLVED | UNRESOLVED; proposed P05/H05 | UNRESOLVED | UNRESOLVED |
| report@3 | UNRESOLVED | UNRESOLVED / API_CONTRACT_REVIEWER | UNRESOLVED | UNRESOLVED; proposed report@3/H06-H08 | UNRESOLVED | UNRESOLVED |

APPROVE accepts only expressly named semantics/API; application and execution remain separate.
REVISE records exact requested changes and affected version, without permission to implement.
REJECT retains current candidate bytes/@2 without claiming rejected semantics or the seventh
metric exists; no replacement is automatically selected.
DEFER records missing evidence, owner and revisit condition; refusal remains active.
For P02/P03 a human may condition acceptance on independent evidence; unfulfilled conditions
cannot be treated as approval to run. No new generic architecture review is needed to record
these six choices; unresolved technical work below remains separate.

## 6. Technical blockers and phase permissions

| Technical blocker | Existing evidence versus missing proof | Responsible human role / state |
| --- | --- | --- |
| Independent reviewers | Role labels only; no named qualification/separation | DCR/ICR/API reviewer; UNRESOLVED |
| OAA/verifier/policy | Default-deny interface; no real qualified authority or pinned expiry/revocation/role policy | SECURITY_AUTHORITY_OWNER; BLOCKED |
| Actual loaded bytes | Source hashes only; missing measured runtime/stdlib/transitive import closure | RUNTIME_SECURITY_REVIEWER; BLOCKED |
| Immutable handles | Nominal paths/recheck interface; no stable protected handle/TOCTOU evidence | RUNTIME_SECURITY_REVIEWER; BLOCKED |
| Network-free isolation | No qualified owned scope or demonstrated denial | OFFLINE_EXECUTION_OWNER; BLOCKED |
| CPU/memory/time/output/cleanup | Local guards only; missing external finite limits and forced-exit proof | OFFLINE_EXECUTION_OWNER; BLOCKED |
| Environment evidence | No pinned runtime/OS/loader/monitor attestation or genuine output-custody proof | OFFLINE_EXECUTION_OWNER; BLOCKED |

No names, vendor, algorithm, environment, signature, key, certificate or backend invented.

| Separate permission | Entry requirement | Permitted future exit / current state |
| --- | --- | --- |
| GENERATE_EXPECTED | Approved semantics; exact six source inputs plus support/runtime closure; qualified authority, handles/isolation/external numeric limits; explicit bounded run permission | Only EXPECTED_UNVERIFIED, review=null, all428 IDs and immutable generation provenance after recheck; NOT_AUTHORIZED |
| REVIEW_AND_FREEZE | Original generated artifact/provenance; independent per-slot review and explicit human freeze permission | Separately approved immutable frozen copy with genuine external binding; NOT_AUTHORIZED |
| COMPARE_FROZEN | Authentic frozen binding; approved API/version and consumers; measured observer/comparator; explicit comparison permission and finite host controls | Bounded divergence evidence after recheck, no report on abort; NOT_AUTHORIZED |

Semantic approval alone authorizes none of these. Report patch application is also a separate
future instruction and is not necessary to select generation semantics.
Future entry requires exact identities/paths/numeric limits and real evidence, never a filled
AI form. Capsule descriptor still records earlier candidate0.20; before any assembly, separately
review updated provenance and bind the final external manifest. No assembly is authorized here.

## 7. Exact evidence bindings

| Ref | Preserved artifact | SHA256 |
| --- | --- | --- |
| H01 | SNAP-P01-DECISION.md | 017391c0fce1b9083c1b62a69ef9299615a8678752a4b98bd6cbc329eb16c048 |
| H02 | SNAP-P02-DECISION.md | 6632dcd7736f5d22297ff0c594a2c8d2c6f6c8bb9fda3807fad4ce186c4bd0b9 |
| H03 | SNAP-P03-DECISION.md | dc35055bfa2423eaa71898eb7407816d07effb415d11272a0e4437c57d32fd0b |
| H04 | SNAP-P04-DECISION.md | 8af1937c93d0583f9bdceb82802ee62c448738e8828805c9d3fa1646c5169fee |
| H05 | SNAP-P05-DECISION.md | e8ee7ac701eeedddf6ee1b7e7e1ba2ff39f1107c3e19b62afafc43b56cf91e36 |
| H06 | COUNTER-MIGRATION.patch | 89ddfa3fd93d0e2d5e4f6fb5ae5ecec33eb7bf8a2968c718fbe1ebd89fac7ea2 |
| H07 | runner/frozen_bundle_compare.py | 8d8ca372c5053f56a031935ef6c1574fbe04faaa46f38a16d48def8de333afe9 |
| H08 | runner/test_expected_bundle_review.py | 2545bfd378666f67e029b759edc87625c14c1b3046f5e3f31bff047d1cf37303 |
| H09 | runner/snapshot_schema.json | 1e64e5e28444b41f4e9bad62db930286810cb62c7769f243a45566d8eb47017a |
| H10 | schema.sql | e1feebaf8b6cdce323fd4c7b95bdd08c2d1b0907f9d43f673e3cfd1933f6542a |
| H11 | SNAPSHOT-INTERPRETATION-REVIEW.md | 0e56704abe70a6c4f0f59b19240a4d97e6b3cd07cdcc0a262934d54b1b81d9c9 |
| H12 | FULL-SNAPSHOT-CONTRACT.md | 271502190093e9353dda6196165f1c4707ccbb51ad5268101fa75234aae8d1bd |

Final MANIFEST inventories all artifacts including this document; its external hash is reported
separately to avoid circular self-binding. Human record must reference the final packet hash
and relevant evidence hashes. File hashes establish integrity, not experimental conformity.

428 slots defined (EMPTY43/TYPED287/MULTI98); generated0/reviewed0/frozen0/observed0.
All expected values UNRESOLVED. No Python/SQL/test/runner/capsule/bank/network/controller,
generation/freeze/comparison/commit/ZIP. Eight capsule entries and original methods preserved.
RH/MIR contracts, availableAt <= decisionTime, T2a/T2b, T3a/TP, DO_NOT_NOTIFY and other
invariants unchanged. EXEC-G1/PERS-G1 OPEN; PUB-T13B/SNAP-P01..05 PENDING_HUMAN_APPROVAL;
A0/refusal active. No empirical conformance or automatic gate promotion.
