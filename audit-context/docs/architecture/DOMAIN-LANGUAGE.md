DataMarket — Canonical Domain Language

Document: "docs/architecture/DOMAIN-LANGUAGE.md"
Status: ACCEPTED
Scope: Canonical terminology, state taxonomies, identifiers, time semantics, type guidance, ownership and cross-document vocabulary
Last updated: 2026-09-08

---

1. Purpose

This document is the canonical vocabulary for DataMarket implementation and documentation. It consolidates terminology already established by PRODUCT, REQUIREMENTS, ARCHITECTURE and ADR-001 through ADR-015 without changing their architectural decisions.

When an older document uses a conceptual or legacy name for the same semantic concept, implementation should use the canonical name defined here. If a naming difference would change semantics rather than merely normalize vocabulary, the applicable ACCEPTED ADR remains authoritative and the conflict must be resolved explicitly.

A new domain term, state, enum, identifier, timestamp or quality concept should not be introduced until this document has been checked.

---

2. Canonical Processing Vocabulary

The primary analytical flow is:

External Market Data
    ↓
Provider Adapter
    ↓
CanonicalEvent
    ↓
MarketState
    ↓
FeatureEngine → FeatureState
    ↓
MarketEngine → AnalyticalState
    ↓
EventEngine → DerivedMarketEvent
    ↓
Publication Port
    ↓
Client Gateway
    ↓
ClientSnapshot / Incremental Update

DerivedMarketEvent may also be consumed by AlertEngine, which applies user/product notification policy. AlertEngine is not part of analytical truth.

ADR-014 refines the analytical portion of this flow without changing its ownership: FeatureEngine produces `DerivedObservable` measurements and may own a `FeatureState` aggregate; MarketEngine performs `CandidateEvaluation`, produces `CandidateEvidence` when evaluable and owns `AnalyticalState`. These are distinct epistemic layers.

Ownership rule:

- Provider Adapter owns provider translation and source semantics, never analytical conclusions.
- MarketState owns authoritative current in-memory market knowledge.
- FeatureEngine owns versioned quantitative measurements as DerivedObservable values and, where needed, their FeatureState aggregate.
- MarketEngine owns CandidateEvaluation, CandidateEvidence and interpretation as AnalyticalState.
- EventEngine owns meaningful analytical transition detection and DerivedMarketEvent lifecycle.
- AlertEngine owns user-specific notification selection/policy.
- Client Gateway owns transport, subscriptions, synchronization and client delivery.
- Persistence is asynchronous relative to the analytical hot path and is not authoritative live MarketState.

---

3. Decision Status

Canonical documentation decision classification:

ACCEPTED — approved decision that may be implemented.
PROPOSED — candidate decision not yet approved.
EXPERIMENTAL — implementation or approach under evaluation.
HYPOTHESIS — proposition requiring empirical validation.
PENDING — blocked by unresolved external or project information.

These values describe documentation/decision maturity. They are not runtime domain states.

Decision blockers are orthogonal metadata, not additional statuses. Canonical blocker values are: `RESEARCH`, `PROVIDER`, `B3`, `LICENSING`, `BENCHMARK`, `IMPLEMENTATION`, `SECURITY`, and `OPERATIONS`. Gate readiness is separately assessed as `SATISFIED`, `OPEN`, `BLOCKED`, or `ACCEPTED_RISK`.

Examples such as `PENDING_PROVIDER` or `PENDING_RESEARCH` found in historical/review text are aliases for `PENDING` plus a blocker. New normative documentation must not create compound status enums.

---

4. Identifier Types

Identifiers are semantically distinct even when their first Java representation is a primitive or String. They must not be interchanged merely because their storage type matches.

Canonical names:

- InstrumentId — DataMarket canonical instrument identity. “CanonicalInstrumentId” in explanatory text is an alias for this concept; implementation name should be InstrumentId.
- InstrumentFamilyId - product/family/selection-level identity; never a concrete observable instrument and never interchangeable with InstrumentId.
- MonitoringSelection - closed structured user-selection target: SpecificInstrumentTarget or InstrumentFamilyTarget.
- ProviderInstrumentRef - provider-boundary compound identity qualified by ProviderId, provider namespace and identifier type; never an InstrumentId.
- ProviderInstrumentMapping - versioned, effective-time and trust-qualified assertion from ProviderInstrumentRef to InstrumentId and definition version.
- InstrumentResolution - closed provider-resolution result: RESOLVED, UNRESOLVED or AMBIGUOUS; non-resolved results never contain InstrumentId.
- ProviderId — provider/vendor identity.
- FeedId — logical provider feed/stream identity.
- ConnectionId — one provider/client connection identity as applicable to its namespace.
- SourceEpoch — DataMarket epoch identifying a coherent source connection/recovery generation; not a provider sequence.
- EventId — stable identity of one logical DerivedMarketEvent lifecycle when used in the Event Engine domain. Canonical source-event identity should be explicitly namespaced in code if ambiguity exists.
- FeatureId — stable feature identity.
- DerivedObservableDefinitionId — exact versioned identity of one governed measurement definition; it is not an evidence identity.
- CandidateDefinitionId — exact versioned identity of one governed candidate-evidence definition; it is not an ExperimentId or evidence instance identity.
- RelationshipDefinitionId - exact versioned identity of one governed multi-instrument relationship/alignment definition; roles do not belong inside InstrumentId.
- ScientificObservationRef - stable research-execution reference to one exact originating canonical or synthetic observation identity and applicable revision/projection; it does not replace or merge those identities.
- ModelId - Market Model identity.
- DatasetId — persisted/research dataset identity.

Do not create a generic Id type that erases domain identity.

DisplayName, ticker text, provider identifier, FixtureId, ExperimentId and CertificationScopeId are not aliases for InstrumentId. Instrument identity is exact and case-sensitive; provider-specific case rules remain at the provider boundary.

---

5. Sequence Domains

The following are different concepts and must remain distinct:

- packetSequence;
- instrumentSequence;
- bookSequence when supplied with distinct semantics;
- snapshotSequence when supplied with distinct semantics;
- orderPriority / provider order-priority semantics;
- internalSequence — DataMarket processing sequence within a defined ordering domain;
- publicationSequence — ordering/versioning used by publication/client synchronization.

No internal sequence may be presented as exchange/provider ordering evidence. No global ordering across unrelated providers is implied.

---

6. Canonical Time Model

Canonical server-side time names follow ADR-005:

- eventTime — best available authoritative time of the underlying market/economic event;
- providerSendTime — provider/exchange publication/send time when available;
- ingestionTime — time DataMarket observes the event entering its controlled ingestion boundary;
- processingTime — time of a defined analytical processing stage when represented in domain/telemetry;
- publicationTime — time derived intelligence becomes available at an external DataMarket consumer boundary;
- clientReceiveTime — client-observed receipt time when reported.

Point-in-time analytical terms:

- availableAt - earliest defensible time at which an observation or derivation could be used under its governed policy; it is not inferred from eventTime alone.
- decisionTime - point-in-time knowledge frontier for an analytical evaluation; every required input must satisfy `availableAt <= decisionTime`.
- phenomenonOnsetTime - optional retrospective estimate of when a phenomenon began; it never backdates candidate/detection/confirmation.
- T_target - target-outcome time used only where a scientific target contract applies; operational candidate evaluation is target-blind.

DerivedMarketEvent lifecycle uses semantic event times in addition to the canonical pipeline times:

- candidateAt — first instant the candidate rule is satisfied;
- detectedAt — instant the event becomes STARTED;
- confirmedAt — instant confirmation criteria are satisfied, when applicable;
- endedAt — instant normal exit criteria are satisfied;
- invalidatedAt — recommended canonical name when invalidation timing is persisted/published.

“publishedAt” in transport DTOs is permitted as a wire-level field name only when it maps unambiguously to publicationTime. Internal analytical terminology should prefer publicationTime. “eventDetectedAt” is a transport-friendly alias for DerivedMarketEvent.detectedAt, not a second time concept.

Use UTC for internal absolute timestamps. TradingDate/session/calendar remain separate domain concepts. Use a monotonic clock for elapsed-duration measurements; wall-clock timestamp precision does not imply clock accuracy.

---

7. Price and Numeric Types

Hot-path price representation should preserve exact tick/scale semantics and prefer fixed-point integer representation where practical, as established by ADR-005.

Canonical type guidance:

- Price — domain value object/semantic type; hot representation preferably scaled long.
- Quantity — integral or fixed-point representation according to instrument/provider semantics; do not assume all quantities are int.
- TickSize / PriceScale — instrument metadata, not hard-coded global constants.
- Ratio / Return / Correlation / Volatility / normalized feature values — double is appropriate for quantitative computation unless a specific feature requires another representation.
- Money/decimal configuration or external administrative values — BigDecimal may be appropriate outside the tick hot path.
- Sequence values — long unless provider semantics require a different unsigned/compound representation.

Null/missing/unavailable is not numeric zero. NaN must not become the universal missing-value protocol across domain boundaries.

---

8. BookCapability

Canonical capability values:

NONE
TOB
MBP
MBO

Semantics:

- TOB — top of book only.
- MBP — aggregated market-by-price depth.
- MBO — individual market-by-order information when genuinely supplied with required semantics.

Capability is runtime truth. MBO must never be fabricated from MBP; MBP must never be fabricated from TOB and represented as equivalent fidelity.

A depth value, when applicable, is separate metadata from BookCapability.

---

9. FreshnessState

Freshness answers: “How current is this information for its source/instrument/domain?”

Canonical values:

LIVE
DELAYED
STALE
UNAVAILABLE

Freshness is source/instrument/domain-specific and must consider source semantics, market phase, expected activity and connection/recovery context. A WebSocket or provider connection being connected does not imply FreshnessState.LIVE.

RECOVERING and SYNCHRONIZING are lifecycle/readiness concepts, not canonical FreshnessState values. Older conceptual examples that place RECOVERING beside freshness values should be interpreted as combined lifecycle + freshness information, not as one universal enum.

---

10. DataQuality

Data quality is not one mutually exclusive enum. Canonical representation is conceptually:

DataQuality
    validity: DataValidity
    flags: Set<DataQualityFlag>

DataValidity:

VALID
SUSPECT
INVALID

Canonical composable DataQualityFlag values currently established by ADR-005 include:

STALE
GAP_DETECTED
RECOVERING
RECOVERED
OUT_OF_ORDER
DUPLICATE
SYNTHETIC
LATE
SOURCE_TIMESTAMP_UNVERIFIED

Additional flags require explicit semantics and documentation. STALE may coexist with FreshnessState.STALE because DataQuality describes evidence carried by an event/state while FreshnessState describes current temporal usability. Code should avoid ambiguous unqualified imports/names.

---

11. MarketStateLifecycle

MarketState lifecycle/readiness established by ADR-006:

UNINITIALIZED
BOOTSTRAPPING
SYNCHRONIZING
LIVE
DEGRADED
RECOVERING

Transitions are not assumed to be a single linear chain; failure/recovery paths are explicit. MarketStateLifecycle.LIVE means coherent/trustworthy state under its domain rules and must not be inferred from transport connection alone.

This enum is namespaced. It is distinct from FreshnessState.LIVE.

---

12. FeatureReadiness

Canonical values from ADR-007:

UNINITIALIZED
WARMING_UP
PARTIAL
READY
DEGRADED
UNAVAILABLE

Feature readiness is distinct from data quality and freshness. A feature may be structurally READY while a current dependency becomes stale; the resulting FeatureResult must propagate quality/freshness degradation according to feature semantics.

Do not introduce FeatureReadiness.LIVE. Older prose using “READY/LIVE” for a feature should be read as “FeatureReadiness.READY with live/usable dependencies.”

---

13. ModelReadiness and ModelHealth

ModelReadiness from ADR-008:

UNINITIALIZED
WARMING_UP
READY
DEGRADED
OUT_OF_DOMAIN
DISABLED

ModelHealth is a separate operational/analytical health dimension and may include:

HEALTHY
DEGRADED
OUT_OF_DOMAIN
UNRELIABLE
DISABLED

The repeated labels are intentionally namespaced; readiness and health answer different questions. Model confidence, evidence strength, data quality and calibrated probability remain separate concepts.

---

14. Analytical Runtime Results and Abstention

DerivedObservable is a deterministic, versioned measurement from admissible governed inputs. It is not automatically CandidateEvidence.

CandidateEvaluation is the closed evaluation boundary that produces CandidateEvidence or explicit NOT_EVALUABLE(reason). NOT_EVALUABLE is an expected inability to evaluate under declared conditions; ERROR is an unexpected invariant/runtime failure.

CandidateEvidence is a definition- and proposition-bound analytical contribution with point-in-time inputs, ancestry, roles, quality, freshness, limitations and lineage. It is not an Evidence Card, Evidence Bundle, Certification, prediction or trading recommendation.

AnalyticalState is continuous structured interpretation, not an event and not an alert.

NO_ANALYTICAL_CONCLUSION is an explicit abstention outcome/semantic state when evidence, quality, readiness or validated-domain conditions are insufficient. It must not be encoded as zero pressure or neutral direction unless the model semantics explicitly establish equivalence.

AnalyticalStateTransition is a versioned change from a previous AnalyticalState to a resulting AnalyticalState. Its candidateAt, detectedAt, optional confirmedAt and optional retrospective phenomenonOnsetTime remain distinct. It is not automatically a DerivedMarketEvent.

EvidenceTimeline is the governed logical point-in-time chronology of material analytical changes. A Runtime Working Timeline is only a bounded/compacted operational projection; compaction never establishes permission to discard scientifically required governed history.

StructuredWhyNow is a deterministic projection over governed AnalyticalState/EvidenceTimeline. It creates no evidence or scientific authority and may be rendered by an optional downstream LLM without allowing that LLM to alter analytical truth.

Support, contradiction, neutral, inconclusive, freshness, lifecycle, NOT_EVALUABLE and NO_ANALYTICAL_CONCLUSION answer different questions. In particular, no evidence is not neutral evidence, and inconclusive is not not-evaluable.

Pressure score is not probability. Confidence is not probability. Severity is not probability.

---

15. EventLifecycle

Canonical lifecycle values from ADR-009:

CANDIDATE
STARTED
STRENGTHENED
CONFIRMED
WEAKENING
ENDED
INVALIDATED

Not every event family must traverse every state. INVALIDATED is distinct from ENDED. Data loss/degradation must not be represented as a market reversal or normal event end.

A stable EventId identifies one logical event lifecycle; eventVersion identifies successive lifecycle representations/updates.

“DEVELOPING” is not a canonical EventLifecycle value. It may describe analytical confirmation maturity in Market Engine semantics.

---

16. EventSeverity

Current proposed taxonomy in ADR-009:

INFO
LOW
MODERATE
HIGH
CRITICAL

Status: PROPOSED / exact thresholds pending research.

Severity is analytical significance. It is not notification priority, probability, model confidence or evidence strength.

---

17. ProviderConnectionState

Canonical cross-provider connection vocabulary should use:

DISCONNECTED
CONNECTING
AUTHENTICATING
CONNECTED
SYNCHRONIZING
LIVE
DEGRADED
RECOVERING
RECONNECTING
FAILED

Provider adapters may expose provider-specific substates, but shared contracts should map them to this vocabulary when semantics are equivalent.

CONNECTED means transport/provider session exists. LIVE means provider Market Data is synchronized and trustworthy under provider readiness rules.

---

18. ProviderSubscriptionState

Canonical values:

REQUESTED
SUBSCRIBING
ACTIVE
UNSUBSCRIBING
INACTIVE
FAILED

Desired subscription intent is separate from actual provider subscription state.

---

19. ClientConnectionState

Canonical client-gateway connection/synchronization vocabulary from ADR-010:

DISCONNECTED
CONNECTING
CONNECTED
AUTHENTICATING
READY
SUBSCRIBED
SYNCHRONIZED
RECONNECTING
UNAUTHORIZED
DEGRADED

These values belong to the client transport/session domain and must not be reused as MarketStateLifecycle or ProviderConnectionState merely because labels overlap.

Client synchronization also carries independent publication sequence/version information. ClientConnectionState.CONNECTED never implies market data LIVE.

---

20. Market Phase and Trading Session

Market phase/status is first-class source/instrument state. Exact exchange/provider mapping is provider-specific and must preserve authoritative semantics.

Do not force all providers into a fabricated universal exchange-status enum if semantics differ. Canonical code may define a small shared category plus provider detail only after mappings are validated.

Trading session identity/date is separate from provider connection session and SourceEpoch.

---

21. Provenance

Canonical provenance must preserve at least:

- provider/source identity;
- original capability/fidelity;
- timestamp provenance/quality;
- sequence provenance;
- derived lineage for DerivedObservable, CandidateEvidence, AnalyticalState and DerivedMarketEvent.

Timestamp quality concepts established by ADR-005 include EXCHANGE_AUTHORITATIVE, PROVIDER_AUTHORITATIVE, LOCALLY_CAPTURED_SYNCED, LOCALLY_CAPTURED_UNVERIFIED, SYNTHETIC, ESTIMATED and UNKNOWN. Exact implementation enum remains PROPOSED until the time-quality model is finalized.

Provider-originated, exchange-originated and DataMarket-derived information must not be silently conflated.

### 21.1 Canonical ingestion and capability terms

The ingestion-specific authority is `CANONICAL-MARKET-INGESTION-AND-CAPABILITY-CONTRACTS.md`.

- SourceLineage - logical provenance across originating authority, delivery source, product/feed/profile, source mode/epoch, native identity, mapping/definition, normalization and capture/dataset context. It may use compact references to shared immutable context and is not required to be one per-event monolith.
- ObservationContext - logical event-specific facts plus compact references needed to recover applicable lineage, temporal, ordering, quality, correction and admission context.
- SourceMode - source execution/data mode, conceptually LIVE, HISTORICAL_DATASET, CAPTURE_REPLAY or SYNTHETIC; it is not ProviderId and does not establish historical/live equivalence.
- CapabilityProfile - scoped/versioned semantic qualification metadata; not a field-presence boolean or provider score.
- EffectiveCapability - purpose-specific result of technical availability, semantic qualification, entitlement, rights and current quality/admissibility. Its contributing dimensions remain separately auditable.
- ConsumerRequirements - declared required/optional capability, fidelity, temporal, quality/coverage and purpose constraints.
- PurposeAdmissibility - contextual decision over an immutable observation. It is not a permanent `trusted` property of that observation.

Canonical/source-native is a semantic boundary: qualified cross-source meaning may become canonical; useful unqualified native facts remain governed behind the source boundary and inaccessible to neutral scientific consumers.

### 21.2 Canonical scientific research-execution terms

The real-market single-instrument authority is `REAL-MARKET-SINGLE-INSTRUMENT-RESEARCH-EXECUTION-CONTRACTS.md` and ADR-015.

- ScientificTradeObservationView - minimal read-only provider-neutral scientific projection over a governed trade observation. It preserves an exact ScientificObservationRef, InstrumentId, fixed-point price, quantity when applicable, eventTime, availableAt, qualified ordering, correction/revision/projection and compact quality/coverage/admissibility/source-dataset lineage. It is not a persisted schema, provider DTO, RealTradeEvent or UniversalTradeEvent.
- Single-Instrument Analytical Topology - definition-owned topology with exactly one TARGET and no CONTEXT or RelationshipDefinition. Absent context is valid, not missing/unavailable/degraded.
- Relationship-Required Analytical Topology - definition-owned topology requiring exact declared roles and a compatible versioned RelationshipDefinition; missing or incompatible relationship material fails activation closed.
- Scientific Observation Adapter - narrow deterministic projection from an authorized synthetic or canonical observation to ScientificTradeObservationView. It preserves source identity/lineage and invents no fact.
- Source mode - lineage describing synthetic, historical, capture/replay or live origin as governed by ingestion authority. It never selects target, episode, baseline or evaluation mathematics.
- H0 Population Authority - immutable coherent identity of the listed contract, instrument definition/mapping, dataset/version, projection/frontier, session, coverage, purpose/admission and population/anchor/episode policies governing one target-characterization run. It is target-blind and cannot be derived from H1.
- H0 Cell Disposition - one of `CHARACTERIZABLE`, `CHARACTERIZABLE_WITH_LIMITATIONS`, `INCONCLUSIVE` or `INADMISSIBLE`; it describes whether a governed target cell can support its declared H0 use and is not a ResearchVerdict.
- H0 Attempt Ledger - complete immutable subordinate record of every governed target-cell/policy/dataset/projection attempt and its disposition, run/result references, limitations and supersession. It complements rather than replaces the Experiment Registry.
- H0-to-H1 Freeze - immutable reference package binding the exact H0 population, target cell or admissible set, projection, results, baseline references, ledger, limitations, rights/admission and code state consumed by an H1 branch. A material later change creates a new branch.
- economicTimeToCross - `crossingEventTime - anchorEventTime`; economic crossing duration. For `ABSOLUTE_FIRST_PASSAGE_V1`, this uses the preserved `T_cross`/event-time domain and does not reinterpret its knowledge-time `T_target`.
- knowledgeTimeToTarget - `targetKnownAt - anchorAvailableAt`; observable knowledge timing under the qualified temporal policy, distinct from economic target timing.

SyntheticEventIdentity, canonical ObservationId, ScientificObservationRef, episode identity, target identity and CandidateEvidence identity remain different namespaces.

---

22. Snapshot Vocabulary

ProviderSnapshot — source/recovery snapshot used to reconstruct provider-originated Market Data state.

AnalyticalSnapshot — stable read representation of AnalyticalState crossing ownership/publication boundaries.

ClientSnapshot — coherent product/client synchronization snapshot used by Client Gateway.

These are not interchangeable. A ProviderSnapshot is not a client payload. A ClientSnapshot is not a provider recovery mechanism.

---

23. State vs Event vs Alert

State answers what DataMarket currently knows.

Event answers what changed enough to be analytically meaningful.

Alert answers whether a particular user/product policy should cause notification/delivery action.

Do not name a continuous state update as an Event merely because it is transported over an event-driven mechanism. Do not name a DerivedMarketEvent an Alert.

---

24. Constants and Configuration

The following must not become unexplained hard-coded constants:

- freshness thresholds;
- pressure thresholds;
- event thresholds;
- hysteresis bands;
- persistence/debounce intervals;
- rolling-window lengths;
- feature normalization parameters;
- model weights;
- evidence-family weights;
- severity thresholds;
- reconnect/backoff limits;
- provider rate limits;
- publication conflation/update rates.

When empirically selected, quantitative constants belong to versioned model/feature/rule configuration and must be reproducible in replay/research. Provider-contract constants belong to provider configuration/capability metadata. Protocol constants belong to versioned contracts.

---

25. Naming Rules

Use PascalCase for Java domain types and camelCase for fields. Documentation may display enum values in UPPER_SNAKE_CASE.

Prefer explicit names over overloaded generic names:

- InstrumentId, not generic SecurityKey;
- eventTime, not sourceTimestamp when the ADR-005 semantic is intended;
- providerSendTime, not providerTimestamp when send/publication time is intended;
- ingestionTime, not IngestionTimestamp in implementation contracts;
- DataQuality, not QualityState when multiple flags can coexist;
- FeatureReadiness, not generic Status;
- MarketStateLifecycle, not generic State;
- ProviderConnectionState and ClientConnectionState, not shared ConnectionState across unrelated namespaces.

Do not create a universal Status enum.

---

26. Legacy / Conceptual Alias Map

Older documentation may contain conceptual names written before ADR-005 through ADR-014 matured. Interpret them as follows when semantics match:

SourceTimestamp → eventTime only when it means the authoritative underlying event time; otherwise preserve provider-specific source timestamp metadata.
ProviderTimestamp → providerSendTime only when it means provider/exchange send/publication time.
IngestionTimestamp → ingestionTime.
QualityState → DataQuality (not a single enum).
CanonicalInstrumentId → InstrumentId.
publishedAt → publicationTime at internal boundaries; transport alias permitted.
eventDetectedAt → DerivedMarketEvent.detectedAt.
READY/LIVE feature prose → FeatureReadiness.READY plus live/usable dependency freshness.
RECOVERING as freshness prose → lifecycle RECOVERING plus explicit FreshnessState/quality flags.
Market State when explicitly used for analytical interpretation → AnalyticalState; MarketState remains factual current/as-known market knowledge.
Market State Transition when explicitly used for interpretive-state change → AnalyticalStateTransition; Event Engine separately owns DerivedMarketEvent.

Aliases must not be applied mechanically when the original source has different semantics.

---

27. Implementation Classification

Before turning a documentation concept into Java, classify it as one of:

DOMAIN ENUM — mutually exclusive named domain state/value.
VALUE OBJECT — value with domain semantics/invariants.
IDENTIFIER — strongly named identity.
FLAG SET — composable simultaneous conditions.
STATE MACHINE — state plus allowed transitions.
CONFIGURATION VALUE — versioned/tunable parameter.
METRIC — telemetry/measurement, not domain truth.
DOCUMENTATION-ONLY CONCEPT — explanatory grouping that does not justify a code type.

Examples:

- BookCapability: DOMAIN ENUM.
- InstrumentId: IDENTIFIER.
- Price: VALUE OBJECT/semantic numeric type.
- DataQualityFlag: FLAG SET element.
- MarketStateLifecycle: STATE MACHINE + DOMAIN ENUM state.
- pressure threshold: CONFIGURATION VALUE.
- queue depth: METRIC.
- “understanding before prediction”: DOCUMENTATION/PRODUCT PRINCIPLE.

---

28. Architectural Invariants

1. No transport connection state may masquerade as market-data freshness/readiness.
2. No unavailable data may masquerade as numeric zero.
3. No internal sequence may masquerade as provider/exchange sequence.
4. No MBP/TOB feed may masquerade as MBO fidelity.
5. No score/confidence/severity may masquerade as calibrated probability.
6. No data failure may masquerade as market reversal.
7. No client/alert policy may mutate analytical truth.
8. No persistence store is authoritative live MarketState.
9. No LLM/news interpretation is required for deterministic hot-path detection.
10. No future information may enter replay/research evaluation at time t.
11. No provider-specific API type may leak into provider-independent analytical core contracts.
12. No new generic enum such as Status, State or Quality may erase an existing domain distinction.
13. No provider DTO, SDK object or arbitrary metadata map may become a neutral scientific contract.
14. No missing capability may be fabricated as zero, false, neutral or generated market/source identity.
15. No adapter declaration may self-certify semantic capability or rights for a purpose.
16. No provider switch may inherit scientific equivalence.
17. No recovered current state may erase a known incomplete event history.
18. No logical SourceLineage or ObservationContext model requires full shared context duplication per event.
19. No DerivedObservable is CandidateEvidence without an exact governed candidate evaluation.
20. No evidence absence, staleness, unavailability or NOT_EVALUABLE outcome may masquerade as neutral or directional evidence.
21. No future correction or retrospective onset may rewrite what was legitimately knowable at an earlier decisionTime.
22. No StructuredWhyNow/LLM output may create or alter analytical evidence.
23. No universal Éteos score, evidence strength, 0-1 confidence, voting or trading semantics is authorized.
24. No legitimate single-instrument definition may be forced to invent, duplicate or fake a CONTEXT/relationship.
25. No real canonical observation may masquerade as a SyntheticTradeEvent or SyntheticEventIdentity, and no synthetic fixture may masquerade as real Market Data.
26. No source-mode, provider, ticker or identity-shape branch may select target, episode, baseline or evaluation mathematics.

---

29. Change Governance

A terminology-only clarification may update this document and affected current architecture/product documentation without a new ADR.

A change that alters an ACCEPTED architectural decision requires a new ADR or explicit superseding ADR. Accepted ADR history must not be silently rewritten to make a new decision appear old.

Research may propose new feature/model/event taxonomies, but PROPOSED or HYPOTHESIS terms must not be promoted to canonical ACCEPTED runtime contracts until approved.

---

30. Guiding Rule

One concept may have several states, but one state label must never erase the concept it belongs to.

In DataMarket, LIVE, READY, DEGRADED and RECOVERING are meaningful only when qualified by their domain.
