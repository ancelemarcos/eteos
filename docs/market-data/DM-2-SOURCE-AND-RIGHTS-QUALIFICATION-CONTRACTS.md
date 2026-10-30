# DataMarket / Éteos - DM-2 Source and Rights Qualification Contracts

**Status:** ACCEPTED / MATERIALIZED DM-2 PROCESS AUTHORITY
**Scope:** purpose-specific source, dataset, temporal, technical, rights and scientific-use qualification
**Internal contract:** MATERIALIZED
**External qualification:** PHASE-1 PUBLIC EVIDENCE MATERIALIZED / SOURCE AND DATASET NOT QUALIFIED
**Provider selection:** NOT MADE
**DM-3A:** INTERNALLY READY BUT EXTERNALLY BLOCKED / NOT AUTHORIZED

## 1. Authority and non-authorization

This document is the principal authority for **how** DM-2 qualification is performed. It consumes the capability requirements in [ANTICIPATORY-INTELLIGENCE-DM-2-HANDOFF.md](ANTICIPATORY-INTELLIGENCE-DM-2-HANDOFF.md) and specializes, without replacing:

- [SOURCE-QUALIFICATION-REGISTER.md](SOURCE-QUALIFICATION-REGISTER.md), which records evolving source-slot outcomes;
- [PROVIDER-EVALUATION.md](PROVIDER-EVALUATION.md), which compares documented candidates;
- [DATA-USAGE-MATRIX.md](../regulatory/DATA-USAGE-MATRIX.md), which records current usage-right state;
- [EVIDENCE-REGISTER.md](../regulatory/EVIDENCE-REGISTER.md), which indexes evidence capable of changing a right;
- [B3-MARKET-DATA-LICENSING.md](../regulatory/B3-MARKET-DATA-LICENSING.md), which preserves the licensing boundary;
- [INSTRUMENT-IDENTITY-AND-RESOLUTION-CONTRACTS.md](../architecture/INSTRUMENT-IDENTITY-AND-RESOLUTION-CONTRACTS.md), which governs canonical instrument admission;
- ADR-005, ADR-011 and ADR-012 for time, persistence, provider and recovery boundaries;
- [DATASET-POLICY.md](../research/DATASET-POLICY.md), [RESEARCH-METHODOLOGY.md](../research/RESEARCH-METHODOLOGY.md) and [RESEARCH-VALIDATION-PROTOCOL.md](../research/RESEARCH-VALIDATION-PROTOCOL.md);
- [ANTICIPATORY-MARKET-INTELLIGENCE-CONTRACTS.md](../research/ANTICIPATORY-MARKET-INTELLIGENCE-CONTRACTS.md).

This materialization does not contact an external party, select a provider, acquire data, qualify a source, grant a right, authorize DM-3A, implement a provider adapter or create a real instrument definition or mapping. External questions are organized in [DM-2-EXTERNAL-QUESTIONS.md](DM-2-EXTERNAL-QUESTIONS.md).

The separately authorized Phase-1 public-evidence review is recorded in [EVIDENCE-REGISTER.md](../regulatory/EVIDENCE-REGISTER.md) with retrieval date 2026-09-05. Public facts are evidence inputs under this process; they do not alter its independent qualification dimensions or gates.

## 2. Fundamental qualification rule

DM-2 follows this direction:

```text
declared capability
        -> required observable
        -> required fidelity
        -> temporal and ordering semantics
        -> use-specific rights
        -> candidate source/product/dataset
        -> external and technical evidence
        -> purpose-specific scientific verdict
```

Qualification is bound to the applicable provider, source/feed, product, dataset/version, instrument scope, effective period, purpose/capability, evidence and limitations. There is no context-free "qualified provider" and no generic provider score.

The following separations are mandatory:

```text
CAN_CONNECT              != CAN_RESEARCH
CAN_DOWNLOAD             != CAN_RETAIN
CAN_RETAIN               != CAN_REPLAY
CAN_RESEARCH             != CAN_DISPLAY
CAN_DERIVE               != CAN_REDISTRIBUTE
TECHNICALLY_WORKING      != SCIENTIFICALLY_FIT_FOR_PURPOSE
PROVIDER_QUALIFIED       != DATASET_QUALIFIED
RIGHTS_QUALIFIED         != FIT_FOR_EVERY_PURPOSE
HISTORICAL_QUALIFICATION != LIVE_EQUIVALENCE
```

Unknown or missing mandatory evidence fails closed.

## 3. Independent qualification dimensions

Qualification is multidimensional. The dimensions may progress independently and converge only at a named purpose gate.

| Dimension | Question answered | Minimum binding |
| --- | --- | --- |
| Source identification | What exact external source is under review? | provider, source/feed, product, version and effective period |
| Semantics documentation | What do its fields, clocks, sequences, corrections and statuses mean? | exact technical authority and version |
| Rights documentation | Which uses are permitted, restricted or prohibited? | agreement/license, dataset/use, parties and effective period |
| Technical validation | Does observed behavior match the documented contract? | exact probe/sample scope and limitations |
| Dataset fit for purpose | Can this exact dataset support the declared scientific use? | DatasetId/version, purpose and evidence |
| Live equivalence | Which historical semantics are reproduced live and vice versa? | historical/live versions and comparison evidence |
| Scientific-use authorization | May the qualified dataset be used for the named activity? | passed gates plus explicit human authorization |

Evidence in one dimension never promotes another dimension implicitly. Rights can be documented before a probe; a technically valid feed can still lack research rights; a research-certified historical dataset can still lack live equivalence.

## 4. Qualification scope and verdicts

Every verdict must bind:

```text
provider
source/feed
product
datasetId + datasetVersion where applicable
instrument scope
effective period
purpose/capability
evidence references
limitations
review/approval provenance
requalification triggers
```

Purpose-bound verdicts are:

- `QUALIFIED_FOR_PURPOSE` - all mandatory evidence and gates for the exact purpose are satisfied;
- `CONDITIONALLY_QUALIFIED` - usable only under explicitly recorded conditions and limitations;
- `NOT_QUALIFIED` - evidence establishes that the scope does not meet the purpose;
- `NOT_EVALUABLE` - evidence is insufficient to make a scientific fit verdict.

Missing evidence produces `NOT_EVALUABLE` or a pending qualification status, never qualification.

## 5. External-fact status and evidence strength

The closed reconciliation vocabulary is:

- `KNOWN_INTERNAL_CONTRACT`;
- `KNOWN_EXTERNAL_FACT`;
- `PENDING_PROVIDER`;
- `PENDING_B3_OR_LICENSOR`;
- `PENDING_RIGHTS`;
- `PENDING_TECHNICAL_VALIDATION`;
- `PENDING_SCIENTIFIC_VALIDATION`;
- `OPTIONAL_FOR_FIRST_SLICE`;
- `NOT_REQUIRED_FOR_FIRST_SLICE`;
- `NOT_YET_JUSTIFIED`;
- `OUT_OF_SCOPE`;
- `CONFLICTING_EVIDENCE`;
- `UNKNOWN`.

This vocabulary qualifies facts and work; it does not replace the canonical architectural decision statuses in `DOMAIN-LANGUAGE.md` or the usage-right states in `DATA-USAGE-MATRIX.md`.

Evidence classes are:

- `OFFICIAL_B3_DOCUMENTATION`;
- `OFFICIAL_PROVIDER_DOCUMENTATION`;
- `CONTRACT_OR_LICENSE`;
- `EXECUTABLE_PROVIDER_PROBE`;
- `CAPTURED_SAMPLE`;
- `PROJECT_INTERNAL_ASSUMPTION`;
- `HISTORICAL_NOTE`.

For a `KNOWN_EXTERNAL_FACT`, the record must identify the external scope, repository-safe evidence reference, evidence class, version/effective date when known, limitations and enabled use. Internal expectations and unanswered questions are not external facts.

## 6. Current known-fact boundary

Only the following narrow family-level facts are preserved by current repository authority:

| Fact ID | Narrow fact | Evidence class | Limitation |
| --- | --- | --- | --- |
| `DM2-KF-001` | B3 public material describes WDO as the Mini U.S. Dollar futures product and records product-level quotation, tick and monthly-maturity facts | `PUB-B3-WDO-001` in `EVIDENCE-REGISTER.md` | not an exact listed contract definition; historically applicable metadata remains required |
| `DM2-KF-002` | ProfitDLL public family documentation conditionally describes trade, historical, TOB and book interfaces | `PUB-NELO-PROD-001`, `PUB-NELO-TECH-001`, `PUB-NELO-BOOK-001` | no exact product, API, dataset, access or behavior is qualified |
| `DM2-KF-003` | ProfitDLL public documentation describes price, quantity, trade number and buyer/seller/aggressor-related fields for named APIs/examples | `PUB-NELO-TECH-001`, `PUB-NELO-VERSION-001` | origin, units, flags, algorithm, exact package, historical parity and rights remain unqualified |
| `DM2-KF-004` | PUMA/UMDF public documentation distinguishes applicable timestamp, sequence, trade-bust, status and recovery domains | `PUB-B3-UMDF-001`, `PUB-B3-MR-001`, `PUB-B3-TS-001`, `PUB-B3-FIX-001` | does not establish that DataMarket has the applicable feed, product, access or entitlement |

No current `CONTRACT_OR_LICENSE`, provider probe, captured sample, technical-access evidence, confirmed external right or real historical dataset exists in the repository. The known facts above support question design only; they do not qualify a source or authorize scientific use.

### 6.1 Phase-1 public-evidence disposition

The exact public items are registered as `PUB-B3-*` and `PUB-NELO-*` records in `EVIDENCE-REGISTER.md`; downstream documents cite those stable IDs. The review fully closed **0/18** questions and partially answered **15/18**. `DM2-Q012` and `DM2-Q018` remain publicly unresolved, and `DM2-Q014` remains not evaluated because no exact-product technical probe was authorized.

ProfitDLL is `CONTINUE TO EXACT-PRODUCT QUALIFICATION` / `NOT SELECTED`. B3 direct is `CONTINUE AS FUTURE CANDIDATE` / `NOT SELECTED`. These are investigation verdicts, not source-slot promotion or product selection. Rights remain `PENDING`; public policy/terms do not establish DataMarket entitlement or exact-contract applicability.

## 7. Current candidates and fidelity priorities

Current candidate state remains:

| Candidate/slot | State | Boundary |
| --- | --- | --- |
| Nelogica / ProfitDLL | `CONTINUE TO EXACT-PRODUCT QUALIFICATION / NOT SELECTED` | Phase-1 public family/API evidence narrows questions; exact product, entitlement, behavior, rights and scientific fit remain absent |
| B3 direct / UMDF | `CONTINUE AS FUTURE CANDIDATE / NOT SELECTED` | Phase-1 public protocol/policy evidence narrows questions; exact product/dataset/access, behavior, rights and scientific fit remain absent |
| `SRC-CONTEXT-MARKET-01` | `PENDING` | no provider/source selected; non-blocking for first slice |
| `SRC-SCHEDULED-CONTEXT-01` | `PENDING` | future selected capability only |
| `SRC-NEWS-CONTEXT-01` | `PENDING` | optional enrichment only |

No candidate is selected or qualified.

Data-fidelity priorities are:

- **ESSENTIAL FIRST PHASE:** TRADE plus required identity, temporal, ordering/coverage, correction, session, lineage and rights semantics;
- **HIGH VALUE FUTURE:** qualified side/aggressor, TOB, one useful cross-market context source and historical/live comparison;
- **OPTIONAL / EXPERIMENTAL:** MBP, point-in-time macro, participant data and structured news;
- **NOT YET JUSTIFIED:** MBO without a declared order-lifecycle hypothesis, LLM/text pipelines and multiple rich feeds without a declared scientific need.

## 8. Fit-for-purpose model

The minimum purpose vocabulary is:

- `FIT_FOR_TARGET_CHARACTERIZATION`;
- `FIT_FOR_NON_ANTICIPATORY_CHARACTERIZATION`;
- `FIT_FOR_ANTICIPATORY_RESEARCH`;
- `FIT_FOR_TRADE_FLOW`;
- `FIT_FOR_SIGNED_FLOW`;
- `FIT_FOR_TOB_LIQUIDITY`;
- `FIT_FOR_MBP_DEPTH`;
- `FIT_FOR_MBO_ORDER_LIFECYCLE`;
- `FIT_FOR_LIVE_EQUIVALENCE`.

A weaker-purpose verdict never implies a stronger one. In particular:

- missing qualified aggressor may block signed flow while unsigned TRADE characterization remains possible;
- missing book data may block liquidity research while trade intensity remains possible;
- missing defensible historical availability may permit non-anticipatory characterization while blocking anticipatory claims;
- historical fit never implies live equivalence.

## 9. First empirical slice and requirement matrix

The minimum candidate entry to DM-3A is one actual listed WDO contract plus an authorized historical TRADE dataset with price, quantity, fit-for-purpose temporal semantics, deterministic identity/ordering and coverage, correction semantics, session/population semantics, lineage/integrity and minimum research/retention/replay rights.

`WDO_SYNTH` is not real WDO. No production `InstrumentId`, family ID, provider mapping or rollover policy is selected here.

| Requirement | Classification | Current status |
| --- | --- | --- |
| Actual listed WDO contract identity | `MANDATORY` | `PENDING_B3_OR_LICENSOR` |
| `ProviderInstrumentRef` | `MANDATORY` | `PENDING_PROVIDER` |
| Price and its representation | `MANDATORY` | `PENDING_PROVIDER` |
| Quantity and its unit/meaning | `MANDATORY` | `PENDING_PROVIDER` |
| `eventTime` | `MANDATORY` | `PENDING_PROVIDER` |
| Source-specific `availableAt` model for point-in-time use | `MANDATORY` for that use | `PENDING_PROVIDER` |
| Native `TradeId` | `CONDITIONALLY_MANDATORY` | `PENDING_PROVIDER` |
| Deterministic source-event identity | `MANDATORY` | `PENDING_TECHNICAL_VALIDATION` |
| Ordering/sequence sufficient for the purpose | `MANDATORY` | `PENDING_PROVIDER` |
| Coverage/gap semantics sufficient for the purpose | `MANDATORY` | `PENDING_PROVIDER` |
| Corrections/cancellations/late trades | `MANDATORY` to qualify | `PENDING_PROVIDER` |
| Session/status or versioned equivalent | `MANDATORY` | `PENDING_PROVIDER` |
| Side/aggressor | `NOT_REQUIRED` | `OPTIONAL_FOR_FIRST_SLICE` |
| Provider/source/feed lineage | `MANDATORY` | internal model known; external facts pending |
| `DatasetId`/version/integrity | `MANDATORY` | `PENDING_TECHNICAL_VALIDATION` |
| Lawful normalized retention sufficient for reproducibility | `MANDATORY` | `PENDING_RIGHTS` |
| Replay/backtest | `MANDATORY` | `PENDING_RIGHTS` |
| Internal research | `MANDATORY` | `PENDING_RIGHTS` |
| Derived scientific artifacts | `MANDATORY` | `PENDING_RIGHTS` |
| Raw storage | `CONDITIONALLY_MANDATORY` only if the approved design depends on it | `PENDING_RIGHTS` |
| Rollover/active-contract policy | `NOT_REQUIRED` | explicitly deferred |
| TOB/MBP/MBO | `NOT_REQUIRED` | future purpose-specific qualification |
| Live feed | `NOT_REQUIRED` | future live/shadow gate |

Native TradeId is not mandatory when another externally grounded, deterministic event identity and correction/deduplication contract is demonstrated. Database row order or an invented provider identity is never such a substitute.

## 10. Temporal qualification and availableAt

Every timestamp record must answer existence, meaning, resolution, timezone/epoch, clock authority/quality, historical/live availability, ordering relevance, suitability for `availableAt`, evidence strength and open questions.

| Time domain | Qualification requirement | First-slice relevance |
| --- | --- | --- |
| event/exchange time | authoritative occurrence meaning and source mapping | mandatory |
| provider receive time | provider-boundary meaning, if exposed | optional unless used by policy |
| provider send/publication time | publication meaning and precision, if exposed | conditional input to `availableAt` |
| DataMarket `ingestionTime` | earliest controlled live receipt point and local clock quality | live/shadow only |
| historical record time | distinguish event, publication, archive and backfill times | mandatory if relied upon |
| correction time | when corrected information became available | mandatory where corrections exist |
| snapshot time | image/application semantics and source sequence | book scope only |

`eventTime` is never automatically `availableAt`.

An `availableAt` policy binds a source/product/dataset version and records:

- source field and authority;
- publication/knowledge semantics;
- precision, timezone and clock quality;
- historical/live differences;
- backfill and late-data treatment;
- correction availability;
- uncertainty;
- conservative rule;
- policy identity/version.

Where exact historical availability cannot be reconstructed, a later conservative time may be used only with explicit justification. Otherwise the dataset may be `FIT_FOR_NON_ANTICIPATORY_CHARACTERIZATION` but is not qualified for an anticipatory claim.

## 11. Ordering, coverage, gaps and corrections

Qualification records each applicable domain separately:

```text
TradeId
trade sequence
packet/channel sequence
instrument sequence
book sequence
sequence scope and reset/wrap
sourceEpoch
duplicates and out-of-order behavior
gaps
corrections/cancellations/late trades
snapshots
recovery
reconnect
```

No generic sequence may collapse distinct source domains. DataMarket internal sequence and database insertion order are not external market-order evidence.

For TRADE-only historical characterization, book snapshots and live recovery are not required. A defensible coverage contract remains mandatory. Silence alone does not prove market inactivity. When source completeness cannot be established for an evaluated horizon, the result must be censored, incomplete or invalid according to the target/dataset contract, not silently counted as `NO_HIT`.

The source qualification must determine whether a record is an original trade, retransmission, bust, cancellation, correction, late trade or historical backfill/revision. `eventTime` remains separate from when a correction became available. Corrections to a frozen dataset create a new `DatasetVersion` or equivalent immutable lineage.

## 12. Session and population qualification

The dataset must support a reproducible, versioned eligibility decision for applicable regular session, pre-open, auction, after-market, halt/interruption, closed market and special phases.

Eligibility comes from a qualified source/status/calendar authority and declared rules. B3 session behavior must not be hardcoded from memory. Native status events are not mandatory when an independently authoritative, versioned alternative is sufficient for the exact research purpose and its exceptions are preserved.

## 13. Rights model

Rights are source-, product-, dataset-, use-, party- and effective-period-specific. Each conclusion must bind an evidence reference and use the rights vocabulary governed by `DATASET-POLICY.md` and `DATA-USAGE-MATRIX.md`.

Required independent rights dimensions are:

```text
ACCESS
TRANSIENT_PROCESSING
RAW_STORAGE
NORMALIZED_STORAGE
HISTORICAL_RETENTION
REPLAY
INTERNAL_RESEARCH
DERIVED_ANALYTICS
MODEL_USE
INTERNAL_VISUALIZATION
EXTERNAL_DISPLAY
ALERTS
API_OUTPUT
REDISTRIBUTION
COMMERCIALIZATION
PARTICIPANT_DATA
QUARANTINE
AUDIT_RETENTION
DELETION
RECONSTRUCTABILITY
```

An allowed, restricted or prohibited conclusion requires repository-safe evidence whose scope/applicability has been checked. Until then the fact status is `PENDING_RIGHTS`, which is not permission.

### 13.1 Minimum lawful DM-3A envelope

Before DM-3A, the exact dataset requires evidence for applicable:

- access;
- transient processing;
- normalized storage/retention sufficient for reproducible research;
- replay/backtest;
- internal research;
- retention/use of derived scientific artifacts;
- audit metadata.

External display, alerts, API output, redistribution, commercialization, participant data, MBO and raw storage are not first-slice gates unless the approved implementation actually requires them.

### 13.2 Raw, normalized, derived, quarantine and audit boundaries

Raw rights, normalized rights and derived-output rights are distinct. Normalization does not remove source restrictions. Derived outputs require purpose/output-family and reconstructability review where applicable.

Persistent raw quarantine requires explicit retention permission. Without it, the system may retain only lawful diagnostic metadata sufficient to explain the unresolved observation, subject to the applicable agreement.

Scientific manifests, hashes, mapping versions, rights references, dataset metadata and derived evidence are distinct from licensed Market Data bytes. A scientific need for auditability never overrides licensing, deletion or retention obligations.

## 14. Real instrument and provider-mapping handoff

Before constructing a real `InstrumentDefinition@version`, external evidence must establish applicable venue/authority, economic product/family, listed contract, contract code, maturity/expiration, price scale, tick size, lifecycle/status, effective interval and definition source/version.

The external source supplies economic facts. DataMarket retains authority over the opaque canonical `InstrumentId` format. No real production WDO ID is chosen by DM-2 documentation.

Before approving a real `ProviderInstrumentMapping`, evidence must establish ProviderId, namespace, identifier type/value, feed/venue context, provider-specific case semantics, uniqueness scope, symbol reuse, effective interval, mapping corrections/history and external provenance. The approved mapping then binds the internally controlled InstrumentId, exact InstrumentDefinitionVersion and mapping version.

Provider symbol never implicitly becomes InstrumentId. Unknown or ambiguous identity remains outside the trusted canonical event stream.

## 15. Future dataset identity and lineage

A future real scientific dataset must record, where applicable:

```text
DatasetId + DatasetVersion
source/provider/feed/product identity
InstrumentId
InstrumentDefinitionVersion
ProviderInstrumentMappingVersion
coverage interval and trading dates
acquisition/capture method
schema and normalization versions
temporal policy version
coverage/gap policy
correction policy
session/population policy
rights profile/evidence references
quality summary and limitations
checksums/integrity
parent/transformation lineage
```

A normalized dataset preserves enough lawful lineage to explain its source, applied semantics, transformation, instrument mapping, temporal policy and exact version. If raw bytes cannot be retained, the design preserves the maximum lawful non-reconstructive audit evidence; DataMarket does not decide legal reconstructability internally.

## 16. External-unknown register

Blocking levels are `BLOCKER_TO_EXTERNAL_QUALIFICATION`, `BLOCKER_TO_DM3A`, `BLOCKER_TO_ANTICIPATORY_RESEARCH` and `BLOCKER_TO_LIVE_PRODUCT`. None of the following is a blocker to this contract materialization.

| ID | Domain / exact question | Why and capability | First-slice impact | Authority | Current evidence/status | Blocking level | Acceptable evidence / next action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `DM2-Q001` | What exact provider product, service and dataset will be evaluated? | defines the qualification object | critical | provider/B3/commercial | generic candidates only / `PENDING_PROVIDER` | external, DM-3A | exact offer, contract and versioned documentation; provider questionnaire |
| `DM2-Q002` | What listed WDO contract is observed and what official metadata governs it? | real InstrumentDefinition | critical | B3/dataset authority | family facts only / `PENDING_B3_OR_LICENSOR` | external, DM-3A | official contract metadata/version |
| `DM2-Q003` | What ProviderInstrumentRef identifies that contract by feed and effective period? | canonical mapping | critical | provider | none / `PENDING_PROVIDER` | external, DM-3A, live | identifier dictionary and symbol history |
| `DM2-Q004` | What exact historical TRADE fields are delivered? | price, quantity and lineage | critical | provider/dataset | family description only / `PENDING_PROVIDER` | external, DM-3A | exact schema plus authorized sample |
| `DM2-Q005` | What clocks exist and how can availableAt be derived? | point-in-time and lead time | critical | provider/B3 + science | internal contract only / `PENDING_PROVIDER` | DM-3A, anticipatory, live | temporal specification plus validation |
| `DM2-Q006` | What stable TradeId or equivalent ordering identity exists? | deduplication, correction and replay | critical | provider/B3 | unknown / `PENDING_PROVIDER` | DM-3A, anticipatory | schema and probe |
| `DM2-Q007` | How are missing data and market inactivity distinguished? | coverage, censoring and intensity | critical | provider/dataset | internal rule only / `PENDING_PROVIDER` | DM-3A, anticipatory | sequence/completeness/status evidence |
| `DM2-Q008` | How are busts, cancellations, corrections, late trades and retransmissions represented? | first passage, volume and replay | critical | provider/B3 | unknown / `PENDING_PROVIDER` | DM-3A, anticipatory | specification and representative cases |
| `DM2-Q009` | How are sessions, auctions, halts and special phases represented? | population eligibility | critical | B3/provider | requirement only / `PENDING_PROVIDER` | DM-3A | status or authoritative calendar evidence |
| `DM2-Q010` | Which historical/live fields and semantics are equivalent? | replay/live equivalence | deferrable | provider | unknown / `PENDING_TECHNICAL_VALIDATION` | live | comparison evidence |
| `DM2-Q011` | Which rights allow access, normalized retention, replay and internal research? | lawful first dataset | critical | contractual counterparty/licensor/legal | no confirmed evidence / `PENDING_RIGHTS` | external, DM-3A | contract/license and reviewed conclusion |
| `DM2-Q012` | Which raw, quarantine, audit and deletion permissions/obligations apply? | operations and diagnostics | raw deferrable | licensor/provider/legal | unknown / `PENDING_RIGHTS` | external, live | use-specific contractual clauses |
| `DM2-Q013` | Which derived scientific artifacts may be retained and how are they classified for reconstructability? | results and lineage | critical for used artifacts | licensor/legal | source-lineage dependent / `PENDING_RIGHTS` | DM-3A, live | conclusion by output family |
| `DM2-Q014` | Does observed behavior match the exact documented product? | technical and scientific fit | critical | authorized technical probe | no sample / `PENDING_TECHNICAL_VALIDATION` | external, DM-3A, live | authorized probe/captured sample |
| `DM2-Q015` | Is side/aggressor native, provider-derived or inferred, and with what limitations? | signed flow | not required | provider | conditional family note / `OPTIONAL_FOR_FIRST_SLICE` | stronger research only | documentation and sample after need is declared |
| `DM2-Q016` | What TOB/MBP capabilities and snapshot/sequence/recovery semantics exist? | liquidity and depth | not required | provider/feed | conditional family note / `OPTIONAL_FOR_FIRST_SLICE` | richer research/live | exact product qualification |
| `DM2-Q017` | Are MBO/participant semantics stable, available and permitted? | order lifecycle/participant activity | not required | provider/B3/licensor | no qualifying evidence / `NOT_YET_JUSTIFIED` | future capability | investigate only after an approved hypothesis |
| `DM2-Q018` | Which cross-market, macro or news sources can satisfy declared future capabilities? | future context | not required | future provider/licensor | abstract slots only / `NOT_REQUIRED_FOR_FIRST_SLICE` | future anticipatory capability | purpose-specific qualification later |

The external work queue and disclosure-minimized question sets are maintained in `DM-2-EXTERNAL-QUESTIONS.md`.

## 17. Capability-blocker map

| Capability | Minimum qualified dependency | Missing-data effect |
| --- | --- | --- |
| Basic first-passage characterization | actual WDO + qualified historical TRADE dataset | real characterization blocked |
| Trade intensity | TRADE identity, timestamps, ordering, gaps and corrections | book/aggressor not required |
| Inter-arrival | defensible time resolution, ordering and gaps | aggressor/book not required |
| Volume | quantity, corrections and coverage | aggressor/book not required |
| Price response | price and aligned TRADE time; TOB only for quote-defined variant | trade-only variant remains possible |
| Signed flow | qualified side/aggressor provenance and rights | unsigned research remains possible |
| Top-level liquidity | qualified TOB | does not block TRADE characterization |
| Depth liquidity | qualified MBP | does not block TRADE characterization |
| MBO lifecycle | qualified MBO identity/lifecycle | `NOT_YET_JUSTIFIED` |
| Cross-market lead/lag | context source, per-source availableAt/freshness, overlap and rights | WDO-only work remains possible |
| Participant activity | participant semantics and rights | no intention inference is allowed |
| Anticipatory claim | point-in-time availableAt for every required input | non-anticipatory characterization may remain possible |

## 18. DM-3A target-characterization gate

DM-3A requires all applicable rows below plus separate human authorization.

| Dimension | Current state | GO condition |
| --- | --- | --- |
| Scientific contract | internally available | exact DM-3A scope authorized |
| Real instrument identity | WDO family characterized by public facts; concrete listed contract and production identity missing | real definition and mapping approved |
| Dataset identity | candidate interfaces identified; exact dataset absent | immutable DatasetId/version established |
| TRADE semantics | public fields plausible; WDO population unobserved | price, quantity, conditions and lineage qualified |
| Temporal semantics | B3 direct documentation strong; ProfitDLL public evidence partial | sufficient for the declared characterization purpose |
| Ordering and coverage | B3 direct documentation strong; ProfitDLL completeness/gap semantics incomplete | deterministic identity/order and defensible coverage |
| Corrections | B3 direct documented; ProfitDLL `is_edit` evidence partial | correction/late/backfill policy qualified |
| Session/population | current B3 public fact known; historical authority and ProfitDLL exposure incomplete | versioned eligibility authority and policy |
| Rights | public framework known; exact rights unresolved | minimum lawful envelope confirmed |
| Lineage/integrity | no real dataset | manifest, versions, checksums and limitations validated |
| Fit for purpose | not scientifically evaluated | `QUALIFIED_FOR_PURPOSE` or explicit acceptable condition |

DM-3A is NO-GO if the real contract is ambiguous, `WDO_SYNTH` substitutes for it, a provider symbol becomes InstrumentId, the dataset cannot be frozen/versioned, price or quantity semantics are unknown, temporal semantics are inadequate for the declared purpose, database row order is used as market order, incomplete coverage becomes `NO_HIT`, corrections are silently absorbed, session/population is undefined, minimum rights are unresolved, technical evidence conflicts remain or fit is not approved.

## 19. Stronger anticipatory gate

An anticipatory test additionally requires:

- defensible `availableAt` for every required input;
- point-in-time reconstructability;
- late/corrected data handling;
- ordering sufficient for the claim;
- freshness where applicable;
- per-source cross-market alignment where applicable;
- reproducible candidate computation;
- defensible target timing;
- temporal anti-laundering;
- preservation of coverage, false-positive burden and limitations.

A dataset qualified only for target or non-anticipatory characterization cannot support an anticipatory claim.

A ProfitDLL trade timestamp alone does not establish knowledge availability. Clock authority, historical transformation, provider/send/receive semantics, DataMarket `ingestionTime` for live observations, ordering/completeness, correction timing, a conservative `availableAt` policy and point-in-time reconstruction remain required. Until then, no anticipatory claim is authorized.

## 20. Future live/shadow gate

Live/shadow equivalence additionally requires an exact qualified live feed, the canonical adapter path, early ingestionTime, characterized callback/thread/backpressure behavior, sequence/gap/reconnect/recovery behavior, snapshot semantics when book is used, quality/freshness propagation, measured latency/jitter, historical/live semantic comparison, the same canonical normalization path and applicable live/shadow rights.

This contract implements none of those mechanisms.

## 21. Evidence boundary and future representative probe

Evidence responsibilities remain separate:

```text
OFFICIAL TECHNICAL DOCUMENTATION -> declared fields, semantics and capabilities
CONTRACT / LICENSE                -> rights and obligations
AUTHORIZED SAMPLE / PROBE         -> observed behavior in its exact scope
SCIENTIFIC VALIDATION             -> fit for the declared research purpose
```

No class substitutes automatically for another.

A future authorized probe records exact product/API/feed/schema/version, one identifiable listed WDO contract, provider-native identity, price/quantity representation, timestamps, TradeId/event identity, sequences/order, duplicates, out-of-order behavior, gaps, corrections/cancellations/late trades, observable session transitions, historical/live differences and unobserved-scenario limitations.

A probe demonstrates only observed behavior in its exact scope. It does not prove universal completeness, grant rights or replace a contract. Probe execution, sample acquisition, download and retention remain unauthorized by this materialization.

## 22. Requalification

Requalification is required after applicable provider, product/API/library/schema, B3 feed, license/contract, historical dataset, backfill/correction, timestamp semantics/precision, sequence/reset/recovery, symbol/mapping, session/status, conflation/filtering, capability, retention/output right, output family, scientific purpose, historical/live or capture/normalization change. It is also explicitly required before any use crossing the announced B3 policy transition on **2026-11-01**.

Qualification is versioned and never permanent by implication.

## 23. Future logical artifact model

Future records may materialize, without collapsing their responsibilities:

```text
SourceQualificationRecord
DatasetFitForPurposeRecord
RightsQualificationRecord
TechnicalValidationRecord
ScientificUseAuthorization
Limitations
ExternalEvidenceRef
```

No Java type, persistence schema or scientific format is introduced by this documentation contract.

## 24. Register ownership and current state

- `SOURCE-QUALIFICATION-REGISTER.md` owns source-slot outcomes;
- `PROVIDER-EVALUATION.md` owns factual candidate comparison;
- `DATA-USAGE-MATRIX.md` owns current use-right states;
- `EVIDENCE-REGISTER.md` owns repository-safe rights evidence;
- `OPEN-QUESTIONS.md` is the concise regulatory queue;
- this document owns qualification process, dimensions and gates;
- `DM-2-EXTERNAL-QUESTIONS.md` owns internal outreach templates and question routing.

Current external rights remain pending. ProfitDLL continues to exact-product qualification without selection; B3 direct remains a future candidate without selection; context slots remain unresolved and non-blocking for the first slice; and no source or dataset is qualified. Phase-1 public evidence does not authorize contact, acquisition, probing, DM-3A or anticipatory research.

## 25. Readiness and protected boundaries

After this materialization:

```text
DM-2 INTERNAL CONTRACT          = MATERIALIZED / VALIDATED
DM-2 PHASE-1 PUBLIC EVIDENCE    = MATERIALIZED
DM-2 SOURCE/DATASET QUALIFICATION = NOT YET COMPLETE
PROFITDLL                       = CONTINUE TO EXACT-PRODUCT QUALIFICATION / NOT SELECTED
B3 DIRECT                       = CONTINUE AS FUTURE CANDIDATE / NOT SELECTED
DM-3A                           = NOT AUTHORIZED
ANTICIPATORY RESEARCH           = NOT AUTHORIZED
WIN                             = NOT STARTED
```

The protected Research Harness release, WDO synthetic science, TEST_INSTRUMENT architecture proof, Evidence V3-V8, Certification V1-V3, fixtures, Oracles, ExperimentSpecs and historical hashes are unchanged. The Phase-1 public-evidence materialization creates no empirical claim and does not complete DM-2 qualification.
