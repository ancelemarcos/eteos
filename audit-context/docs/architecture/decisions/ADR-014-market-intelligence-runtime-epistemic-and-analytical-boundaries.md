# ADR-014 - Market Intelligence Runtime Epistemic and Analytical Boundaries

**Status:** ACCEPTED
**Date:** 2026-09-05
**Decision scope:** epistemic layers, analytical definitions/evidence/state, point-in-time derivation, explanation and neutral runtime ownership
**Implementation authorization:** CONTRACT MATERIALIZED; EXECUTABLE IMPLEMENTATION NOT AUTHORIZED
**Supersedes:** None
**Superseded by:** None

## 1. Context

ADR-006 reserves `MarketState` for factual current/as-known market knowledge. ADR-007 separates quantitative measurement from interpretation. ADR-008 assigns interpretation and structured evidence to `AnalyticalState`; ADR-009 assigns material event creation to Event Engine. ADR-013 now provides canonical observations, compact lineage/context, capability admission, corrections and point-in-time foundations.

The remaining architectural question is how Éteos turns admissible canonical knowledge into structured analytical intelligence without confusing measurement, evidence, conclusion, prediction, recommendation, quality or retrospective narrative. The Anticipatory authority also used “Market State” once for interpretation, conflicting terminologically with the canonical vocabulary. The detailed normative contract is `../MARKET-INTELLIGENCE-RUNTIME-CONTRACTS.md`.

## 2. Decision

DataMarket adopts these boundaries:

1. `MarketState` remains factual; `AnalyticalState` is the point-in-time interpretation of admissible analytical evidence. No second analytical `MarketState` or cross-layer megaobject is permitted.
2. Observation, `DerivedObservable`, `CandidateEvidence`, analytical conclusion, prediction and trading recommendation are distinct epistemic layers with no automatic promotion.
3. Feature Engine produces deterministic/versioned `DerivedObservable` measurements. Candidate evaluation returns `CandidateEvidence` or explicit `NOT_EVALUABLE(reason)`; missing is never null, zero or neutral evidence.
4. Support, contradiction, neutral, inconclusive, freshness, evaluation availability, lifecycle and abstention remain orthogonal. Support and contradiction may coexist; `NO_ANALYTICAL_CONCLUSION` is first-class. A separate `EvidenceState` is not required in the first Slice.
5. One immutable physical analytical-definition catalog exposes typed definitions for derived observables, candidate evidence and relationships. Identity/version lookup is exact, activation is explicit and material parameters are versioned.
6. Every required input must be available by `decisionTime`; derived availability cannot precede required-input availability. Cross-instrument alignment uses admissible point-in-time inputs. Corrections preserve `AS_KNOWN_AT(t)` separately from `FINAL_CORRECTED`; retrospective onset never backdates detection.
7. `EvidenceTimeline` is governed logical analytical history; a bounded/compacted runtime working projection is separate. `StructuredWhyNow` is a deterministic projection that creates no evidence. LLM rendering is downstream and non-authoritative.
8. Runtime candidate evaluation remains target-blind and separate from scientific target/baseline/incrementality evaluation, Evidence Bundles/Cards and Certification. Analytical transitions remain separate from Derived Market Events and alerts.
9. No universal Éteos score, evidence strength, 0-1 confidence, voting, probability or trading semantics are accepted. Confluence preserves family/domain/ancestry for later scientific ablation and incremental evaluation.
10. Runtime execution uses immutable pre-resolved contexts, compact references, controlled time and provider/instrument-neutral dispatch. Quality/control facts may constrain admissibility but are not market evidence.
11. The preferred future ownership boundary is one `research-analytics` module, revalidated before implementation and never created by this checkpoint. Source/semantic foundations do not depend on analytics, and analytics cannot access native provider metadata.
12. The first executable Slice, if separately authorized, is deterministic synthetic architecture conformance covering the complete chain, contradiction, abstention, multi-instrument roles, corrections, timeline, Why Now, replay and a later zero-neutral-core-change definition extension.

## 3. Rejected alternatives

Rejected:

- analytical `MarketState` as a second meaning or universal megaobject;
- derived measurement as automatic evidence;
- null/zero/empty as non-evaluation;
- universal EvidenceState/EvidenceGraph, score, confidence or voting;
- last-evidence-wins or retrospective contradiction removal;
- event-time-only cross-market joins and correction backdating;
- generic object registries, expression/rule engines, plugin discovery or graph databases for Slice 1;
- per-observation registry scans, legal evaluation, full-profile copies, Evidence Bundles, LLM or synchronous persistence;
- provider/instrument/string-pattern dispatch;
- runtime self-promotion, self-certification or target/outcome access.

## 4. Consequences

Positive consequences include explicit epistemic accountability, deterministic replay, point-in-time auditability, preserved contradiction, provider/instrument neutrality, explainability from governed facts and enough lineage for later ablation/incrementality work.

Costs include more explicit identities, definitions, revisions, lineage and activation validation; lifecycle policies for working state/timeline; and a deliberate boundary between runtime evidence and scientific evidence. Exact representations and performance must be validated by the future Slice rather than inferred from documentation.

The non-blocking Anticipatory terminology defect is resolved: interpretive uses are `AnalyticalState`/`AnalyticalStateTransition`, while factual `MarketState` remains unchanged. This reconciliation changes no scientific claim.

## 5. Compatibility

This decision is post-v1 and additive. It does not change `research-harness-v1.0.0`, WDO synthetic material, TEST_INSTRUMENT, Canonical Ingestion Slice 1, Evidence V3-V8, Certification V1-V3, schemas, fixtures, Oracles, ExperimentSpecs or known scientific hashes. It creates no Evidence V9 or Certification V4 and transfers no certification between instruments or providers.

DM-2 source/dataset qualification remains incomplete. Real provider adapters, Market Data, DM-3A, Anticipatory Research and WIN remain unauthorized/not started as applicable.

## 6. Deferred decisions

Deferred are exact Java/API representations, physical module creation, evidence/analytical taxonomies beyond the minimum boundaries, real features/candidates/relationships, formulas, thresholds, weights, windows, expiry/retention durations, confidence/probability, prediction, deployment/promotion mechanisms, persistence/event store, UI/API, LLM orchestration, provider/data/rights, threading/queues/brokers/off-heap, capacities, latency/SLOs and production topology.

The next candidate activity is `MARKET INTELLIGENCE RUNTIME - EXECUTABLE SLICE 1`. This recommendation does not authorize it.
