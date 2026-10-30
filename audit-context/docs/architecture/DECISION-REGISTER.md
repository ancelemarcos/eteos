# DataMarket — Decision Register

**Document:** `docs/architecture/DECISION-REGISTER.md`  
**Status:** ACCEPTED  
**Scope:** Implementation-facing index of architectural decisions  
**Last updated:** 2026-09-08

---

## 1. Purpose

Accepted ADRs contain context, alternatives, accepted decisions and intentionally unresolved items. This register prevents an implementation agent from interpreting the status of an entire ADR as approval for every option discussed inside it.

This register does not supersede an ADR. If this register and an ADR conflict, the ADR is authoritative and this register must be corrected.

Decision status uses the canonical documentation statuses in `DOMAIN-LANGUAGE.md`: `ACCEPTED`, `PROPOSED`, `EXPERIMENTAL`, `HYPOTHESIS`, and `PENDING`. `BENCHMARK_REQUIRED`, `RESEARCH_REQUIRED`, provider/B3/licensing dependencies and gate names are blockers or readiness metadata; they are not decision statuses and never promote a decision to `ACCEPTED`.

## 2. Normative Rule

This register is **normative and exhaustive for implementation-authorizing architectural decisions**. An accepted ADR may contain context, constraints, rationale, rejected alternatives and accepted principles that have not yet been catalogued here. **If an architectural choice would authorize concrete implementation behavior and it has no Decision ID in this register, it must be catalogued before implementation begins.** Absence from this register is therefore not permission to implement.

The governing ADR remains the authoritative source for meaning and rationale. The register is the implementation authorization index. If the two conflict, stop, correct the register or resolve the architectural conflict; do not choose whichever wording is convenient.

Before implementing a significant architectural choice:

1. identify the governing ADR;
2. locate the decision in this register;
3. implement only `ACCEPTED` behavior unless the current task explicitly authorizes an experiment/research activity;
4. do not choose among `PROPOSED` or `PENDING` alternatives merely to complete a task;
5. update this register when a new ADR changes decision status.

## 3. Current Register

| ID | ADR | Decision | Status | Implementation note |
| --- | --- | --- | --- | --- |
| D001-001 | ADR-001 | Java/JVM is the primary backend/runtime | ACCEPTED | Initial target is Java 21 or newer supported LTS; exact distribution/version remains pre-scaffold configuration. |
| D001-002 | ADR-001 | Analytical core remains executable independently of application framework | ACCEPTED | Do not introduce Spring into core domain packages. |
| D001-003 | ADR-001 | Python is research/exploration tooling, not the production real-time core | ACCEPTED | Production quantitative semantics must remain reproducible in the Java core. |
| D001-004 | ADR-001 | Rust/native rewrite requires measured evidence | ACCEPTED | Do not introduce a second production language for theoretical performance. |
| D002-001 | ADR-002 | Initial topology is a modular monolith | ACCEPTED | Logical boundaries do not imply network services. |
| D002-002 | ADR-002 | Hot-path analytical interactions are in-process initially | ACCEPTED | Avoid premature microservices. |
| D002-003 | ADR-002 | Research/replay may run as a separate executable while sharing analytical libraries | ACCEPTED | Preserve semantic parity. |
| D003-001 | ADR-003 | Spring Boot is the application/integration shell | ACCEPTED | Bootstrap, configuration, REST, security boundary, health and infrastructure integration. |
| D003-002 | ADR-003 | Spring APIs, Spring Events, `@Async`, ORM and per-tick transactions are not analytical hot-path mechanisms | ACCEPTED | Enforce with architecture-conformance tests once code exists. |
| D003-003 | ADR-003 | Spring MVC/WebFlux choice for suitable external I/O remains workload-specific | PENDING | No option is currently preferred; decide from workload evidence before the relevant external I/O implementation is frozen. |
| D004-001 | ADR-004 | Mutable analytical state uses controlled ownership/single-writer where practical | ACCEPTED | Add deterministic partitioning only when measured scaling requires it. |
| D004-002 | ADR-004 | Asynchronous boundaries are bounded and observable | ACCEPTED | Queue age and depth are first-class metrics. |
| D004-003 | ADR-004 | LMAX Disruptor/JCTools/exact queue, sizes, wait strategy, lanes and affinity | PROPOSED | BENCHMARK_REQUIRED. |
| D005-001 | ADR-005 | Provider-independent, versioned, strongly typed `CanonicalEvent` model | ACCEPTED | Preserve provenance, capabilities and source semantics. |
| D005-002 | ADR-005 | Multiple timestamp and sequence domains remain distinct | ACCEPTED | No generic timestamp/sequence replacement. |
| D005-003 | ADR-005 | Fixed-point integer prices are preferred in the hot path where domain permits | ACCEPTED | Quantitative features may use `double` where appropriate. |
| D005-004 | ADR-005 | `MarketClock` and monotonic elapsed-time clock are distinct | ACCEPTED | Required for deterministic replay and latency measurement. |
| D005-005 | ADR-005 | `InstrumentId` is the opaque, exact, case-sensitive identity of one concrete observable instrument | ACCEPTED | Provider symbols, labels, family IDs and scientific scope IDs are distinct namespaces; historical WDO/TEST values remain unchanged. |
| D005-006 | ADR-005 | Product/family monitoring intent is typed separately from concrete instrument identity | ACCEPTED | `InstrumentFamilyTarget` requires an explicit future policy result; no default rollover or active-contract selection. |
| D005-007 | ADR-005 | Versioned definitions and an immutable deterministic registry authorize canonical identity and price metadata | ACCEPTED | Current implementation is in-memory; persistence and production ID grammar remain deferred. |
| D006-001 | ADR-006 | Authoritative live `MarketState` is in memory | ACCEPTED | Database/Redis are not authoritative per-tick state. |
| D006-002 | ADR-006 | TOB, MBP and MBO capabilities are distinct and never fabricated | ACCEPTED | Capability downgrade propagates downstream. |
| D006-003 | ADR-006 | Stable snapshots cross ownership boundaries | ACCEPTED | No full book copy per tick. |
| D006-004 | ADR-006 | Exact book structures, primitive collections, dense arrays and double-buffer recovery | PROPOSED | BENCHMARK_REQUIRED where applicable. |
| D007-001 | ADR-007 | Dedicated Feature Engine, separate from interpretation | ACCEPTED | Feature definitions/configuration are versioned. |
| D007-002 | ADR-007 | Incremental computation, bounded windows and explicit readiness/quality | ACCEPTED | No future information and no missing-as-zero. |
| D007-003 | ADR-007 | Exact windows, thresholds and predictive relationships | HYPOTHESIS | RESEARCH_REQUIRED. |
| D008-001 | ADR-008 | Dedicated Market Engine owns `AnalyticalState` | ACCEPTED | Separate from Feature, Event and Alert engines. |
| D008-002 | ADR-008 | Structured Evidence/Evidence Families, confirmation, divergence, regime and abstention are first-class | ACCEPTED | Score/confidence are not probability. |
| D008-003 | ADR-008 | Exact pressure formula/range, evidence weights, regime rules and predictive targets | HYPOTHESIS | RESEARCH_REQUIRED. |
| D008-004 | ADR-008 | Anticipatory evidence is a point-in-time research classification evaluated against declared targets/baselines and a multidimensional value vector | ACCEPTED | `ANTICIPATORY-MARKET-INTELLIGENCE-CONTRACTS.md` provides the general boundary; `../research/H1-ACTIVITY-ARRIVAL-LEAD-SCIENTIFIC-PROTOCOL.md` specializes future H1 claims, arrival, opportunity and lead semantics without accepting a detector, parameter, predictive claim or relationship. |
| D009-001 | ADR-009 | Event Engine detects meaningful analytical transitions | ACCEPTED | Analytical state is not a derived event. |
| D009-002 | ADR-009 | Derived events have explicit lifecycle, stable event identity and versioned revisions | ACCEPTED | Deduplication is distinct from user cooldown. |
| D009-003 | ADR-009 | Exact thresholds, persistence, hysteresis and debounce values | HYPOTHESIS | RESEARCH_REQUIRED. |
| D010-001 | ADR-010 | Dedicated Client Gateway outside analytical truth | ACCEPTED | Client backpressure cannot reach Market Engine. |
| D010-002 | ADR-010 | Foreground real-time uses WSS with snapshot + incremental synchronization | ACCEPTED | Per-stream sequence/gap/resync; no exactly-once assumption. |
| D010-003 | ADR-010 | Mobile push is an attention/wake channel, not authoritative synchronization | ACCEPTED | Client re-establishes current truth through Gateway snapshot. |
| D010-004 | ADR-010 | JSON/compression/exact queue sizes/stream taxonomy/compatibility window | PROPOSED | BENCHMARK_REQUIRED. |
| D010-005 | ADR-010 | Exact authentication/token/WebSocket handshake mechanism | PENDING | Security boundary is accepted; concrete mechanism must be decided before client implementation. |
| D011-001 | ADR-011 | Persistence remains outside the analytical hot path | ACCEPTED | MarketState remains authoritative in memory. |
| D011-002 | ADR-011 | PostgreSQL is the initial operational application database | ACCEPTED | Does not imply permanent raw tick storage. |
| D011-003 | ADR-011 | Historical/research retention is gated by licensing and point-in-time integrity | ACCEPTED | Raw/normalized retention is not authorized until applicable rights are confirmed. |
| D011-004 | ADR-011 | Versioned immutable completed research datasets and deterministic replay | ACCEPTED | Production/replay share analytical semantics. |
| D011-005 | ADR-011 | ClickHouse/specialized analytical storage | PROPOSED | Introduce only after measured PostgreSQL baseline inadequacy and licensing fit. |
| D011-006 | ADR-011 | Parquet as a mandatory production format | PROPOSED | Candidate only. |
| D012-001 | ADR-012 | Every Market Data provider is isolated behind a Provider Adapter anti-corruption boundary | ACCEPTED | No provider-specific logic in analytical engines. |
| D012-002 | ADR-012 | Provider capabilities, provenance, timestamps, sequences, `sourceEpoch`, gaps and recovery are explicit | ACCEPTED | Never fabricate fidelity or continuity. |
| D012-003 | ADR-012 | One authoritative primary source per domain by default; shadow comparison is supported | ACCEPTED | No silent feed fusion. |
| D012-004 | ADR-012 | Provider certification precedes authoritative production use | ACCEPTED | Requires representative dataset/scenarios and measured behavior. |
| D012-005 | ADR-012 | Automatic provider failover | PROPOSED | Requires capability/state equivalence validation. |
| D012-006 | ADR-012 | Provider sidecar/native isolation topology | PROPOSED | Blockers: `PROVIDER`, `BENCHMARK`. |
| D012-007 | ADR-012 | Initial B3 provider/product and exact feed capability | PENDING | Blockers: `PROVIDER`, `LICENSING`; required by `PRODUCTION_SCAFFOLD` for concrete adapter freeze. |
| D012-008 | ADR-012 | Provider-native instrument identity must resolve through exactly one applicable approved point-in-time mapping before canonical event admission | ACCEPTED | Unknown, unapproved, revoked or ambiguous identity fails closed outside the canonical stream. |
| D012-009 | ADR-012 | Real provider namespaces, identifier values, mapping facts and quarantine/retention rights | PENDING | Blockers: `PROVIDER`, `LICENSING`; DM-2 must supply evidence without changing the canonical boundary. |
| D012-010 | ADR-012 | DM-2 qualification is driven by declared analytical capabilities and must establish data fidelity, temporal/sequence semantics and rights per use | ACCEPTED | `DM-2-SOURCE-AND-RIGHTS-QUALIFICATION-CONTRACTS.md` materializes the process and consumes `ANTICIPATORY-INTELLIGENCE-DM-2-HANDOFF.md`; no provider/source/right is thereby qualified. |
| D013-001 | ADR-013 | Canonical ingestion normalizes qualified semantics without erasing lawful useful source information | ACCEPTED | Provider-neutral does not mean lowest common denominator; native facts remain governed and non-scientific until qualified. |
| D013-002 | ADR-013 | Missing source semantics remain unavailable and are never fabricated for canonical or scientific consumers | ACCEPTED | Required absence fails closed only for the dependent consumer; optional absence degrades explicitly. |
| D013-003 | ADR-013 | `SourceLineage` and `ObservationContext` are logical models permitting compact references to shared immutable context | ACCEPTED | Do not require full definitions, profiles, rights or evidence duplication per event. |
| D013-004 | ADR-013 | Temporal identities, event identity and source ordering domains remain semantically distinct | ACCEPTED | `availableAt` is governed by versioned policy; callback, thread and database order are not market order. |
| D013-005 | ADR-013 | Corrections use append/reference/supersession lineage capable of `AS_KNOWN_AT(t)` and `FINAL_CORRECTED` projection | ACCEPTED | No silent mutation, backdating or promotion of an unqualified native edit flag. |
| D013-006 | ADR-013 | Validity, quality flags, freshness, gaps, recovery, history completeness, coverage and source health remain orthogonal where meanings differ | ACCEPTED | Recovered current state never establishes complete event history. |
| D013-007 | ADR-013 | Capability is scoped/versioned and becomes effective only through technical, semantic, entitlement, rights and current admissibility gates | ACCEPTED | Adapter declaration cannot self-certify; consumers declare required/optional capabilities and purpose. |
| D013-008 | ADR-013 | Rights and purpose-specific admission constrain use without redefining immutable market facts | ACCEPTED | Processing, native/canonical retention, research/replay and publication remain independent decisions. |
| D013-009 | ADR-013 | Multi-provider attribution and provider switching preserve source context without inheriting scientific equivalence | ACCEPTED | Cross-provider deduplication/reconciliation and automatic scientific failover remain non-default and separately gated. |
| D013-010 | ADR-013 | First executable proof is bounded synthetic conformance with rich/sparse/correcting sources, two instruments and post-architecture Source D | ACCEPTED | Slice 1 implemented and validated: A/B/C preceded D; D changed zero neutral-core production files; Beta changed zero neutral ingestion/semantic algorithms. |
| D014-001 | ADR-014 | `MarketState` remains factual while `AnalyticalState` owns point-in-time interpretation under a strict epistemic ladder | ACCEPTED | Observation, measurement, candidate evidence, analytical conclusion, prediction and trading recommendation never promote automatically. |
| D014-002 | ADR-014 | Feature Engine produces versioned `DerivedObservable` measurements and candidate evaluation returns `CandidateEvidence` or explicit `NOT_EVALUABLE(reason)` | ACCEPTED | Missing/null/zero/empty and runtime error cannot masquerade as an evaluation outcome. |
| D014-003 | ADR-014 | Analytical evidence semantics preserve support, contradiction, neutral, inconclusive, freshness and abstention as distinct dimensions | ACCEPTED | `NO_ANALYTICAL_CONCLUSION` is first-class; support and contradiction may coexist; no separate `EvidenceState` in Slice 1. |
| D014-004 | ADR-014 | One immutable typed analytical-definition catalog governs exact definitions, parameters, activation and versioned relationships | ACCEPTED | No generic registry, string-pattern dispatch, auto-discovery or hidden material parameters. |
| D014-005 | ADR-014 | Point-in-time derivation, admissible cross-instrument alignment and bitemporal correction lineage are mandatory | ACCEPTED | Required inputs satisfy `availableAt <= decisionTime`; derived availability cannot be laundered; T2 corrections never rewrite T1. |
| D014-006 | ADR-014 | `EvidenceTimeline` preserves logical analytical history and `StructuredWhyNow` is a deterministic non-evidentiary projection | ACCEPTED | Working timeline compaction is separate from governed history; LLM rendering is downstream and non-authoritative. |
| D014-007 | ADR-014 | Runtime, scientific evaluation, Evidence, Certification and Event Engine remain separate authority domains | ACCEPTED | Runtime is target-blind, cannot self-promote/certify and does not turn every analytical transition into a market event. |
| D014-008 | ADR-014 | Universal score, evidence strength, 0-1 confidence, voting, probability and trading semantics are not authorized | ACCEPTED | Confluence preserves family/domain/ancestry for later scientific ablation and incrementality instead of heuristically deciding independence. |
| D014-009 | ADR-014 | Analytical execution uses immutable pre-resolved contexts, controlled time, compact lineage and provider/instrument-neutral ownership | ACCEPTED | Preferred future `research-analytics` boundary requires revalidation and separate authorization; foundations never depend on analytics and analytics never reaches native metadata. |
| D014-010 | ADR-014 | First executable proof is separately authorized synthetic conformance followed by a zero-neutral-core-change definition extension | ACCEPTED | No Java/module/schema is authorized here; real candidates, WDO/WIN, providers, Market Data, empirical thresholds and Evidence/Certification versioning remain out of scope. |
| D015-001 | ADR-015 | Analytical topology is definition-owned and supports legitimate single-instrument `TARGET`-only execution | ACCEPTED | `CONTEXT`/relationship absence is valid for a single-instrument definition; relationship-dependent definitions still fail closed. Fake, doubled or dummy context is prohibited. |
| D015-002 | ADR-015 | A minimal provider-neutral scientific trade-observation view is the common input boundary above source mode | ACCEPTED | Prefer ownership in existing `research-semantic-core`; target/episode/baseline/evaluation must not consume provider/native DTOs or generic maps. |
| D015-003 | ADR-015 | Synthetic and future real canonical observations adapt to the same scientific port without identity impersonation | ACCEPTED | Real observations never become `SyntheticTradeEvent`/`SyntheticEventIdentity`; source mode remains lineage and cannot select target mathematics. |
| D015-004 | ADR-015 | Real H0 reuses `ABSOLUTE_FIRST_PASSAGE_V1` and target-blind episode semantics through additive generalized execution | ACCEPTED | No real-specific target identity, candidate-dependent population or rewrite of historical synthetic material is permitted. |
| D015-005 | ADR-015 | Real B0-B3 and paired evaluation consume immutable experiment/dataset authorities and remain downstream of target-blind runtime candidates | ACCEPTED | `../research/REAL-MARKET-BASELINE-LADDER-B0-B3-CONTRACTS.md` materializes one-population pairing, PIT/correction, B0 prevalence, B1 session/time, B2 causal target-instrument price/self-history and B3 price-confirmation timing; empirical parameters, real data and execution remain pending. |
| D015-006 | ADR-015 | Real scientific execution requires exact instrument/session/dataset/PIT/correction/ordering/quality/purpose admission | ACCEPTED | DM-2 supplies external facts and rights; scientific formulas consume pre-resolved authority and cannot invent or evaluate them. |
| D015-007 | ADR-015 | Real-path extension is additive and must prove historical synthetic compatibility plus real-shaped canonical synthetic conformance | ACCEPTED | Conformance Slice 1.1 closes RM-A01..RM-A09 and replaces the earlier weak proof with a chronological corrected Phase-A baseline followed by Source E at the edge: zero neutral-core/target-mathematics changes; Evidence V3-V8, Certification V1-V3 and historical hashes remain unchanged. |
| D015-008 | ADR-015 | Real H0 uses one immutable target-blind population and anchor authority and characterizes the complete governed Phase-A target grid | ACCEPTED | `H0-REAL-MARKET-EXPERIMENTAL-PROTOCOL.md` freezes one listed contract, exact dataset/instrument/session/projection authority, complete anchor accounting and all 25 Phase-A attempts; no real execution follows. |
| D015-009 | ADR-015 | Target admissibility and selection consume H0-only facts and preserve a small defensible set without a composite score | ACCEPTED | Slice 1.2 resolves an opaque pre-H1 `TargetUseAuthority` from the exact branch/split authority; process-scoped material exposure shared across branches invalidates current confirmatory eligibility while preserving historical freeze authenticity. Branch-scoped tokens cannot be transplanted; new branches cannot reset exposure. H1 facts cannot mint a replacement policy. |
| D015-010 | ADR-015 | A complete immutable attempt ledger and H0-to-H1 freeze bind the target/population authority before H1 preregistration | ACCEPTED | Slice 1.2 preserves the separation between the per-run 25-cell ledger and append-only planned/completed branch history with revisions/supersession; freeze eligibility rechecks current attempt and access history. Material post-freeze change requires a new branch. |
| D015-011 | ADR-015 | Real H0 is primarily point-in-time, reports economic and knowledge target time separately, and remains gated by DM-2 plus a qualified-dataset benchmark | ACCEPTED | `AS_KNOWN_AT(t)` and `FINAL_CORRECTED` remain distinct; `eventTime` cannot replace `availableAt`; the performance tag is not market evidence or execution authorization. |

## 4. Decision Metadata Vocabulary

Use only the canonical decision statuses from `DOMAIN-LANGUAGE.md`:

- `ACCEPTED`
- `PROPOSED`
- `EXPERIMENTAL`
- `HYPOTHESIS`
- `PENDING`

When a decision is `PENDING`, record why separately instead of inventing compound statuses. Canonical blocker values are currently:

- `RESEARCH`
- `PROVIDER`
- `B3`
- `LICENSING`
- `BENCHMARK`
- `IMPLEMENTATION`
- `SECURITY`
- `OPERATIONS`

When relevant, also record `requiredByGate` using the gate names defined by `MVP-READINESS-GATE.md`. Example:

```yaml
decisionStatus: PENDING
blockers:
  - PROVIDER
  - LICENSING
requiredByGate: PRODUCTION_SCAFFOLD
```

Legacy phrases such as `PENDING_PROVIDER`, `PENDING_B3` or `PENDING_RESEARCH` may appear in historical documents. They must be interpreted as `decisionStatus: PENDING` plus the corresponding blocker, not as additional decision statuses. New documentation must use the normalized model.

## 5. Cross-Cutting Pending Decisions

The following are intentionally not selected yet and must not be inferred from technology familiarity:

- exact JDK distribution/version and build tool;
- exact Spring Boot version;
- queue/ring-buffer implementation and capacity;
- permanent historical analytical store;
- cache/broker infrastructure;
- client framework;
- authentication/token mechanism;
- observability stack beyond accepted telemetry requirements;
- cloud/orchestration topology;
- exact performance/SLO numbers;
- exact provider contract/capabilities/licensing rights.

These decisions are promoted only by an accepted ADR, an explicit accepted update to an existing ADR where semantically non-breaking, or a task that is explicitly scoped as an experiment/benchmark rather than production architecture.
