# DataMarket / Éteos - Canonical Market Ingestion and Capability Contracts

**Status:** ACCEPTED / MATERIALIZED
**Scope:** post-v1 provider-neutral ingestion, information preservation, capability qualification and admission boundaries
**Executable implementation:** SLICE 1 IMPLEMENTED / VALIDATED - SYNTHETIC CONFORMANCE ONLY
**Last updated:** 2026-09-05

---

## 1. Purpose and authority

This document governs how DataMarket may transform heterogeneous source observations into provider-neutral market semantics without erasing useful qualified information, inventing unavailable facts or allowing provider-native contracts to become scientific APIs.

It specializes, without superseding:

- `DOMAIN-LANGUAGE.md` and ADR-005 for canonical names, event and time semantics;
- `INSTRUMENT-IDENTITY-AND-RESOLUTION-CONTRACTS.md` for `InstrumentId`, definitions, mappings and admission;
- ADR-011 and `../research/DATASET-POLICY.md` for immutable datasets, replay, corrections and retention;
- ADR-012 for Provider Adapter, capability, source epoch, gap and recovery boundaries;
- `../market-data/DM-2-SOURCE-AND-RIGHTS-QUALIFICATION-CONTRACTS.md` for source, semantic, technical, rights and fit-for-purpose qualification;
- `../research/ANTICIPATORY-MARKET-INTELLIGENCE-CONTRACTS.md` for scientific point-in-time admissibility and anti-laundering;
- `../research/CURRENT-RESEARCH-CONTRACTS.md` for the released Research Harness and historical scientific contracts.

Authority ownership remains separate:

| Authority | Owns |
| --- | --- |
| Instrument Identity | canonical instrument identity, definitions and point-in-time mapping/resolution |
| DM-2 | source/product/dataset semantics, technical validation, rights and purpose qualification |
| This contract | canonical/native separation, preservation, normalization and runtime admission boundaries |
| Anticipatory contracts | scientific availability, decision-time and anti-laundering requirements |
| Dataset Policy | scientific dataset assembly, immutability, lineage and certification governance |
| Research Harness | historical scientific execution, Evidence and Certification contracts |

## 2. Governing principles

DataMarket shall normalize semantics, not erase information. Provider-specific observations remain confined to governed source boundaries; qualified market semantics are projected into provider-neutral canonical contracts; useful additional source facts retain lawful lineage where needed; scientific consumers may use only explicitly qualified capabilities.

The following invariants are accepted:

1. **The first provider must not become the ontology of DataMarket.** ProfitDLL, Binary UMDF or any future first provider cannot define the neutral model merely by arriving first. A new source exposing already governed semantics targets zero neutral-core change.
2. **Provider-neutral is not provider-poor.** A richer source is not reduced to a sparse source's information ceiling, and a sparse source does not fabricate richer facts.
3. **Absence is not information.** Missing does not become zero, false, neutral, generated market sequence, placeholder identity or synthetic instrument.
4. **More fields do not imply more capability.** Capability requires technical availability, semantic qualification, scope/version, entitlement, rights and current admissibility.
5. **Provider interchangeability is architectural; provider equivalence is scientific and not inherited.** A common API is not evidence of equivalent information.
6. **Instrument independence is architectural; scientific transfer is not inherited.** A new `InstrumentId` with existing semantics targets zero neutral algorithm change, but needs its own applicable evidence.
7. **Point-in-time and final corrected truth answer different questions.** Both must remain reconstructable when the declared purpose requires them.
8. **Recovered current state is not complete event history.** Recovery cannot erase a known history gap.
9. **Technical support, semantic qualification, rights, quality and scientific fitness are independent gates.** No gate promotes another implicitly.
10. **Rights constrain preservation and use; they do not redefine market truth.**

Lossless-first means preserving qualified or legitimately useful source information required for authorized purposes. It does not require retaining every provider byte, copying every field into canonical events, preserving arbitrary metadata indefinitely or exposing unknown semantics to science. Preservation remains purpose- and rights-bound.

## 3. Semantic ownership planes

The architecture has three logical ownership planes:

- **Reference plane:** `InstrumentDefinition`, provider mappings and versioned source, capability, normalization, temporal and rights-policy references.
- **Data plane:** immutable provider-neutral canonical market observations.
- **Control plane:** gaps, recovery, source/connection health, mapping failures, rejections, conflicts and capability/quality state.

These planes are semantic ownership boundaries. They do not require three services, modules, processes, threads, databases or deployables.

Reference authority is explicit: canonical instrument definition and mapping authority remain separate from source-event observation, and originating market authority remains distinct from delivery provider. A provider assertion does not promote a timestamp, sequence, identity or status to exchange-authoritative semantics.

Gap, reconnect, stale feed, recovery, transport loss and normalization failure are control/quality facts. They are not liquidity withdrawal, absorption, exhaustion, pressure, market inactivity or another market interpretation without an independently governed hypothesis.

## 4. Canonical and native boundary

Provider acquisition, SDK objects, callback structures and wire DTOs remain at the provider edge. Source interpretation converts them into governed source facts. Exact approved instrument resolution occurs before trusted canonical admission. Normalization projects only qualified semantics into provider-neutral event families.

Provider DTOs, SDK types and source-native metadata must not become scientific interfaces. Canonical extensibility must not use `Map<String,Object>`, `Map<String,String>` or arbitrary JSON blobs. If a useful native fact is retained, it must be namespaced, schema/version scoped, governed, rights-aware, non-scientific by default and structurally inaccessible to neutral scientific consumers.

A source-native fact is promoted only when all of the following exist:

- native semantic authority;
- canonical semantic definition;
- deterministic normalization rule where claimed;
- applicable source/schema/scope and version;
- semantic qualification and capability identity;
- explicit failure behavior.

Field-name or numeric-value similarity is insufficient.

Normalization is typed, provider-neutral in output semantics, deterministic where declared, versioned and loss-audited. A material semantic or structural transformation change requires a new normalization version; applicable replay and dataset lineage preserve that version. Reprocessing must declare whether it preserves or transforms prior semantics, and matching normalization versions do not establish equivalent source inputs.

Source acquisition owns native transport and decoding; normalization owns qualified semantic projection; admission owns purpose-specific gates; science consumes admitted canonical observations. Source/ingestion packages must not depend on future Market Intelligence semantics, and scientific code must not depend on provider adapters or native metadata.

## 5. SourceLineage and ObservationContext

`SourceLineage` is the logical provenance needed to recover, where applicable:

- originating market authority and delivery provider as distinct identities;
- product, feed or source profile;
- source mode and source epoch;
- native instrument reference;
- mapping and `InstrumentDefinition` versions;
- native event identity;
- normalization version;
- capture or dataset context.

`ObservationContext` is the logical set of event-specific governed facts plus references to shared immutable context, including applicable lineage, temporal, ordering, quality, correction and admission context.

Neither concept requires a monolithic object duplicated inside each event. Hot-path representations should carry event-specific facts and compact immutable IDs/references sufficient to recover shared context. Full definitions, capability profiles, rights profiles, URLs, qualification evidence, prose and large metadata containers must not be copied per event.

## 6. Temporal semantics

Applicable temporal identities remain distinct:

| Identity | Meaning |
| --- | --- |
| `eventTime` | best qualified time of the underlying market/economic event |
| exchange/aggressor time | source-defined event-specific time only when separately qualified |
| provider receive time | provider-boundary receipt fact |
| `providerSendTime` | provider/exchange publication or send fact when semantics match |
| `ingestionTime` | earliest controlled DataMarket receipt point for live/shadow use |
| historical record time | archive, record or backfill time with its exact authority |
| correction availability | when corrected information became available |
| `availableAt` | earliest defensible scientific availability under a versioned policy |
| `processingTime` | operational time of a defined DataMarket processing stage |

No source must provide every clock. A missing clock remains missing and is never silently replaced by another. Numeric equality does not collapse temporal identity.

`availableAt` remains a governed DataMarket scientific fact. Provider timestamps may contribute to its derivation but never become `availableAt` automatically. Anticipatory use requires a defensible policy bound to the applicable source/product/dataset version. Derived information obeys:

```text
derivedAvailableAt >= max(requiredInput.availableAt)
```

plus any declared computation semantics. Historical replay does not assign current wall-clock time or backdate later corrections.

## 7. Identity, ordering and corrections

Event identity is distinct from ordering. Applicable ordering domains include trade order, report sequence, instrument sequence, packet/channel sequence, book sequence and internal processing sequence. Each source sequence requires its semantic authority and scope and, where applicable, source epoch and reset/wrap behavior. Callback, thread, file-row and database insertion order are not market-order evidence.

Canonical correction handling follows append plus explicit reference/supersession lineage. A later correction, cancellation or bust-like action retains its own availability and does not mutate or backdate the original observation. Governed projections must be capable of distinguishing:

```text
AS_KNOWN_AT(t)
FINAL_CORRECTED
```

A generic source edit indicator does not automatically mean `BUST`, `CANCEL`, `CORRECT` or `SUPERSEDE`. It remains native/unqualified until its action and timing are qualified.

## 8. Quality, recovery and completeness

Quality is multidimensional. Implementations must preserve applicable distinctions among validity, composable quality flags, freshness, gaps, out-of-order observations, duplicates, recovery, history completeness, coverage and source health. They must reuse canonical `DataValidity`, `DataQuality`, `DataQualityFlag` and `FreshnessState` concepts where their semantics match rather than introduce overlapping generic states.

Recovery may restore a valid current state while event history remains incomplete. Consumers requiring complete event history must reject, abstain or use an explicitly allowed incomplete-history policy; they may not infer completeness from a successful snapshot.

Silence is interpretable as inactivity only under a qualified coverage/completeness contract. Provider request completion does not establish dataset completeness.

## 9. Event-family direction

Canonical events use typed families or composition when semantics differ materially. `CanonicalMarketEvent` may evolve additively as a root contract but must not become one universal provider-shaped event with dozens of nullable fields.

The justified direction includes Trade, source/control/quality observations, book semantics with explicit fidelity, market status/session and reference data. The first executable proof should use Trade plus only the richer/control semantics needed to exercise this contract. Participant, macro and news semantics remain deferred. Derived intelligence is downstream and never a source observation.

## 10. Capability and consumer contract

A capability is a governed semantic contract, not a field-presence boolean or provider score. The currently justified conceptual vocabulary covers:

- Trade core;
- external/deterministic event identity;
- ordering by named domain;
- qualified `availableAt`;
- observed trade side versus provider-derived trade side;
- corrections with a declared action set;
- book with explicit TOB/MBP/MBO fidelity and delivery semantics;
- gap/recovery;
- market status;
- participant identity as a deferred, separately qualified domain.

This list freezes semantic distinctions, not Java enum constants or an obligation to implement every item in Slice 1.

A versioned capability profile may bind capability identity and definition, minimum facts, provider/source/product/mode/schema, dataset or instrument scope when material, effective interval, provenance, evidence, limitations and requalification triggers.

Authority flows as follows:

```text
adapter -> reports technical observation/support
DM-2 -> qualifies semantic meaning and scope
rights authority -> authorizes use for a purpose
runtime -> resolves the approved context
```

An adapter cannot self-certify. Effective capability is the purpose-specific intersection of technical availability, semantic qualification, entitlement, rights and current quality/admissibility. The underlying dimensions remain visible for audit; they are not collapsed into a permanent source boolean.

Consumers declare required and optional capabilities, accepted fidelity, temporal requirements, quality/coverage requirements and purpose. A missing optional capability causes explicit bounded degradation. A missing or unqualified required capability produces `NOT_EVALUABLE`, rejection or abstention according to the consumer contract. No placeholder is synthesized.

## 11. Rights and purpose-specific admission

Observation facts are immutable; admissibility is contextual. The same observation may be admitted for target characterization, rejected for anticipatory research because its availability is not sufficiently qualified, and prohibited for external display by rights.

An approved rights profile or equivalent governs transient processing, native retention, canonical retention, research, replay, display and API/publication independently. Scientific algorithms consume inputs admitted for their declared purpose; they do not parse legal prose or elevate permissions.

If native retention is prohibited but canonical retention is allowed, the source boundary may normalize transiently and retain only authorized canonical facts plus lawful non-reconstructive lineage. If all retention is prohibited, the observation may participate only in an authorized transient path and cannot become a retained dataset. Internal use never implies external publication.

## 12. Source modes, multiple providers and datasets

Source mode is independent of provider. The conceptual modes are `LIVE`, `HISTORICAL_DATASET`, `CAPTURE_REPLAY` and `SYNTHETIC`. Historical and live profiles for one logical source may differ; class equality does not establish clock, coverage, correction or capability equivalence.

Two providers observing the same `InstrumentId` remain distinct observations through lineage. Cross-provider deduplication and reconciliation are not defaults. Conflicts retain both attributable observations and become explicit control/diagnostic state; implicit provider priority, latest arrival, lowest latency and majority are prohibited.

A provider switch changes source, capability, temporal, ordering, quality and limitation context while the canonical instrument may remain stable. Continuation is allowed only if the consumer's requirements remain satisfied. Scientific equivalence is not inherited.

Capture is not a frozen `DatasetVersion`, and provider replay is not DataMarket scientific replay. Dataset assembly remains governed by Dataset Policy and requires normalized observations, lineage, coverage, correction/ordering policies, mapping/definition versions, integrity and rights sufficient for its purpose.

## 13. Operational boundaries

Provider/native buffers remain provider- or adapter-owned until explicit safe decoding, copying or ownership transfer. Canonical observations must not retain references to mutable provider callback buffers. Callback or thread schedule is not a scientific ordering authority. Slice 1 must also avoid per-event registry scans where pre-resolution is possible, full context copies, arbitrary maps and per-event rights-policy or evidence-prose interpretation.

Silent loss under backpressure is prohibited. Any loss becomes explicit quality, gap, coverage or source-health information. Queue technology, concurrency topology, capacities, threading, batching, zero-copy, off-heap design, latency targets and storage technology remain deferred until representative facts exist.

Future operational metrics may include received, parsed, normalized, admitted, rejected, unresolved, ambiguous, duplicate, out-of-order, gap, correction, rights-rejected, capability-rejected and processing latency. Operational metrics are not automatically scientific observables.

Failures such as unknown instrument, ambiguous mapping, unsupported semantic version, invalid timestamp, ordering conflict, missing/unqualified capability, rights rejection and quality inadmissibility require typed failure or rejection. Operational failure never becomes a market observation.

## 14. Synthetic conformance contract

The first executable slice, if separately authorized, uses neutral synthetic material only:

| Source | Mode and semantics | Purpose |
| --- | --- | --- |
| `SYNTH_SOURCE_SPARSE@1` | historical Trade core, deterministic event identity, `eventTime`, one qualified trade-order domain and declared coverage; no side, participant, book, correction or publication clock | prove sparse admission without invention; transient/canonical retention allowed, native retention/display denied |
| `SYNTH_SOURCE_RICH@1` | historical Trade plus native identity, qualified observed side, distinct provider receive/send clocks, trade and packet orders, and one lawful useful native fact not qualified for science | prove richer preservation and canonical/native isolation |
| `SYNTH_SOURCE_CORRECTING@1` | capture/replay Trade, qualified side, lightweight book-lifecycle proof, append correction, gap, snapshot recovery, multiple epochs and clocks | prove correction, recovery, incomplete history and transient-only rights; it models no real provider |
| `SYNTH_SOURCE_D` | added only after A/B/C using existing governed semantics | prove zero neutral-core production change |

Synthetic consumers equivalent to `TRADE_ONLY_CONSUMER`, `SIGNED_FLOW_CONSUMER` and `BOOK_LIFECYCLE_CONSUMER` declare capabilities and purpose; they are conformance probes, not strategies. Expected compatibility is:

| Consumer | Sparse A | Rich B | Correcting C |
| --- | --- | --- | --- |
| Trade-only | admitted | admitted | technically admitted subject to purpose/rights |
| Signed-flow | rejected: required fact absent | admitted | technically admitted subject to purpose/rights |
| Book lifecycle | rejected: required fact absent | rejected: required fact absent | technically admitted, with gap/history constraints |

At least two neutral synthetic instruments, equivalent to `SYNTH_INSTRUMENT_ALPHA` and `SYNTH_INSTRUMENT_BETA`, use distinct definitions such as different price scale/tick characteristics. Beta is added after the neutral machinery and requires zero neutral ingestion/core algorithm changes. Neither identity represents WDO, WIN or a provider.

Every source fact is machine-checkably classified as applicable: `CANONICALIZED`, `SOURCE_LINEAGE`, `CONTROL_QUALITY`, `UNQUALIFIED_NATIVE`, `INTENTIONALLY_DROPPED`, `TRANSIENT_ONLY_BY_RIGHTS` or `UNSUPPORTED`. Every intentionally dropped useful-looking fact requires a reason.

Required adversarial cases include semantic, temporal, ordering and identity collisions; unavailable-information defaults; false capability/MBO promotion; qualification, rights, quality and purpose bypass; correction backdating; gap/recovery history laundering; provider version drift; source conflict/switch; and historical/live fake equivalence. Each attack fails closed or preserves the declared limitation.

Synthetic conformance validates architecture only. It makes no provider-performance, latency, real-market capability, predictive, causal or scientific-equivalence claim.

## 15. Historical compatibility and defect disposition

This foundation is additive. `research-harness-v1.0.0`, which peels to `d400ed9ab049aa4f7a887113b4de646bf2d1e40e`, WDO synthetic material, the TEST_INSTRUMENT proof, Evidence V3-V8, Certification V1-V3, historical schemas, ExperimentSpecs, Oracles and scientific hashes remain immutable. Historical adapters or in-memory wrappers are preferred to rewriting frozen material.

The accepted reconciliation found no released-v1 canonical-ingestion defect, Multi-Instrument foundation defect, Instrument Identity foundation defect, Anticipatory foundation defect or DM-2 qualification foundation defect. Those verdicts are not reopened without new contradictory evidence.

```text
RELEASED_V1_CANONICAL_INGESTION_DEFECT = NOT FOUND
MULTI_INSTRUMENT_FOUNDATION_DEFECT = NOT FOUND
INSTRUMENT_IDENTITY_FOUNDATION_DEFECT = NOT FOUND
ANTICIPATORY_FOUNDATION_DEFECT = NOT FOUND
DM2_QUALIFICATION_FOUNDATION_DEFECT = NOT FOUND
```

## 16. Slice 1 entry, scope and stop conditions

Slice 1 requires separate human authorization. It may prove only the minimum contracts exercised by a Slice-1 production path, conformance test, adversarial test or necessary architecture boundary; an executable type outside those uses must not be created. It should reuse existing modules; a new Maven module requires stopping and reporting a genuine dependency-cycle or ownership need before creation.

The outcome must prove:

1. sparse Trade admission without fabricated semantics;
2. preservation of richer qualified facts;
3. structural isolation of one useful unqualified native fact;
4. distinct temporal and ordering domains;
5. append correction with point-in-time/final projections;
6. recovered state without false history completeness;
7. qualification authority independent of adapter declaration;
8. independent rights and purpose decisions;
9. a second synthetic instrument with zero neutral algorithm changes;
10. Source D with zero neutral-core production changes.

The implementation must stop if it requires rewriting historical scientific material, provider-specific semantics in neutral core, incompatible `InstrumentId` change, weaker `availableAt`, bypass of DM-2 or rights, invented provider behavior or real instrument identity, or Evidence/Certification change without independent scientific need.

The existing Research Harness remains a scientific laboratory. Synthetic conformance may execute inside its current modules, but Slice 1 must not turn the historical Harness into a production provider runtime; any later extraction to production modules or services requires separate architectural authority.

Executable exit requires focused unit, synthetic conformance, adversarial and architecture tests; historical regressions; applicable material validators; and the repository-authoritative clean Maven verification with zero failures, errors or skipped tests. Architecture tests must prohibit provider SDK/name dependencies, instrument literals, scientific access to native metadata, provider-switch dispatch in analytical code, governed wall-clock use and reverse core-to-adapter dependencies.

## 17. Deferred and prohibited scope

This contract does not authorize a real provider adapter, provider/source selection, real WDO/WIN identity, Market Data acquisition, real capability/right profile, dataset, DM-3A, anticipatory research, Market Intelligence Runtime executable implementation, production book/session engine, participant model, persistence, message bus, cross-provider reconciler, rollover or release.

It does not select Kafka, RabbitMQ, Aeron, Chronicle, Disruptor, database/object storage, serializer, queue, thread pool, batch size, zero-copy/off-heap framework, latency target or SLO.

Do not create a `UniversalProvider`, universal nullable market mega-event, `GenericSequence`, `GenericTimestamp`, provider plugin framework, capability/provider score, `MarketDataRepository`, `MarketDataBus`, `UniversalBook`, `ParticipantMaster`, `CrossProviderReconciler`, `RolloverEngine`, `MarketDataPersistence` or `LatencyOptimizer` under this authority.

DM-2 external qualification may progress independently, including the pending B3 response and any future Nelogica qualification; neither response is assumed, fabricated or required to materialize this synthetic-first contract. Missing real-provider facts do not block the synthetic foundation, but real adapter, real dataset and DM-3A remain blocked until their applicable DM-2 gates and separate authorizations pass.

`MARKET-INTELLIGENCE-RUNTIME-CONTRACTS.md` is now the materialized future-consumer contract after this foundation. The implemented synthetic Slice 1 proves its bounded architectural prerequisites; it does not authorize runtime implementation, a provider or data acquisition.

CANONICAL MARKET INGESTION & CAPABILITY CONTRACT =
MATERIALIZED

EXECUTABLE IMPLEMENTATION =
SLICE 1 IMPLEMENTED / VALIDATED - SYNTHETIC CONFORMANCE ONLY
