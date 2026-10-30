# DataMarket / Éteos - Market Intelligence Runtime Contracts

**Status:** ACCEPTED / MATERIALIZED CONTRACT AUTHORITY
**Scope:** provider- and instrument-neutral transformation of point-in-time canonical knowledge into governed analytical state and explanation
**Executable implementation:** NOT AUTHORIZED
**External state:** DM-2 SOURCE/DATASET QUALIFICATION NOT YET COMPLETE; DM-3A, ANTICIPATORY RESEARCH, REAL PROVIDER ADAPTER and WIN NOT AUTHORIZED

## 1. Authority and boundary

This document is the normative Market Intelligence Runtime contract. ADR-014 records the architectural decision; `DECISION-REGISTER.md` is the implementation-authorization index. Before executable work, the exact Slice must receive separate human authorization.

This contract specializes, without duplicating or replacing:

- ADR-005 through ADR-009 and ADR-013 for canonical time, factual `MarketState`, feature, analytical-state, event and ingestion boundaries;
- `CANONICAL-MARKET-INGESTION-AND-CAPABILITY-CONTRACTS.md` for observation, lineage, correction, quality, capability and purpose admission;
- `INSTRUMENT-IDENTITY-AND-RESOLUTION-CONTRACTS.md` for exact `InstrumentId` and provider-boundary resolution;
- `../research/ANTICIPATORY-MARKET-INTELLIGENCE-CONTRACTS.md` for research direction and non-claim boundaries;
- `../research/RESEARCH-METHODOLOGY.md`, `EXPERIMENT-SPECIFICATION.md` and `EXPERIMENT-REGISTRY.md` for scientific evaluation and promotion;
- existing Evidence V3-V8 and Certification V1-V3 contracts for scientific artifacts and certification.

It authorizes no Java, Maven module, POM, schema, provider, Market Data, real analytical candidate, empirical parameter, Evidence profile, Certification protocol, product event, alert, prediction or trading recommendation.

## 2. Canonical chain and epistemic ownership

The governed chain is:

```text
CanonicalObservation / factual MarketState
        -> DerivedObservable
        -> CandidateEvaluation
             -> CandidateEvidence
             OR NOT_EVALUABLE(reason)
        -> AnalyticalState
        -> AnalyticalStateTransition
        -> EvidenceTimeline
        -> StructuredWhyNow
```

`MarketState` is factual current/as-known market knowledge. `AnalyticalState` is the point-in-time interpretation of admissible analytical evidence. DataMarket must not create a second analytical `MarketState` or a megaobject mixing facts, measurements, evidence, interpretation and prediction.

The epistemic ladder is strict:

```text
OBSERVATION
!= DERIVED OBSERVABLE
!= CANDIDATE EVIDENCE
!= ANALYTICAL CONCLUSION
!= PREDICTION
!= TRADING RECOMMENDATION
```

Promotion between layers is never automatic. A runtime result has no scientific authority merely because it was computed, structured or produced by AI/ML.

`FeatureEngine` produces `DerivedObservable` values and may own a distinct aggregate `FeatureState`. `MarketEngine` owns candidate evaluation and `AnalyticalState`. `EventEngine` retains authority over `DerivedMarketEvent`. Existing names must not be multiplied into overlapping `FeatureResult`, `FeatureValue`, `DerivedFeature` and `DerivedObservable` representations.

## 3. Derived observables and candidate evaluation

A `DerivedObservable` is a deterministic, versioned measurement derived from admissible governed inputs. It is not evidence by default. Its logical contract preserves or references, as applicable:

- definition identity/version and immutable parameter-set identity/version/hash;
- exact input observation/derived-observable identities and revisions;
- root-observation ancestry, `InstrumentId` values and explicit roles;
- input temporal facts, observed interval, `decisionTime` and output `availableAt`;
- measurement semantics, value and unit;
- validity, quality, freshness, readiness, coverage and history limitations;
- capability/purpose context, transformation lineage and code/model state.

A `CandidateEvaluation` is an execution result with exactly one of these semantic outcomes:

- `CandidateEvidence`; or
- `NOT_EVALUABLE(reason)`.

`null`, zero, an empty collection or a normal exception path must not substitute for non-evaluation. `NOT_EVALUABLE` is an expected inability to evaluate under declared conditions; `ERROR` is an unexpected invariant or runtime failure. Errors must not be silently converted into abstention.

`CandidateEvidence` exists only under an exact governed candidate definition and proposition. It preserves or references:

- candidate definition identity/version;
- proposition or `HypothesisRef` and evaluation-specification reference;
- derived inputs, root ancestry and relationship/alignment provenance;
- `InstrumentId` values and explicit role bindings;
- parameter and methodology references;
- `candidateAt`, `detectedAt` when applicable, `decisionTime` and `availableAt`;
- semantic contribution, quality, freshness, capability context and limitations;
- lineage and code/model state.

Candidate existence does not imply predictive usefulness, statistical independence, scientific promotion, permission for operational use or permission to display/commercialize.

## 4. Evidence semantics and AnalyticalState

Semantic contribution, freshness, evaluation availability, lifecycle and analytical conclusion are orthogonal. The model must represent, without requiring these exact Java constants:

- support;
- contradiction;
- neutral evidence;
- inconclusive evidence;
- stale and unavailable dependencies;
- not-evaluable evaluation;
- analytical abstention.

The following are invariant distinctions:

```text
NO EVIDENCE != NEUTRAL EVIDENCE != CONTRADICTORY EVIDENCE
INCONCLUSIVE != NOT_EVALUABLE
STALE / UNAVAILABLE != MARKET DIRECTION
```

Support and contradiction may coexist. They are not normalized to neutral, newer evidence does not automatically win, and contradiction must not be removed retrospectively to improve a narrative. Neutral evidence is legitimate only when an evaluation explicitly produces it. No evidence means no admissible evidence exists.

`AnalyticalState` is a versioned point-in-time interpretation of currently admissible evidence. Its logical model may include:

- identity, semantic version and revision;
- analytical model/definition and parameter-set references;
- analytical scope, relationship reference, `InstrumentId` values and role bindings;
- `decisionTime`, `asOf` and `availableAt`;
- supporting, contradictory, neutral and inconclusive evidence references;
- stale, unavailable and not-evaluable dependencies;
- quality, freshness, readiness, limitations and non-probabilistic uncertainty;
- a definition-owned typed conclusion or `NO_ANALYTICAL_CONCLUSION`;
- previous-state lineage and code/model state.

`NO_ANALYTICAL_CONCLUSION` is first-class abstention. It remains distinct from neutral evidence, unavailable, stale, not-evaluable and error. Missing capability, insufficient quality, stale/unavailable dependency, incomplete history, insufficient or contradictory evidence, unsupported version and inadmissible purpose may cause abstention according to the exact definition.

There is no separate `EvidenceState` in the first executable Slice. `CandidateEvidence`, `AnalyticalState` and `EvidenceTimeline` cover its current responsibility. A future `EvidenceState` requires a concrete independent consumer/use case and a new decision.

No universal evidence strength, confidence value, score, probability, signal, alert, BUY or SELL semantics are defined here.

## 5. Definitions, relationships and activation

The minimum definition authority is one immutable physical `AnalyticalDefinitionCatalog` with typed namespaces/contracts for:

- `DerivedObservableDefinition`;
- `CandidateDefinition`;
- `RelationshipDefinition`.

Lookup and dispatch use exact typed identity/version. Unknown versions fail closed; there is no fallback to latest/default/nearest and no prefix, suffix, ticker or experiment-name pattern dispatch. An active execution selects exact definitions and parameter sets; definition existence does not imply activation. Catalog or material-context change creates a new catalog/context version rather than in-place mutation.

Material parameter sets have stable identity/version/hash. Windows, thresholds and other material configuration cannot be hidden in code. Parameter search and optimization belong to research; runtime executes frozen parameters. Definitions and parameters used in replay/science are immutable. Effective/activation intervals, if needed, remain separate from definition identity so today's definition is never silently applied to historical replay.

A versioned `RelationshipDefinition` preserves, as applicable:

- identity/version and effective interval;
- explicit roles and exact `InstrumentId` bindings or governed binding criteria;
- transformation identity/version;
- temporal-alignment and per-role freshness policies;
- methodology/specification, capability requirements, limitations and provenance.

ADR-015 specializes future real single-instrument research execution: topology is definition-owned. A `SINGLE_INSTRUMENT` definition binds exactly one `TARGET` and has no `CONTEXT` or `RelationshipDefinition`; that absence is valid rather than unavailable or degraded. A relationship-dependent definition still requires its exact roles and compatible relationship and fails activation closed without them. The Slice-1 synthetic TARGET/CONTEXT proof is not a universal relationship requirement.

Role is never inferred from `InstrumentId`, ticker, array position or file name. Cross-instrument alignment uses actual admissible inputs selected at `decisionTime`; equality of `eventTime` alone is insufficient. Future interpolation is prohibited. Forward-fill requires an explicit freshness bound and methodology.

Derived-on-derived dependencies may be explicit, acyclic and pre-resolved. Candidate-on-candidate dependency is deferred for the first Slice; evidence composition belongs in `AnalyticalState`. If an execution dependency DAG is needed, it remains an execution-plan detail rather than a universal domain graph. Cycles and invalid/missing definitions are rejected before hot-path execution.

Activation validates exact IDs/versions, parameter sets, instruments/roles, relationship references when declared, required capabilities, dependency existence/acyclicity, purpose/admission and temporal-policy compatibility. A candidate can be technically evaluable while scientifically unpromoted; scientific promotion remains separate, and operational/display/alert/commercial use requires its own authorization. Architecture-only synthetic definitions may bypass scientific promotion only inside unmistakably identified conformance scopes and never become product candidates automatically.

## 6. Execution context and ownership

An `AnalyticalExecutionContext` is compact, immutable and pre-resolved during activation/configuration. It references exact definitions, parameter sets, `InstrumentId`/role bindings, the exact relationship when definition-required, effective capability admission, purpose, quality/freshness policies, `MarketClock`, code/model state and a direct execution plan.

Analytics reuses the existing purpose, rights and capability-admission authority; it does not create a parallel rights model. Rights determine admissibility, retention and output use, not mathematical truth. An optional capability may degrade behavior only through an explicitly declared analytical mode/identity. Loss of a required effective capability produces `NOT_EVALUABLE` or abstention. A material definition, parameter, relationship, capability, purpose or admission change creates a new context revision/epoch.

Rights/purpose changes and later scientific promotion/deprecation affect new governed contexts; neither retroactively reinterprets prior lawful or scientific execution. Arbitrary exploratory definitions cannot masquerade as confirmatory/promoted definitions. Rights cannot silently select a different formula: any degraded formula is a separately declared mode/definition.

An `AnalyticalScopeKey` may be composed from definition/model version, parameter-set version and relationship/role binding. Prefer one owner/writer per logical partition where practical and immutable snapshots across ownership boundaries. A new state revision is emitted only for a definition-governed material change, including new admissible evidence, staleness, unavailability, correction or governed context transition.

The future preferred dependency boundary is a single `research-analytics` module owning definitions, derived observables, candidate evaluation/evidence, analytical state/transition, timeline, explanation, relationships and execution context. It is conceptual only in this checkpoint and must be revalidated before executable work. It must not own ingestion, adapters, native metadata, instrument resolution, scientific evaluation, Evidence/Certification, persistence, UI or LLM orchestration. Semantic/source foundations must not depend on analytics; analytics must not reach native metadata. Dependency cycles, foundation inversion or duplication of `research-evaluation` are stop conditions.

## 7. Point-in-time, corrections, quality and lineage

Every required analytical input obeys:

```text
availableAt(input) <= decisionTime
```

Every derived result obeys:

```text
derivedAvailableAt >= max(requiredInput.availableAt)
```

plus its declared computation semantics. Equality with the latest input is not universally assumed. Event, ingestion, processing, availability, decision, candidate, detection, confirmation, retrospective onset and target times remain separate.

`phenomenonOnsetTime`, when retrospectively inferred, never backdates `candidateAt`, `detectedAt` or `confirmedAt`. Operational candidate evaluation is target-blind and cannot depend on future target/outcome/Oracle material. Targets and baselines are consumed by downstream scientific evaluation.

Analytical correction semantics are bitemporal:

```text
AS_KNOWN_AT(t) != FINAL_CORRECTED
```

A correction becoming available at T2 creates deterministic analytical revisions at/after T2 and preserves the exact input revision used. It never rewrites the state, evidence, timeline or explanation legitimately knowable at T1. Withdrawal/invalidation is appended or revision-linked; prior evidence is not deleted.

Derived analytical objects cannot silently improve source quality. Computing now does not make stale input `LIVE`. Validity, freshness, gaps/coverage, ordering, history completeness, unavailable dependencies and source limitations remain separately auditable. Required stale/unavailable input may make evaluation not evaluable. Source-quality or runtime-control transitions may affect admissibility/state without becoming market evidence.

Derivation lineage preserves compact references to definition/version, parameter set, exact inputs/revisions, root observations, instruments/roles, relationship/alignment, temporal facts, quality/freshness, capability/purpose context, limitations and code/model state. An ancestry fingerprint is deterministic identity, not evidence of statistical independence. Full definitions, profiles and ancestry graphs are not copied per hot-path object.

Window/stateful definitions declare window, warmup and availability semantics in their parameter/spec identity. Insufficient warmup is explicit and may be `NOT_EVALUABLE`; centered future windows are forbidden. Restart/restoration by replay or a future qualified immutable snapshot must preserve definition/context identity and point-in-time semantics. A recovered `AnalyticalState` is not proof of a complete `EvidenceTimeline`, and no persistence mechanism is selected here.

## 8. Transitions, timeline and explanation

An `AnalyticalStateTransition` preserves previous and resulting state references, `candidateAt`, `detectedAt`, optional `confirmedAt`, optional retrospective `phenomenonOnsetTime`, evidence references, limitations, quality and availability. It is not automatically a `DerivedMarketEvent`, alert, notification or product event. Event Engine retains that authority.

`EvidenceTimeline` is the governed logical point-in-time chronology of material analytical changes. Its semantics preserve evidence appearance, contradiction, confirmation, staleness, unavailability, revision, withdrawal, invalidation and scientifically applicable target occurrence. It does not record every calculation or duplicate the raw market stream, and its deterministic ordering never implies semantic importance.

Two timeline concepts remain distinct:

- **Logical Evidence Timeline:** governed analytical history whose point-in-time truth is preserved.
- **Runtime Working Timeline:** operational in-memory projection that may be bounded or compacted under an explicit lifecycle policy.

Compaction of the working projection never authorizes silent loss of scientifically required history. Historical preservation, when required and legally permitted, remains under dataset/evidence/audit governance. Recovered current analytical state is not proof of complete analytical history. This contract does not authorize an event store or persistence technology.

`StructuredWhyNow` is a deterministic projection over governed `AnalyticalState` and `EvidenceTimeline`. It may expose what changed, when it became knowable, instruments/roles, support, contradiction, neutral/inconclusive evidence, stale/unavailable/not-evaluable dependencies, delta from prior state, limitations, uncertainty and the reason for abstention. Every authoritative element traces to governed runtime material; explanation creates no evidence.

The projection remains valid when the conclusion is `NO_ANALYTICAL_CONCLUSION` or a candidate is `NOT_EVALUABLE`: it explains the absence/abstention without manufacturing evidence. Support, contradiction and neutral evidence retain independent lifecycle facts and may later become stale, withdrawn or invalidated without erasing that they existed.

The projection uses deterministic ordering, compact references and definition-resolved labels. Labels/localization are presentation concerns and do not change identity. Point-in-time and final-corrected explanation views may differ without overwriting one another.

A future LLM may render `StructuredWhyNow` outside the authoritative hot path. It cannot add/remove evidence, invent causality, define `availableAt`, act as its own Oracle, alter the conclusion or block detection.

## 9. Scientific, Evidence, Certification and score boundaries

Runtime `CandidateEvaluation` answers whether a declared candidate can be evaluated now and what analytical evidence it produces. `research-evaluation` owns evaluation against targets, baselines, populations, metrics, ablation, incremental contribution and research verdicts. Formal research/promotion references the existing Experiment Registry and specifications; the runtime catalog never replaces them.

The conceptual promotion chain remains candidate definition -> exploratory research -> scientific evaluation -> replication/controls -> promotion decision -> eligible analytical capability. Baselines B0-B4 are scientific comparison material, not a mandatory runtime dependency; a baseline used later as a runtime observable/candidate requires its own declared definition.

Runtime `CandidateEvidence` is not an Evidence Card, Evidence Bundle or Certification. Certification remains downstream, cannot be inherited across instruments/providers, and is never called from the runtime hot path. Technical evaluability, scientific promotion and operational/product permission remain separate gates.

Confluence means coexistence of admissible evidence, not voting. Preserve `EvidenceFamilyId`, `InformationDomainId`, root ancestry and transformation/parameter lineage so redundancy, ablation and incremental contribution can be tested scientifically. Two candidates sharing observations are not automatically independent confirmations; hash inequality is not proof of independence.

```text
UNIVERSAL ÉTEOS SCORE = NOT AUTHORIZED
UNIVERSAL EVIDENCE STRENGTH = NOT DEFINED
GENERIC CONFIDENCE 0-1 = NOT AUTHORIZED
AUTOMATIC EVIDENCE VOTING = NOT AUTHORIZED
```

No weights, score bands, universal probability or BUY/SELL threshold are frozen.

## 10. Hot path, determinism and neutrality

The hot path may perform factual state update, direct pre-resolved dispatch, incremental calculation, candidate evaluation, material `AnalyticalState` revision and compact working-timeline change.

Per observation it must not require Evidence Bundle/Card, Certification, LLM, registry scan, reflection/plugin discovery, full definition/profile copying, legal-policy evaluation, graph reconstruction, remote calls, synchronous persistence or explanation rendering. Invalid configuration should fail during activation. A pre-resolved dependency index may map inputs to affected definitions/scopes without defining its data structure here.

Replay/synthetic semantics are deterministic under frozen inputs, semantic ordering, `availableAt`, definitions, parameters, capability context and code/model state. Wall clock, unseeded random, thread scheduling, default locale/timezone and filesystem/map iteration order are not scientific authority. Window membership/warmup is explicit and point-in-time; centered future windows are prohibited. Duplicate canonical observations do not create duplicate independent evidence.

Logical equality ignores incidental object identity, collection implementation, insertion order, localized labels and non-scientific processing timestamps while distinguishing semantic equality from revision identity. Where source semantics permit, different physical callback order must yield the same governed result; semantically different source ordering remains explicit. Failure of one definition is isolated from unrelated scopes according to declared dependencies, without selecting a failure-domain topology here.

Neutral analytical code does not branch on B3, Nelogica, ProfitDLL, Binary UMDF, WDO, WIN, TEST_INSTRUMENT or synthetic source identity. Provider-native metadata is inaccessible. Provider architectural interchangeability is supported; provider scientific equivalence is not inherited. Generic code does not transfer scientific validity between instruments.

Gap, reconnect, recovery, stale feed, engine failure and operational telemetry are quality/admissibility/control facts, not alpha or market direction. They can make a scope unavailable or not evaluable but cannot create market `CandidateEvidence` without a separately authorized hypothesis/spec/target/baseline.

Structural performance guards are compact references, pre-resolved context, incremental updates, active-scope lifecycle, shared ancestry references, catalog resolution outside the hot path and explicit temporal buffers. Window sizes, retention durations, state capacity, SLOs, queues, brokers, threading, off-heap and latency targets remain deferred pending need and measurement.

## 11. Future synthetic executable proof

The next candidate activity is `MARKET INTELLIGENCE RUNTIME - EXECUTABLE SLICE 1`, requiring separate human authorization. It is limited to deterministic architecture conformance and must use at least two governed synthetic instruments with explicit `TARGET` and `CONTEXT` roles, a synthetic relationship and unmistakably synthetic definitions/proposition. It must not use real hypothesis names, WDO/WIN, provider analytics, Market Data, empirical thresholds, product deployment, alerts or trading semantics.

The future proof must exercise:

1. canonical observation to deterministic `DerivedObservable`;
2. `CandidateEvaluation` to `CandidateEvidence` and `NOT_EVALUABLE(reason)`;
3. simultaneous support and contradiction, explicit neutral evidence, no evidence and inconclusive distinction;
4. stale evidence retained historically but excluded from current contribution;
5. missing capability and stale/unavailable required context causing abstention;
6. exact multi-instrument roles, point-in-time alignment and no event-time-only join;
7. T1 original state/explanation, T2 correction and distinct final-corrected projection without backdating;
8. deterministic `AnalyticalState`, transition, logical timeline and `StructuredWhyNow`;
9. logical equality across replay of the same frozen inputs/configuration;
10. target/outcome blindness and runtime/scientific-evaluation separation.

The correction scenario cascades through `DerivedObservable`, `CandidateEvidence`, `AnalyticalState`, `EvidenceTimeline` and `StructuredWhyNow`; final-corrected revisions are deterministic while the legitimate T1 explanation remains historically available. Logical replay equality covers all six of those runtime products plus `CandidateEvaluation`, using stable semantic ordering rather than collection/provider/thread order.

Adversarial tests must reject contradiction deletion, no-evidence/contradiction conflation, stale contribution, T2 rewriting T1, derived-availability laundering, event-time-only alignment, required-capability bypass, undeclared optional degradation, duplicate-root independence, native access, provider/instrument literals, pattern dispatch, score/trading semantics, uncontrolled time/random/order and control telemetry as market evidence.

After the initial Slice, a new synthetic analytical definition must be addable outside the neutral runtime core using only existing semantics with:

```text
neutral runtime-core production changes = 0
```

If new semantics are genuinely required, the result is `NEW_SEMANTICS_REQUIRED`, followed by explicit authority review. No core change may be hidden in an extension.

## 12. Compatibility, stop conditions and exit gate

This contract is additive and changes no released or scientific material. `research-harness-v1.0.0`, WDO synthetic material, TEST_INSTRUMENT, Canonical Ingestion Slice 1, Evidence V3-V8, Certification V1-V3, schemas, fixtures, Oracles, ExperimentSpecs and known scientific hashes remain unchanged. No Evidence V9 or Certification V4 is justified by runtime conformance.

Future implementation must stop if it requires an unregistered architectural decision, executable/scientific scope beyond its authorization, historical material rewrite, provider/instrument branching, native access, weaker point-in-time/correction semantics, quality/control as evidence, hidden parameters, Evidence/Certification/LLM/persistence in the hot path, unbounded state without lifecycle, rights or provider facts invented, or dependency inversion/cycle.

The likely minimum Slice-1 executable set is `DerivedObservableDefinition`, `DerivedObservable`, `CandidateDefinition`, `CandidateEvaluation`, `CandidateEvidence`, `AnalyticalState`, `AnalyticalStateTransition`, a minimal timeline entry/projection, `StructuredWhyNow`, `RelationshipDefinition`, `AnalyticalDefinitionCatalog` and `AnalyticalExecutionContext`; implementation must consolidate or defer any type not exercised. If `research-analytics` remains justified, its conceptual packages are `.definition`, `.observable`, `.candidate`, `.state`, `.timeline`, `.explanation`, `.relationship` and `.execution`; empty packages/interfaces are prohibited.

Explicitly deferred from Slice 1 are `EvidenceState`, a universal `EvidenceGraph`, generic `RuleEngine`/expression language, ML model registry, prediction/probability/confidence/ÉteosScore, trading signal/alert/recommendation, event store/persistence, LLM orchestration and real candidate libraries.

Executable exit requires every created type to be exercised by a conformance path or invariant; focused unit, adversarial and architecture tests; the full synthetic chain; correction, contradiction, abstention, multi-instrument, replay and extension proofs; applicable historical/material validators; and the repository-authoritative clean Maven verification with zero failures, errors or skipped tests. Exact implementation types and the `research-analytics` module remain subject to revalidation and separate authorization.

Decisions deferred include real definitions/candidates/relationships, empirical dimensions/formulas/thresholds/weights/windows, universal evidence strength/confidence/probability, scientific promotion vocabulary, deployment governance, prediction, provider/data/rights, persistence, UI/API, alerts, LLM orchestration, physical topology, state capacities, performance budgets and WIN.

The Anticipatory authority's former use of “Market State” for an interpretation was a non-blocking terminology defect. It is resolved by preserving factual `MarketState` and using `AnalyticalState`/`AnalyticalStateTransition` for interpretation. This is not a scientific-result change and does not affect historical Evidence or Certification.

```text
ANTICIPATORY_MARKET_INTELLIGENCE_DEFECT =
FOUND / NON-BLOCKING / TERMINOLOGY / RESOLVED
```
