# ADR-013 - Canonical Market Ingestion and Capability Boundaries

**Status:** ACCEPTED
**Date:** 2026-09-05
**Decision scope:** provider-neutral normalization, canonical/native separation, information preservation, lineage, capability authority, purpose admission, correction and quality boundaries
**Implementation authorization:** NOT GRANTED BY THIS CHECKPOINT
**Supersedes:** None
**Superseded by:** None

---

## 1. Context

ADR-005 established typed canonical events and distinct time/ordering semantics. ADR-011 established point-in-time dataset and replay constraints. ADR-012 established Provider Adapters, capability-driven integration, source epochs, gaps and recovery. Instrument Identity later materialized exact provider-to-canonical resolution, and DM-2 materialized purpose-specific source, semantic, technical and rights qualification.

The remaining architectural question is how sparse and rich providers can target one neutral domain without either erasing qualified richness or fabricating semantics that a sparse source does not possess. The current Research Harness event slice is intentionally synthetic and narrow; it is historical compatibility input, not the ontology for real ingestion.

The detailed normative contract is `../CANONICAL-MARKET-INGESTION-AND-CAPABILITY-CONTRACTS.md`.

## 2. Decision

DataMarket will use a governed canonical ingestion boundary with these rules:

1. Provider acquisition and native semantics remain behind Provider Adapters/source boundaries.
2. Only qualified semantics are projected into provider-neutral typed event families.
3. Useful native facts may retain lawful, versioned lineage but are non-scientific by default and inaccessible to neutral scientific consumers.
4. Provider-neutral does not mean lowest common denominator: rich facts remain available through qualified capabilities, while missing facts remain absent.
5. Source lineage and observation context are logical models that permit compact immutable references; full profiles, definitions, rights and evidence are not duplicated per event.
6. Temporal identities, event identity and ordering domains remain distinct. `availableAt` remains a DataMarket scientific fact governed by versioned policy.
7. Corrections are append/reference/supersession facts capable of point-in-time and final-corrected projection; silent overwrite and correction backdating are prohibited.
8. Validity, quality flags, freshness, gaps, recovery, history completeness, coverage and source health remain orthogonal where their meanings differ.
9. Capability is scoped, versioned and purpose-specific. Adapters report technical support; DM-2 qualifies semantics; rights authority permits uses; runtime resolves effective capability with current quality/admissibility.
10. Multiple providers observing one `InstrumentId` remain attributable. Switch/failover does not inherit scientific equivalence, and cross-provider reconciliation is not implicit.
11. Rights constrain processing, retention and publication without changing semantic truth.
12. First executable proof is synthetic, additive and must demonstrate rich/sparse behavior, canonical/native isolation, time/order distinctions, corrections, recovery/history, purpose/rights, two instruments and a post-architecture Source D with zero neutral-core production changes.

The first provider must not become the ontology of DataMarket. A new provider with existing governed semantics and a new instrument with existing semantics both target zero neutral-core algorithm change.

## 3. Consequences

Positive consequences:

- provider and instrument lock-in are reduced;
- sparse providers remain usable for compatible consumers without invention;
- richer qualified information is not globally erased;
- scientific consumers receive qualified semantics rather than native SDK contracts;
- provider substitution and historical/live comparison can be evaluated explicitly;
- point-in-time, correction, quality and rights limitations remain auditable.

Costs:

- more explicit semantic identities and qualification/profile governance;
- additional lineage and admission context;
- deliberate onboarding and requalification after semantic/version changes;
- compact shared-context lifecycle and lookup must be designed carefully for the hot path;
- common Java types alone cannot prove scientific equivalence.

The reference/data/control planes are logical ownership only. This ADR does not mandate three services, modules, threads or databases. It preserves future efficient implementation by allowing pre-resolved contexts and compact references rather than requiring monolithic per-event envelopes.

## 4. Compatibility

The decision is post-v1 and additive. `research-harness-v1.0.0`, WDO synthetic material, TEST_INSTRUMENT, Evidence V3-V8, Certification V1-V3, historical schemas, ExperimentSpecs, Oracles and hashes remain unchanged. Existing `SyntheticTradeEvent` and fixture contracts may be wrapped or adapted in memory but are not rewritten.

Provider architecture and scientific equivalence remain separate. Instrument architecture and scientific transfer remain separate. The reconciliation identified no blocking structural or scientific defect in Released V1, Multi-Instrument, Instrument Identity, Anticipatory or DM-2 foundations. ADR-014 later records and resolves a non-scientific Anticipatory terminology defect: interpretive `Market State` is canonicalized as `AnalyticalState` while factual `MarketState` remains unchanged.

## 5. Rejected alternatives

Rejected:

- provider-shaped canonical core;
- lowest-common-denominator canonical core;
- universal nullable market mega-event;
- arbitrary maps or JSON as scientific extensibility;
- one generic timestamp or sequence;
- adapter self-certification;
- permanent `trusted=true` or boolean capability sets;
- silent correction overwrite;
- provider switch as scientific equivalence;
- raw-retention assumption;
- provider priority, arrival time or majority as implicit cross-source truth.

## 6. Deferred decisions

Deferred are exact Java type names, physical module extraction, provider adapters and products, production IDs, real capability/right profiles, storage, serialization, queue/concurrency technology, capacities, backpressure mechanics, performance/SLO values, book/session production models, cross-provider reconciliation, rollover, Market Intelligence Runtime executable implementation and all empirical/scientific claims.

No Market Intelligence Runtime executable architecture, real provider, real Market Data, DM-3A, anticipatory research, WIN or release is authorized by this ADR checkpoint.
